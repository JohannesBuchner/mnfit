from mnfit.mnSpecFit.Model import Model
from mnfit.mnSpecFit.synchrotron_glue import synchrotronPy
from numpy import power
from mnfit.priorGen import *


class Synchrotron(Model):


    def __init__(self):


        def TotalSynchrotron(ene,norm,estar,index):

            norm = power(10.,norm)

            return synchrotronPy(ene, norm, estar,index)


        def SynchPrior(params, ndim, nparams):
         

            params[0] = jefferysPrior(params[0],1E-15,1.)
            params[1] = uniformPrior(params[1], 0., 3.)
            params[2] = uniformPrior(params[2], 2., 12.)#Must be positive!
             
            pass

       


        self.modName = "Synchrotron"
        self.model=TotalSynchrotron
        self.prior=SynchPrior
        self.n_params = 3
        self.parameters = ["logNorm",r"E$_{crit}$",r"$\delta$"]



