from Model import Model
from synchrotron_glue import synchrotronPLPy
from numpy import power
class PLSynchrotron(Model):


    def __init__(self):


        def TotalSynchrotron(ene,norm,estar,index):
            #For now, gammaMin is an undeterminable
            # So set it to 900
            norm = power(10.,norm)

            return synchrotronPyPL(ene, norm, estar, index, 900.)


        def SynchPrior(params, ndim, nparams):
         

            params[0] = -4*params[0] #Check on this
            params[1] = 3.*params[1]
            params[2] = 10.*params[2]+2.1 #Must be positive!
             
            pass

       


        self.modName = "PLSynchrotron"
        self.model=TotalSynchrotron
        self.prior=SynchPrior
        self.n_params = 3
        self.parameters = ["logNorm",r"E$_{crit}$",r"$\delta$"]



