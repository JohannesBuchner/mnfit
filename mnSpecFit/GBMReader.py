from DataRead import DataRead
import astropy.io.fits as fits
from astropy.table import Table
import pyqt_fit.kernel_smoothing as smooth
from numpy import logical_and, array, mean, histogram, arange

import matplotlib.pyplot as plt
from spectralTools.step import Step

from spectralTools.binning.tteBinning import tteBinning
from glob import glob



class GBMReader(DataRead):


    
    def ReadData(self,bkgIntervals=[[-20,-.1],[50.,300.]]):
        '''
        Momentarily GBM specific 
        
        '''

        
        self.trigTime=self.data[0].header["TRIGTIME"]
        self.tstart = self.data[0].header["TSTART"]-self.trigTime
        self.tstop = self.data[0].header["TSTOP"]-self.trigTime
        
     
        

        self.instrument="GBM"
        self.det = self.dataFile.split('/')[-1][8:10]


        directory = ""

        for x in self.dataFile.split('/')[:-1]:
            directory+=x+"/"
            
        self.directory = directory
        
        rsp = glob(directory+"glg_cspec_"+self.det+"*.rsp")[0]
        print "Found RSP: "+rsp
        self.rsp = rsp

        self.emin = self.data[1].data["E_MIN"]
        self.emax = self.data[1].data["E_MAX"]

        chans = array(zip(self.emin,self.emax))


        meanChan = array(map(mean,chans))

        self.meanChan = meanChan
        #self.chans = chans


        self.chanWidth = self.emax-self.emin
        
        self.bkgIntervals = bkgIntervals
        
        #phas =self.data[2]["PHA"]
        
        #tt = logical_and(phas>=chans[0],phas<=chans[1])
        self.evts = self.data[2].data["TIME"] - self.trigTime #Filter chans
        
        
        #get the background fit
        
        tb = tteBinning(self.dataFile,self.tstart,self.tstop,self.bkgIntervals)
        self.dataBinner = tb
        


    def CreateCounts(self,start=0,stop=10):
        
        
        self.dataBinner.MakeBackgroundSelectionsForDataBinner()
        self.dataBinner._FitBackground()
        self.bkgMods = self.dataBinner.polynomials
        
        #GO BY TIME BIN

        
        bins = self.dataBinner.bins
        j=0
        for i in range(len(bins)-1):
            
            lob=bins[i]
            hib=bins[i+1]
            
            if lob>=start and hib<=stop:
                bkgCounts = []
                bkgError = []
            
                totalCounts = []
            
                for ch in range(128):
                
                    tt = self.data[2].data["PHA"] == ch
                
                
                    ## get evts between times:
                    tt2 = self.evts >= lob
                    tt2 = logical_and(tt2,self.evts <hib)
                
                    tt= logical_and(tt,tt2)
                
                    #Num total counts
                
                    totalCounts.append(len(self.evts[tt]))
                    bkgCounts.append(self.bkgMods[ch].integral(lob,hib))
                    bkgError.append(self.bkgMods[ch].integralError(lob,hib))
                totalCounts =array(totalCounts)/(hib-lob)
                bkgCounts=array(bkgCounts)/(hib-lob)
                bkgError = array(bkgError)/(hib-lob)
                sourceCounts  = totalCounts  - bkgCounts


                directory = "bin%d"%j

                
                
                        
                tab = Table(array(zip(totalCounts,sourceCounts,bkgCounts,bkgError,self.emin,self.emax,self.meanChan)),names=["total","source","bkg","berr","emin","emax","meanChan"])
                tab.meta={"duration":hib-lob,"INST":self.instrument,"DET":self.det,"RSP":self.rsp,"TMIN":lob,"TMAX":hib}
                
                
                
                tab.meta["binN"]=directory
                tab.meta["fileLoc"] = self.directory+directory+"/"

                self.binDict[directory] = tab
                
                
                j+=1


    def PlotData(self):

        tBins = []
        for i in range(len(self.dataBinner.bins)-1):
    
            tBins.append([self.dataBinner.bins[i],self.dataBinner.bins[i+1]])
        tBins=array(tBins)


        cnts,_ = histogram(self.dataBinner.evts,bins=self.dataBinner.bins)

        
        fig=plt.figure(200)
        ax=fig.add_subplot(111)

        Step(ax,tBins,cnts/self.dataBinner.binWidth,"k",.5)
        #Step(ax,tBins,cnts,"k",.5)

        cnts,_ = histogram(self.dataBinner.filteredEvts,bins=self.dataBinner.bins)

        Step(ax,tBins,cnts/self.dataBinner.binWidth,"b",.7)
        #Step(ax,tBins,cnts,"b",.7)

        
        #bkg = []
        #for i in range(len(self.dataBinner.bins)-1):
    
        #    b=0
        #    for j in range(len(self.bkgMods)):
        
        #        b+= self.bkgMods[j].integral(self.dataBinner.bins[i],self.dataBinner.bins[i+1])#/(self.dataBinner.bins[i+1]-self.dataBinner.bins[i])
        #    bkg.append(b)
        #meanT = array(map(mean,tBins))

        bkg = []
        oneSecBins =arange(self.dataBinner.bins[0],self.dataBinner.bins[-1],1.) 
        for i in range(len(oneSecBins)-1):
    
            b=0
            for j in range(len(self.bkgMods)):
        
                b+= self.bkgMods[j].integral(oneSecBins[i],oneSecBins[i+1])/(oneSecBins[i+1]-oneSecBins[i])
            bkg.append(b)
        meanT = map(mean,zip(oneSecBins[:-1],oneSecBins[1:]))
        ax.plot(meanT,array(bkg),linewidth=2,color="r")
        #Step(ax,tBins,bkg/,"r",1)
