// $Id: plotDiPhoton.cc,v 1.3 2012/06/26 13:58:23 auterman Exp $

/*** ------------------------------------------------------------------------------------------------------- ***
     TheBetterPlotScript, a tool to plot final results, limits and exclusion contours, based on 'PlotScript'

     Christian Autermann, Hamburg University/LPC, February 2012
 *** ------------------------------------------------------------------------------------------------------- ***/

#include "plot.h"

#include "TRint.h"
#include "TROOT.h"
#include "TObjArray.h"
#include "TStyle.h"
#include "TChain.h"
#include "TFile.h"
#include "TH2.h"
#include "TH2F.h"
#include "TTree.h"
#include "TKey.h"
#include "Riostream.h"
#include "TCanvas.h"
#include "TLegend.h"
#include "TLatex.h"
#include "TMarker.h"
#include "TPaveText.h"
#include "TGraph.h"

#include <iostream>
#include <sstream>
#include <stdlib.h>
#include <cmath>
#include <stdio.h>

#include "StyleSettings.h"
#include "Plotting.h"

void AddEvents(PlotTools*& plotTools, std::string filename, std::string GeneratorFile)
{
  Events * additionalEvents = new Events;
  ReadEvents(*additionalEvents, filename);
  plotTools->addEvents( additionalEvents );
  if (GeneratorFile!="") {
    std::vector<GeneratorMasses> GenMasses;
    ReadGeneratorMasses(GenMasses, GeneratorFile);
    Match( GenMasses, *additionalEvents);
  }  
  delete additionalEvents;
}

void DoPlotsFor(const std::string& x, const std::string& y, const std::string& flag, const std::string& file, style*s, int factor=0, TH2*plot_range=0, TH2*plot_excl=0)  {
    PlotTools * PlotTool;
    GetPlotTools(PlotTool, file, x, y, "", 0);
    GetInfo("squark")->SetLabel("m(#tilde{q}) [GeV]");
    GetInfo("gluino")->SetLabel("m(#tilde{g}) [GeV]");
    GetInfo("chi1")->SetLabel("m(#tilde{#chi}^{0}_{1}) [GeV]");
    GetInfo("cha1")->SetLabel("m(#tilde{#chi}^{#pm}_{1}) [GeV]");
    if (!plot_range) plot_range = PlotTool->GetHist(x,y);
    if (!plot_excl)  plot_excl = plot_range;
    DrawStandardPlots(PlotTool, flag, x,y, s, plot_range);
    //DrawStandardPlotsPerBin(PlotTool, "GMSB", x,y, &plot_range);
    DrawStandardLimitPlots(PlotTool, flag, x,y, s, plot_range);
  
    for (int i=2; i<=factor; i*=2)
      PlotTool->ExpandGrid(x, y);

    if (plot_excl == plot_range) {
      delete plot_range; 
      plot_range = PlotTool->GetHist(x,y);
      plot_excl = plot_range;
    } else {
      delete plot_range; 
      plot_range = PlotTool->GetHist(x,y);
    }  
    DrawExclusion(PlotTool,flag,x,y,plot_range,plot_excl,s); //removes points, which have no limits and fills the gaps by interpolation
}

void PlotAll(std::vector<LimitGraphs*>& lg, const std::string& flag, const std::string& limit, TH2*h=0)
{
  if (!h) h = (TH2F*)lg.front()->GetHist()->Clone();
  h->Draw();
  TLegend* leg = new TLegend(0.55,0.52,0.88,0.83,NULL,"brNDC");
  leg->SetFillColor(0);leg->SetShadowColor(0);
  leg->SetTextFont(42);leg->SetTextSize(0.025);leg->SetBorderSize(1);
  leg->SetHeader("CMS, L_{int} = 4.7 fb^{-1}, #sqrt{s} = 7 TeV");
  for (std::vector<LimitGraphs*>::iterator it=lg.begin();it!=lg.end();++it) {
    TGraph * g = (*it)->Limit(limit);
    g->Draw("l");
    leg->AddEntry(g,(*it)->Name().c_str(),"l");
  }
  leg->Draw();
  gPad->RedrawAxis();
  c1->SaveAs(("results/"+flag +"_"+limit+".pdf").c_str());
  if (plotPNG) c1->SaveAs(("results/"+flag+limit+".png").c_str());
}


