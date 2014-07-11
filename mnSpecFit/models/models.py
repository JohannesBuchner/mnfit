from Band import Band
from BandBB import BandBB
from PL2BB import PL2BB
from SBPL import SBPL 

from Synchrotron import Synchrotron
from SynchrotronComplex import SynchrotronComplex
from SynchrotronBB import SynchrotronBB

from BB2 import BB2

models = {"Band":Band,\
          "Band+BB": BandBB,\
          "PL2BB": PL2BB,\
          "Synchrotron":Synchrotron,\
          "SynchrotronComplex":SynchrotronComplex,\
          "SynchrotronBB":SynchrotronBB ,\
          "SBPL":SBPL,\
          "Two BBs":BB2}
