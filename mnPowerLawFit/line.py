from mnfit.mnPowerLawFit.GeneralModel import GeneralModel
from mnfit.priorGen import *

from numpy import  power






class line(GeneralModel):



    def __init__(self):


        def BrokenPL(x, logA, indx):
            logA = power(10., logA)
            
            
            val = indx * x + logA
            
            return val
    

        


        self.paramsRanges = [[self.ampLo,self.ampHi,"J"],[self.indxLo,self.indxHi,"U"]]

        def linePrior(params, ndim, nparams):

            for i in range(ndim):
                params[i] = priorLU[self.paramsRanges[i][-1]](params[i],self.paramsRanges[i][0],self.paramsRanges[i][1])
            


        self.modName = "brokenPL"
        self.model=line
        self.prior=linePrior
        self.n_params = 2
        self.parameters = ["log(N)","indx"]

    
