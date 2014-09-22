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


    def _WriteLightCurve(self):


        tab = Table(array( zip(self.timebins, self.dataPoints, self.errors)),names=["TIMEBINS","DATA","ERR"]    )

        tab.meta = {"TYPE":self.lcType,"EMIN":self.emin,"EMAX":self.emax,'DURATION':self.duration,"TMIN":self.time,"TMAX":self.tmax}

        
        tab.write(self.fileName,format="fits")
        print "Wrote:\n\t%s"%self.fileName    

            


        
 