void MultipleChannels(const std::string& x, const std::string& y, const std::string& flag, const std::string& dir, TH2*plot_range=0)  
{
  //read all channels
  std::vector<LimitGraphs*> lg;  
  lg.push_back(new LimitGraphs(dir+"/filelist.txt",    "", 1, x, y, "combined", 15, 1, 2, 1, 0, 0, plot_range) );
  lg.push_back(new LimitGraphs(dir+"/filelist_ch0.txt","", 1, x, y, "Bin 0",    15, 2, 0, 0, 0, 0, plot_range) );
  lg.push_back(new LimitGraphs(dir+"/filelist_ch1.txt","", 1, x, y, "Bin 1",    15, 3, 0, 0, 0, 0, plot_range) );
  lg.push_back(new LimitGraphs(dir+"/filelist_ch2.txt","", 1, x, y, "Bin 2",    15, 4, 0, 0, 0, 0, plot_range) );
  lg.push_back(new LimitGraphs(dir+"/filelist_ch3.txt","", 1, x, y, "Bin 3",    15, 5, 0, 0, 0, 0, plot_range) );
  lg.push_back(new LimitGraphs(dir+"/filelist_ch4.txt","", 1, x, y, "Bin 4",    15, 6, 2, 0, 0, 0, plot_range) );
  lg.push_back(new LimitGraphs(dir+"/filelist_ch5.txt","", 1, x, y, "Bin 5",    15, 7, 2, 0, 0, 0, plot_range) );

  //define plot range and labels
  GetInfo("squark")->SetLabel("m(#tilde{q}) [GeV]");
  GetInfo("gluino")->SetLabel("m(#tilde{g}) [GeV]");
  GetInfo("chi1"  )->SetLabel("m(#tilde{#chi}^{0}_{1}) [GeV]");
  if (!plot_range) plot_range = (TH2F*)lg.front()->GetHist()->Clone();
  plot_range->GetXaxis()->SetTitle(GetInfo(x)->GetLabel().c_str());
  plot_range->GetYaxis()->SetTitle(GetInfo(y)->GetLabel().c_str());

  //plotting
  PlotAll(lg,flag,x+"_"+y+"_allObsAsym",plot_range);
  PlotAll(lg,flag,x+"_"+y+"_allExpAsym",plot_range);
  c1->SetRightMargin(0.2);

  for (std::vector<LimitGraphs*>::iterator it=lg.begin();it!=lg.end();++it) {
      std::string l=flag+"_"+(*it)->Name();
      std::replace(l.begin(),l.end(),' ','_');
      c1->SetLogz(0);
      DrawPlot2D((*it)->GetPlot(),c1,(*it)->GetHist(),l,x,y,"Acceptance",        "Acceptance");
      c1->SetLogz(1);
      DrawPlot2D((*it)->GetPlot(),c1,(*it)->GetHist(),l,x,y,"ObsXsecLimitasym", "Observed asympt. cross section limit [pb]");
      DrawPlot2D((*it)->GetPlot(),c1,(*it)->GetHist(),l,x,y,"ExpXsecLimitasym", "Expected asympt. cross section limit [pb]");
      DrawPlot2D((*it)->GetPlot(),c1,(*it)->GetHist(),l,x,y,"ObsRasym", "Asymptotic Observed R ");
      //In/Out plot 
      {
      TH2F *hplot = (TH2F*)(*it)->GetHist()->Clone();
      hplot->GetZaxis()->SetTitle("Observed in/out");
      InOutPlot((*it)->GetPlot(),l,x,y,"ObsRasym",hplot);
      delete hplot;
      }
      {
      TH2F *hplot = (TH2F*)(*it)->GetHist()->Clone();
      hplot->GetZaxis()->SetTitle("Expected in/out");
      InOutPlot((*it)->GetPlot(),l,x,y,"ExpRasym",hplot);
      delete hplot;
      }
  }
}


int plot(int argc, char** argv) {
  util::StyleSettings::paperNoTitle();
  gStyle->SetPadTopMargin(0.1);
  gStyle->SetPadBottomMargin(0.18);
  gStyle->SetPadRightMargin(0.18);

  TCanvas* c_square    = new TCanvas("c_squ", "c_squ", 800, 800);
  c1 = c_square;
  c1->cd();

  
  ///Di-Photon 7 TeV Paper
  ///syntax: <x>,     <y>,     <label for the scan>,          <file listing all limit files>,     <instance of style class>, <increase number of bins by this factor>
  DoPlotsFor("cha1",  "chi1",  "GMSB_DiPhoton7TeV_WinoBino2j","20120622/WB_1jet/filelist.txt",     WinoBino_Style(),0);
  DoPlotsFor("squark","gluino","GMSB_DiPhoton7TeV_Wino2j",    "20120622/gsq_W_1jet/filelist.txt",  SqGlWino_Style(),4);
  DoPlotsFor("squark","gluino","GMSB_DiPhoton7TeV_Bino2j",    "20120622/gsq_B_1jet/filelist.txt",  SqGlBino_Style(),4);
  DoPlotsFor("cha1",  "gluino","GMSB_DiPhoton7TeV_Wino2j",    "20120622/gW_1jet/filelist.txt",     GlWino_Style(),4);
  DoPlotsFor("chi1",  "gluino","GMSB_DiPhoton7TeV_Bino2j",    "20120622/gB_1jet/filelist.txt",     GlBino_Style(),4);
  DoPlotsFor("chi1",  "gluino","T1gg2j_DiPhoton",	      "20120622/sms_gg_1jet/filelist.txt", SMST1gg_Style(),2);
  
  
}

int main(int argc, char** argv) {
  return plot(argc, argv);
}
