from Model import Model
from synchrotron_glue import synchrotronPLPy
from numpy import power
from mnfit.priorGen import *
class PLSynchrotron_Cutoff(Model):


    def __init__(self):


        def TotalSynchrotron(ene,norm,estar,index,gammaMax):
            #For now, gammaMin is an undeterminable
            # So set it to 900
            norm = power(10.,norm)

            return synchrotronPyPL(ene, norm, estar, index, 900.)


        def SynchPrior(params, ndim, nparams):
         

            params[0] = jefferysPrior(param[0],0,1E-4) #Check on this
            params[1] = uniformPrior(params[1],0.,3.)
            params[2] = uniformPrior(params[2],2.,12.)#Must be positive!
            params[3] = uniformPrior(params[3],900.,6000.)
            pass

       


        self.modName = "PLSynchrotron_Cutoff"
        self.model=TotalSynchrotron
        self.prior=SynchPrior
        self.n_params = 4
        self.parameters = ["logNorm",r"E$_{crit}$",r"$\delta$",r"$\gamma_{max}$"]



