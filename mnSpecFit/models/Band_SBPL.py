from mnfit.mnSpecFit.Model import Model
from numpy import log, exp, log10, power
from mnfit.priorGen import *


class Band_SBPL(Model):



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



        def band(x,logA,Ep,alpha,beta):

            cond = (alpha-beta)*Ep/(2+alpha)
       
            if (x < cond):
                return  10**(logA)*( power(x/100., alpha) * exp(-x*(2+alpha)/Ep) )


            else:
                return 10**(logA)* ( power( (alpha -beta)*Ep/(100.*(2+alpha)),alpha-beta)*exp(beta-alpha)*power(x/100.,beta))


        def band_sbpl(x,logAband,Ep,alpha,beta,logNsbpl, indx1, breakE, breakScale, indx2):

            val = band(x,logAband,Ep,alpha,beta)
            val+= sbpl(x, logNsbpl, indx1, breakE, breakScale, indx2)
            return val

        def SBPLPrior(params, ndim, nparams):

            params[0] = jefferysPrior(params[0],1E-6,1.)
            params[1] = uniformPrior(params[1], 10., 20000.)
            params[2] = uniformPrior(params[2], -2., 1.)
            params[3] = uniformPrior(params[3], -10, -2.)
            params[4] = jefferysPrior(params[4], 1E-15, 1.)
            params[5] = uniformPrior(params[5],-5.,1.)
            params[6] = uniformPrior(params[6], 10., 200000.)
            params[7] = uniformPrior(params[7], 0., 3.)
            params[8] = uniformPrior(params[8], -10., -1.)
            
            pass



        bandDict={"params":\
                [r"logN_band",r"E$_{\rm p}$",r"$\alpha$",r"$\beta$"],\
                "model":band\
      }
        sbplDict={"params":["logN_sbpl",r"indx1",r"breakE",r"breakScale","indx2"],\
                  "model":sbpl}

        self.componentLU={"Band":bandDict,\
                          "SBPL":sbplDict}

        self.modName = "Band_SBPL"

        self.model=band_sbpl
        self.prior=SBPLPrior
        self.n_params = 9
        self.parameters = ["logN_band",r"E$_{\rm p}$",r"$\alpha$",r"$\beta$","logN_sbpl",r"indx1",r"breakE",r"breakScale","indx2"]

