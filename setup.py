#!/usr/bin/env python
 
from distutils.core import setup
from distutils.extension import Extension
from distutils.command.install_headers import install_headers
from Cython.Distutils import build_ext
from Cython.Build import cythonize

import os

#boost_root = os.environ.get("BOOSTROOT")

#if(boost_root):
#  #The user want to override pre-defined location of boost
  
#  print("\n\n **** Using boost.python from the env. variable $BOOSTROOT (%s)" %(boost_root))
  
#  include_dirs = [ os.path.join(boost_root,'include')]
#  library_dirs = [ os.path.join(boost_root,'lib') ]
  
#  print("     Include dir: %s" %(include_dirs))
#  print("     Library dir: %s" %(library_dirs))

#else:

#  include_dirs = []
#  library_dirs = []




import numpy



ext_modules = [Extension("multifit/likelihood/cstat",["multifit/likelihood/cstat.pyx"],include_dirs=[numpy.get_include()]),
               Extension("multifit/likelihood/pgstat",["multifit/likelihood/pgstat.pyx"],include_dirs=[numpy.get_include()]),
               Extension("multifit/likelihood/rmfit",["multifit/likelihood/rmfit.pyx"],include_dirs=[numpy.get_include()])]




setup(
    
    name="multiFit",
    
    packages = ['multiFit','multifit/likelihood'],

    include_dirs = [numpy.get_include()],                
    
    version = 'v0.0.1',
    
    description = "MultiNest Spectral and Temporal Fitting Framework",
    
    author = 'J. Michael Burgess',
    
    author_email = 'jmichaelburgess@gmail.com',
    
    url = 'https://github.com/drJfunk/mnfit',
    
    download_url = 'https://github.com/giacomov/3ML/archive/v0.0.5',
    
    keywords = ['Likelihood',"GBM", "Spectral"],
    
    classifiers = [],
    
    ext_modules=cythonize(ext_modules),
        
        
 
    
    install_requires=[
          'numpy',
          'scipy',
          'numexpr',
           #'emcee',
          'astropy',
          'matplotlib',
          'ipython>=2.0.0, <3.0.0'          
      ])

