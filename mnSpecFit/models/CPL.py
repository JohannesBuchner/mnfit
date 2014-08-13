from mnfit.mnSpecFit.Model import Model
from numpy import exp, power
from mnfit.priorGen import *








class CPL(Model):

   def __init__(self):



      def cpl(x,logA,index,eFolding):
         
         val = power(10.,logA)*power(x/300.,index)*exp(-x/eFolding)
         return val

      
        



      def CPLPrior(params, ndim, nparams):
         
         params[0] = jefferysPrior(params[0], 1E-15,1.E3)
         params[1] = uniformPrior(params[1], -4., 2.)
         params[2] = uniformPrior(params[2], 5., 3.E6)#keV
         pass


      #Component definitions


      self.modName = "CPL"
      self.model=cpl
      self.prior=CPLPrior
      self.n_params = 3
      self.parameters = [r"logN$_{\rm CPL}$",r"$\delta$","eFold"]
