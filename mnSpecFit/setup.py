
from distutils.core import setup
from distutils.extension import Extension
from Cython.Distutils import build_ext
from Cython.Build import cythonize
import numpy

import cython_gsl


ext_modules = [Extension("Model",["Model.pyx"]),Extension("cstat",["cstat.pyx"]),Extension("pgstat",["pgstat.pyx"])]


#ext_modules = [Extension("rspCYTHON",["rspCYTHON.pyx"],libraries=cython_gsl.get_libraries(),library_dirs=[cython_gsl.get_library_dir()],include_dirs=[cython_gsl.get_cython_include_dir()]) ]
 

setup(
        name = "rsptools",
        include_dirs = [numpy.get_include()],
        cmdclass = {'build_ext': build_ext},
        ext_modules = cythonize(ext_modules)
    )
