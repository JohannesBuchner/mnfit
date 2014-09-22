from mnfit.mnPulseFit.PulseModel import PulseModel
from mnfit.priorGen import *

from numpy import exp, power






class krl(PulseModel):



    def __init__(self):


        def KRLPulse(t,tmax,c,r,d,fmax):
            fmax=power(10.,fmax)
            f = (fmax*(power((((t+c)/(tmax+c))),r)/power(((d+(r*power((((t+c)/(tmax+c))),(1+r))))/(d+r)),((d+r)/(1+r)))))
            return f


        self.paramsRanges = [[0.,100,"U"],[0.,1.,"U"],[0,5.,"U"],[0,5.,"U"],[1E-5,1E5,"J"]]

        def KRLPrior(params, ndim, nparams):

            for i in range(ndim):
                params[i] = priorLU[self.paramsRanges[i][-1]](params[i],self.paramsRanges[i][0],self.paramsRanges[i][1])
            


        self.modName = "KRL"
        self.model=KRLPulse
        self.prior=KRLPrior
        self.n_params = 5
        self.parameters = ["tmax","c","r","d","fmax"]

    
