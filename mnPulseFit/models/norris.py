from mnfit.mnPulseFit.PulseModel import PulseModel
from mnfit.priorGen import *

from numpy import exp, power






class norris(PulseModel):



    def __init__(self):

        def NorrisPulse(t,ts,A,tr,td):
            A=power(10.,A)
            f = A*exp(2.*(tr/ td)**.5 ) * exp( -tr / (t - ts) - (t - ts) / td )
            return f




        self.paramsRanges = [[0.,10.,"U"],[1E-5,1.E5,"J"],[0,50.,"U"],[0,5.,"U"],[0.,200.,"U"]]

        def NorrisPrior(params, ndim, nparams):

            for i in range(ndim):
                params[i] = priorLU[self.paramsRanges[i][-1]](params[i],self.paramsRanges[i][0],self.paramsRanges[i][1])
            


        self.modName = "Norris"
        self.model=NorrisPulse
        self.prior=NorrisPrior
        self.n_params = 4
        self.parameters = ["ts","A","tr","td"]
