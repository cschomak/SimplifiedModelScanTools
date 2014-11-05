// $Id: plotSinglePhoton8TeV.cc,v 1.13 2012/06/26 13:58:23 auterman Exp $

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
#include "TError.h"

#include <iostream>
#include <sstream>
#include <fstream>
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
    GetInfo("sbottom")->SetLabel("m(#tilde{b}) [GeV]");
    GetInfo("neutralino2")->SetLabel("m(#tilde{#chi}_{2}^{0}) [GeV]");
    TH2 * new_plot_range = (plot_range?plot_range:PlotTool->GetHist(x,y));
    TH2 * new_plot_excl  = (plot_excl ?plot_excl :new_plot_range);
	
    TH2 * old_plot_range = (plot_range?plot_range:PlotTool->GetHist(x,y));
    TH2 * old_plot_excl  = (plot_excl ?plot_excl :old_plot_range);
	
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
    DrawExclusion(PlotTool,flag,x,y,new_plot_range,new_plot_excl,old_plot_range,old_plot_excl,s); //removes points, which have no limits and fills the gaps by interpolation
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
  GetInfo("sbottom")->SetLabel("M_{sbottom} [GeV]");
  GetInfo("neutralino2"  )->SetLabel("M_{neutralino 2} [GeV]");
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
      DrawPlot2D((*it)->GetPlot(),c1,(*it)->GetHist(),l,x,y,"AcceptanceCorrected", "Acceptance (corrected for signal cont.)");
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
  plotROOT   = true;
  plotPrelim = true;
  
  TCanvas* c_square    = new TCanvas("c_squ2", "c_squ2", 900, 800);
  c1 = c_square;
  c1->cd();

  Overview = new OverviewTable();

  //~ DoPlotsFor("sbottom","neutralino2","Fixed_Edge_8TeV","2014-08-26-15-30-T6bblledge/filelist.txt",Fixed_Edge_Style(),2);
  //~ DoPlotsFor("sbottom","neutralino2","Fixed_Edge_13TeV_Sel_Eff","2014-09-03-00-37-PU20BX25_Efficiencies/filelist.txt",Fixed_Edge_Style(),2);
  //~ DoPlotsFor("sbottom","neutralino2","Fixed_Edge_13TeV_Direct","2014-09-03-00-37-PU20BX25_direct/filelist.txt",Fixed_Edge_Style(),2);
  //~ DoPlotsFor("sbottom","neutralino2","Fixed_Edge","2014-09-08-16-53-T6bblledge/filelist.txt",Fixed_Edge_Style(),1.5);
  DoPlotsFor("sbottom","neutralino2","Fixed_Edge","2014-09-14-15-04-T6bblledge/filelist.txt",Fixed_Edge_Style(),2);
  //~ DoPlotsFor("sbottom","neutralino2","Fixed_Neutralino","2014-09-14-15-04-T6bbllsleptonReweighted/filelist.txt",Fixed_Edge_Style(),2);
  //~ DoPlotsFor("sbottom","neutralino2","Fixed_Neutralino","2014-08-28-09-41-T6bbllsleptonReweighted/filelist.txt",Fixed_Edge_Style(),2);
  //~ DoPlotsFor("sbottom","neutralino2","Fixed_Neutralino","2014-08-20-11-53-T6bbllslepton/filelist.txt",Fixed_Edge_Style(),2);

  //~ }
  
  std::ofstream ofile;
  ofile.open("results/OverviewTable.txt");
  ofile << *Overview->Get() << std::endl;
  ofile.close();
  
  return 0;
}

int main(int argc, char** argv) {
  return plot(argc, argv);
}
