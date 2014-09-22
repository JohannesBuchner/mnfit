from mnfit.mnfit import mnfit
from PulseModel import PulseModel
from numpy import array
from astropy.table import Table
import json

class mnPulseFit(mnfit):


    def LoadData(self,dataBins):
        '''
        This member loads a light curve object. The lightcurve object
        is either built from TTE data or from flux points. depending on 
        which, a statistics is chosen. Chi2 for flux data and pgstat for 
        TTE data.

        '''


        #Load the LC object and check is type

        #Choose a statistic


        

        pass




    


    



            


    def SetSaveFile(self,savefile):
        '''
        Set the name of the json file to be created
        after the fit is made

        ____________________________________________________________
        arguments:
        savefile: str() file name


        '''
        self.savefile = savefile
        self._saveFileSet = True

    def SetPulseModel(self, model):
        '''
        Pass a model class which will be instantiated
        

        _____________________________________________________________
        arguments:
        model: a derived Model class

        '''

        
        self.n_params = self.model.n_params

        pass

    def ConstructLikelihood(self):
        '''
        Provides a likelihood function based off the data and
        model provided. This function is fed to MULTINEST.

        '''

        # The Likelihood function for MULTINEST
        def likelihood(cube, ndim, nparams):


            params = array([cube[i] for i in range(ndim)])
            logL = 0. # This will be -2. * log(L)


            #Calculates the model counts based off the params

            #calculate the statistic
            
            

            
            jointLH = -0.5*(logL)
            #jointLH = logL    
            return jointLH
        
        # Becuase this is inside a class we want to create a
        # likelihood function that does not have an object ref
        # as an argument, so it is created here as a callback

        self.likelihood = likelihood  #likelihood callback
        self.prior = self.models[0].prior  #prior callback



    def _WriteFit(self):
        '''
        Private function that is called after running MULTINEST.
        It saves relevant information from the fits

        '''


        dof = len(self.lightcurve.timeBins)

        # need to subtract off the number of fit params

        
        
       # Construct the dictionary that will be read by
       # SpecFitView.
        out = {"outfiles":self.outfilesDir,\
               "basename":self.basename,\
               "duration":self.lightcurve.duration,\
               "params":self.pulseModel.parameters,\
               
               "lightCurve":self.lightcurve.fileLoc,\
               "model":self.pulseModel.modName,\
               "stat":self.stat.statName,\
               "dof":dof,\
               
               "tmin":self.lightcurve.tmin,\
               "tmax":self.lightcurve.tmax\
        }

        f = open(self.outfilesDir+self.savefile,'w')
        
        json.dump(out,f) # Write to a JSON file
        print
        print "Wrote "+self.outfilesDir+self.savefile
        print
        print
        
        f.close()

        

    def _PreFitInfo(self):

        print "Starting fit of model:"
        print "\t%s"%self.pulseModel.modName
        print

