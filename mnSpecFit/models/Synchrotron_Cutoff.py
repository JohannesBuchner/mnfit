from mnfit.mnSpecFit.Model import Model
from mnfit.mnSpecFit.synchrotron_glue import synchrotron_CO_Py
from mnfit.priorGen import *
from numpy import power
class Synchrotron_Cutoff(Model):


    def __init__(self):


        def TotalSynchrotron(ene,norm,estar,index,gammaMax):

            norm = power(10.,norm)

            return synchrotron_CO_Py(ene, norm, estar,index,gammaMax)



        self.paramsRanges = [[1.E-15,1.,"J"],[0.,3.,"U"],[2.,12.,"U"],[90,8000.,"U"]]
                            

      
        def SynchPrior(params, ndim, nparams): 

            for i in range(ndim):
                params[i] = priorLU[self.paramsRanges[i][-1]](params[i],self.paramsRanges[i][0],self.paramsRanges[i][1])
        

       


        self.modName = "Synchrotron_Cutoff"
        self.model=TotalSynchrotron
        self.prior=SynchPrior
        self.n_params = 4
        self.parameters = ["logNorm",r"E$_{crit}$",r"$\delta$",r"$\gamma_{max}$"]



