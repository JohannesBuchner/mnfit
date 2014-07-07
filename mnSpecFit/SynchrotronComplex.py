from Model import Model
from synchrotron_glue import synchrotronComplexPy
from numpy import power
class SynchrotronComplex(Model):


    def __init__(self):


        def TotalSynchrotron(ene,norm,estar,gammaMin,gammaTH,index):

            norm = power(10.,norm)

            return synchrotronComplexPy(ene, norm, estar, gammaMin, gammaTH, index)


        def SynchPrior(params, ndim, nparams):
         

            params[0] = -4*params[0]
            params[1] = 3.*params[1]
            params[2] = 1.+1800.*params[2]
            params[3] = 1.+900.*params[3]
            params[4] = 10.*params[4]+2.1 #Must be positive!
             
            pass

       


        self.modName = "SynchrotronComplex"
        self.model=TotalSynchrotron
        self.prior=SynchPrior
        self.n_params = 5
        self.parameters = ["logNorm",r"E$_{crit}$", r"$\gamma_{min}$", r"$\gamma_{th}$", r"$\delta$"]



