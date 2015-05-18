from mnfit.FitView import FitView
from astropy.table import Table
from mnfit.mnEpFit.EpEvo import EpEvo
from mnfit.mnEpFit.models.models import models
import matplotlib.pyplot as plt
from numpy import array, cumsum, linspace, sqrt, logspace, log10
from numpy import mean, meshgrid, histogram2d, zeros
from scipy.stats import ks_2samp
import json


class EpFitView(FitView):


    def _LoadData(self,data):



        f = open(data)

        fit = json.load(f)

        self.modName = fit["model"]

        
            
        self.parameters = fit["params"]
        self.n_params = len(self.parameters)

        
        self.EpEvoFile = fit["EpEvo"]
        self.basename = fit["basename"]
        self.stat =fit["stat"]
        self.dof = fit['dof']

        self.dataRange=linspace(fit["tmin"],fit["tmax"],500)

        self.tmin = fit["tmin"]
        self.tmax = fit["tmax"]

        thisModel =  models[self.modName]()


        self.model = thisModel.model



    def _CustomInfo(self):

        print

        print "Model:\n\t%s"%self.modName

        print "TMIN: %.2f"%self.tmin
        print "TMAX: %.2f"%self.tmax

        print "\nBest Fit Parameters (1-sigma err):"

        marg = self.anal.get_stats()["marginals"]

        for params,val,err in zip(self.parameters,self.bestFit,marg):

            err = err["1sigma"]
            
            print "\t%s:\t%.2f\t+%.2f -%.2f"%(params,val,err[1]-val,val-err[0])

        print
        print "%s per d.o.f.:\n\t %.2f/%d"%(self.stat,-2.*self.loglike,self.dof)



    def PlotEvo(self,fignum=1000):


        fig = plt.figure(fignum)

        ax = fig.add_subplot(111)

        evo = EpEvo(self.EpEvoFile)
        
        

        
       

        yData = []


        # posterior = array([ self.model(self.dataRange,*params)  for params in self.anal.get_equal_weighted_posterior()[::10,:-1]])
        

        # posterior = posterior.reshape(len(self.dataRange)*len(self.anal.get_equal_weighted_posterior()[::10,:-1]))
        # eneVals = array(self.dataRange.tolist()*len(self.anal.get_equal_weighted_posterior()[::10,:-1]))

        
        # yRange = logspace(log10(min(posterior)),log10(max(posterior)),100)

        
        # H,xE,yE, = histogram2d(eneVals,posterior,bins=(self.dataRange,yRange),normed=True)
        # tt = H>0
        # alpha = H[tt]
        # alpha/=max(alpha)
        # #alpha/
        # self.alpha = alpha
        # xCoord = array(map(mean,array([xE[:-1],xE[1:]]).T))
        # yCoord = array(map(mean,array([yE[:-1],yE[1:]]).T))
        # xy = array(meshgrid(xCoord,yCoord))
        # coords = xy.T[H>0]
        # rgba_colors = zeros((len(coords),4))
        # rgba_colors[:,0] = 1.0


        # rgba_colors[:, 3] = alpha
        # #rgba_colors[:,3]=.5
        
        
        # ax.scatter(coords[:,0],coords[:,1],c=rgba_colors,marker="H",s=1,edgecolors=None,linewidth=0)
        

        for params in self.anal.get_equal_weighted_posterior()[::100,:-1]:

            tmp = []
            
            for x in self.dataRange:

                tmp.append(self.model(x, *params))
            yData.append(tmp)

        



        
        #Plot the spread in data
            
        for y in yData:

            ax.loglog(self.dataRange,y,"#fc8d62",alpha=.05,lw=self.linewidth*.5,ls="-",zorder=-32) ## modify later

        bfModel = []


        # Plot the best fit
        for x in self.dataRange:

            bfModel.append(self.model(x, *self.bestFit))
        
            
        ax.loglog(self.dataRange,bfModel,"#8da0cb",lw=self.linewidth,ls="-",zorder=-10) #modify later


        ax.errorbar(evo.GetTimeBins(),evo.GetEp(),yerr=evo.GetErr(),fmt='.',color='#66c2a5',capsize=self.capsize,elinewidth=self.elinewidth,markersize=3.3)

        ax.set_yscale('log',nonposy='clip')
        ax.set_xlabel("Time [s]")
        ax.set_ylabel(r"$E_{\rm p}$ [keV]")

        
        return ax

        
