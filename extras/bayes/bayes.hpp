#ifndef BAYES_HPP
#define BAYES_HPP

#include "common.hpp"
#include "distributions.hpp"
#include "kmeans.hpp"

class Bayes
{
  // data
  ublas::matrix<double> x;
  int n;
  int p;
  int k;

  // working
  ublas::matrix<double> probx;
  ublas::vector<double> pi;
  ublas::vector<ublas::vector<double> > mu;
  ublas::vector<ublas::matrix<double> > Omega;
  ublas::vector<int> z;

  // max loglik values
  double current;
  double loglik;
  ublas::vector<double> ml_pi;
  ublas::vector<ublas::vector<double> > ml_mu;
  ublas::vector<ublas::matrix<double> > ml_Omega;

  // storage
  std::vector<ublas::vector<int> > save_z;
  std::vector<ublas::vector<double> > save_pi;
  std::vector<ublas::vector<ublas::vector<double> > > save_mu;
  std::vector<ublas::vector<ublas::matrix<double> > > save_Omega;

public:
  // initialize data set x
  void init(const ublas::matrix<double>& _x, const int _n, const int _p, const int _k);

  // accessors
  double get_loglik() const { return loglik; }
  ublas::vector<double> get_ml_pi() const { return ml_pi; }
  ublas::vector<ublas::vector<double> > get_ml_mu() const { return ml_mu; }
  ublas::vector<ublas::matrix<double> > get_ml_Omega() const { return ml_Omega; }

  ublas::matrix<double> get_probx() const { return probx; }
  ublas::vector<double> get_pi() const { return pi; }
  ublas::vector<ublas::vector<double> > get_mu() const { return mu; }
  ublas::vector<ublas::matrix<double> > get_Omega() const { return Omega; }
  ublas::vector<int> get_z() const { return z; }
  std::vector<ublas::vector<double> > get_save_pi() const { return save_pi; }
  std::vector<ublas::vector<ublas::vector<double> > > get_save_mu() const { return save_mu; }
  std::vector<ublas::vector<ublas::matrix<double> > > get_save_Omega() const { return save_Omega; }
  std::vector<ublas::vector<int> > get_save_z() const { return save_z; }

  // mutators
  void set_pi(ublas::vector<double> _pi) { pi = _pi; }
  void set_mu(ublas::vector<ublas::vector<double> > _mu) { mu = _mu; }
  void set_Omega(ublas::vector<ublas::matrix<double> > _Omega) { Omega = _Omega; }

  // samplers
  void sample_zpi();
  void sample_muOmega();

  // driver
  void mcmc(const int nit, const int nmc, const string& data_file=".out", const bool record=false);
};

#endif
