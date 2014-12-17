from mnfit.mnfit import mnfit
from mnfit.mnPulseFit.chi2 import chi2

from EpEvo import EpEvo


from numpy import array
#from astropy.table import Table
import json

class mnEpFit(mnfit):


    def LoadData(self,EpEvoFile):
        '''
        An EpEvofile is read in. It is JSON file containing the Ep and time
        derived from either an SCAT or in the future, an mnSpecFit file

        '''

        
        self.EpEvo = EpEvo(EpEvoFile)

        self.stat = chi2() #Will always be using chi2
    
        
        self._dataLoaded = True #Mark that data are loaded

                    
    def SetOffset(self,offset):

        self.EpEvo.SetOffset(offset)


        

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

    def SetEpModel(self, model):
        '''
        Pass a model class which will be instantiated
        

        _____________________________________________________________
        arguments:
        model: a derived Model class

        '''
        self.epModel = model()
        
        self.n_params = self.epModel.n_params


        # In this case I can go ahead and construct
        # the likelihood... because I'm fucking awesome!
        self.ConstructLikelihood()

    
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

            #Get the time intervals
            self.epModel.SetTimes(self.EpEvo.GetTimeBins())
    
            
            #Calculates the model counts based off the params
            self.epModel.SetParams(params)

            self.stat.SetModelCounts(self.epModel.GetModelCounts())



            self.stat.SetCounts(self.EpEvo.GetEp())
            self.stat.SetErrors(self.EpEvo.GetErr())

            logL = self.stat.ComputeLikelihood()



            #calculate the statistic




            jointLH = -0.5*(logL)

            return jointLH
        
        # Becuase this is inside a class we want to create a
        # likelihood function that does not have an object ref
        # as an argument, so it is created here as a callback

        self.likelihood = likelihood  #likelihood callback
        self.prior = self.epModel.prior  #prior callback



    def _WriteFit(self):
        '''
        Private function that is called after running MULTINEST.
        It saves relevant information from the fits

        '''
        dof = len(self.EpEvo.GetTimeBins())-self.n_params




        # Construct the dictionary that will be read by
        # SpecFitView.
        out = {"outfiles":self.outfilesDir,\
               "basename":self.basename,\
               "params":self.epModel.parameters,\
               "EpEvo":self.EpEvo.fileName,\
               "model":self.epModel.modName,\
               "stat":self.stat.statName,\
               "dof":dof,\
               "tmin":self.EpEvo.GetTimeBins()[0],\
               "tmax":self.EpEvo.GetTimeBins()[-1]\
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
        print "\t%s"%self.epModel.modName
        print

