from mnfit.FitView import FitView
from astropy.table import Table
from DataBin import DataBin
from models import models
import json


class SpecFitView(FitView):


    def _LoadData(self,data):



        f = open(data)

        fit = json.load(f)


        self.parameters = fit["params"]
        self.n_params = len(self.parameters)

        self.detectors = fit["detectors"]
        self.dataBinExt = fit["dataBinExt"]
        self.duration = fit["duration"]
        self.sourceCounts = []
        self.rsps = fit["rsps"]
        self.basename = fit["basename"]

        model = (models[fit["model"]])()
        self.model = model.model
        
        #load counts and model counts
        for det in self.detectors:

            db = DataBin(self.dataBinExt+det+".fits")
            self.sourceCounts.append(db.source)
            
        
            


