from mnfit.mnSpecFit.Model import Model
from numpy import exp, power
from mnfit.priorGen import *








class CPL(Model):

   def __init__(self):



      def cpl(x,logA,index,eFolding):
         
         val = power(10.,logA)*power(x/300.,index)*exp(-x/eFolding)
         return val

      
        
      self.paramsRanges = [[1.E-6,1.E4,"J"],[-2.,1.,"U"],[1.E1,1.E6,"U"]]


      def CPLPrior(params, ndim, nparams):
         
         for i in range(ndim):
            params[i] = priorLU[self.paramsRanges[i][-1]](params[i],self.paramsRanges[i][0],self.paramsRanges[i][1])
      


      


      self.modName = "CPL"
      self.model=cpl
      self.prior=CPLPrior
      self.n_params = 3
      self.parameters = [r"logN$_{\rm CPL}$",r"$\delta$","eFold"]
      self._modelDict = {"params":self.parameters,\
                         "model":cpl\
                      }
      self._composite = False
