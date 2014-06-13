from rsp import rsp
import numpy as np
from joblib import Parallel, delayed

class RSPconvolve:


    def __init__(self,rspFile):


        thisRSP = rsp(rspFile)

        self.drm = thisRSP.drm
        self.channelE = thisRSP.channelE
        self.photonE = thisRSP.photonE

        del thisRSP

        #energyChans = range(len(self.photonE)) ###Modify!
        
    def SetModel(self,model):
        '''
        Pass a function that is the spectral model for the fit


        '''

        self.model = model

        return


    def CreateModelVector(self):
        '''
        Call the Cython integrator to make a vector that will 
        be convolved with the DRM.

        '''
        #print "DIE"
        
        vec=[]
        for lim in self.photonE:
            vec.append(self.model.integrate(lim))

        
        self.vec = vec

        
        self._ConvolveMatrix()


    def _ConvolveMatrix(self):

        self.counts = np.dot(self.drm.transpose(),self.vec)


    def GetCounts(self):

        return self.counts


    
