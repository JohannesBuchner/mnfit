cimport cython
cimport numpy as np
import numpy as np


from mnfit.Likelihood import Likelihood


##Import math log


cdef extern from "math.h":
    double log(double)
cdef extern from "math.h":
    double sqrt(double)






class chi2(Likelihood):



    def _SetName(self):
        self.statName = "chi2"

    def SetCounts(self,counts):

        self.counts = counts


    def SetTimeBins(self,timeBins):

        self.timeBins

    def SetErrors(self,errors):

        self.errors = errors

    def SetModelCounts(self,modelCounts):

        self.modelCounts
        
    @cython.cdivision(True)
    @cython.boundscheck(False)
    cpdef ComputeLikelihood(self):

        C=np.array(self.counts)
        M=np.array(self.modelCounts)
        Err = np.array(self.errors)
        S=np.power(C-M,2.)/np.power(Err,2.)
        sSum = np.sum(S)

        return sSum





