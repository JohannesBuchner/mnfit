from mnfit.mnSpecFit.Model import Model
from numpy import exp, power
from mnfit.priorGen import *








class BandBBCPL(Model):

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

      def cpl(x,logA,index,eFolding):
               
         val = power(10.,logA)*power(x/300.,index)*exp(-x/eFolding)
         return val



      def bb(x,logA,kT):
         
         val = power(10.,logA)*power(x,2.)*power( exp(x/float(kT)) -1., -1.)
         return val


      def bandBBCPL(x,logA,Ep,alpha,beta,logA2,index,eFolding,logA3,kT):

         val =  band(x,logA,Ep,alpha,beta)
         val += cpl(x,logA2,index,eFolding)
         val += bb(x,logA3,kT)
         return val

          
          
      def BandBBCPLPrior(params, ndim, nparams):
         
         params[0] = jefferysPrior(params[0],1E-6,1.)
         params[1] = uniformPrior(params[1], 10., 100000.)
         params[2] = uniformPrior(params[2], -2., 1.)
         params[3] = uniformPrior(params[3], -10, -2.)
         params[4] = jefferysPrior(params[4], 1E-15,1E-0)
         params[5] = uniformPrior(params[5], -4, 2.)
         params[6] = uniformPrior(params[6], 5., 3.E6)#keV
         params[7] = jefferysPrior(params[7], 1E-15,1E-0)
         params[8] = uniformPrior(params[8], 5., 500.)#keV
         pass



      bandDict={"params":\
                [r"logN$_{\rm Band}$",r"E$_{\rm p}$",r"$\alpha$",r"$\beta$"],\
                "model":band\
      }

      
      cplDict = {"params":\
                 [r"logN$_{\rm CPL}$",r"$\delta$","eFold"],\
                "model":cpl\
      }

      bbDict = {"params":\
                [r"logN$_{\rm BB}$","kT"],\
                "model":bb\
      }
      
      self.componentLU={"Band":bandDict,\
                        "CPL":cplDict,\
                        "Blackbody":bbDict\
      }

      
      self.modName = "BandBBCPL"
      self.model=bandBBCPL
      self.prior=BandBBCPLPrior
      self.n_params = 9
      self.parameters = [r"logN$_{\rm Band}$",r"E$_{\rm p}$",r"$\alpha$",r"$\beta$",r"logN$_{\rm CPL}$",r"$\delta$","eFold",r"logN$_{\rm BB}$","kT"]
