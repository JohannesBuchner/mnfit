from mnfit.mnSpecFit.Model import Model
from numpy import exp, power
from mnfit.priorGen import *








class BandBBPL(Model):

   def __init__(self):




      #Component definitions

      def band(x,logA,Ep,alpha,beta):

          cond = (alpha-beta)*Ep/(2+alpha)

          if (x < cond):
              val =   power(10.,logA)*( power(x/100., alpha) * exp(-x*(2+alpha)/Ep) )
              return val
          else:
              val =  power(10.,logA)*( power( (alpha -beta)*Ep/(100.*(2+alpha)),alpha-beta)*exp(beta-alpha)*power(x/100.,beta))
              return val

      def pl(x,logA,index):
         
         val = power(10.,logA)*power(x/300.,2.)
         return val


      def bb(x,logA,kT):
         
         val = power(10.,logA)*power(x,2.)*power( exp(x/float(kT)) -1., -1.)
         return val


      def bandBBPL(x,logA,Ep,alpha,beta,logA2,index,logA3,kT):

         val =  band(x,logA,Ep,alpha,beta)
         val += pl(x,logA2,index)
         val += bb(x,logA3,kT)
         return val

          
          
      def BandBBPLPrior(params, ndim, nparams):
         
         params[0] = jefferysPrior(params[0],1E-6,1.)
         params[1] = uniformPrior(params[1], 10., 20000.)
         params[2] = uniformPrior(params[2], -2., 1.)
         params[3] = uniformPrior(params[3], -10, -2.)
         params[4] = jefferysPrior(params[4], 1E-15,1E-0)
         params[5] = uniformPrior(params[5], -4, 2.)
         params[6] = jefferysPrior(params[6], 1E-15,1E-0)
         params[7] = uniformPrior(params[7], 5., 500.)#keV
         pass



      bandDict={"params":\
                [r"logN$_{\rm Band}",r"E$_{\rm p}$",r"$\alpha$",r"$\beta$"],\
                "model":band\
      }
      plDict = {"params":\
                [r"logN$_{\rm PL}",r"$\delta$"],\
                "model":pl\
      }

      bbDict = {"params":\
                [r"logN$_{\rm BB}","kT"],\
                "model":bb\
      }
      
      self.componentLU={"Band":bandDict,\
                        "PowerLaw":plDict,\
                        "Blackbody":bbDict\
      }

      
      self.modName = "BandBBPL"
      self.model=bandBBPL
      self.prior=BandBBPLPrior
      self.n_params = 8
      self.parameters = [r"logN$_{\rm Band}",r"E$_{\rm p}$",r"$\alpha$",r"$\beta$",r"logN$_{\rm PL}",r"$\delta$",r"logN$_{\rm BB}","kT"]
