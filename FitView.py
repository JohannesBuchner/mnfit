from pymultinest import Analyzer
import probPlot
import matplotlib.pyplot as plt





class FitView(object):
    '''
    PUT INFO HERE

    '''

    def __init__(self,data):



        self.xlabel = "x"
        
        self._LoadData(data)



        #self.n_params = n_params
        #self.basename = basename
        
        self.anal  = Analyzer(n_params=self.n_params,outputfiles_basename=self.basename)


        self.bestFit = self.anal.get_best_fit()["parameters"]
        self.loglike = self.anal.get_best_fit()["log_likelihood"]

        self._StatResults()

        



    def _StatResults(self):
        '''
        Prints the statistical results of the fit
        as well as other information via the self._CustomInfo()
        set in inherited classes

        '''

        s = self.anal.get_stats() 

        print
        print "-"*30+" ANALYIS "+"-"*30
        print

        self._CustomInfo()
        print
        
        print "Global Evidence:\n\t%.3e +- %.3e" % ( s['nested sampling global log-evidence'],\
                                                     s['nested sampling global log-evidence error'] )

        
        print "LogLikelihood of Best Fit:\n\t %.2f"%self.loglike
        print
        print "-"*69
        

    def _CustomInfo(self):

        pass



    def _LoadData(self,data):

        pass


    def ViewChain(self):


        pass

    def ViewMarginals(self):

        marg = self.anal.get_stats()["marginals"]

        p = probPlot.PlotMarginalModes(self.anal)
        fig = plt.figure(figsize=(5*self.n_params,5*self.n_params))

        for i in range(self.n_params):
            ax = fig.add_subplot(self.n_params,self.n_params, i+1, axisbg="#FCF4F4")

            p.plot_marginal(i, with_ellipses=False , with_points = False, grid_points=50)

            marg1 = marg[i]["1sigma"]
            h=.005
            ax.hlines(h,marg1[0],marg1[1],color="#FF0040",linewidth=1.2)
            ax.plot(self.bestFit[i],h,"o",color="#FF0040")
            if i == 0:
                ax.set_ylabel("Probability")
            ax.set_xlabel(self.parameters[i])


            for j in range(i):

                ax = fig.add_subplot(self.n_params,self.n_params, self.n_params*(j+1)+i+1)
                p.plot_conditional(i, j, with_ellipses = False, with_points = False, grid_points=20)

                marg1 = marg[i]["1sigma"]
                marg2 = marg[j]["1sigma"]

                ax.hlines(self.bestFit[j],marg1[0],marg1[1],color="#FF0040",linewidth=1.2)
                ax.vlines(self.bestFit[i],marg2[0],marg2[1],color="#FF0040",linewidth=1.2)

                ax.plot(self.bestFit[i],self.bestFit[j],"o",color="#FF0040")

                if j==i-1:
                    ax.set_xlabel(self.parameters[i])
                    ax.set_ylabel(self.parameters[j])


        return ax


    def ViewFit(self):

        fig = plt.figure(120)
        ax = fig.add_subplot(111)

        yData = []


        for params in self.anal.get_equal_weighted_posterior()[::100,:-1]:

            tmp = []
            
            for x in self.dataRange:

                tmp.append(self.model(x, *params))
            yData.append(tmp)

        



        
        #Plot the spread in data
            
        for y in yData:

            ax.plot(self.dataRange,y,"#2EFE64") ## modify later

        bfModel = []


        # Plot the best fit
        for x in self.dataRange:

            bfModel.append(self.model(x, *self.bestFit))
        
            
        ax.plot(self.dataRange,bfModel,"#642EFE") #modify later

        ax.set_xlabel(self.xlabel)


        return ax
        
        

        
        pass


  
