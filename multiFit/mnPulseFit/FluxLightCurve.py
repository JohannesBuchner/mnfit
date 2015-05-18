from mnfit.mnPulseFit.LightCurve import LightCurve

import pickle

import astropy.io.fits as fits
from numpy import sqrt, power, array, logical_and, mean, arange


class FluxLightCurve(LightCurve):


    def ReadFluxFile(self,flcFile,make="energy"):
        '''
        Read flux fit light curve. For now this is based off
        the flux files created by spectralTools. However, that method
        takes for ever and I should find a better way to generate them

        '''

        self.makeType = make


        f=open(flcFile)


        flc = pickle.load(f)


        #extract energies
        self.emin, self.emax = flc['energies']
        
        #Setup the timing properties
        self.binStart = flc['tBins'][:,0]
        self.binStop = flc['tBins'][:,1]

        self.duration = self.binStop[-1] - self.binStart[0]

        self.tmin = self.binStart[0]
        self.tmax = self.binStop[-1]

        self.timebins = array(map(mean, flc['tBins']))

        #Extract the energy flux data based on the input 
        if self.makeType == 'energy':

            flux = flc['energy fluxes']['total'] ### Should change this to grab models!
            errors = flc['errors']['total']
        

        if self.makeType == 'photon':

            flux = flc['fluxes']['total'] ### Should change this to grab models
            errors = flc['errors']['total']
        
        self.lcType = 'flux'
        self.fileName = flcFile[:-2]+"_"+self.makeType+"_lightcurve.fits"

        self.dataPoints = flux
        self.errors = errors
        self._WriteLightCurve()
