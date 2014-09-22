from mnfit.mnPulseFit.LightCurve import LightCurve
from mnfit.mnSpecFit.binning.tteBinning import tteBinning
import astropy.io.fits as fits
from numpy import sqrt, power, array, logical_and, mean, arange


class TTELightCurve(LightCurve):



    def ReadTTEfile(self,tteFile,tstart=0.,tstop=10.,dt=1.,bkgInt=[[-10,0.],[10.,20.]]):


        self.lcType = "TTE"
        tte = fits.open(tteFile)
        evts = tte[2].data["TIME"]
        trigTime=tte[0].header["TRIGTIME"]
        fileStart = tte[0].header["TSTART"]-trigTime
        fileStop = tte[0].header["TSTOP"]-trigTime
        evts=evts-trigTime
        #First we bin the file and fit the background
        tb = tteBinning(tteFile,fileStart,fileStop,bkgInt)


        tb.MakeConstantBins(dt)
        tb.MakeBackgroundSelectionsForDataBinner()
        tb._FitBackground()


        
        channels = self._Energy2Channel(tteFile,self.emin,self.emax)



        counts = []
        bkg = []
        bkgErr = []
        timebins = []

        binStart= []
        binStop = []
        
        bins = arange(tstart,tstop,dt)
        j=0
        for i in range(len(bins)-1):
            
            lob=bins[i]
            hib=bins[i+1]

            
            
            if lob>=tstart and hib<=tstop:

                timebins.append(mean([lob,hib]))
                binStart.append(lob)
                binStop.append(hib)
                bkgCounts = []
                bkgError = []
            
                totalCounts = []
            
                for ch in channels:
                
                    tt = tte[2].data["PHA"] == ch
                
                
                    ## get evts between times:
                    tt2 = evts >= lob
                    tt2 = logical_and(tt2,evts <hib)
                
                    tt= logical_and(tt,tt2)
                
                    #Num total counts
                
                    totalCounts.append(len(evts[tt]))
                    bkgCounts.append(tb.polynomials[ch].integral(lob,hib))
                    bkgError.append(tb.polynomials[ch].integralError(lob,hib))
                totalCounts = array(totalCounts)#/(hib-lob)
                bkgCounts=array(bkgCounts)#/(hib-lob)
                bkgError = array(bkgError)#/(hib-lob)
                sourceCounts  = totalCounts  - bkgCounts
                sourceCounts[sourceCounts<0.]=0
                self.evts = evts
                bkgErr.append(sqrt(power(bkgError,2.).sum()  ))
                counts.append(sourceCounts.sum())
                
                bkg.append(bkgCounts.sum())


        self.timebins = array(timebins)
        self.dataPoints = array(counts)
        self.errors = sqrt(self.dataPoints)
        self.bkg = array(bkg)
        self.bkgErr = array(bkgErr)
        tte.close()
      

        self.tmin = min(bins)
        self.tmax = max(bins)
        self.duration = self.tmax - self.tmin

        self.binStart = array(binStart)
        self.binStop  = array(binStop)
        
        self.fileName=tteFile[:-4]+"_lightcurve.fits"


       
    def SetEnergyRange(self,emin=8.,emax=300.):

        self.emin = emin
        self.emax = emax


    def _Energy2Channel(self,tteFile,emin,emax):

        tteFile = fits.open(tteFile)

        
        e_min = tteFile[1].data["E_MIN"]
        e_max = tteFile[1].data["E_MAX"]

        tt = e_min>=emin

        tt2 = e_max<=emax


        choice = logical_and(tt,tt2)


        return tteFile[1].data["CHANNEL"][choice]
