from mnfit.mnSpecFit.Model import Model
from mnfit.mnSpecFit.synchrotron_glue import synchrotronPLPy, SSCpy
from numpy import power
from mnfit.priorGen import *

class SynchSSC(Model):


    def __init__(self):


        def SynSSCmod(ene,norm1,estar,norm2,chi,index):
            #For now, gammaMin is an undeterminable
            # So set it to 900
            norm1 =  power(10.,norm1)
            norm2 =  power(10.,norm2)
            val   =  synchrotronPLPy(ene, norm1, estar, index, 900.)
            val   += SSCpy(ene,norm2,chi,index)

        def SynchPrior(params, ndim, nparams):
         
            params[0] = jefferysPrior(params[0],1E-15,1.)
            params[1] = uniformPrior(params[1], 0., 3.)
            params[2] = jefferysPrior(params[0],1E-15,1.)
            params[3] = uniformPrior(params[1], 0., 3.)
            params[4] = uniformPrior(params[2], 2., 12.)#Must be positive!
             
            pass





        #Component definitions
        def synch(ene,norm,estar,index):
            norm = power(10.,norm)
            return synchrotronPLPy(ene,norm,estar,index,900.)

        def ssc(ene,norm,chi,index):
            norm = power(10.,norm)
            return SSCpy(ene,norm,chi,index)

        synchDict={"params":\
                   ["logNorm1",r"E$_{crit}$",r"$\delta$"],\
                   "model":synch\
        }
        sscDict = {"params":\
              ["logNorm2",r"$\chi$",r"$\delta$"],\
                   "model":ssc\
        }    


        self.componentLU={"Synchrotron":synchDict,\
                          "SSC":sscDict}

        self.modName = "SynchSSC"
        self.model=SynSSCmod
        self.prior=SynchPrior
        self.n_params = 5
        self.parameters = ["logNorm1",r"E$_{crit}$","logNorm2",r"$\chi$",r"$\delta$"]

