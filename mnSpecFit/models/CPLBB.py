from mnfit.mnSpecFit.Model import Model
from numpy import exp, power
from mnfit.priorGen import *








class CPLBB(Model):

   def __init__(self):





      def bb(x,logA,kT):
         
         val = power(10.,logA)*power(x,2.)*power( exp(x/float(kT)) -1., -1.)
         return val


      def cpl(x,logA,index,eFolding):
         
         val = power(10.,logA)*power(x,index)*exp(-x/eFolding)
         return val

      

      def cplBB(x,logA1,index,eFolding,logA2,kT):



          val  = bb(x,logA2,kT)
          val += cpl(x,logA1,index,eFolding)
          return val
        
        



      def CPLbbPrior(params, ndim, nparams):
         
         params[0] = jefferysPrior(params[0], 1E-15,1.E2)
         params[1] = uniformPrior(params[1], -4., 2.)
         params[2] = uniformPrior(params[2], 5., 3.E6)#keV
         params[3] = jefferysPrior(params[3], 1E-15,1E-0)
         params[4] = uniformPrior(params[4], 5., 500.)#keV

         pass


      #Component definitions



      bbDict = {"params":\
                [r"logN$_{\rm BB}$","kT"],\
                "model":bb\
      }
      }
      cplDict = {"params":\
                 [r"logN$_{\rm CPL}$",r"$\delta$","eFold"],\
                "model":cpl\
      }

      self.componentLU={"Band":bandDict,\
                        "CPL":cplDict\
      }

      
      self.modName = "BandCPL"
      self.model=cplBB
      self.prior=CPLbbPrior
      self.n_params = 5
      self.parameters = [r"logN$_{\rm CPL}$",r"$\delta$","eFold",r"logN$_{\rm BB}$","kT"]
