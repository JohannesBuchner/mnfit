import json
import matplotlib.pyplot as plt

class DataExtractor(object):

    def __init__(self):


        self._xSet = False
        self._ySet = False

    def Save(self,output="outputData"):


        
        self.output = output

        if (self._xSet and self._ySet):

            self._WriteJSON()
        else:

            print "Data not loaded!"


    def SetX(self,data,err,name="y",isLog = True):

        self._xData = data
        self._xErr  = err
        self._xName = name
        self._xLog = isLog 
        self._xSet = True 
        
    def SetY(self,data,err,name="y",isLog = True):

        self._yData = data
        self._yErr  = err
        self._yName = name
        self._yLog = isLog 
        self._ySet = True

    
    def _WriteJSON(self):


        outdata = {"xData":self._xData,\
                   "xErr":self._xErr,\
                   "yData":self._yData,\
                   "yErr":self._yErr,\
                   "xName":self._xName,\
                   "yName":self._yName,
                   "logX":self._xLog,\
                   "logY":self._yLog}


        f = open("%s.json" % self.output,'w')
        
        json.dump(outdata,f) # Write to a JSON file
               
        f.close()

                  
        

    
