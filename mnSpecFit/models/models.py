from Band import Band
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
from SynchSSC import SynchSSC
from CPL import CPL
from BandCO import BandCO
from ZhaoSynchrotron import ZhaoSynchrotron
from FastSynchrotronBB import FastSynchrotronBB
from SynchSSC_BB import SynchSSC_BB
from BB import BB
from PL import PL


models = {"Band":Band,\
          "Synchrotron":Synchrotron,\
          "SynchrotronComplex":SynchrotronComplex,\
          "SynchrotronBB":SynchrotronBB ,\
          "SBPL":SBPL,\
          "Synchrotron_Cutoff":Synchrotron_Cutoff,\
          "PLSynchrotron":PLSynchrotron,\
          "PLSynchrotron_Cutoff":PLSynchrotron_Cutoff,\
          "TsviSlow":TsviSlow,\
          "TsviFast":TsviFast,\
          "FastSynchrotron":FastSynchrotron,\
          "SynchSSC":SynchSSC,\
          "CPL":CPL,\
          "BandCO":BandCO,\
          "ZhaoSynchrotron":ZhaoSynchrotron,\
          "FastSynchrotronBB":FastSynchrotronBB,\
          "SynchSSC_BB":SynchSSC_BB,\
          "blackbody":BB,\
          "powerlaw":PL,\
}
