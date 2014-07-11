from Model import Model
from synchrotron_glue import synchrotronPy
from numpy import power
class Synchrotron(Model):


    def __init__(self):


        def TotalSynchrotron(ene,norm,estar,index):

            norm = power(10.,norm)

            return synchrotronPy(ene, norm, estar,index)


        def SynchPrior(params, ndim, nparams):
         

            params[0] = -4*params[0]
            params[1] = 3.*params[1]
            params[2] = 10.*params[2]+2.1 #Must be positive!
             
            pass

       


        self.modName = "Synchrotron"
        self.model=TotalSynchrotron
        self.prior=SynchPrior
        self.n_params = 3
        self.parameters = ["logNorm",r"E$_{crit}$",r"$\delta$"]



