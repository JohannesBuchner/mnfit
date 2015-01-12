from mnfit.mnfit import mnfit
from mnfit.mnPowerLawFit.chi2_2D import chi2_2D

from mnfit.mnPowerLawFit.PowerLawData import PowerLawData

from PowerLawData import PowerLawData


from numpy import array, log10
#from astropy.table import Table
import json

class mnPowerLawFit(mnfit):


    def LoadData(self,dataFile):
        '''
        Load a data file containing the x and y data and
        errors 

        '''

        
        self.data = PowerLawData(dataFile)
        self.dataFile = dataFile


        
        self.stat = chi2_2D() #Will always be using chi2_2D
    
        
        self._dataLoaded = True #Mark that data are loaded



        self.n_params = 2

        
        

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

    
    

    
        pass


    def SetModel(self,model):

        self.fitModel = model()
        self.ConstructLikelihood()

                
    def ConstructLikelihood(self):
        '''
        Provides a likelihood function based off the data and
        model provided. This function is fed to MULTINEST.

        '''

        # The Likelihood function for MULTINEST

        def likelihood(cube, ndim, nparams):


            params = array([cube[i] for i in range(ndim)])
            logL = 0. # This will be -2. * log(L)




            if self.data.xLog:
    
                self.stat.SetXerrors(self.data.GetLogXerr())
                self.fitModel.SetXdata(self.data.GetLogXdata())
            else:
                self.stat.SetXerrors(self.data.GetXerr())

                self.fitModel.SetXdata(self.data.GetXdata())
           
            
            #Calculates the model counts based off the params
            self.fitModel.SetParams(params)


            

            if self.data.yLog:
                self.stat.SetYdata(self.data.GetLogYdata())
                self.stat.SetYerrors(self.data.GetLogYerr())
                self.stat.SetModelData(log10(self.fitModel.GetModelY()))

            else:
                self.stat.SetYdata(self.data.GetYdata())
                self.stat.SetYerrors(self.data.GetYerr())
                self.stat.SetModelData(self.fitModel.GetModelY())

                
    
            self.stat.SetSlope(self.fitModel.GetSlope())
            
            logL = self.stat.ComputeLikelihood()

            
    
            #calculate the statistic




            jointLH = -0.5*(logL)

            return jointLH
        
        # Becuase this is inside a class we want to create a
        # likelihood function that does not have an object ref
        # as an argument, so it is created here as a callback

        self.likelihood = likelihood  #likelihood callback
        self.prior = self.fitModel.prior  #prior callback



    def _WriteFit(self):
        '''
        Private function that is called after running MULTINEST.
        It saves relevant information from the fits

        '''
        dof = len(self.data.GetXdata())-self.n_params




        # Construct the dictionary that will be read by
        # SpecFitView.
        out = {"outfiles":self.outfilesDir,\
               "basename":self.basename,\
               "params":self.fitModel.parameters,\
               "dataFile":self.dataFile,\
               "model":self.fitModel.modName,\
               "stat":self.stat.statName,\
               "dof":dof,\
               "pivot":self.fitModel.GetPivot(),\
               "ampLo":self.fitModel.GetAmpLo(),\
               "ampHi":self.fitModel.GetAmpHi(),\
               "indxLo":self.fitModel.GetIndxLo(),\
               "indxHi":self.fitModel.GetIndxHi(),\
               "xmin":self.data.GetXdata()[0],\
               "xmax":self.data.GetXdata()[-1]\
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
        print "\t%s"%self.fitModel.modName
        print

