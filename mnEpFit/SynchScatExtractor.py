from mnfit.mnEpFit.ScatExtract import ScatExtract



class SynchScatExtractor(ScatExtract):


    def _PrepareData(self):



        self._Ep = (self.scat.GetParamArray("Total Test Synchrotron","Energy Crit")[:,0]*900.).tolist()
        self._EpErr = (self.scat.GetParamArray("Total Test Synchrotron","Energy Crit")[:,1]*900.).tolist()
        self._tbins = self.scat.meanTbins.tolist()
        
