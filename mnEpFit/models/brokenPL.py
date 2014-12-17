from mnfit.mnEpFit.EpModel import EpModel
from mnfit.priorGen import *

from numpy import exp, power, logical_and, piecewise






class brokenPL(EpModel):



    def __init__(self):


        def BrokenPL(x, logA, indx1, breakPoint, indx2):

            logA = power(10., logA)
            
            t0=0.
            pivot=1.
            cond1 = x <  breakPoint
            cond2 = x >= breakPoint

            val = piecewise(x, [cond1, cond2],\
            [lambda x:power((x-t0)/pivot ,indx1),\
            lambda x:power( (breakPoint-t0) / pivot ,indx1-indx2 ) * power((x-t0)/pivot, indx2)  ])
            return logA*val
    

        


        self.paramsRanges = [[1.E1,1.E3,"J"],[-4.,1.,"U"],[1E-3,3.E2,"U"],[-4.,0.,"U"]]

        def EpEvoPrior(params, ndim, nparams):

            for i in range(ndim):
                params[i] = priorLU[self.paramsRanges[i][-1]](params[i],self.paramsRanges[i][0],self.paramsRanges[i][1])
            


        self.modName = "brokenPL"
        self.model=BrokenPL
        self.prior=EpEvoPrior
        self.n_params = 4
        self.parameters = ["log(N)","idx1","breakPoint","idx2"]

    
