from mnfit.FitView import FitView
from astropy.table import Table
from DataBin import DataBin



class SpecFitView(FitView):


    def _LoadData(self,data):



        tab = Table.read(data,format="fits")


        self.parameters = tab["paramters"]
        self.n_params = len(self.parameters)

        self.detectors = tab["detectors"]
        self.dataBinExt = tab.meta["databin"]
        self.duration = tab.meta["duration"]
        self.sourceCounts = []
        self.rsps = tab["rsps"]
        self.basename = tab.meta["basename"]

        #load counts and model counts
        for det in self.detectors:

            db = DataBin(self.dataBinExt+"/"+det+".fits")
            self.sourceCounts.append(db.source)
            
        
            


