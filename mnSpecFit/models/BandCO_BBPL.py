from mnfit.mnSpecFit.Model import Model
from numpy import exp, power, zeros
from mnfit.priorGen import *








class BandBBPL(Model):

   def __init__(self):




      #Component definitions


      def band(x,logA,Ep,alpha,beta,eFolding):

         val = zeros(x.flatten().shape[0])

         
         
         A = power(10.,logA)
         idx  = (x < (alpha-beta)*Ep/(2+alpha))
         nidx = ~idx
         

         val[idx]  = A*( power(x[idx]/100., alpha) * exp(-x[idx]*(2+alpha)/Ep) )
         
         val[nidx] = A*power((alpha -beta)*Ep/(100.*(2+alpha)),alpha-beta)*exp(beta-alpha)*power(x[nidx]/100.,beta)
         val = val*exp(-x/eFolding)
         
         return val

      def pl(x,logA,index):
         
         val = power(10.,logA)*power(x/300.,index)
         return val


      def bb(x,logA,kT):
         
         val = power(10.,logA)*power(x,2.)*power( exp(x/float(kT)) -1., -1.)
         return val


      def bandBBPL(x,logA,Ep,alpha,beta,eFolding,logA2,index,logA3,kT):

         val =  band(x,logA,Ep,alpha,beta,eFolding)
         val += pl(x,logA2,index)
         val += bb(x,logA3,kT)
         return val

          
          
      def BandBBPLPrior(params, ndim, nparams):
         
         params[0] = jefferysPrior(params[0],1E-6,1.)
         params[1] = uniformPrior(params[1], 10., 100000.)
         params[2] = uniformPrior(params[2], -2., 1.)
         params[3] = uniformPrior(params[3], -10, -2.)
         params[4] = uniformPrior(params[4], 1E2, 1E7)
         params[5] = jefferysPrior(params[5], 1E-15,1E-0)
         params[6] = uniformPrior(params[6], -4, 2.)
         params[7] = jefferysPrior(params[7], 1E-15,1E-0)
         params[8] = uniformPrior(params[8], 5., 500.)#keV
         pass



      bandDict={"params":\
                [r"logN$_{\rm Band}$",r"E$_{\rm p}$",r"$\alpha$",r"$\beta$","eFold"],\
                "model":band\
      }
      plDict = {"params":\
                [r"logN$_{\rm PL}$",r"$\delta$"],\
                "model":pl\
      }

      bbDict = {"params":\
                [r"logN$_{\rm BB}$","kT"],\
                "model":bb\
      }
      
      self.componentLU={"BandCO":bandDict,\
                        "PowerLaw":plDict,\
                        "Blackbody":bbDict\
      }

      
      self.modName = "BandCO+BB+PL"
      self.model=bandBBPL
      self.prior=BandBBPLPrior
      self.n_params = 9
      self.parameters = [r"logN$_{\rm Band}$",r"E$_{\rm p}$",r"$\alpha$",r"$\beta$",r"eFold",r"logN$_{\rm PL}$",r"$\delta$",r"logN$_{\rm BB}$","kT"]
