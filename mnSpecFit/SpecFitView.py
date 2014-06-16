from mnfit.FitView import FitView
from astropy.table import Table
from DataBin import DataBin
from models import models
import matplotlib.pyplot as plt

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


        self.xlabel = "Energy [keV]"


    def PlotvFv(self):
        '''
        Plots the best fit and the surrounding likelihood space
        but in vFv space instead of the standard photon space.

        self.dataRange must be set!

        '''



        fig = plt.figure(130)
        ax = fig.add_subplot(111)

        yData = []


        for params in self.anal.get_equal_weighted_posterior()[::100,:-1]:

            tmp = []
            
            for x in self.dataRange:

                tmp.append(x*x*self.model(x, *params)) #Computes vFv
            yData.append(tmp)



        
       


        for y in yData:

            ax.plot(self.dataRange,y,"#2EFE64") ## modify later

        bfModel = []
        for x in self.dataRange:

            bfModel.append(x*x*self.model(x, *self.bestFit))
        
            
        ax.plot(self.dataRange,bfModel,"#642EFE",linewidth=1.2) #modify later
        ax.set_xscale('log')
        ax.set_yscale('log')

        ax.set_xlabel(self.xlabel)
        ax.set_ylabel(r"$\nu F_{\nu}$ [keV$^2$ s$^{-s}$ cm$^{-2}$ keV$^{-1}$]")
        ax.grid(False)
        ax.set_xlim(min(self.dataRange),max(self.dataRange))

        return ax
        
            
        
            


