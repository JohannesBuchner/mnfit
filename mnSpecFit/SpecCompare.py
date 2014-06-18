from mnfit.FitCompare import FitCompare
import json


class SpecCompare(FitCompare):
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

        
        self.rsps = fit["rsps"]
        self.basename = fit["basename"]
        self.meanChan = []
        self.chanWidths = []
        #model = (models[fit["model"]])()
        #self.model = model.model


        self.stat = fit["stat"]
        self.dof = fit["dof"]

