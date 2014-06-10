
from mnfit.Likelihood import Likelihood


##Import math log


from numpy import log, sqrt

    
class cstat(Likelihood):


    def SetBackGround(self,bg, bgErr):

        self.bg = bg
        self.berr = bgErr

    def SetCounts(self,counts):

        self.counts = counts


    def SetModelCounts(self,mc):

        self.modc = mc

    def ComputeLikelihood(self):

        t = self.ts + self.tb
        FLOOR = 1.0e-5
        fi = 0.
        
        stat = 0.

        for i in range(len(self.counts)):


            if self.counts[i] == 0:
                print "ZERO SOURCE COUNTS"
                stat+=self.ts*self.modc[i] - self.bg[i]*log(self.tb/t)

            else:
                if self.bg[i] == 0:
                    print "ZERO BKG COUNTS"
                    if self.modc[i] <= self.counts/t:
                        stat+= -self.tb*self.modc[i] - self.counts[i]*log(self.ts/t)
                    else:
                        stat+= self.ts*self.modc[i] + self.source[i]*(log(self.source[i])-log(self.ts*self.modc[i])-1)
                # Source and bkg present
                else:

                    print "CALC QUAD"
                    a = t
                    b = t*self.modc[i] - self.counts[i] - self.bg[i]
                    c = -self.bg[i]*self.modc[i]
                    
                    if b>=0.:
                        sign=1.
                    else:
                        sign = -1.
                    q = -.5*(b + sign*sqrt(b*b - 4.0*a*c))
                    fi = q/a
                    if fi< 0.:
                        fi = c/q
                    stat+= self.ts*self.modc[i] +t*fi
                    stat-= self.counts[i]*log(self.ts*self.modc[i]+self.ts*fi)
                    stat-= self.bg[i]*log(self.tb*fi)
                    stat-= self.counts[i]*(1-log(self.counts[i]))
                    stat-= self.bg[i]*(1-log(self.bg[i]))

        return stat
