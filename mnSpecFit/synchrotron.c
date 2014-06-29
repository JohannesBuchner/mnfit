#include "synchrotron.h"



double intergrand(double gamma, void *p)
{

  double f;
  struct synch_params *params = (struct synch_params *)p;
  double energy = (params->energy);
  double norm = (params->norm);
  double estar = (params->estar);
  double index = (params->index);

  
  double gammaMin = 90.;
  double gammaTH = 30.;


  f = electronDist(gamma,norm,index, gammaMin, gammaTH)*gsl_sf_synchrotron_1(energy/(estar*gamma*gamma));
  

  return f;
}



double electronDist(double gamma, double norm, double index, double gammaMin, double gammaTH)
{

  double ed;
  double ratio = gammaMin/gammaTH;

  double epsilon = pow(ratio,2.+index)*exp(-ratio);
  
    if (gamma<=gammaMin)
      {
	ed = norm * pow(gamma/gammaTH,2.) * exp(-(gamma/gammaTH));
      }
    else
      {
	ed = norm * epsilon * pow(gamma/gammaTH,-index);
      }	
	

  return ed;


}

double synchrotron(double energy, double norm, double estar, double index)
{
  gsl_set_error_handler_off();

  double result, error;

  double epsabs = 0;
  double epsrel = 1e-5;
  double abserr;
  size_t limit = 10000;


  
  gsl_integration_workspace *w = gsl_integration_workspace_alloc(10000);

  struct synch_params p = {energy, norm, estar, index};

  gsl_function F;
  F.function = &intergrand;
  F.params=&p;

  gsl_integration_qagiu(&F, 1., epsabs, epsrel,limit, w, &result, &abserr);
  
  
  gsl_integration_workspace_free(w);
  
  result/=energy;
  return result;


}
