from DataRead import DataRead
import astropy.io.fits as fits
from numpy import array
from numpy import mean
from astropy.table import Table


detLU = {"NAI_00":"n0",\
         "NAI_01":"n1",\
         "NAI_02":"n2",\
         "NAI_03":"n3",\
         "NAI_04":"n4",\
         "NAI_05":"n5",\
         "NAI_06":"n6",\
         "NAI_07":"n7",\
         "NAI_08":"n8",\
         "NAI_09":"n9",\
         "NAI_10":"na",\
         "NAI_11":"nb",\
         "BGO_00":"b0",\
         "BGO_01":"b1"}

class PHAReader(DataRead):



    def SetBAKFile(self, bakFile):



        f= fits.open(bakFile)

        self.bkg =f[1].data["COUNTS"]
        self.berr = f[1].data["COUNTS"]
        
        f.close()


    def SetRSP(self,rsp):

        self.rsp  = rsp
        
    def CreateCounts(self):


        duration = self.data[1].header["EXPOSURE"]

        self.bkg = self.bkg/duration

        totalCounts = self.data[1].data["COUNTS"]/duration
        sourceCounts = totalCounts - self.bkg

        self.berr = self.berr/duration 


        emin = self.data[2].data["E_MIN"]
        emax = self.data[2].data["E_MAX"]
        self.det = detLU[self.data[0].header["DETNAM"]]
        self.instrument = self.data[0].header["INSTRUME"]


        chans = array(zip(emin,emax))


        meanChan = array(map(mean,chans))


        directory = ""

        for x in self.dataFile.split('/')[:-1]:
            directory+=x+"/"
            
        self.directory = directory

        tab = Table(array(zip(totalCounts,sourceCounts,self.bkg,self.berr,emin,emax,meanChan)),names=["total","source","bkg","berr","emin","emax","meanChan"])


        tab.meta={"duration":duration,"INST":self.instrument,"DET":self.det,"RSP":self.rsp}

        directory = "bin0"

        
                

                
        tab.meta["binN"]=directory
        tab.meta["fileLoc"] = self.directory+directory+"/"

        
        
        self.binDict[directory] = tab
