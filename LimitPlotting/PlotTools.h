// $Id: PlotTools.h,v 1.5 2012/06/26 13:58:23 auterman Exp $

/*** ------------------------------------------------------------------------------------------------------- ***
     TheBetterPlotScript, a tool to plot final results, limits and exclusion contours, based on 'PlotScript'

     Christian Autermann, Hamburg University/LPC, February 2012
 *** ------------------------------------------------------------------------------------------------------- ***/

#ifndef PLOTTOOLS_H
#define PLOTTOOLS_H

#include <vector>
#include <string>

#include "Overview.h"
#include "Event.h"
#include "table.h"

class TGraph;
class SusyScan;
class TH2;
class TH1;
class TCanvas;


///The last line of defense: Fill all empty bins with one defined double (1 means not-excluded in the in/out hists)
void      FillEmptyPoints(TH2*h, const double def=1);

///Used internally and for debugging: All contours, sorted by length, are returned in an vector
std::vector<TGraph *> GetContours(TH2*, int ncont=20);

///The graph 'g' is cut in 'x' or 'y' '<' or '>' than the value 'cut'
void      Cut(TGraph * &g, const char f, const char c, double cut);

///The graph 'g' is smoothed. 'n' determines the number of points used for the Gaussian average
void      Smooth(TGraph * g, int n=3, int flag=0);

///The 2D hsitogram 'g' is smoothed. 'n' determines the number of bins (radius) used for the Gaussian average
void      Smooth(TH2 * g, int n=3);

///The area between 'g1' and 'g2' is filled
TGraph*   MakeBand(TGraph *g1, TGraph *g2, bool b=false);

///returns the official cMSSM plotting template, i.e. the background with previous limits, etc
TCanvas*  GetLimitTemplateCanvas(std::string file,std::string key);

TH2 * BinWiseOr(TH2*h1, TH2*h2);

void SetZRange(TH2 * h, TH2*h2=0);

class PlotTools {
 public:
 
  ///Constructor taking the vector of scan-points as argument. Determines the maximal number of search channels (bins).
  PlotTools(Events * scan):scan_(scan){
    for (Events::const_iterator evt=scan->begin();evt!=scan->end();++evt){
      int nc=evt->Get("n_channels"); 
      if(nc>nchannels_)nchannels_=nc;
  } }
  
  PlotTools(){scan_=new Events();};
  
  ///Clone
  PlotTools * Clone();
  
  ///Fill 2D histogram 'h' in 'x' and 'y' with variable 'f'
  void Area(   TH2*h, const std::string& x, const std::string& y, const std::string& f);

  ///Fill 2D histogram 'h' in 'x' and 'y' with the boolean result of the comparison 'co' of 'f' with 'value', e.g. "ObsR" LessThan 1.0
  void InOut(  TH2*h, const std::string& x, const std::string& y, const std::string& f, const Compare::comparator co, const double value=1.0);

  ///Fill 2D histogram 'h' in 'x' and 'y' with the boolean result of 'f' LessThan 1.0. Before, the 2D histogram of 'f' is smoothed using the steering parameter 'param'
  void InOutFromR(TH2*h, const std::string& x, const std::string& y, const std::string& f, int param=3);

  ///Fill a 1D histogram 'h' with the variable 'f'
  void Hist(TH1*h, const std::string& f);

  ///returns a vector 'v' containing the variables 'f'. Used, e.g. to calculate the median and sigma-quantiles of 'f'.
  void VectorOf(std::vector<double>& v, const std::string& f);

  ///Fills empty points of the scan by linear interpolation (currently only in 'x'). No extrapolation is done.
  void FillEmptyPointsByInterpolation(const std::string& x, const std::string& y);
  void FillEmptyPointsByInterpolationOld(const std::string& x, const std::string& y);
  void FillEmptyPointsByInterpolation1D(const std::string& x, const std::string& y);
  
  ///Increases the bin granularity in 'x' and 'y' by a factor of two, increasing the number of points by a factor of four.
  void ExpandGrid(const std::string& x, const std::string& y );
  
  ///Returns contour number 'flag' of a vector of all found contours sorted by length. 'ncont' specifies the number of differnt heights for wich contours are calculated. 'flag' can be larger than 'ncont'.
  TGraph * GetContour(TH2*, int ncont=20, int flag=0);

  ///Returns contour number 'flag' of a vector of all found contours sorted by length. 'ncont' specifies the number of differnt heights for wich contours are calculated. 'flag' can be larger than 'ncont'.
  TGraph * GetContour(TH2*,const std::string& x,const std::string& y,const std::string& f, 
                      int ncont=20, int flag=0,int color=1, int style=1, TH2* o=0);

  ///Delete points, for which the boolean result of the operation 'co' of 'var' with 'value' is true. 
  void Remove(const std::string& var, const Compare::comparator co, double value);

  void Print(const std::string& varvar, const Compare::comparator coco, double valvalue, const std::string& var="", const Compare::comparator co=Compare::equal, double value=0);

/*
  TGraph * Line( double(*x)(const T*), double(*y)(const T*), 
                 double(*func)(const T*), const double mass, const double diff=5.);
  
  
  void Graph(  TGraph*g, double(*x)(const T*), double(*y)(const T*), double ymin=-999. );
    

  void Print(double(*x)(const T*), double(*x2)(const T*), double(*y)(const T*),
             TGraph*, double p=10.);
  void Print(double(*x)(const T*), double(*x2)(const T*), double(*y)(const T*), double(*x3)(const T*), double(*y2)(const T*),
             TGraph*, double p=10.);
*/
    
  TH2 * GetHist(const std::string& x, const std::string& y);
  
  ///add (more) scan points
  void addEvents(Events*evts){scan_->insert(scan_->end(),evts->begin(),evts->end());}

  ///add (more) scan points
  void addEvents(Event evt){scan_->push_back(evt);}
  
  int N_Channels() const{return nchannels_;};
  void Set_N_Channels(int n) {nchannels_=n;};
 private:
  
  Events * scan_; 
  int plotindex_;
  int nchannels_; 

};

///helper class to sort a vector of TGraphs by the length of the graphs
class sort_TGraph{
  public:
   sort_TGraph(){}
   bool operator()(const TGraph*g1, const TGraph*g2);
};


TGraph* Atlas0l24j_1fb( );
TGraph* RA2Observed_36pb();
TGraph* RA2Observed_1fb( );
TGraph* gl_LEP();
TGraph* sq_TEV();
TGraph* sq_CDF();
TGraph* sq_DEZ();
TGraph* glsq_NoSol();
TGraph* glsq_NoSol_aux();


#endif
