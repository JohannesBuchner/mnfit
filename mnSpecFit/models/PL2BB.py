from mnfit.mnSpecFit.Model import Model
from numpy import exp, power
from mnfit.priorGen import *








class PL2BB(Model):

   def __init__(self):



      

      def pl2bb(x,logA1,kT1,logA2,kT2,logA3,index):




          #BB1
          val = power(10.,logA1)*power(x,2)*power( exp(x/float(kT1)) -1.,-1.)

          #BB2
          val += power(10.,logA2)*power(x,2)*power( exp(x/float(kT2)) -1.,-1.)

          #PL
          val += power(10.,logA3)*power(x/300.,index)
          
          return val
        
        



      def PL2BBPrior(params, ndim, nparams):
         
         params[0] = jefferysPrior(params[0], 1E-15,1E-0)
         params[1] = uniformPrior(params[1], 5., 500.)#keV
         params[2] = jefferysPrior(params[2], 1E-15,1E-0)
         params[3] = uniformPrior(params[3], 5., 500.)#keV
         params[4] = jefferysPrior(params[4],1E-15,1.)
         params[5] = uniformPrior(params[5],-1.,-4.)
         pass

       


      #Component Definitions

      def bb(x,logA,kT):
         return power(10.,logA)*power(x,2.)*power( exp(x/float(kT)) -1., -1.)
         

      def pl(x, logA, index):
         return power(10.,logA)*power(x/300.,index)


      bb1Dict={"params":\
               [r"logN$_{\rm BB1}",r"kT1"],\
               "model":bb\
            }
      bb2Dict={"params":\
               [r"logN$_{\rm BB2}",r"kT2"],\
               "model":bb\
            }
      plDict={"params":\
              [r"logN$_{\rm PL}","index"],\
              "model":pl\
           }
         
      self.componentLU={"Blackbody1":bb1Dict,\
                        "Blackbody2":bb2Dict,\
                        "PowerLaw":plDict\
                     }
      
      self.modName = "PL2BB"
      self.model=pl2bb
      self.prior=PL2BBPrior
      self.n_params = 6
      self.parameters = [r"logN$_{\rm BB1}",r"kT1",r"logN$_{\rm BB2}",r"kT",r"logN$_{\rm PL}","index"]
