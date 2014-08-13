from mnfit.mnSpecFit.Model import Model
from numpy import exp, power, maximum, zeros
from mnfit.priorGen import *








class Band(Model):

   def __init__(self):



      
      
      def band(x,logA,Ep,alpha,beta):

         val = zeros(x.flatten().shape[0])

         
         
         A = power(10.,logA)
         idx  = (x < (alpha-beta)*Ep/(2+alpha))
         nidx = ~idx
         

         val[idx]  = A*( power(x[idx]/100., alpha) * exp(-x[idx]*(2+alpha)/Ep) )
         
         val[nidx] = A*power((alpha -beta)*Ep/(100.*(2+alpha)),alpha-beta)*exp(beta-alpha)*power(x[nidx]/100.,beta)
         return val


      def BandPrior(params, ndim, nparams):
         
         params[0] = jefferysPrior(params[0],1E-6,1E3)
         params[1] = uniformPrior(params[1], 10., 100000.)
         #params[1] = jefferysPrior(params[1],1,1E5)
         params[2] = uniformPrior(params[2], -2., 1.)
         params[3] = uniformPrior(params[3], -10, -2.)
         pass

       

      self.modName = "Band"
      self.model=band
      self.prior=BandPrior
      self.n_params = 4
      self.parameters = ["logNorm",r"E$_{\rm p}$",r"$\alpha$",r"$\beta$"]
