from mnfit.mnfit import mnfit
from Model import Model



class mnSpecFit(mnfit):


    def LoadData(self,dataBins):
        '''
        This member aranges the DataBins and prepares them
        for sampling. The DataBin objects are astropy Tables
        that are created by separate objects which ultimately 
        make a uniform interface for reading here.

        args: DataBin or list of DataBins

        '''


        
        
        if type(dataBins)==list:
        
            self.detList = dataBins

        else:
            self.detList = [dataBins]


            
    def SetLikelihood(self,lhType):
        '''
        Pass a likelihood class. This is important because the method
        instantiates a likelihood object for each detector

        '''

        
        
        self.lhs = []
        for x in self.detList:

            lh = lhType()
            lh.tb = x.duration
            lh.ts = x.duration
            self.lhs.append(lh)
       
    def SetEnergyBounds(self,detector,lo,hi):

        for db in self.detList:

            if db.det == detector:

                db.SetHiChan(hi)
                db.SetLoChan(lo)
                return
        print "\n Detector: %s has not been loaded!  \n"
            



    def SetModel(self, model):
        '''
        
        Pass a model class which will be instantiated
        and the rsp loaded for each DataBin

        
        '''


        self.models = []

        for db in self.detList:

            mod = model()   # Instantiate a model
            mod.SetRSP(db.rsp) #Pass the rsp to model
            self.models.append(mod)
        self.n_params = self.models[0].n_params

        pass

    def ConstructLikelihood(self):
        '''
        Provides a likelihood function based off the data and
        model provided. This function is fed to MULTINEST.

        '''

        # The Likelihood function for MULTINEST
        def likelihood(params, n_dim, n_params):

            
            logL = 0. # This will be -2. * log(L)
            for det,mod,lh in zip(self.detList,self.models,self.lhs):
                
                
                # Here the model's params are set and the
                # and the matrix is convolved to get
                # model counts
                
                mod.SetParams(params) #set params for the models
                modCnts = mod.GetModelCnts() # convolve the matrix and ret counts

                lh.SetModelCounts(modCnts[det.activeLoChan:det.activeHiChan+1]) #pass model counts to lh

                # Here the DataBin objects' source and background
                # counts are sent to the likelihood object

                lh.SetBackGround(det.bkg[det.activeLoChan:det.activeHiChan+1],det.berr[det.activeLoChan:det.activeHiChan+1])
                lh.SetCounts(det.source[det.activeLoChan:det.activeHiChan+1])

                #This is log(L) so the joint stat is an addition
    

                logL+=lh.ComputeLikelihood()
            #print "logL = %f"%logL
            jointLH = exp(-0.5*(logL))
                
            return jointLH
        
        # Becuase this is inside a class we want to create a
        # likelihood function that does not have an object ref
        # as an argument, so it is created here as a functor
        
        self.likelihood = likelihood
        self.prior = self.models[0].prior
