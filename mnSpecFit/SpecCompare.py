from mnfit.FitCompare import FitCompare
from mnfit.mnSpecFit.models import models
import json
import matplotlib.pyplot as plt

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

    def CompareVFV(self):

        colorLU = ["red","blue","green"]

        fig = plt.figure(130)
        ax = fig.add_subplot(111)

        
        i=0
        for res in self.results:
            yData = []
            mod = models[res[0]]()
            
            for params in res[2].get_equal_weighted_posterior()[::100,:-1]:

                tmp = []
            
                for x in self.dataRange:

                    tmp.append(x*x*mod.model(x, *params)) #Computes vFv
                yData.append(tmp)



            bestFit = res[2].get_best_fit()["parameters"]
       


            for y in yData:

                ax.plot(self.dataRange,y,colorLU[i],alpha=.2) ## modify later

            bfModel = []
            for x in self.dataRange:

                bfModel.append(x*x*mod.model(x, *bestFit))
        
            
            ax.plot(self.dataRange,bfModel,color="k",linewidth=1.2) #modify later
            ax.set_xscale('log')
            ax.set_yscale('log')
            i+=1
        #ax.legend(self.modelnames)
        ax.set_xlabel("Energy [keV]")
        ax.set_ylabel(r"$\nu F_{\nu}$ [keV$^2$ s$^{-s}$ cm$^{-2}$ keV$^{-1}$]")
        ax.grid(False)
        ax.set_xlim(min(self.dataRange),max(self.dataRange))

        return ax
        
