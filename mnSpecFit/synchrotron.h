#include <math.h>
#include <gsl/gsl_integration.h>
#include <gsl/gsl_sf.h>
#include <gsl/gsl_errno.h>





double intergrand(double gamma, void *p);


double synchrotron(double energy, double norm, double estar, double index);


double electronDist(double gamma, double norm, double index, double gammaMin, double gammaTH);
  
  
struct synch_params {double energy; double norm; double estar; double index;};
