from Model import Model
from numpy import log, exp, log10, power

class SBPL(Model):



    def __init__(self):



        def sbpl(ene, logN, indx1, breakE, breakScale, indx2):

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

            if arg < -6.0:

                pcosh = M * breakScale * (-arg-log(2.0))

            elif arg > 4.0:

                pcosh = M * breakScale * (arg - log(2.0))

            else:

                pcosh = M * breakScale * (log( (exp(arg) + exp(-arg))/2.0 ))

            val = power(10,logN) * power(ene/pivot,B)*power(10.,pcosh-pcosh_piv)

            return val


        def SBPLPrior(params, ndim, nparams):

            params[0]=-6.*params[0]+1.
            params[1] = 3.*params[1]-2.
            params[2] = 9.9E3*params[2]+1E2
            params[3] = 3*params[3]
            params[4] = 4.*params[4]-5.
            
            pass


        self.modName = "SBPL"

        self.model=sbpl
        self.prior=SBPLPrior
        self.n_params = 5
        self.parameters = ["logNorm",r"indx1",r"breakE",r"breakScale","indx2"]

