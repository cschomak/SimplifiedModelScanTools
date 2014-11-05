// $Id: plotSinglePhoton7TeV.cc,v 1.13 2012/06/26 13:58:23 auterman Exp $

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
//#include "TCanvas.h"
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
    GetInfo("squark")->SetLabel("M_{squark} [GeV]");
    GetInfo("gluino")->SetLabel("M_{gluino} [GeV]");
    GetInfo("chi1"  )->SetLabel("M_{bino} [GeV]");
    GetInfo("neutralino"  )->SetLabel("M_{neutralino} [GeV]");
    GetInfo("cha1"  )->SetLabel("M_{wino} [GeV]");
    TH2 * new_plot_range = (plot_range?plot_range:PlotTool->GetHist(x,y));
    TH2 * new_plot_excl  = (plot_excl ?plot_excl :new_plot_range);

    gStyle->SetOptStat(0);
    gStyle->SetPalette(1);
    gStyle->SetPadRightMargin(0.2);
    gStyle->SetPadLeftMargin(0.18);
    gStyle->SetPadTopMargin(0.1);
    gStyle->SetPadBottomMargin(0.15);
    gStyle->SetTitleOffset(1.0, "x");
    gStyle->SetTitleOffset(1.5, "y");
    gStyle->SetTitleOffset(1.2, "z");
    gStyle->SetNdivisions(505);
    gStyle->SetTitleFont(43, "xyz");
    gStyle->SetTitleSize(32, "xyz");
    //gStyle->SetLabelSize(0.03, "XYZ");

 

    DrawStandardPlots(PlotTool->Clone(), flag, x,y, s, new_plot_range);
    //DrawStandardPlotsPerBin(PlotTool, "GMSB", x,y, &new_plot_range);
    DrawStandardLimitPlots(PlotTool->Clone(), flag, x,y, s, new_plot_range);
    
    for (int i=2; i<=factor; i*=2)
      PlotTool->ExpandGrid(x, y);

    new_plot_range = (plot_range?plot_range:PlotTool->GetHist(x,y));
    new_plot_excl  = (plot_excl?plot_excl:new_plot_range);
/*
    if (plot_excl == plot_range) {
      delete plot_range; 
      plot_range = PlotTool->GetHist(x,y);
      plot_excl = plot_range;
    } else {
      delete plot_range; 
      plot_range = PlotTool->GetHist(x,y);
    }  
*/    
    DrawExclusion(PlotTool,flag,x,y,new_plot_range,new_plot_excl,s); //removes points, which have no limits and fills the gaps by interpolation

    PlotTool->Print("gluino",Compare::equal,1020);
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
  std::cout<<c1<<"  "<<flag<<"  "<<limit<<std::endl;
  c1->SaveAs(("results/"+flag +"_"+limit+".pdf").c_str());
  if (plotPNG) c1->SaveAs(("results/"+flag+"_"+limit+".png").c_str());
}


void MultipleChannels(const std::string& x, const std::string& y, const std::string& flag, const std::string& dir, TH2*plot_range=0)  
{
  //read all channels
  std::vector<LimitGraphs*> lg;  
  lg.push_back(new LimitGraphs(dir+"/filelist.txt",    "", 1, x, y, "combined", 15, 1, 0, 0, 0, 0, plot_range) );
  lg.push_back(new LimitGraphs(dir+"/filelist_ch0.txt","", 1, x, y, "Bin 0",    15, 2, 0, 0, 0, 0, plot_range) );
  lg.push_back(new LimitGraphs(dir+"/filelist_ch1.txt","", 1, x, y, "Bin 1",    15, 3, 0, 0, 0, 0, plot_range) );
  lg.push_back(new LimitGraphs(dir+"/filelist_ch2.txt","", 1, x, y, "Bin 2",    15, 4, 0, 0, 0, 0, plot_range) );
  lg.push_back(new LimitGraphs(dir+"/filelist_ch3.txt","", 1, x, y, "Bin 3",    15, 5, 0, 0, 0, 0, plot_range) );
  lg.push_back(new LimitGraphs(dir+"/filelist_ch4.txt","", 1, x, y, "Bin 4",    15, 6, 0, 0, 0, 0, plot_range) );
  lg.push_back(new LimitGraphs(dir+"/filelist_ch5.txt","", 1, x, y, "Bin 5",    15, 7, 0, 0, 0, 0, plot_range) );

  //define plot range and labels
  GetInfo("squark")->SetLabel("M_{squark} [GeV]");
  GetInfo("gluino")->SetLabel("M_{gluino} [GeV]");
  GetInfo("chi1"  )->SetLabel("M_{bino} [GeV]");
  GetInfo("neutralino"  )->SetLabel("M_{neutralino} [GeV]");
  GetInfo("cha1"  )->SetLabel("M_{wino} [GeV]");
  if (!plot_range) plot_range = (TH2F*)lg.front()->GetHist()->Clone();
  plot_range->GetXaxis()->SetTitle(GetInfo(x)->GetLabel().c_str());
  plot_range->GetYaxis()->SetTitle(GetInfo(y)->GetLabel().c_str());

  //plotting
  c1->cd();
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
      c1->cd();
      //In/Out plot 
      {
      TH2F *hplot = (TH2F*)(*it)->GetHist()->Clone();
      hplot->GetZaxis()->SetTitle("Observed in/out");
      InOutPlot((*it)->GetPlot(),c1,l,x,y,"ObsRasym",hplot);
      }
      {
      TH2F *hplot = (TH2F*)(*it)->GetHist()->Clone();
      hplot->GetZaxis()->SetTitle("Expected in/out");
      InOutPlot((*it)->GetPlot(),c1,l,x,y,"ExpRasym",hplot);
      }
  }
}


