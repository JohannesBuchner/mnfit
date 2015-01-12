from mnfit.mnPowerLawFit.GeneralModel import GeneralModel
from mnfit.priorGen import *

from numpy import  power






class line(GeneralModel):



    def __init__(self):



        self.ampHi = 10
        self.ampLo = -10.
        self.indxLo = 0.
        self.indxHi = 5.
        self.pivot = 2.5
        

        
        def linear(x, logA, indx):


            #logA = power(10., logA)
            
            
            val = indx * (x/self.pivot) + logA
            
            return val
    

        


        self.paramsRanges = [[self.ampLo,self.ampHi,"U"],[self.indxLo,self.indxHi,"U"]]

        def linePrior(params, ndim, nparams):

            for i in range(ndim):
                params[i] = priorLU[self.paramsRanges[i][-1]](params[i],self.paramsRanges[i][0],self.paramsRanges[i][1])
            


        self.modName = "line"
        self.model=linear
        self.prior=linePrior
        self.n_params = 2
        self.parameters = ["log(N)","indx"]

    
