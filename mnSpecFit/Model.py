
#cimport numpy as np
from scipy.integrate import quad, quadrature
from mnfit.Likelihood import Likelihood
from RSPconvolve import RSPconvolve
from numpy import array

class Model:



    def __init__(self):


        self.prior = 0
        self.n_params = 0
        self.likelihood = 0




    def SetParams(self, params):
        self.params = params
    


   # def SetEval(self, model):

   #     self.model = model


        

    def integrate(self, lims):

        lowE = lims[0]
        highE = lims[1]

        


        result = quad(self.model,lowE,highE,args=tuple(self.params))[0]

        return result






    def SetRSP(self,rsp):


        rsp = RSPconvolve(rsp)
        rsp.SetModel(self)
        self.rsp=rsp
    

    def GetModelCnts(self):
        '''


        '''


        self.rsp.CreateModelVector()
        modelCnts = self.rsp.GetCounts()
        
        return array(modelCnts)[0]

        


        
        
