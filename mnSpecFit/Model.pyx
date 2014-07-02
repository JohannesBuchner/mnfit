cimport cython
#cimport numpy as np
from scipy.integrate import quad, quadrature
from mnfit.Likelihood import Likelihood
from RSPconvolve import RSPconvolve
from numpy import array, zeros

class Model:



    def __init__(self):
        

        self.prior = 0
        self.n_params = 0
        self.likelihood = 0




    def SetParams(self, params):
        '''
        Set the parameters of the model

        ____________________________________________
        arguments:
        params: numpy array of paramerters

        '''


        self.params = params

        ####New code for faster convolution
        self._EvalModel()

        

    def integrate(self, lims):
        '''
        Intergrate the model via scipy.intergrate.quad
        over the limits. Note model must braodcasting aware

        ____________________________________________
        arguments:
        lims: [lo/hi]

        '''

        cdef double lowE = lims[0]
        cdef double highE = lims[1]

        cdef double result

        tmp = []

        for i in range(self.n_params):

            tmp.append(self.params[i])
            
        tmp = tuple(tmp)
        
        result = quad(self.model,lowE,highE,args=tmp,full_output=0,limit=100)[0]

        return result


    def _EvalModel(self):

        tmpCounts = zeros(len(self.rsp.photonE))

        #Low res bins

        lowRes = array( map(lambda e: self.model(e,*self.params),self.rsp.lowEne)) 

        medRes = array(map(lambda x: sum(map(lambda e: self.model(e,*self.params), x    ))/3.,self.rsp.medEne         ))

        hiRes = array(map(lambda x: sum(map(lambda e: self.model(e,*self.params), x    ))/7.,self.rsp.highEne         ))

        tmpCounts[self.rsp.lowEval]=lowRes
        tmpCounts[self.rsp.medEval]=medRes
        tmpCounts[self.rsp.highEval]=hiRes

        self.rsp.SetModelVec(tmpCounts)
        

        
    def SetRSP(self,rsp):
        '''
        Set the instrument response matrix for the model.

        ________________________________________________
        arguments:
        rsp: path to a fits rsp file
        
        sets self.rsp

        ##############
        29/6/2014

        Improving for a faster convolution process

        '''

        rsp = RSPconvolve(rsp)

        rsp.SetModel(self)

        self.rsp=rsp
    


        
    def GetModelCnts(self):
        '''
        Convolves the set model with the RSP and creates the 
        model counts

        ____________________________________________
        returns:
        modelCnts: numpy array of Convolved model counts.

        '''


        self.rsp.CreateModelVector()
        modelCnts = self.rsp.GetCounts()
        
        return array(modelCnts)[0]

        

    def SelectComponent(self,comp):
        '''
        Grabs the component parameters from the component
        dictionary that must be created in subclasses

        '''

        comp = self.componentLU[comp]

        return comp
        
        
