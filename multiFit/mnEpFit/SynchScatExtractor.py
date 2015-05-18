from mnfit.mnEpFit.ScatExtract import ScatExtract



class SynchScatExtractor(ScatExtract):


    def _PrepareData(self):

        gammaMin = self.scat.GetParamArray("Total Test Synchrotron","Eta")[0,0]

        self._Ep = (self.scat.GetParamArray("Total Test Synchrotron","Energy Crit")[:,0]*gammaMin**2).tolist()
        self._EpErr = (self.scat.GetParamArray("Total Test Synchrotron","Energy Crit")[:,1]*gammaMin**2).tolist()
        self._tbins = self.scat.meanTbins.tolist()
        
