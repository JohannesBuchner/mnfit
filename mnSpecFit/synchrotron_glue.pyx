cimport cython

cdef extern from "synchrotron.h":
    double synchrotron(double,double,double,double)
    double synchrotronComplex(double,double,double,double,double,double)
    double synchrotronPL(double, double, double, double, double)
{



cpdef double synchrotronPy(double energy, double norm, double estar, double index):

    return synchrotron(energy, norm, estar, index)

cpdef double synchrotronComplexPy(double energy, double norm, double estar, double gammaMin, double gammaTH, double index):

    return synchrotronComplex(energy, norm, estar, gammaMin, gammaTH, index)

cpdef double synchrotronPLPy(double energy, double norm, double estar, double index, double gammaMin):

    return synchrotronPL(energy, norm, estar, index, gammaMin)

