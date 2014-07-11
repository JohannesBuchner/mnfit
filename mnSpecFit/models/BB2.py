from mnfit.mnSpecFit.Model import Model
from numpy import exp, power
from mnfit.priorGen import *








class BB2(Model):

   def __init__(self):
      '''
      Spectral Model containing two blackbodies
      '''
      

      def bb2(x,logA1,kT1,logA2,kT2):




          #BB1
          val = power(10.,logA1)*power(x,2.)*power( exp(x/float(kT1)) -1.,-1.)

          #BB2
          val += power(10.,logA2)*power(x,2.)*power( exp(x/float(kT2)) -1.,-1.)
          return val
        
        



      def BB2Prior(params, ndim, nparams):
         
         params[0] = jefferysPrior(params[0], 1E-15,1E-0)
         params[1] = uniformPrior(params[1], 5., 500.)#keV
         params[2] = jefferysPrior(params[2], 1E-15,1E-0)
         params[3] = uniformPrior(params[3], 5., 500.)#keV

         pass

       


      #Component Definitions

      def bb(x,logA,kT):
         return power(10.,logA)*power(x,2.)*power( exp(x/float(kT)) -1., -1.)
         


      bb1Dict={"params":\
               [r"logN$_{\rm BB1}",r"kT1"],\
               "model":bb\
            }
      bb2Dict={"params":\
               [r"logN$_{\rm BB2}",r"kT2"],\
               "model":bb\
            }

         
      self.componentLU={"Blackbody1":bb1Dict,\
                        "Blackbody2":bb2Dict\
                     }
      
      self.modName = "Two BBs"
      self.model=bb2
      self.prior=BB2Prior
      self.n_params = 4
      self.parameters = [r"logN$_{\rm BB1}",r"kT1",r"logN$_{\rm BB2}",r"kT"]
