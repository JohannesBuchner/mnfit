from mnfit.mnPulseFit.LightCurve import LightCurve

import pickle

import astropy.io.fits as fits
from numpy import sqrt, power, array, logical_and, mean, arange


class FluxLightCurve(LightCurve):


    def ReadFluxFile(flcFile,make="energy"):


        self.makeType = make


        f=open(flcFile):


        flc = pickle.load(f)



        
        #Setup the timing properties
        self.binStart = flc['tBins'][:,0]
        self.binStop = flc['tBins'][:,1]

        self.duration = self.binStop[-1] - self.binStart[0]

        self.tmin = self.binStart[0]
        self.tmax = self.binStop[-1]

        self.timebins = array(map(mean, flc['tBins']))

        if self.makeType == 'energy' or self.makeType == 'both':

            flux = flc['energyFlux']['flux']
            errors = flc['energyFlux']['errors']
        




