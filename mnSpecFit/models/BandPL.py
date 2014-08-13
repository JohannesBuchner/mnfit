from mnfit.mnSpecFit.Model import Model
from numpy import exp, power, zeros
from mnfit.priorGen import *








class BandPL(Model):

   def __init__(self):


      #Component definitions

      def band(x,logA,Ep,alpha,beta):

         val = zeros(x.flatten().shape[0])

         
         
         A = power(10.,logA)
         idx  = (x < (alpha-beta)*Ep/(2+alpha))
         nidx = ~idx
         

         val[idx]  = A*( power(x[idx]/100., alpha) * exp(-x[idx]*(2+alpha)/Ep) )
         
         val[nidx] = A*power((alpha -beta)*Ep/(100.*(2+alpha)),alpha-beta)*exp(beta-alpha)*power(x[nidx]/100.,beta)

         return val

      def pl(x,logA,index):
         
         val = power(10.,logA)*power(x/300.,index)
         return val

      

      def bandPL(x,logA,Ep,alpha,beta,logA2,index):


         val = band(x,logA,Ep,alpha,beta)
         val +=pl(x,logA2,index)
         
         return val
        
        



      def BandPLPrior(params, ndim, nparams):
         
         params[0] = jefferysPrior(params[0],1E-6,1.)
         params[1] = uniformPrior(params[1], 10., 100000.)
         params[2] = uniformPrior(params[2], -2., 1.)
         params[3] = uniformPrior(params[3], -10, -2.)
         params[4] = jefferysPrior(params[4], 1E-15,1E-0)
         params[5] = uniformPrior(params[5], -4, 2.)
         pass


      


      bandDict={"params":\
                [r"logN$_{\rm Band}$",r"E$_{\rm p}$",r"$\alpha$",r"$\beta$"],\
                "model":band\
      }
      plDict = {"params":\
                [r"logN$_{\rm PL}$",r"$\delta$"],\
                "model":pl\
      }

      self.componentLU={"Band":bandDict,\
                        "PowerLaw":plDict\
      }

      
      self.modName = "BandPL"
      self.model=bandPL
      self.prior=BandPLPrior
      self.n_params = 6
      self.parameters = [r"logN$_{\rm Band}$",r"E$_{\rm p}$",r"$\alpha$",r"$\beta$",r"logN$_{\rm PL}$",r"$\delta$"]
