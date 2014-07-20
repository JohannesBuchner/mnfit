from Band import Band
from BandBB import BandBB
from PL2BB import PL2BB
from SBPL import SBPL 


from Synchrotron import Synchrotron
from SynchrotronComplex import SynchrotronComplex
from SynchrotronBB import SynchrotronBB
from Synchrotron_Cutoff import Synchrotron_Cutoff
from PLSynchrotron import PLSynchrotron
from PLSynchrotron_Cutoff import PLSynchrotron_Cutoff
from FastSynchrotron import FastSynchrotron
from TsviSlow import TsviSlow
from TsviFast import TsviFast

from Bandx2 import Bandx2
from Band_SBPL import Band_SBPL
from BandPL import BandPL
from BandBBPL import BandBBPL
from SynchSSC import SynchSSC


from BB2 import BB2

models = {"Band":Band,\
          "Band+BB": BandBB,\
          "PL2BB": PL2BB,\
          "Synchrotron":Synchrotron,\
          "SynchrotronComplex":SynchrotronComplex,\
          "SynchrotronBB":SynchrotronBB ,\
          "SBPL":SBPL,\
          "Two BBs":BB2,\
          "Synchrotron_Cutoff":Synchrotron_Cutoff,\
          "PLSynchrotron":PLSynchrotron,\
          "PLSynchrotron_Cutoff":PLSynchrotron_Cutoff,\
          "TsviSlow":TsviSlow,\
          "TsviFast":TsviFast,\
          "FastSynchrotron":FastSynchrotron,\
          "SynchSSC":SynchSSC,\
          "Bandx2":Bandx2,\
          "Band_SBPL":Band_SBPL,\
          "BandPL":BandPL,\
          "BandBBPL":BandBBPL\
}
