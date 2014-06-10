from Model import Model
from numpy import exp, power

def band(x,logA,Ep,alpha,beta):


    cond = (alpha-beta)*Ep/(2+alpha)
       
    if x < cond:

        val = 10**(logA)*( power(x/100., alpha) * exp(-x*(2+alpha)/Ep) )
    else:
        val = 10**(logA)* ( power( (alpha -beta)*Ep/(100.*(2+alpha)),alpha-beta)*exp(beta-alpha)*power(x/100.,beta))

    return val


def BandPrior(params, ndim, n_params):

    
    #logNorm
    params[0] = -2.5*params[0]
        
    #Ep
    params[1] = 9.9E3*params[1]+1E2

    #alpha
    params[2] = 2.*params[2]-2.

    #beta
    params[3] = 4.*params[3]-5.


class Band(Model):

   def __init__(self):

       self.model=band
       self.prior=BandPrior
       self.n_params = 4
