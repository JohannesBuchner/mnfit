from mnfit.mnSpecFit.Model import Model
from numpy import log, exp, log10, power, logical_or
from mnfit.priorGen import *


class SBPL_BB(Model):



    def __init__(self):



        def bb(x,logA,kT):
         
            val = power(10.,logA)*power(x,2.)*power( exp(x/float(kT)) -1., -1.)
            return val
        


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

        def sbplBB(x,logN1,indx1,breakE,breakScale, indx2, logN2, kT):

            val = sbpl(x,logN1, indx1, breakE, breakScale, indx2)
            val += bb(x,logN2,kT)

            return val


            

        
        def SBPLBBPrior(params, ndim, nparams):

            params[0] = jefferysPrior(params[0], 1E-15, 1.)
            params[1] = uniformPrior(params[1],-5.,1.)
            params[2] = uniformPrior(params[2], 10., 20000.)
            params[3] = uniformPrior(params[3], 0., 3.)
            params[4] = uniformPrior(params[4], -10, -1.)
            params[5] = jefferysPrior(params[5], 1E-15,1E-0)
            params[6] = uniformPrior(params[6], 5., 500.)#keV
            pass



        bbDict = {"params":\
                [r"logN$_{\rm BB}$","kT"],\
                "model":bb\
            }

        sbplDict = {"params":\
              ["logNorm1",r"indx1",r"breakE",r"breakScale","indx2"],\
                "model":sbpl\
               }

        self.componentLU={"Blackbody":bbDict,\
                        "SBPL":sbplDict\
                      }




        self.modName = "SBPL+BB"

        self.model=sbplBB
        self.prior=SBPLBBPrior
        self.n_params = 7
        self.parameters = ["logNorm1",r"indx1",r"breakE",r"breakScale","indx2",r"logN$_{\rm BB}$","kT"]