int plot(int argc, char** argv) {
  util::StyleSettings::paperNoTitle();
  gStyle->SetPadTopMargin(0.1);
  gStyle->SetPadBottomMargin(0.18);
  gStyle->SetPadRightMargin(0.18);

  plotPNG    = false;
  plotC	     = false;
  plotROOT   = false;
  plotPrelim = false;
  
  TCanvas* c_square    = new TCanvas("c_squ2", "c_squ2", 900, 800);
  c1 = c_square;
  c1->cd();


  //DoPlotsFor("squark","gluino","GMSB_7-8TeVCombination_Bino_corr","2012-06-21-17-05-GMSB_sqgBino375_8TeV_2j/filelist.txt",SqGlBino_Style(),4);

  if (1){ // 4.02 fb-1
  ///Single-Photon 7 TeV and 8 TeV Combination --- correlated systematics
  DoPlotsFor("squark","gluino","GMSB_7-8TeVCombination_Bino_corr","2012-09-13-15-58-GMSB_sqgBino_78_corr/filelist.txt",SqGlBino_Style(),4);
  DoPlotsFor("squark","gluino","GMSB_7-8TeVCombination_Wino_corr","2012-09-12-19-40-GMSB_sqgWino_78_corr/filelist.txt",SqGlWino_Style(),4);

  ///Single-Photon 7 TeV and 8 TeV Combination --- systematics (default: corr, un-co in addition) 
  DoPlotsFor("squark","gluino","GMSB_7-8TeVCombination_Bino_systematics","2012-09-13-15-58-GMSB_sqgBino_78_corr/filelist.txt",SqGlBino_78Syst_Style(),4);
  DoPlotsFor("squark","gluino","GMSB_7-8TeVCombination_Wino_systematics","2012-09-12-19-40-GMSB_sqgWino_78_corr/filelist.txt",SqGlWino_78Syst_Style(),4);

  ///Di-Photon 7 TeV and 8 TeV Combination --- un-correlated systematics
  //DoPlotsFor("squark","gluino","DiPhoton_7-8TeVCombination_Bino_unco","2012-09-21-20-09-DiPhoton_sqgBino_78/filelist.txt",SqGlBino_DiP_Style(),4);
  //DoPlotsFor("squark","gluino","DiPhoton_7-8TeVCombination_Wino_unco","2012-09-21-20-10-DiPhoton_sqgWino_78/filelist.txt",SqGlWino_DiP_Style(),4);

  /// Di-Photon 8 TeV
  //DoPlotsFor("squark","gluino","DiPhoton_8TeV_Bino","2012-09-21-20-10-DiPhoton_8TeV_gsq_B/filelist.txt",SqGlBino_DiP_Style(),4);
  //DoPlotsFor("squark","gluino","DiPhoton_8TeV_Wino","2012-09-21-20-10-DiPhoton_8TeV_gsq_W/filelist.txt",SqGlWino_DiP_Style(),4);

  ///Di-Photon 7 TeV and 8 TeV Combination --- correlated systematics
  DoPlotsFor("squark","gluino","DiPhoton_7-8TeVCombination_Bino_corr","2012-09-22-21-51-DiPhoton_sqgBino_78_corr/filelist.txt",SqGlBino_DiP_Style(),4);
  DoPlotsFor("squark","gluino","DiPhoton_7-8TeVCombination_Wino_corr","2012-09-22-21-52-DiPhoton_sqgWino_78_corr/filelist.txt",SqGlWino_DiP_Style(),4);

  ///Di-Photon 7 TeV and 8 TeV Combination --- systematics (default: corr, un-co in addition) 
  DoPlotsFor("squark","gluino","DiPhoton_7-8TeVCombination_Bino_systematics","2012-09-22-21-51-DiPhoton_sqgBino_78_corr/filelist.txt",SqGlBino_DiP78Syst_Style(),4);
  DoPlotsFor("squark","gluino","DiPhoton_7-8TeVCombination_Wino_systematics","2012-09-22-21-52-DiPhoton_sqgWino_78_corr/filelist.txt",SqGlWino_DiP78Syst_Style(),4);
  }




  if (0) {
  /// 7TeV Single- and Di Photon Combination
  DoPlotsFor("squark","gluino","GMSB_SD_78TeV_Bino_unco","2012-09-21-20-44-GMSB_sqgBino_SD78/filelist.txt",SqGlBino_Style_SD8(),4);
  DoPlotsFor("squark","gluino","GMSB_SD_78TeV_Wino_unco","2012-09-21-20-43-GMSB_sqgWino_SD78/filelist.txt",SqGlWino_Style_SD8(),4);

  //DoPlotsFor("squark","gluino","GMSB_SD_7TeV_Bino_unco","2012-09-19-22-33-GMSB_sqgBino_SD_unco/filelist.txt",SqGlBino_Style_SD7(),4);
  //DoPlotsFor("squark","gluino","GMSB_SD_7TeV_Wino_unco","2012-09-19-22-44-GMSB_sqgWino_SD_unco/filelist.txt",SqGlWino_Style_SD7(),4);

  //DoPlotsFor("squark","gluino","GMSB_SD_8TeV_Bino_unco","2012-09-21-20-42-GMSB_sqgBino_SD8/filelist.txt",SqGlBino_Style_SD8(),4);
  //DoPlotsFor("squark","gluino","GMSB_SD_8TeV_Wino_unco","2012-09-21-20-42-GMSB_sqgWino_SD8/filelist.txt",SqGlWino_Style_SD8(),4);




  }
  
  
  
}

int main(int argc, char** argv) {
  return plot(argc, argv);
}
