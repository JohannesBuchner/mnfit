
import pymultinest
import threading, subprocess
import os
#if not os.path.exists("chains"): os.mkdir("chains")




class mnfit:


    def __init__(self,silent=False):
        '''
        This is a Bayesian MC utilizing the package
        multinest to explore the posterior space of the 
        parameter

        '''

        self.silent = silent
        self.n_live_points = 100
        self.importance_nested_sampling = False
        self.resume = False
        self.verbose = True
        self.sampling_efficiency = 'model'
        


    def LoadData(self):

        pass

    def Explore(self):
        '''
        This member function invokes multinest.
        The data must be loaded and the likihood set

        '''
        if not os.path.exists("chains"): os.mkdir("chains")
        
        # we want to see some output while it is running
        if not self.silent:
            print "SILENT"
            progress = pymultinest.ProgressPlotter(n_params = self.n_params); progress.start()
            threading.Timer(2, show, ["chains/1-phys_live.points.pdf"]).start() # delayed opening


        # run MultiNest
        pymultinest.run(self.likelihood, self.prior, self.n_params, importance_nested_sampling = self.importance_nested_sampling, resume = self.resume, verbose = self.verbose, sampling_efficiency = self.sampling_efficiency, n_live_points = self.n_live_points, init_MPI=False)


        # ok, done. Stop our progress watcher
        if not self.silent:
            progress.stop()

        
        

    def PlotParamDists(self):

        pass


    def ExportFit(self):

        pass
