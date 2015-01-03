from mnfit.mnEpFit.EpModel import EpModel
from mnfit.priorGen import *

from numpy import exp, power, logical_and, piecewise






class extShock(EpModel):



    def __init__(self):


        def EpEvo(t,eta,g,Gamma0, q):


            #
            # For now I'm going to set a few params at good values
            # Adjust later

            z=1.
            #q=power(10.,q)
            #            q=1.E-4
            #E0 = 1.E54
            E0 = 7.8E54        
            #E0 = power(10.,E0)
            #g = (3.-eta)/2.
            n0 = 1.E2

            #xd = ((3.-eta)*E0 / ( 4.*pi*n0*Gamma0**2. * mp  ) )**(1./3.)
            xd = 2.6E16*((1.-eta/3.)*(E0/1.E54)/((n0/100.)*(Gamma0/300.)))**(1./3.)
            #td = (1.+z)*xd / (Gamma0**2. * c)
            td = 9.7*(1.+z)*((1.-eta/3.)*(E0/1.E54)/((n0/100.)*(Gamma0/300.)**8.))**(1./3.)

            ### Calculate X(t)  ###
            test = td/(2. * g + 1.) *( Gamma0**(2.+1./g) + 2.*g)
            #frac = t/td

            condition1 = t<td
            condition2 = logical_and(td<=t, t<=test)


            X = piecewise(t, [condition1, condition2],\
            [lambda t: t/td, \
            lambda t: ((2.*g+1.)*(t/td) - 2.*g)**(1./(2.*g+1.)) ])

            ### Calculate X(t)  ###



            ### Calculate Gamma(X)  ###



            condition3 = X<1.
            condition4 = logical_and(1.<=X, X<=Gamma0**(1./g))

            Gamma = piecewise(X, [condition3, condition4],\
            [lambda X: Gamma0, \
            lambda X: Gamma0*X**(-g) ])

            ### Calculate Gamma(X)  ###
    
            eE0 = 3.E-8 * (1E-3)  * n0**(.5)*q*Gamma0**4. /(1.+z)

#            eE0 = 3.E-8 * n0**(.5)*q*Gamma0**4. /(1.+z)

            return 511. *  eE0*(Gamma/Gamma0)**4. * (X/xd)**(-eta/2.)





        self.paramsRanges = [[0.,4,"U"],[1E-1,2.,"U"],[10.,1000.,"U"],[0.,1.,"U"]]        

        #self.paramsRanges = [[0.,4,"U"],[1E-1,3.,"U"],[10.,1000.,"U"]]

        #self.paramsRanges = [[0.,3,"U"],[1E-1,3.,"U"],[10.,1000.,"U"],[1.E-6,1.E-2,"J"],[1E50,1E56,"J"]]

        def EpEvoPrior(params, ndim, nparams):

            for i in range(ndim):
                params[i] = priorLU[self.paramsRanges[i][-1]](params[i],self.paramsRanges[i][0],self.paramsRanges[i][1])
            


        self.modName = "extShock"
        self.model=EpEvo
        self.prior=EpEvoPrior
        self.n_params = 4
        #self.parameters = [r"$\eta$","g",r"$\Gamma_0$","q","E0"]
        self.parameters = [r"$\eta$","g",r"$\Gamma_0$","q"]

    
