cimport cython
cimport numpy as np
import numpy as np
from multiFit.Likelihood import Likelihood


##Import math log


cdef extern from "math.h":
    double log(double)
cdef extern from "math.h":
    double sqrt(double)

FLOOR = 1.E-5

def findall(L, test):
    i=0
    indices = []
    while(True):
        try:
            nextvalue = filter(test, L[i:])[0]
            indices.append(L.index(nextvalue, i))
            i=indices[-1]+1
        except IndexError:
            return indices




class rmfit(Likelihood):



    def _SetName(self):
        self.statName = "cstat_rmfit"

    def SetBackGround(self,bg, bgErr):

        self.bg = bg
        self.berr = bgErr

    def SetCounts(self,counts):

        self.counts = counts


    def SetModelCounts(self,mc):

        self.modc = mc


    @cython.cdivision(True)
    @cython.boundscheck(False)
    def ComputeLikelihood(self):

        S=np.array(self.counts)
        B=np.array(self.bg)
        ts=np.float(self.ts)
        M=np.array(self.modc)

        smallM = M<FLOOR
        M[smallM] = FLOOR
        M+=B/self.tb
        # Here we subtract the background counts!
        # This is fucking illegal!
        
        #S = C-B
        
        stat = ts * M

        posS = S>0.

                        
        stat[posS] += S[posS]* (np.log(S[posS]) - np.log(ts*M[posS]) -1. )

        stat_sum= 2.* stat.sum()
        
        return stat_sum





