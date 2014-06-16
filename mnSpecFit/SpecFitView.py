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

        self.modName = fit["model"]
        self.parameters = fit["params"]
        self.n_params = len(self.parameters)

        self.detectors = fit["detectors"]
        self.dataBinExt = fit["dataBinExt"]
        self.duration = fit["duration"]
        self.sourceCounts = []
        self.rsps = fit["rsps"]
        self.basename = fit["basename"]
        self.meanChan = []
        self.chanWidths = []
        model = (models[fit["model"]])()
        self.model = model.model


        self.stat = fit["stat"]
        self.dof = fit["dof"]

        self.cntMods = []
        
        #load counts and model counts
        for det in self.detectors:

            db = DataBin(self.dataBinExt+det+".fits")

            mod = (models[fit["model"]])()
            mod.SetRSP(db.rsp)

            chanWidth = db.chanMax - db.chanMin
            self.chanWidths.append(chanWidth)

            self.cntMods.append(mod)

            self.meanChan.append(db.meanChan)
            
            self.sourceCounts.append(db.source)


        self.xlabel = "Energy [keV]"



    def _CustomInfo(self):

        print

        print "Model:\n\t%s"%self.modName
        print "\nBest Fit Parameters (1-sigma err):"

        marg = self.anal.get_stats()["marginals"]

        for params,val,err in zip(self.parameters,self.bestFit,marg):

            err = err["1sigma"]
            
            print "\t%s:\t%.2f\t+%.2f -%.2f"%(params,val,err[1]-val,val-err[0])

        print
        print "%s per d.o.f.:\n\t %.2f/%d"%(self.stat,-2.*self.loglike,self.dof)


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
        
            
        
            


    def PlotCounts(self):
        '''
        Plots the data counts along with the deconvolved models
        for each detector used in the fit. 

        '''

        
        
        fig = plt.figure(140)

        ax = fig.add_subplot(111)

        colorLU = ["#FF0000","#01DF01","#DA81F5","#0101DF"]


        for c,chan, color,cw in zip(self.sourceCounts,self.meanChan,colorLU,self.chanWidths):

            ax.loglog(chan,c/cw,"+", color=color)

        ax.legend(self.detectors,loc="lower left")


        # Here the model's params are set and the
        # and the matrix is convolved to get
        # model counts

        for mod,chan,cw in zip(self.cntMods,self.meanChan,self.chanWidths):

            yData = []


            for params in self.anal.get_equal_weighted_posterior()[::100,:-1]:

                mod.SetParams(params)
                    
                yData.append(mod.GetModelCnts()/cw)

            for y  in yData:


                ax.loglog(chan,y,"#585858",alpha=.09)


        ax.set_xlabel(self.xlabel)
        ax.set_ylabel(r"cnts s$^{-1}$ keV$^{-1}$")


        
        return ax

        


        

             




        
