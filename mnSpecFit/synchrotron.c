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


/*

  More complex synchrotron model

 */

double synchrotronComplex(double energy, double norm, double estar, double gammaMin, double gammaTH, double index)
{
  gsl_set_error_handler_off();

  double result, error;

  double epsabs = 0;
  double epsrel = 1e-5;
  double abserr;
  size_t limit = 10000;


  
  gsl_integration_workspace *w = gsl_integration_workspace_alloc(10000);

  struct synch_params_complex p = {energy, norm, estar, gammaMin, gammaTH, index};

  gsl_function F;
  F.function = &intergrand;
  F.params=&p;

  gsl_integration_qagiu(&F, 1., epsabs, epsrel,limit, w, &result, &abserr);
  
  
  gsl_integration_workspace_free(w);
  
  result/=energy;
  return result;


}

double intergrandComplex(double gamma, void *p)
{

  double f;
  struct synch_params_complex *params = (struct synch_params_complex *)p;
  double energy = (params->energy);
  double norm = (params->norm);
  double estar = (params->estar);
  double index = (params->index);

  
  double gammaMin = (params->gammaMin);
  double gammaTH = (params->gammaTH);


  f = electronDist(gamma,norm,index, gammaMin, gammaTH)*gsl_sf_synchrotron_1(energy/(estar*gamma*gamma));
  

  return f;
}


/* PL Synch*/



double electronPL(double gamma, double norm, double index, double gammaMin)
{

  double ed;


  ed = norm * (index - 1.) * pow(gammaMin,index-1.)  *pow(gamma,-index);
	
	

  return ed;


}

double intergrandPL(double gamma, void *p)
{

  double f;
  struct synch_params_pl *params = (struct synch_params_pl *)p;
  double energy = (params->energy);
  double norm = (params->norm);
  double estar = (params->estar);
  double index = (params->index);
  double gammaMin = (params->gammaMin);
  


  f = electronPL(gamma,norm,index, gammaMin)*gsl_sf_synchrotron_1(energy/(estar*gamma*gamma));
  

  return f;
}

double synchrotronPL(double energy, double norm, double estar, double index, double gammaMin)
{
  gsl_set_error_handler_off();

  double result, error;

  double epsabs = 0;
  double epsrel = 1e-5;
  double abserr;
  size_t limit = 10000;


  
  gsl_integration_workspace *w = gsl_integration_workspace_alloc(10000);

  struct synch_params_pl p = {energy, norm, estar, index, gammaMin};

  gsl_function F;
  F.function = &intergrand;
  F.params=&p;

  gsl_integration_qagiu(&F, gammaMin, epsabs, epsrel,limit, w, &result, &abserr);
  
  
  gsl_integration_workspace_free(w);
  
  result/=energy;
  return result;



}




/**********

	  Fast cooled synchrotron


**************/

double intergrandFast(double gamma, void *p)
{

  double f;
  struct synch_params_fast *params = (struct synch_params_fast *)p;
  double energy = (params->energy);
  double norm = (params->norm);
  double estar = (params->estar);
  double index = (params->index);
  double gammaMin = (params->gammaMin);
  

  f = electronDistFast(gamma,norm,index, gammaMin)*gsl_sf_synchrotron_1(energy/(estar*gamma*gamma));
  

  return f;
}


double electronDistFast(double gamma, double norm, double index, double gammaMin)
{

  double ed;
  

  double epsilon = norm*gammaMin/(gamma*gamma);
  
    if (gamma<=gammaMin)
      {
	ed = epsilon;
      }
    else
      {
	ed = epsilon*pow(gamma/gammaMin,1-index)
      }	
	

  return ed;


}

double synchrotronFast(double energy, double norm, double estar, double index)
{
  gsl_set_error_handler_off();

  double result, error;

  double epsabs = 0;
  double epsrel = 1e-5;
  double abserr;
  size_t limit = 10000;


  
  gsl_integration_workspace *w = gsl_integration_workspace_alloc(10000);

  struct synch_params_fast p = {energy, norm, estar, index, gammaMin};

  gsl_function F;
  F.function = &intergrand;
  F.params=&p;

  gsl_integration_qagiu(&F, 1., epsabs, epsrel,limit, w, &result, &abserr);
  
  
  gsl_integration_workspace_free(w);
  
  result/=energy;
  return result;


}




