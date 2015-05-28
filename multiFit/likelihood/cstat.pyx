cimport cython
cimport numpy as np
import numpy as np
from multiFit.Likelihood import Likelihood


##Import math log


cdef extern from "math.h":
    double log(double)
cdef extern from "math.h":
    double sqrt(double)



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




class cstat(Likelihood):



    def _SetName(self):
        self.statName = "cstat"

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
        tb=np.float(self.tb)
        ti=ts+tb
        M=np.array(self.modc)
        m=M#/ts
        W=np.ndarray(len(S))*0.0
        di=np.ndarray(len(S))*0.0
        fi_plus=np.ndarray(len(S))*0.0
        fi_minus=np.ndarray(len(S))*0.0
        fi=np.ndarray(len(S))*0.0
        a=ti
        b=ti*m-S-B
        c=-1.*B*m
        sign=np.sign(b)
        q=-0.5*(b+(np.array(sign))*np.sqrt(b*b-4.0*a*c))
        fi=q/a
        index_f_lt_zero=np.where(fi<0.0)
        if(len(index_f_lt_zero) >=1):
            fi[index_f_lt_zero]=c[index_f_lt_zero]/q[index_f_lt_zero]
        SB=S*B
        index_nonzero=np.flatnonzero(np.array(SB))
        index_nonzero=np.array(index_nonzero)
        if(len(index_nonzero) >=1):
            i=index_nonzero
            W[i]=1.*(ts*m[i]\
                    +(ti)*fi[i]\
                    -S[i]*np.log(ts*m[i]+ts*fi[i])\
                    -B[i]*np.log(tb*fi[i])\
                    -S[i]*(1.0-np.log(S[i]))\
                    -B[i]*(1.0-np.log(B[i])))
        index_sb_zero=findall(list(SB), lambda nummyx:nummyx==0)
        if(len(index_sb_zero) >=1):
            
            for i in index_sb_zero:
                if(S[i]==0):
                    tmp=ts*m[i]\
                        -B[i]*np.log((tb)/(ti))
                else:
                    if(B[i]==0.0):
                        if(m[i]<=S[i]/ts):
                            tmp=-1.*tb*m[i]\
                                -S[i]*np.log((ts)/(ti))
                        else:
                            tmp=ts*m[i]\
                                +S[i]*(np.log(S[i])-np.log(ts*m[i])-1.0)
                W[i]=tmp
        W_sum=2.*sum(W)
        if(not (W_sum>0)):
            W_sum=1.e90
        return W_sum 



    def RMFIT(self):


        W=2.*np.sum(self.modc*self.ts-self.counts+self.counts*(np.log(self.counts)-np.log(self.modc*self.ts)))
        return W



