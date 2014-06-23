cimport cython

cdef extern from "synchrotron.h":
    double synchrotron(double,double,double,double)





cpdef double synchrotronPy(double energy, double norm, double estar, double index):

    return synchrotron(energy, norm, estar, index)


