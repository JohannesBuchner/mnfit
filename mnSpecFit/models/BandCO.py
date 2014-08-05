from mnfit.mnSpecFit.Model import Model
from numpy import exp, power
from mnfit.priorGen import *








class BandCO(Model):

   def __init__(self):



      

      def bandCO(x,logA,Ep,alpha,beta,eFolding):



         cond = (alpha-beta)*Ep/(2+alpha)
       
         if (x < cond):
            val = 10.**(logA)*( power(x/100., alpha) * exp(-x*(2+alpha)/Ep) )


         else:
            val =  10.**(logA)* ( power( (alpha -beta)*Ep/(100.*(2+alpha)),alpha-beta)*exp(beta-alpha)*power(x/100.,beta))

         val *= exp(-x/eFolding)
         return val


      def BandPrior(params, ndim, nparams):
         
         params[0] = jefferysPrior(params[0],1E-6,1.)
         params[1] = uniformPrior(params[1], 10., 100000.)
         params[2] = uniformPrior(params[2], -2., 1.)
         params[3] = uniformPrior(params[3], -10, -2.)
         params[4] = uniformPrior(params[4], -100,1.E7)
         pass

       

      self.modName = "BandCO"
      self.model=bandCO
      self.prior=BandPrior
      self.n_params = 5
      self.parameters = ["logNorm",r"E$_{\rm p}$",r"$\alpha$",r"$\beta$","eFold"]
