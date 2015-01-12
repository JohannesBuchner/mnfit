import numpy as np


from mnfit.Likelihood import Likelihood




class chi2_2D(Likelihood):



    def _SetName(self):
        self.statName = "chi2_2D"

    def SetYdata(self,yData):

        self.yData = yData




    def SetYerrors(self,yErr):

        self.yErr = yErr

    def SetXerrors(self,xErr):

        self.xErr = xErr

        
    def SetModelData(self,modelData):

        self.modelData = modelData
        

    def ComputeLikelihood(self):

        Y=np.array(self.yData)
               
        M=np.array(self.modelData)
        YErr = np.array(self.yErr)
        XErr = np.array(self.xErr)

         S = (Y-M)/np.sqrt(np.power(YErr,2.)+ np.power(self.slope,2)*np.power(XErr,2) )


        sSum = np.sum(S)

        return sSum





