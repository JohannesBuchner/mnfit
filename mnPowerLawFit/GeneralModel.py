



class GeneralModel(object):


    def __init__(self):


        self.prior = None
        self.n_params = None
        self.likelihood = None

    def SetXdata(self,xData):

        self.xData = xData

    def SetParams(self, params):
        '''
        Pass the parameters to the model
        and then evaluate it
        '''

        self.params = params


        self._EvaluateModel()


    def GetModelY(self):

        return self.modelY

    def GetSlope(self):

        return self.params[1]

    def SetAmplitudeRange(self,lo,hi):


        self.ampHi = hi
        self.ampLo = lo

    def SetSlopeRange(self,lo,hi):

        self.indxLo = lo
        self.indxHi = hi
            
    def _EvaluateModel(self):
        '''
        Evaluate the model at its timebins
        
        '''


        self.modelY = self.model(self.xData,*self.params)
