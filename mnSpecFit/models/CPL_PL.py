from mnfit.mnSpecFit.Model import Model
from numpy import exp, power
from mnfit.priorGen import *








class CPL_PL(Model):

   def __init__(self):



      def cpl(x,logA,index,eFolding):
         
         val = power(10.,logA)*power(x/300.,index)*exp(-x/eFolding)
         return val

      def pl(x,logA,index):
         
         val = power(10.,logA)*power(x/300.,index)
         return val

      def cplpl(x,logA,index,eFolding,logA2,index2):

         val =  cpl(x,logA,index,eFolding)
         val += pl(x,logA2,index2)

         return val

      def CPLPrior(params, ndim, nparams):
         
         params[0] = jefferysPrior(params[0], 1E-15,1.E2)
         params[1] = uniformPrior(params[1], -4., 2.)
         params[2] = uniformPrior(params[2], 5., 3.E6)#keV
         params[3] = jefferysPrior(params[3], 1E-15,1E-0)
         params[4] = uniformPrior(params[4], -4, 2.)
         pass


      #Component definitions

      cplDict = {"model":cpl,\
                  "params":[r"logN$_{\rm CPL1}$",r"$\delta$1","eFold1"]\
      }
      
      plDict = {"params":\
                [r"logN$_{\rm PL}$",r"$\delta$"],\
                "model":pl\
      }

      self.componentLU={"CPL":cplDict,\
                        "PL":plDict\
                        }


      self.modName = "CPL+PL"
      self.model=cplpl
      self.prior=CPLPrior
      self.n_params = 5
      self.parameters = [r"logN$_{\rm CPL1}$",r"$\delta$1","eFold1",r"logN$_{\rm PL}$",r"$\delta$"]
