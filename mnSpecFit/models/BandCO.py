from mnfit.mnSpecFit.Model import Model
from numpy import exp, power, zeros
from mnfit.priorGen import *








class BandCO(Model):

   def __init__(self):






      def bandCO(x,logA,Ep,alpha,beta,eFolding):

         val = zeros(x.flatten().shape[0])

         
         
         A = power(10.,logA)
         idx  = (x < (alpha-beta)*Ep/(2+alpha))
         nidx = ~idx
         

         val[idx]  = A*( power(x[idx]/100., alpha) * exp(-x[idx]*(2+alpha)/Ep) )
         
         val[nidx] = A*power((alpha -beta)*Ep/(100.*(2+alpha)),alpha-beta)*exp(beta-alpha)*power(x[nidx]/100.,beta)
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
