from mnfit.mnSpecFit.Model import Model
from numpy import exp, power, zeros
from mnfit.priorGen import *








class BandCPL(Model):

   def __init__(self):





      def band(x,logA,Ep,alpha,beta):

         val = zeros(x.flatten().shape[0])

         
         
         A = power(10.,logA)
         idx  = (x < (alpha-beta)*Ep/(2+alpha))
         nidx = ~idx
         

         val[idx]  = A*( power(x[idx]/100., alpha) * exp(-x[idx]*(2+alpha)/Ep) )
         
         val[nidx] = A*power((alpha -beta)*Ep/(100.*(2+alpha)),alpha-beta)*exp(beta-alpha)*power(x[nidx]/100.,beta)

         return val


      def cpl(x,logA,index,eFolding):
         
         val = power(10.,logA)*power(x/300.,index)*exp(-x/eFolding)
         return val

      

      def bandCPL(x,logA,Ep,alpha,beta,logA2,index,eFolding):



          val  = band(x,logA,Ep,alpha,beta)
          val += cpl(x,logA2,index,eFolding)
          return val
        
        



      def BandCPLPrior(params, ndim, nparams):
         
         params[0] = jefferysPrior(params[0],1E-6,1.)
         params[1] = uniformPrior(params[1], 10., 100000.)
         params[2] = uniformPrior(params[2], -2., 1.)
         params[3] = uniformPrior(params[3], -10, -2.)
         params[4] = jefferysPrior(params[4], 1E-15,1.E2)
         params[5] = uniformPrior(params[5], -4., 2.)
         params[6] = uniformPrior(params[6], 5., 3.E6)#keV
         pass


      #Component definitions



      bandDict={"params":\
                [r"logN$_{\rm Band}$",r"E$_{\rm p}$",r"$\alpha$",r"$\beta$"],\
                "model":band\
      }
      cplDict = {"params":\
                 [r"logN$_{\rm CPL}$",r"$\delta$","eFold"],\
                "model":cpl\
      }

      self.componentLU={"Band":bandDict,\
                        "CPL":cplDict\
      }

      
      self.modName = "BandCPL"
      self.model=bandCPL
      self.prior=BandCPLPrior
      self.n_params = 7
      self.parameters = [r"logN$_{\rm Band}$",r"E$_{\rm p}$",r"$\alpha$",r"$\beta$",r"logN$_{\rm CPL}$",r"$\delta$","eFold"]
