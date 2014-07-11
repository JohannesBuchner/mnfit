from numpy import log10



def jeffreysPrior(par,bottom,top):


    low = log10(bottom)
    spread = log10(top)-log10(bottom)
    par = par*spread + low
    return par

def uniformPrior(par,bottom,top):

    low = float(bottom)
    spread = float(top-bottom)
    par = par*spread + low
    return par

def modifiedJefferysPrior(par,top):
    pass

