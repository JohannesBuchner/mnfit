from mnfit.mnSpecFit.Model import Model
from mnfit.mnSpecFit.synchrotron_glue import synchrotron_CO_Py
from mnfit.priorGen import *
from numpy import power
class Synchrotron_Cutoff(Model):


    def __init__(self):


        def TotalSynchrotron(ene,norm,estar,index,gammaMax):

            norm = power(10.,norm)

            return synchrotron_CO_Py(ene, norm, estar,index,gammaMax)


        def SynchPrior(params, ndim, nparams):
         

            params[0] = jefferysPrior(params[0], 0., 1E-4)
            params[1] = uniformPrior(params[1], 0., 3.)
            params[2] = uniformPrior(params[2], 2., 12.) #Must be positive!
            params[4] = uniformPrior(params[3], 90., 1000.)
            pass

       


        self.modName = "Synchrotron_Cutoff"
        self.model=TotalSynchrotron
        self.prior=SynchPrior
        self.n_params = 4
        self.parameters = ["logNorm",r"E$_{crit}$",r"$\delta$",r"$\gamma_{max}$"]



