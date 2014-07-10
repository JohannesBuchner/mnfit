cimport cython

cdef extern from "synchrotron.h":
    double synchrotron(double,double,double,double)
    double synchrotronComplex(double,double,double,double,double,double)
    double synchrotronPL(double, double, double, double, double)
    double synchrotronFast(double, double, double, double, double)
    double synchrotronPL_cutoff(double, double, double, double, double, double)

#Synchrotron from shock accelerated electrons
cpdef double synchrotronPy(double energy, double norm, double estar, double index):

    return synchrotron(energy, norm, estar, index)



#Synchrotron from shock accelerated electrons but with lots of parameters
cpdef double synchrotronComplexPy(double energy, double norm, double estar, double gammaMin, double gammaTH, double index):

    return synchrotronComplex(energy, norm, estar, gammaMin, gammaTH, index)


#Synchrotron from a power law of electrons
cpdef double synchrotronPLPy(double energy, double norm, double estar, double index, double gammaMin):

    return synchrotronPL(energy, norm, estar, index, gammaMin)

#Synchrotron from a power-law with a high-energy cutoff due to a max gamma
cpdef double synchrotronPL_CO_Py(double energy, double norm, double estar, double index, double gammaMin, double gammaMax):

    return synchrotronPL_cutoff(energy, norm, estar, index, gammaMin, gammaMax)



#Simple Fast cooled synchrotron
cpdef double synchrotronFastPy(double energy, double norm, double estar, double index, double gammaMin):

    return synchrotronFast(energy, norm, estar, index, gammaMin)





