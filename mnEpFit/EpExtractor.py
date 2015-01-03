import json
import matplotlib.pyplot as plt

class EpExtractor(object):

    def __init__(self,file,ext_name=""):


        self.ext_name = ext_name
        self._ReadFile(file)
        self._PrepareData()
        print self._tbins[0]
        plt.loglog(self._tbins,self._Ep)
        
        self._WriteJSON()

    def _ReadFile(self,file):
        '''
        Virtual function
        '''

        pass

    def _WriteJSON(self):


        outdata = {"Ep":self._Ep,\
                   "EpErr":self._EpErr,\
                   "tbins":self._tbins}


        f = open("%sep_save_file.json" % self.ext_name,'w')
        
        json.dump(outdata,f) # Write to a JSON file
               
        f.close()

                  
        

    
