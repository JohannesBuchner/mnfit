from mnfit.mnSpecFit.Model import Model
from numpy import exp, power, zeros
from mnfit.priorGen import *








class BandBB(Model):

   def __init__(self):




      def band(x,logA,Ep,alpha,beta):

         val = zeros(x.flatten().shape[0])

         
         
         A = power(10.,logA)
         idx  = (x < (alpha-beta)*Ep/(2+alpha))
         nidx = ~idx
         

         val[idx]  = A*( power(x[idx]/100., alpha) * exp(-x[idx]*(2+alpha)/Ep) )
         
         val[nidx] = A*power((alpha -beta)*Ep/(100.*(2+alpha)),alpha-beta)*exp(beta-alpha)*power(x[nidx]/100.,beta)
         return val


      def bb(x,logA,kT):
         
         val = power(10.,logA)*power(x,2.)*power( exp(x/float(kT)) -1., -1.)
         return val


      def bandBB(x,logA,Ep,alpha,beta,logA2,kT):

          #BB
          val = bb(x,logA2,kT)
          val += band(x,logA,Ep,alpha,beta)


          return val
        
        
                      


      def BandBBPrior(params, ndim, nparams):
         
         params[0] = jefferysPrior(params[0],1E-6,1.)
         params[1] = uniformPrior(params[1], 10., 100000.)
         params[2] = uniformPrior(params[2], -2., 1.)
         params[3] = uniformPrior(params[3], -10, -2.)
         params[4] = jefferysPrior(params[4], 1E-15,1.)
         params[5] = uniformPrior(params[5], 5., 500.)#keV
         pass


      #Component definitions

      
      

      bandDict={"params":\
                [r"logN$_{\rm Band}$",r"E$_{\rm p}$",r"$\alpha$",r"$\beta$"],\
                "model":band\
      }
      bbDict = {"params":\
                [r"logN$_{\rm BB}$","kT"],\
                "model":bb\
      }

      self.componentLU={"Band":bandDict,\
                        "Blackbody":bbDict\
      }

      
      self.modName = "Band+BB"
      self.model=bandBB
      self.prior=BandBBPrior
      self.n_params = 6
      self.parameters = [r"logN$_{\rm Band}$",r"E$_{\rm p}$",r"$\alpha$",r"$\beta$",r"logN$_{\rm BB}$","kT"]
