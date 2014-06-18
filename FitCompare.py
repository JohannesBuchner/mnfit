


class FitCompare(object):
    '''
    Compare evidences from mnfit chains
    '''
    def __init__(self,fits):
        '''
        Loads the fits and creates an array of analyzers
        to compare with

        '''

        analyzers = []
        modelnames = []
        parameters = []

        # Loop over the loaded chains and fit files
        for f in fits:

            self._LoadData(fit) #method should attach self.modelnames and self.parameters

            anal = Analyzer(n_params=self.n_params,outputfiles_basename=self.basename)
            analyzers.append(anal)  #Gather the analyzers
            modelnames.append(self.modName)  #Gather the model names
            parameters.append(self.parameters)  #Gather the parameter names of the models


        self.analyzers = analyzers
        self.modelnames = modelnames
        self.parameters = parameters

        #Call the private functions
        self._Evidence() #Compute logZ for each model
        self._SortModels()  # Sort the models based on logZ
        self._EvidenceMatrix() # Calculate the bayes factors
        self._PrintResults()
        
    def _Evidence(self):

        self.logZ = [] 
        
        for a in self.analyzers:


            s = a.get_stats()
            logZ = s['global evidence']/np.log(10.)
            self.logZ.append(logZ)



    
    
    def _SortModels(self):


        results = zip(self.modelnames,self.parameters ,self.analyzers, self.logZ)
        results = sorted(results, key=lambda (self.modelnames, self.parameters, self.analyzers,self.logZ): self.logZ)

        self.results = results


    def _EvidenceMatrix(self):


        deltaZ = []
        for i in range(len(self.results)):

            hiZ=self.results[i][2]

            for j in range(i):

                loZ = self.results[j][2]

                dZ  = hiZ - loZ
                deltaZ.append(dZ)

        self.deltaZ = deltaZ

    def _PrintResults(self):

        #First print best models
        print "_"*30 + "Model Rankings"+"_"*30
        print
        print "Model:\tlogZ:"
        print "------\t-----"
        for i in range(len(self.results) -1):
            print "%s\t%.2f"%(self.results[i][0],self.results[i][2])
        print "%s\t%.2f\t<---- BEST MODEL"
