from numpy import array
import json


class EpEvo(object):


    def __init__(self,EpEvoFile):


        f = open(EpEvoFile) # Open the file
        self.fileName = EpEvoFile
        
        jsonFile = json.load(f)


        self._Ep       = array(jsonFile['Ep'])
        self._EpErr    = array(jsonFile['EpErr'])
        self._timebins = array(jsonFile['tbins'])
        self._offset   = 0.0  #This sets a shift in the times if the time bin is not zero 

    
    def SetOffset(self,offset):


        self._offset = offset

    def GetTimeBins(self):

        return self._timebins + self._offset


    def GetEp(self):


        return self._Ep

    def GetErr(self):


        return self._EpErr


   
