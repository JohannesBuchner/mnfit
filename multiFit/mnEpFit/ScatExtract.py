from mnfit.mnEpFit.EpExtractor import EpExtractor
from spectralTools.scatReader import scatReader


class ScatExtract(EpExtractor):
    '''
    Reads an SCAT file(s)

    '''


    def _ReadFile(self,scatfile):
    

        if type(scatfile) == list:


            scats  = map(scatReader,scatfile)

            scat = scats[0]

            for sc in scats[1:]:

                scat = scat + sc
        else:

            scat = scatReader(scatfile)

        self.scat = scat
        
