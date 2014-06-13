from pymultinest import Analyzer
import probPlot
import matplotlib.pyplot as plt





class FitView(self):
    '''
    PUT INFO HERE

    '''

    def __init__(selfdata):

        
        self._LoadData(data)



        #self.n_params = n_params
        #self.basename = basename
        
        self.anal  = Analyzer(n_params=self.n_params,outputfiles_basename=self.basename)


        self.bestFit = self.get_best_fit()["parameters"]
        self.loglike = self.get_best_fit()["log_likelihood"]


    def _LoadData(self,data):

        pass


    def ViewChain(self):


        pass

    def ViewMarginals(self):

        marg = self.anal.get_stats()["marginals"]

        p = probPlot.PlotMarginalModes(self.anal)
        fig = plt.figure(figsize=(5*self.n_params,5*self.n_params))

        for i in range(self.n_params):
            ax = fig.add_subplot(self.n_params,self.n_params, i+1)

            p.plot_marginal(i, with_ellipses=False , with_points = False, grid_points=50)

            ax.vlines(self.bestFit[i],0,.1,color="#FF0040")

            if i == 0:
                ax.set_ylabel("Probability")
            ax.set_xlabel(self.parameters[i])


            for j in range(i):

                ax = fig.add_subplot(self.n_params,self.n_params, self.n_params*(j+1)+i+1)
                p.plot_conditional(i, j, with_ellipses = False, with_points = False, grid_points=20)

                marg1 = marg[i]["1sigma"]
                marg2 = marg[j]["1sigma"]

                ax.hlines(bf[j],marg1[0],marg1[1],color="#FF0040")
                ax.vlines(bf[i],marg2[0],marg2[1],color="#FF0040")

                ax.plot(bf[i],bf[j],"o",color="#FF0040")

                if j==i-1:
                    ax.set_xlabel(self.parameters[i])
                    ax.set_ylabel(self.parameters[j])

        pass


    def ViewFit(self):

        fig = plt.figure(120)
        ax = fig.add_subplot(111)

        yData = map(lambda params: self.model(self.dataRange,*params) ,self.anal.get_equal_weighted_posterior()[::100,:-1])


        for y in yData:

            ax.plot(self.dataRange,y,"b") ## modify later


        
        ax.plot(self.dataRange,self.model(self.dataRange,*self.bestFit),"r") #modify later


        return ax
        
        

        
        pass
