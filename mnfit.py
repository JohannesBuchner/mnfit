
import pymultinest
import threading, subprocess
import os
import time




class mnfit:


    def __init__(self,silent=False,live_points = 1000, ins=True, resume = True, verbose = False, sampling_efficiency = 'model'):
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

        self.silent = silent
        self.n_live_points = live_points
        self.importance_nested_sampling = ins
        self.resume = resume
        self.verbose = verbose
        self.sampling_efficiency = sampling_efficiency
        self.basename = "chains/1-"
        self.savefile="fit"
        

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

        if not self.dataLoaded: #Make sure to have loaded data
            print
            print "YOU HAVE NOT LOADED ANY DATA!!"
            print
            return

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

        # run MultiNest
        pymultinest.run(self.likelihood, self.prior, self.n_params, importance_nested_sampling = self.importance_nested_sampling, resume = self.resume, verbose = self.verbose, sampling_efficiency = self.sampling_efficiency, n_live_points = self.n_live_points,outputfiles_basename=self.basename, init_MPI=False)


        # ok, done. Stop our progress watcher
        if not self.silent:
            progress.stop()

        print 
        print "Finished sampling in %.2f seconds"%(time.time()-startTime)
        print
        self._WriteFit()

    def _WriteFit(self):

        print "Generic Writer. This must be inherited"
