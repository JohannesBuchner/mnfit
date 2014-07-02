from mnfit.mnSpecFit.SpecFitView import SpecFitView as sfv
from scipy.integrate import quad
from mnfit.mnSpecFit.models import models


class flux(object):


    def __init__(self, databin):

        self.fit = sfv(databin,silent=True)
        self.model = models[self.fit.modName]() #This is the class not the function!
        
    def CalculatateTotalFlux(self,emin=10.,emax=40000.):
        pass

    def CalculatateComponentFlux(self,comp,emin=10.,emax=40000.):

        #Get the component
        comp = self.model.SelectComponent(comp)

        #First the best fit flux
        tt = self.fit.GetParamIndex(comp["params"])
        bfParams = self.fit.bestFit[tt]
        print comp["params"]
        print tt
        print bfParams
        # Construct a callback that is only a
        # function of energy for the bestFit params
        
        def tmpModel(ene):

            return ene*comp["model"](ene,*bfParams)

        bfFlux = self._fluxIntergral(tmpModel,emin,emax)


        # Use the propagate function to propagate the fluc
        # first ew Construct a fucntion to send to it

        def propFunc(params):

            def tmpModel(ene):
                return ene*comp["model"](ene,*params)

            return self._fluxIntergral(tmpModel,emin,emax)

        fluxDist = self.fit.Propagate(propFunc,comp["params"],direct=False)
        self.bestFitFlux = bfFlux
        self.fluxDistribution = fluxDist
        
    def _fluxIntergral(self,model,emin, emax):


        
        f = quad(model,emin,emax)[0]

        return f
