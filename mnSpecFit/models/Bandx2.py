from mnfit.mnSpecFit.Model import Model
from numpy import exp, power
from mnfit.priorGen import *








class Bandx2(Model):

   def __init__(self):




      def bandx2(x,logA,Ep,alpha,beta,logA2,Ep2,alpha2,beta2):

         val =  band(x,logA,Ep,alpha,beta)
         val += band(x,logA2,Ep2,alpha2,beta2)
         return val

      def band(x,logA,Ep,alpha,beta):



         cond = (alpha-beta)*Ep/(2+alpha)
       
         if (x < cond):
            return  10**(logA)*( power(x/100., alpha) * exp(-x*(2+alpha)/Ep) )


         else:
            return 10**(logA)* ( power( (alpha -beta)*Ep/(100.*(2+alpha)),alpha-beta)*exp(beta-alpha)*power(x/100.,beta))



      def BandPrior(params, ndim, nparams):
         
         params[0] = jefferysPrior(params[0],1E-6,1.)
         params[1] = uniformPrior(params[1], 10., 20000.)
         params[2] = uniformPrior(params[2], -2., 1.)
         params[3] = uniformPrior(params[3], -2., -6.)
         params[0] = jefferysPrior(params[0],1E-6,1.)
         params[1] = uniformPrior(params[1], 10., 200000.)
         params[2] = uniformPrior(params[2], -2., 1.)
         params[3] = uniformPrior(params[3], -2., -6.)
         pass


      #Component Definitions
      band1Dict={"params":\
                [r"logN$_{\rm Band}",r"E$_{\rm p}$",r"$\alpha$",r"$\beta$"],\
                "model":band\
      }


      band2Dict={"params":\
                [r"logN$_{\rm Band}2",r"E$_{\rm p}$2",r"$\alpha$2",r"$\beta$2"],\
                "model":band\
      }

      self.componentLU={"Band":bandDict,\
                        "Blackbody":bbDict\
      }


      self.modName = "Bandx2"
      self.model=bandx2
      self.prior=BandPrior
      self.n_params = 8
      self.parameters = ["logNorm",r"E$_{\rm p}$",r"$\alpha$",r"$\beta$","logNorm2",r"E$_{\rm p}$2",r"$\alpha$2",r"$\beta$2"]
