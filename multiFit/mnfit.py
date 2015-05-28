import pymultinest
import threading, subprocess
import os
import time




class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
                                    


class mnfit:


    def __init__(self,silent=True,live_points = 1000, ins=True, resume = True, verbose = False, sampling_efficiency = 'model', write=True):
        '''
        This is a Bayesian MC utilizing the package
        multinest to explore the posterior space of the 
        parameters.

        __________________________________________________________
        keyword args:
        silent: [False/True]   turns off/on live tracking via pdf
        live_points: number of active points 
        ins: [True/False]  turn on/off information sampling
        resume: [True/False] turn on/off resuming chain from last run
        verbose: [True/False] turn on/off verbose output
        sampling_efficiency: blah blah blah

        '''

        self.callback = None
        self.silent = silent
        self.n_live_points = live_points
        self.importance_nested_sampling = ins
        self.resume = resume
        self.verbose = verbose
        self.sampling_efficiency = sampling_efficiency
        self.basename = "chains/1-"
        self.savefile="fit"
        self.write = write
        self._dataLoaded = False
        self._saveFileSet = False

    def SetBasename(self,basename):
        '''
        Set the basename for writing the mcmc chains
        '''

        self.basename = basename
        

    def LoadData(self):
        '''
        Functionality set in subclass
        '''

        print "Generic Loader. This must be inherited"

        pass

    def Explore(self):
        '''
        This member function invokes multinest.
        The data must be loaded and the likihood set

        '''
        print bcolors.WARNING+'___________________________________________________'+bcolors.ENDC
        print bcolors.WARNING+'|'+bcolors.OKBLUE+' _____       _____                 _____  _  _   '+bcolors.WARNING+'|'+bcolors.ENDC
        print bcolors.WARNING+'|'+bcolors.OKBLUE+'|     | ___ |   __| ___  ___  ___ |   __||_|| |_ '+bcolors.WARNING+'|'+bcolors.ENDC
        print bcolors.WARNING+'|'+bcolors.OKBLUE+'| | | ||   ||__   || . || -_||  _||   __|| ||  _|'+bcolors.WARNING+'|'+bcolors.ENDC
        print bcolors.WARNING+'|'+bcolors.OKBLUE+'|_|_|_||_|_||_____||  _||___||___||__|   |_||_|  '+bcolors.WARNING+'|'+bcolors.ENDC
        print bcolors.WARNING+'|'+bcolors.OKBLUE+'                   |_|                           '+bcolors.WARNING+'|'+bcolors.ENDC
        print bcolors.WARNING+'|                                                 |'+bcolors.ENDC
        print bcolors.WARNING+'|                                                 |'+bcolors.ENDC
        print bcolors.WARNING+'|                                                 |'+bcolors.ENDC
        print bcolors.WARNING+'|                          '+bcolors.OKGREEN+'-J. Michael Burgess'+bcolors.WARNING+'    |'+bcolors.ENDC
        print bcolors.WARNING+'|                                                 |'+bcolors.ENDC
        print bcolors.WARNING+'|_________________________________________________|'+bcolors.ENDC

        #print
        #print "%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%"
        #print
        #print "License Info:"
        #print "\t Don't read this.\n\t Do whatever the hell you want with this software"
        #print
        #print "%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%"

        
        if not self._dataLoaded: #Make sure to have loaded data
            print
            print bcolors.FAIL+ "YOU HAVE NOT LOADED ANY DATA!!"+ bcolors.ENDC
            print
            return

        if not self._saveFileSet: #Warn that no savefile is set
            print
            print bcolors.WARNING+"Save file not set!!! Fit params not saved!"+ bcolors.ENDC
            print

        outfilesDir = ""
        tmp = self.basename.split('/')
        for s in tmp[:-1]:
            outfilesDir+=s+'/'
            
        self.outfilesDir = outfilesDir
        

        if not os.path.exists(outfilesDir): os.makedirs(outfilesDir)
        
        # we want to see some output while it is running
        if not self.silent:
            print "SILENT"
            progress = pymultinest.ProgressPlotter(n_params = self.n_params); progress.start()
            threading.Timer(2, show, [self.basename+"phys_live.points.pdf"]).start() # delayed opening
        startTime = time.time()

        self._PreFitInfo()

        # run MultiNest
        pymultinest.run(self.likelihood, self.prior, self.n_params, importance_nested_sampling = self.importance_nested_sampling, resume = self.resume, verbose = self.verbose, sampling_efficiency = self.sampling_efficiency, n_live_points = self.n_live_points,outputfiles_basename=self.basename, init_MPI=False, dump_callback=self.callback,write_output=self.write)


        # ok, done. Stop our progress watcher
        if not self.silent:
            progress.stop()

        print 
        print bcolors.OKGREEN +"Finished sampling in %.2f seconds"%(time.time()-startTime) + bcolors.ENDC
        print
        if self._saveFileSet:
            self._WriteFit()

    def _WriteFit(self):

        print "Generic Writer. This must be inherited"

    def _PreFitInfo(self):

        pass
