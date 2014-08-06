from mnfit.mnSpecFit.Model import Model
from numpy import exp, power
from mnfit.priorGen import *








class CPL2(Model):

   def __init__(self):



      def cpl(x,logA,index,eFolding):
         
         val = power(10.,logA)*power(x/300.,index)*exp(-x/eFolding)
         return val

      
      def cpl2(x,logA,index,eFolding,logA2,index2,eFolding2):

         val =  cpl(x,logA,index,eFolding)
         val += cpl(x,logA2,index2,eFolding2)

         return val

      def CPLPrior(params, ndim, nparams):
         
         params[0] = jefferysPrior(params[0], 1E-15,1.E2)
         params[1] = uniformPrior(params[1], -4., 2.)
         params[2] = uniformPrior(params[2], 5., 3.E6)#keV
         params[3] = jefferysPrior(params[3], 1E-15,1.E2)
         params[4] = uniformPrior(params[4], -4., 2.)
         params[5] = uniformPrior(params[5], 5., 3.E6)#keV
         pass


      #Component definitions

      cpl1Dict = {"model":cpl,\
                  "params":[r"logN$_{\rm CPL1}$",r"$\delta$1","eFold1"]\
      }
      cpl2Dict = {"model":cpl,\
                  "params":[r"logN$_{\rm CPL2}$",r"$\delta$2","eFold2"]\
      }

      self.componentLU={"CPL1":cpl1Dict,\
                        "CPL2":cpl2Dict\
                        }


      self.modName = "CPL+CPL"
      self.model=cpl2
      self.prior=CPLPrior
      self.n_params = 6
      self.parameters = [r"logN$_{\rm CPL1}$",r"$\delta$1","eFold1",r"logN$_{\rm CPL2}$",r"$\delta$2","eFold2"]
