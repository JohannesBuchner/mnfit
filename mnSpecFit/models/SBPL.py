from mnfit.mnSpecFit.Model import Model
from numpy import log, exp, log10, power, logical_or, zeros
from mnfit.priorGen import *


class SBPL(Model):



    def __init__(self):



        def sbpl(ene, logN, indx1, breakE, breakScale, indx2):


            val = zeros(ene.flatten().shape[0])
            
            pivot =300. #keV

            B = (indx1 + indx2)/2.0
            M = (indx2 - indx1)/2.0

            arg_piv = log10(pivot/breakE)/breakScale

            if arg_piv < -6.0:

                pcosh_piv = M * breakScale * (-arg_piv-log(2.0))

            elif arg_piv > 4.0:

                pcosh_piv = M * breakScale * (arg_piv - log(2.0))

            else:

                pcosh_piv = M * breakScale * (log( (exp(arg_piv) + exp(-arg_piv))/2.0 ))

            

            arg = log10(ene/breakE)/breakScale

            
            idx1 =  arg < -6.0
            idx2 =  arg >  4.0
            idx3 =  ~logical_or(idx1,idx2)

            pcosh = zeros(ene.flatten().shape[0])
            
            pcosh[idx1] = M * breakScale * (-arg[idx1]-log(2.0))

            pcosh[idx2] = M * breakScale * (arg[idx2] - log(2.0))

            pcosh[idx3] = M * breakScale * (log( (exp(arg[idx3]) + exp(-arg[idx3]))/2.0 ))

            val = power(10.,logN) * power(ene/pivot,B)*power(10.,pcosh-pcosh_piv)

            return val


        def SBPLPrior(params, ndim, nparams):

            params[0] = jefferysPrior(params[0], 1E-15, 1.)
            params[1] = uniformPrior(params[1],-5.,1.)
            params[2] = uniformPrior(params[2], 10., 20000.)
            params[3] = uniformPrior(params[3], 0., 3.)
            params[4] = uniformPrior(params[4], -10, -1.)
            
            pass


        self.modName = "SBPL"

        self.model=sbpl
        self.prior=SBPLPrior
        self.n_params = 5
        self.parameters = ["logNorm",r"indx1",r"breakE",r"breakScale","indx2"]

