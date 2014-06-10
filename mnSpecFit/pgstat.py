from mnfit.Likelihood import Likelihood


from numpy import log, sqrt

    
class pgstat(Likelihood):


    def SetBackGround(self,bg,bgErr):

        self.bg = bg
        self.berr = bgErr

    def SetCounts(self,counts):

        self.counts = counts


    def SetModelCounts(self,mc):

        self.modc = mc

    def ComputeLikelihood(self):

        tr = self.ts/self.tb
        FLOOR = 1.0e-5
        fi = 0.
        
        stat = 0.

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
