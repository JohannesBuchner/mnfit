import json


class EpExtractor(object):

    def __init__(self,file):



        self._ReadFile(file)
        self._PrepareData()
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


        f = open("ep_save_file.json",'w')
        
        json.dump(outdata,f) # Write to a JSON file
               
        f.close()

                  
        

    
