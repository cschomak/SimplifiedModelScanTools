// $Id: plot.h,v 1.7 2012/06/29 20:27:21 auterman Exp $

/*** ------------------------------------------------------------------------------------------------------- ***
     TheBetterPlotScript, a tool to plot final results, limits and exclusion contours, based on 'PlotScript'

     Christian Autermann, Hamburg University/LPC, February 2012
 *** ------------------------------------------------------------------------------------------------------- ***/

#ifndef PLOT_H
#define PLOT_H

#include "PlotTools.h"
#include "GeneratorMasses.h"
#include "Plotting.h"

#include "TLatex.h"

#include <string>
#include <vector>


void GetPlotTools(PlotTools*& plotTools, std::string filename, const std::string& x, const std::string& y, std::string GeneratorFile="", unsigned factor=0);
void AddEvents(PlotTools*& plotTools, std::string filename, std::string GeneratorFile="");

class LimitGraphs{
 public:
  LimitGraphs(const std::string& scan, std::string gen, int factor, const std::string& x, const std::string y,
              const std::string& name, int nsmooth, int color, int idx_obs, int idx_exp, int idx_exp_m1, int idx_exp_p1, TH2*h=0):
	      name_(name),h_(h){

    Events * events = new Events();
    ReadEvents(*events, scan);
  
    //plotting helper functions
    PlotTool = new PlotTools(events);

    //Require an observed CLs limit:
    //plotTools->Remove("ObsR", Compare::less, 0.0);
    //PlotTool->FillEmptyPointsByInterpolation(x, y);

    if (!h_) h_= PlotTool->GetHist(x,y);

    //Make grid in Mzero, Mhalf finer by factors of 2 by linear interpolation
    //~ for (int i=2; i<=factor; i*=2)
      //~ PlotTool->ExpandGrid("gluino", "squark");
    for (int i=2; i<=factor; i*=2)
      PlotTool->ExpandGrid("sbottom", "neutralino2");
    // New 'pseudo' points are added, therefore the binning of all plots has to be made finer by a factor
    // of 2 in x and y for each "ExpandGrid
  
    //Add generator information of particles masses if a file is given
    if (gen!="") {
      std::vector<GeneratorMasses> GenMasses;
      ReadGeneratorMasses(GenMasses, gen);
      Match( GenMasses, *events);
    }  

    limits_[x+"_"+y+"_allObs"]       = PlotTool->GetContour(h_, x, y, "ObsR",   3, idx_obs,    color, 1);
    limits_[x+"_"+y+"_allExp"]       = PlotTool->GetContour(h_, x, y, "ExpR",   3, idx_exp,    color, 1);
    limits_[x+"_"+y+"_allExpM1"]     = PlotTool->GetContour(h_, x, y, "ExpRM1", 3, idx_exp_m1, color, 3);
    limits_[x+"_"+y+"_allExpP1"]     = PlotTool->GetContour(h_, x, y, "ExpRP1", 3, idx_exp_p1, color, 3);
    limits_[x+"_"+y+"_allObsAsym"]   = PlotTool->GetContour(h_, x, y, "ObsRasym",   3, idx_obs,    color, 1);
    limits_[x+"_"+y+"_allExpAsym"]   = PlotTool->GetContour(h_, x, y, "ExpRasym",   3, idx_exp,    color, 1);
    limits_[x+"_"+y+"_allExpM1Asym"] = PlotTool->GetContour(h_, x, y, "ExpRasymM1", 3, idx_exp_m1, color, 3);
    limits_[x+"_"+y+"_allExpP1Asym"] = PlotTool->GetContour(h_, x, y, "ExpRasymP1", 3, idx_exp_p1, color, 3);
    for (std::map<std::string,TGraph*>::iterator it=limits_.begin();it!=limits_.end();++it)
      Smooth(it->second, nsmooth);
  }

  TGraph * Limit(const std::string& l){return limits_[l];}
  TH2* GetHist(){return h_;}
  PlotTools * GetPlot(){return PlotTool;}
  std::string Name(){return name_;}
  ~LimitGraphs(){delete PlotTool;};

 private:
  TGraph * g_obs, *g_exp, *g_expm1, *g_expp1;
  TGraph * g_obs_asym, *g_exp_asym, *g_expm1_asym, *g_expp1_asym;
  std::map<std::string,TGraph*> limits_;
  TH2 * h_;
  std::string name_;
  PlotTools * PlotTool;
};

#endif
