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
    def ComputeLikelihood_SLOW(self):

        cdef double t= self.tb +self.ts
        cdef double FLOOR = 1.0e-5
        cdef double fi = 0.
        cdef double a,b,c,sign,q
        cdef double stat = 0.

        #Convert count rate to counts
        
        bkg = self.bg*self.tb
        counts = self.counts*self.ts +bkg
        

        for i in range(len(self.counts)):

            
            if counts[i] == 0:
                stat+=self.ts*self.modc[i] - bkg[i]*log(self.tb/t)

            else:
                if bkg[i] == 0:
                    if self.modc[i] <= counts/t:
                        stat+= -self.tb*self.modc[i] - counts[i]*log(self.ts/t)
                    else:
                        stat+= self.ts*self.modc[i] + self.source[i]*(log(self.source[i])-log(self.ts*self.modc[i])-1)
                # Source and bkg present
                else:
                    a = t
                    b = t*self.modc[i] - counts[i] - bkg[i]
                    c = -1.*bkg[i]*self.modc[i]
                    
                    if b>=0:
                        sign=1.
                    else:
                        sign = -1.
                    q = -.5*(b + sign*sqrt(b*b - 4.0*a*c))
                    fi = q/a
                    if fi< 0.:
                        fi = c/q
                    stat+= self.ts*self.modc[i] +t*fi
                    stat-= counts[i]*log(self.ts*self.modc[i]+self.ts*fi)
                    stat-= bkg[i]*log(self.tb*fi)
                    stat-= counts[i]*(1-log(counts[i]))
                    stat-= bkg[i]*(1-log(bkg[i]))

        return 2.*stat


    @cython.cdivision(True)
    @cython.boundscheck(False)
    def ComputeLikelihood_SLOWEST(self):


        cdef np.ndarray[np.float64_t, ndim=1]  W = np.zeros(len(self.counts),dtype=np.float64)
        cdef double  ti = self.ts +self.tb
        cdef np.ndarray[np.float64_t, ndim=1]  fi = np.zeros(len(self.counts),dtype=np.float64)
        


        cdef double  a = ti

        cdef np.ndarray[np.float64_t, ndim=1]  b = ti*self.modc-self.counts-self.bg
        cdef np.ndarray[np.float64_t, ndim=1]  c = -1.*self.bg*self.modc

        sign = np.sign(b)

        cdef np.ndarray[np.float64_t, ndim=1]   q = -0.5*(b+(np.array(sign))*np.sqrt(b*b-4.0*a*c))

        fi = q/a

        fi[fi<0.]=c[fi<0.]/q[fi<0.]

        cdef np.ndarray[np.float64_t, ndim=1] sb = self.counts*self.bg

        i = sb > 0.
       
        #nonzero
        W[i]=1.*(self.ts*self.modc[i]\
                +(ti)*fi[i]\
                -self.counts[i]*np.log(self.ts*self.modc[i]+self.ts*fi[i])\
                -self.bg[i]*np.log(self.tb*fi[i])\
                -self.counts[i]*(1.0-np.log(self.counts[i]))\
                -self.bg[i]*(1.0-np.log(self.bg[i])))

        if len(sb[sb==0]) >=1:

            i = self.counts == 0
            W[i] = self.ts*self.modc[i] - self.bg[i]*np.log(self.tb/ti)

            i = self.bg == 0

            j = self.modc[i]<=self.counts[i]/self.ts

            W[j] = -1.*self.tb*self.modc[j]-self.counts[j]*np.log(self.ts/ti)

            
            j = self.modc[i]>self.counts[i]/self.ts

            W[j] = self.ts*self.modc[j]+self.counts[j]*(np.log(self.counts[j])-np.log(self.ts*self.modc[j])-1.)


        W_sum = 2*W.sum()
        if(not (W_sum>0)):
            W_sum=1.e90
        return W_sum


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



