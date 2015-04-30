from mnfit.mnSpecFit.Model import Model
from mnfit.mnSpecFit.synchrotron_glue import synchrotronPy
from numpy import power
from mnfit.priorGen import *


class Synchrotron(Model):


    def __init__(self):


        def TotalSynchrotron(ene,norm,estar,index):

            norm = power(10.,norm)
            
            return synchrotronPy(ene, norm, estar,index)


        ###################################################    
        self.paramsRanges = [[1.E-15,1.,"J"],[0.,3.,"U"],[2.,12.,"U"]]#Changed the prior... should change back
                            

      
        def SynchPrior(params, ndim, nparams): 

            for i in range(ndim):
                params[i] = priorLU[self.paramsRanges[i][-1]](params[i],self.paramsRanges[i][0],self.paramsRanges[i][1])
         

       


        self.modName = "Synchrotron"
        self.model=TotalSynchrotron
        self.prior=SynchPrior
        self.n_params = 3
        self.parameters = ["logNorm",r"E$_{crit}$",r"$\delta$"]



