from Model import Model
from numpy import exp, power









class BandBB(Model):

   def __init__(self):



      

      def bandBB(x,logA,Ep,alpha,beta,logA2,kT):




          #BB
          val = power(10,logA2)*power(x,2)*power( exp(x/float(kT)) -1.,-1.)


          cond = (alpha-beta)*Ep/(2+alpha)

          if (x < cond):
              val +=   10**(logA)*( power(x/100., alpha) * exp(-x*(2+alpha)/Ep) )
              return val
          else:
              val +=  10**(logA)* ( power( (alpha -beta)*Ep/(100.*(2+alpha)),alpha-beta)*exp(beta-alpha)*power(x/100.,beta))
              return val
        
        



      def BandBBPrior(params, ndim, nparams):
         
         params[0] = -2.5*params[0]
         params[1] = 9.9E3*params[1]+1E2 #keV
         params[2] = 3.*params[2]-2.
         params[3] = 4.*params[3]-5.
         params[4] = -8.*params[4]
         params[5] = 397.*params[5]+3 #keV
         pass

       

      self.modName = "Band+BB"
      self.model=bandBB
      self.prior=BandBBPrior
      self.n_params = 6
      self.parameters = [r"logN$_{\rm Band}",r"E$_{\rm p}$",r"$\alpha$",r"$\beta$",r"logN$_{\rm Band}","kT"]
