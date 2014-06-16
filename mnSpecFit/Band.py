from Model import Model
from numpy import exp, power
from ctypes import *








class Band(Model):

   def __init__(self):



      

      def band(x,logA,Ep,alpha,beta):



         cond = (alpha-beta)*Ep/(2+alpha)
       
         if (x < cond):
            return  10**(logA)*( power(x/100., alpha) * exp(-x*(2+alpha)/Ep) )


         else:
            return 10**(logA)* ( power( (alpha -beta)*Ep/(100.*(2+alpha)),alpha-beta)*exp(beta-alpha)*power(x/100.,beta))



      def BandPrior(params, ndim, nparams):
         
         params[0] = -2.5*params[0]
         params[1] = 9.9E3*params[1]+1E2
         params[2] = 2.*params[2]-2.
         params[3] = 4.*params[3]-5.
         pass

       

      self.modName = "Band"
      self.model=band
      self.prior=BandPrior
      self.n_params = 4
      self.parameters = ["logNorm",r"E$_{\rm p}$",r"$\alpha$",r"$\beta$"]
