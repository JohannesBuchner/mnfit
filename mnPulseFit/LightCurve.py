from numpy import array
import astropy.io.fits as fits
from astropy.table import Table

class LightCurve(object):



    def __init__(self):
        '''
        The Lightcurve object stores the flux or count
        data points based off of what type of data are read
        
        It contains a reader and a writer. The reader is general
        but the write is is a subclass.


        '''

        self.lcType = None
        self.timebins = None
        self.dataPoints = None


    def ReadData(self,lcSave):
        '''
        Read a LightCurve FITS file. The type is saved within the file
        Will set all the proper members and alert the user of the various 
        info.


        '''

        #Open the file
        lcTable = Table.read(lcSave,format="fits")

        self.lcType = lcTable.meta["TYPE"]
        self.timebins = lcTable["TIMEBINS"]
        self.dataPoints = lcTable["DATA"]
        self.errors = lcTable["ERR"]
        self.binStart = lcTable["BSTART"]
        self.binStop  = lcTable["BSTOP"]
        if self.lcType == "TTE":
            self.bkg = lcTable["BKG"]
            self.bkgErr = lcTable["BKGERR"]

        self.duration = lcTable.meta["DURATION"]
        self.tmin = lcTable.meta["TMIN"]
        self.tmax = lcTable.meta["TMAX"]
        self.emin = lcTable.meta["EMIN"]
        self.emax = lcTable.meta["EMAX"]
        self.fileName=lcSave
            
    def _WriteLightCurve(self):


        if self.lcType == "TTE":

            tab = Table(array( zip(self.timebins,  self.binStart,  self.binStop, self.dataPoints, self.errors,self.bkg,self.bkgErr)),names=["TIMEBINS","BSTART","BSTOP","DATA","ERR","BKG","BKGERR"]    )
        else:
            tab = Table(array( zip(self.timebins, self.binStart,  self.binStop, self.dataPoints, self.errors)),names=["TIMEBINS","BSTART","BSTOP","DATA","ERR"]    )

        tab.meta = {"TYPE":self.lcType,"EMIN":self.emin,"EMAX":self.emax,'DURATION':self.duration,"TMIN":self.tmin,"TMAX":self.tmax}

        self.filename = self.filename[:-5]+"_%.1f_%.1f.fits"%(self.emin,self.emax)
        tab.write(self.fileName,format="fits",overwrite=True)
        print "Wrote:\n\t%s"%self.fileName    

            

    def GetTimeBins(self):

        return self.timebins

    def GetCounts(self):

        return self.dataPoints

    def GetBkg(self):

        return self.bkg


    def GetBkgErr(self):

        return self.bkgErr


    def GetErr(self):

        return self.errors
 
