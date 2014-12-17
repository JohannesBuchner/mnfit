from mnfit.FitCompare import FitCompare
from mnfit.mnSpecFit.models.models import models
import json
import matplotlib.pyplot as plt
from numpy import logspace, log10

class EvoCompare(FitCompare):
    '''
    Subclass of FitCompare that is will performs model selection 
    for spectral fits made with mnSpecFit.
    '''

    def _LoadData(self, data):

        f = open(data)

        fit = json.load(f)

        self.modName = fit["model"]
        self.parameters = fit["params"]
        self.n_params = len(self.parameters)
        self.tmin = fit["tmin"]
        self.tmax = fit["tmax"]
        
        self.basename = fit["basename"]
        
        self.stat = fit["stat"]
        self.dof = fit["dof"]


        self.xlabel = "Energy [keV]"

                
        self.dataRange = logspace(self.tmin,self.tmax,700)
  

    def _CustomInfo(self):

        print "-----> mnSpecFit "
        print "Duration:\n\t%.2f :: %.2f"%(self.tmin,self.tmax)
