cimport cython
cimport numpy as np
import numpy as np
from multiFit.Likelihood import Likelihood


##Import math log


cdef extern from "math.h":
    double log(double)
cdef extern from "math.h":
    double sqrt(double)


    
class pgstat(Likelihood):



 

    def _SetName(self):
        self.statName = "pgstat"


    def SetBackGround(self,bg,bgErr):
        '''
        Set the background and background error 
        PGstat uses gaussian errors and when the 
        background fit is done with a polynomial the
        full propoagated errors SHOULD be gaussian.
        '''
        self.bg = np.array(bg)

        self.berr = bgErr #This is the correct implementation

        
    def SetCounts(self,counts):

        self.counts = counts


    def SetModelCounts(self,mc):

        self.modc = mc

            

    def ComputeLikelihood(self):

        cdef double tr = self.ts/self.tb
        cdef double FLOOR = 1.0e-5
        #cdef double fi = 0.
        #cdef double a,b,c,sign,q, yb
        #cdef double stat = 0.



        stat = np.zeros(len(self.counts))
        fi = np.zeros(len(self.counts))


        a = self.tb*self.tb
        b = self.ts*self.berr - self.tb*self.bg + self.tb*self.tb*self.modc
        c = self.ts*self.berr*self.modc - self.counts*self.berr - self.tb*self.bg*self.modc
        sign = np.sign(b)

        q = -.5*(b + sign*np.sqrt(b*b - 4.0*a*c))
        fi = q/a


        fi[fi<0.] = c[fi<0.]/q[fi<0.]


        stat = self.ts*(self.modc + fi)\
               - self.counts*np.log(self.ts*self.modc+self.ts*fi)\
                + 0.5*(self.bg-self.tb*fi)*(self.bg-self.tb*fi)/self.berr\
                - self.counts*(1-np.log(self.counts))

        
        
        sb = self.berr*self.counts
        
        if len(sb[sb==0]) >= 1:

            i = self.berr==0.

                      
            yb = np.array(map(lambda x: max(FLOOR/self.ts,x), self.modc+self.bg))

            stat[i] = self.ts*yb[i]

 
            i = np.logical_and(self.counts >0.,i)
            
            stat[i] += self.counts[i]*(np.log(self.counts[i])-np.log(self.ts*yb[i])-1)

            
            i = self.counts == 0

            stat[i] = self.ts*self.modc[i] + self.bg[i]*tr - 0.5*self.berr[i]*tr*tr

        stat_sum = 2.*stat.sum()


        return stat_sum
