



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

    def GetPivot(self):

        return self.pivot

    def GetAmpHi(self):

        return self.ampHi

    def GetAmpLo(self):

        return self.ampLo

    def GetIndxHi(self):

        return self.indxHi

    def GetIndxLo(self):

        return self.indxLo

    
            
    def _EvaluateModel(self):
        '''
        Evaluate the model at its timebins
        
        '''


        self.modelY = self.model(self.xData,*self.params)
