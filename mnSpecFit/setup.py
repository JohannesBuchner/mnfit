
if __name__=="__main__":
    
    from distutils.core import setup
    from distutils.extension import Extension
    from Cython.Distutils import build_ext
    from Cython.Build import cythonize
    import numpy

    import cython_gsl


    ext_modules = [Extension("Model",["Model.pyx"]),Extension("cstat",["cstat.pyx"]),Extension("pgstat",["pgstat.pyx"])]



 

    setup(
        name = "rsptools",
        include_dirs = [numpy.get_include()],
        cmdclass = {'build_ext': build_ext},
        ext_modules = cythonize(ext_modules))
