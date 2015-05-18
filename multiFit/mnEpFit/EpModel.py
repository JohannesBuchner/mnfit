



class EpModel(object):


    def __init__(self):


        self.prior = None
        self.n_params = None
        self.likelihood = None

    def SetTimes(self,times):

        self.timebins = times

    def SetParams(self, params):
        '''
        Pass the parameters to the model
        and then evaluate it
        '''

        self.params = params


        self._EvaluateModel()


    def GetModelCounts(self):

        return self.modelCounts
        
    def _EvaluateModel(self):
        '''
        Evaluate the model at its timebins
        
        '''


        self.modelCounts = self.model(self.timebins,*self.params)
