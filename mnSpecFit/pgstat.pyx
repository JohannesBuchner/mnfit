cimport cython
cimport numpy as np
import numpy as np



from mnfit.Likelihood import Likelihood


##Import math log


cdef extern from "math.h":
    double log(double)
cdef extern from "math.h":
    double sqrt(double)


    
class pgstat(Likelihood):



 

    def _SetName(self):
        self.statName = "pgstat"


    def SetBackGround(self,bg,bgErr):

        self.bg = np.array(bg)

        self.berr = bgErr #THIS IS TEMPORARY!!!!!

        #self.berr = np.zeros(len(bg))
        #i = self.bg>0.
        #self.berr[i] = np.sqrt(self.bg[i])
        #i = self.bg<=0.

        #self.bg[i]=0.
        #self.berr[i]=0
        #self.berr = np.sqrt(bg)


        
    def SetCounts(self,counts):

        self.counts = counts


    def SetModelCounts(self,mc):

        self.modc = mc

    def ComputeLikelihood_SLOW(self):

        cdef double tr = self.ts/self.tb
        cdef double FLOOR = 1.0e-5
        cdef double fi = 0.
        cdef double a,b,c,sign,q, yb
        cdef double stat = 0.

        for i in range(len(self.counts)):

            if self.berr[i] == 0:
                yb = max(self.modc[i]+self.bg[i],FLOOR/self.ts)
                stat+= self.ts*yb
                if self.counts[i] > 0.:
                    stat += self.counts[i]*(log(self.counts[i])-log(self.ts*yb)-1)
                
            ###################
            if self.counts[i] == 0:
                stat+=self.ts*self.modc[i] + self.bg[i]*tr - 0.5*self.berr[i]*tr*tr

            else:
                # Solve quadratic equation for fi, using Numerical Recipes technique
                # to avoid round-off error that can easily cause problems here
                # when b^2 >> ac.
                #
               
                a = self.tb*self.tb
                b = self.ts*self.berr[i] - self.tb*self.tb + self.tb*self.tb*self.modc[i]
                c = self.ts*self.berr[i]*self.modc[i] - self.counts[i]*self.berr[i] - self.tb*self.bg[i]*self.modc[i]
                    
                if b>=0:
                    sign=1.
                else:
                    sign = -1.
                q = -.5*(b + sign*sqrt(b*b - 4.0*a*c))
                fi = q/a
                if fi< 0.:
                    fi = c/q
                stat+= self.ts*(self.modc[i] + fi)
                stat-= self.counts[i]*log(self.ts*self.modc[i]+self.ts*fi)
                stat+= 0.5*(self.bg[i]-self.tb*fi)*(self.bg[i]-self.tb*fi)/self.berr[i]
                stat-= self.counts[i]*(1-log(self.counts[i]))
                

        return stat
            

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

                      
            yb = np.array(map(lambda x: max(FLOOR/self.ts,x), self.modc[i]+self.bg[i]))

            stat[i] = self.ts*yb

            j=i
            i = np.logical_and(self.counts >0.,i)
            
            stat[i] += self.counts[i]*(np.log(self.counts[i])-np.log(self.ts*yb)-1)

            
            i = self.counts == 0
             
            stat[i] = self.ts*self.modc[i] + self.bg[i]*tr - 0.5*self.berr[i]*tr*tr

        stat_sum = 2.*stat.sum()


        return stat_sum
