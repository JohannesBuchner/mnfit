from astropy.table import Table
class DataBin:
    
    
    def __init__(self,databin):
        
        self.data = Table.read(databin,format="fits")
        self.berr = self.data['berr']
        self.bkg = self.data["bkg"]
        self.source = self.data["source"]
        self.total = self.data["total"]
        #self.chans = self.data["chans"]
        self.meanChan = self.data["meanChan"]
        self.totBkg = self.bkg.sum()
        self.totSource =self.source.sum()
        self.totTot = self.total.sum()
        self.duration = self.data.meta["DURATION"]
        self.det = self.data.meta["DET"]
        self.rsp = self.data.meta["RSP"]
        self.instrument = self.data.meta["INST"]
        self.chanMin = self.data["emin"]
        self.chanMax = self.data["emax"]
        self.binN = self.data.meta["BINN"]
        self.fileLoc = self.data.meta["FILELOC"]
        
        self.activeLoChan = 0
        self.activeHiChan = len(self.chanMax)-1


        #Remove the negative counts and replace with zeros || EXPERIMENTNAL

  #      self._RemoveNegativeCounts(self.source)
  #      self._RemoveNegativeCounts(self.bkg)
        


    def _GetChannel(self,energy):

        if energy < self.chanMin[0]:
            return 0
        elif energy > self.chanMax[-1]:
            return len(self.chanMax)-1
    

        
        ch = 0
        for lo, hi in zip(self.chanMin,self.chanMax):

            if energy >= lo and energy <= hi:
                return ch
            else:
                ch+=1

    def SetLoChan(self,lo):

        self.activeLoChan = self._GetChannel(lo)

    def SetHiChan(self,hi):

        self.activeHiChan = self._GetChannel(hi)

    def _RemoveNegativeCounts(self, spectrum):


        tt = spectrum < 0.

        spectrum[tt] = 0.


    def GetTotalCounts(self):

        return (self.total[self.activeLoChan:self.activeHiChan+1])*self.duration

    def GetTotalRate(self):

        return (self.total[self.activeLoChan:self.activeHiChan+1])

    def GetSourceCounts(self):

        return (self.source[self.activeLoChan:self.activeHiChan+1])*self.duration

    def GetSourceRate(self):

        return (self.source[self.activeLoChan:self.activeHiChan+1])


    def GetBkgCounts(self):

        return (self.bkg[self.activeLoChan:self.activeHiChan+1])*self.duration

    def GetBkgRate(self):

        return (self.bkg[self.activeLoChan:self.activeHiChan+1])


    def GetBkgErr(self):

        return (self.berr[self.activeLoChan:self.activeHiChan+1])*self.duration

    def GetBkgErrRate(self):

        return (self.berr[self.activeLoChan:self.activeHiChan+1])
