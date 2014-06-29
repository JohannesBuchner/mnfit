from Model import Model
from synchrotron_glue import synchrotronPy
from numpy import power, exp
class SynchrotronBB(Model):


    def __init__(self):


        def TotalSynchrotronBB(ene,norm,estar,index,bblogN,kT):

            norm = power(10.,norm)




            val = synchrotronPy(ene, norm, estar,index)
            #BB
            val += power(10.,bblogN)*power(ene,2.)*power( exp(ene/float(kT)) -1.,-1.)
            return val
            
        def SynchBBPrior(params, ndim, nparams):
         

            params[0] = -3*params[0]
            params[1] = 3.*params[1]
            params[2] = 10.*params[2]+2.1 #Must be positive!
            params[3] = -8.*params[3]
            params[4] = 397.*params[4]+3 #keV
         
            pass

       


        self.modName = "SynchrotronBB"
        self.model=TotalSynchrotronBB
        self.prior=SynchBBPrior
        self.n_params = 5
        self.parameters = ["logNorm",r"E$_{crit}$",r"$\delta$","logNormBB","kT"]



