from numpy import log10



def jefferysPrior(par,bottom,top): #spelling is bad!


    low = log10(bottom)
    spread = log10(top)-log10(bottom)
    par = par*spread + low
    return par

def uniformPrior(par,bottom,top):

    low = float(bottom)
    spread = float(top-bottom)
    par = par*spread + low
    return par


def gaussian(par,mean,spread):

    pass


    
    return par


def modifiedJefferysPrior(par,top):
    pass

priorLU={"U":uniformPrior,"J":jefferysPrior}
