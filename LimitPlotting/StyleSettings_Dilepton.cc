// $Id: StyleSettings_SinglePhoton_8TeV.cc,v 1.1 2012/06/29 20:27:21 auterman Exp $

/*** ------------------------------------------------------------------------------------------------------- ***
     TheBetterPlotScript, a tool to plot final results, limits and exclusion contours, based on 'PlotScript'

     Christian Autermann, Hamburg University/LPC, February 2012
 *** ------------------------------------------------------------------------------------------------------- ***/

#include <iostream>

#include "TString.h"
#include "TStyle.h"
#include "TLatex.h"
#include "TGraph.h"
#include "TH2F.h"

#include "StyleSettings.h"
#include "OldExclusionContours.h"
#include "Overview.h"

void SetDefault(style * s=0)
{
  if (!s) return;
  if (s->legTemperaturePlot) {
    s->legTemperaturePlot->SetBorderSize(0);
    s->legTemperaturePlot->SetLineColor(0);
    //~ s->legTemperaturePlot->SetFillColor(10);
    s->legTemperaturePlot->SetFillColor(0);
    s->legTemperaturePlot->SetFillStyle(1001);
    s->legTemperaturePlot->SetTextFont(42);
    s->legTemperaturePlot->SetTextSize(0.04);
  }
  if (s->leg) {
    s->leg->SetBorderSize(0);
    s->leg->SetLineColor(0);
    //~ s->leg->SetFillColor(10);
    s->leg->SetFillColor(0);
    s->leg->SetFillStyle(1001);
    s->leg->SetTextFont(42);
    s->leg->SetTextSize(0.03);
  }
  if (s->excluded) {
    s->excluded->SetNDC(true);
    s->excluded->SetTextColor(1);
    s->excluded->SetTextFont(43);
    s->excluded->SetTextSize(25);
  }
  if (s->cmsprelim) {
    s->cmsprelim->SetNDC(true);
    //~ s->cmsprelim->SetTextColor(1);
    s->cmsprelim->SetTextFont(52);
    s->cmsprelim->SetTextSize(0.03);
  }
  if (s->lumi) {
    s->lumi->SetNDC(true);
    //~ s->lumi->SetTextColor(1);
    s->lumi->SetTextFont(42);
    s->lumi->SetTextSize(0.04);
    s->lumi->SetTextAlign(31);
  }
  if (s->cms) {
    s->cms->SetNDC(true);
    //~ s->cms->SetTextColor(1);
    s->cms->SetTextFont(61);
    s->cms->SetTextSize(0.055);
  }
  //~ s->legTemperaturePlot      = new TLegend(0.175,0.6,0.525,0.9,"T6bblledge: #Deltam =70 GeV");
  s->legTemperaturePlot      = new TLegend(0.18,0.605,0.5,0.885,"Fixed edge, #Deltam = 70 GeV");
  //~ s->legTemperaturePlot      = new TLegend(0.175,0.6,0.525,0.9,"#splitline{T6bblledge: #Deltam =70 GeV}{Selection Efficiency Method}");
  //~ s->legTemperaturePlot      = new TLegend(0.175,0.6,0.525,0.9,"#splitline{T6bblledge: #Deltam =70 GeV}{SF background from MC}");
  //~ s->legTemperaturePlot      = new TLegend(0.18,0.605,0.53,0.885,"Slepton model, m(#tilde{#chi}_{1}^{0}) = 100 GeV");
  s->legTemperaturePlot->SetTextSize(0.03);
  s->legTemperaturePlot->SetFillColor(0);
  //~ s->lumiTemperaturePlot = new TLatex(0.48, 0.912, "L_{int} = 19.4 fb^{  -1}, SF, central signal region");
  s->lumiTemperaturePlot = new TLatex(0.8, 0.91, "19.4 fb^{-1} (8 TeV)");
  //~ s->lumiTemperaturePlot = new TLatex(0.85, 0.91, "20 fb^{-1} (13 TeV)");
  s->lumiTemperaturePlot->SetNDC(true);
  //~ s->lumiTemperaturePlot->SetTextColor(1);
  s->lumiTemperaturePlot->SetTextFont(42);
  s->lumiTemperaturePlot->SetTextSize(0.04);
  s->lumiTemperaturePlot->SetTextAlign(31);
  s->cmsTemperaturePlot = new TLatex(0.18, 0.91, "CMS");
  s->cmsTemperaturePlot->SetNDC(true);
  //~ s->cmsTemperaturePlot->SetTextColor(1);
  s->cmsTemperaturePlot->SetTextFont(61);
  s->cmsTemperaturePlot->SetTextSize(0.055);
  //~ s->cmsprelimTemperaturePlot = new TLatex(0.65, 0.81, "Preliminary");
  //~ s->cmsprelimTemperaturePlot = new TLatex(0.65, 0.81, "Private Work");
  s->cmsprelimTemperaturePlot->SetNDC(true);
  //~ s->cmsprelimTemperaturePlot->SetTextColor(1);
  s->cmsprelimTemperaturePlot->SetTextFont(52);
  s->cmsprelimTemperaturePlot->SetTextSize(0.03);

}

/// ----------- Fixed Neutralino ------------ /// ----------------------------------------------------------------------------------

void Draw_Fixed_Neutralino_CoverUp(style * s=0, TLegend*l=0) {
	TGraph*cover = new TGraph(0);
	cover->SetPoint(0, 200,  300);
	cover->SetPoint(1, 880,   920);
	cover->SetPoint(2, 900,   900);
	cover->SetPoint(3,    0,    0);
	cover->SetFillColor(kWhite);
	//cover->SetLineColor(kBlack);
	cover->Draw("f");

	TGraph*Fixed_Neutralino = new TGraph(0);
	Fixed_Neutralino->SetPoint(0, 50, 50);
	Fixed_Neutralino->SetPoint(1, 3000, 3005);
	Fixed_Neutralino->SetPoint(2, 50, 3000);
	Fixed_Neutralino->SetPoint(3, 50, 50);
	//~ Fixed_Neutralino->SetFillColor(kGray);
	Fixed_Neutralino->SetFillColor(kWhite);
	Fixed_Neutralino->Draw("f");

	TLatex tex;
	tex.SetTextSize(0.03);
	tex.SetTextFont(62);
	tex.SetNDC(true);
	//~ tex.DrawLatex(0.6, 0.25, "Fixed Neutralino");
	gPad->RedrawAxis();
	
}


style* Fixed_Neutralino_Style(){ 
  style * s = new style();
  //~ s->leg       = new TLegend(0.2,0.6,0.6,0.89,"m(#tilde{#chi}_{1}^{0}) = 100 GeV, BR 10 %");
  //~ s->lumi      = new TLatex(0.525, 0.902, "L_{int} = 19.4 fb^{  -1}, SF,");
  //~ s->cms       = new TLatex(0.18, 0.902, "#bf{CMS preliminary}, #sqrt{s} = 8 TeV");
  //~ s->cmsprelim = new TLatex(0.18, 0.902, "#bf{CMS preliminary}, #sqrt{s} = 8 TeV");
  s->leg       = new TLegend(0.175,0.6,0.525,0.9,"m(#tilde{#chi}_{1}^{0}) = 100 GeV");  
  s->lumi      = new TLatex(0.85, 0.91, "19.4 fb^{-1} (8 TeV)");
  //~ s->cmsprelim = new TLatex(0.65, 0.81, "Preliminary");
  s->cms = new TLatex(0.65, 0.85, "CMS");
  //~ s->excluded  = new TLatex(0.35, 0.25, "Excluded");
  s->smooth_flag=4;
  s->smooth_points=25;
  s->PostExclusionPlotting=Draw_Fixed_Neutralino_CoverUp;
  s->iCLsObsExcl=1;  
  s->iCLsExpExcl=0;  
  s->iCLsExpExclm1=0;
  s->iCLsExpExclp1=0;
  s->iCLsObsTheom1=0;
  s->iCLsObsTheop1=0;
  s->MinXsecZ=0.005;
  s->MaxXsecZ=5.;
  s->MinAccZ=0;
  s->MaxAccZ=0.8;

  SetDefault(s);
  return s;
}

/// ----------- Fixed Edge ------------ /// ----------------------------------------------------------------------------------
void Draw_Fixed_Edge_CoverUp(style * s=0, TLegend*l=0) {
	TGraph*cover = new TGraph(0);
	cover->SetPoint(0, 300,  350);
	cover->SetPoint(1, 950, 1000);
	cover->SetPoint(2, 1000, 1000);
	cover->SetPoint(3,    0,    0);
	cover->SetFillColor(kWhite);
	//cover->SetLineColor(kBlack);
//	cover->Draw("f");

	TGraph*Fixed_Edge = new TGraph(0);
	Fixed_Edge->SetPoint(0, 50, 50);
	Fixed_Edge->SetPoint(1, 3000, 3000);
	Fixed_Edge->SetPoint(2, 50, 3000);
	Fixed_Edge->SetPoint(3, 50, 50);
	//~ Fixed_Edge->SetFillColor(kGray);
	Fixed_Edge->SetFillColor(kWhite);
	Fixed_Edge->Draw("f");
	

	//~ TLatex tex;
	//~ tex.SetTextSize(0.04);
	//~ tex.SetTextFont(62);
	//~ tex.SetNDC(true);
	//~ tex.DrawLatex(0.423, 0.215, "x");
	//~ gPad->RedrawAxis();
}

style* Fixed_Edge_Style(){ 
  style * s = new style();
  //~ s->leg       = new TLegend(0.2,0.6,0.6,0.89,"Fixed Edge: #Deltam =70 GeV, BR: 10%");
  //~ s->leg       = new TLegend(0.5,0.6,0.92,0.89,"Fixed Edge: #Deltam =70 GeV");
  //~ s->leg       = new TLegend(0.175,0.6,0.55,0.9,"T6bbllslepton: m(#tilde{#chi}_{1}^{0}) = 100 GeV");
  //~ s->leg       = new TLegend(0.4,0.6,0.91,0.875,"T6bblledge: #Deltam =70 GeV, 19.4 resp. 20 fb^{-1}"); 
  s->leg       = new TLegend(0.4,0.6,0.91,0.875,"T6bblledge: #Deltam =70 GeV"); 
  //~ s->leg       = new TLegend(0.175,0.6,0.55,0.9,"#splitline{T6bblledge: #Deltam =70 GeV}{Selection Efficiency Method}"); 
  //~ s->leg       = new TLegend(0.175,0.6,0.55,0.9,"#splitline{T6bblledge: #Deltam =70 GeV}{SF background from MC}"); 
  //~ s->lumi      = new TLatex(0.92, 0.9, "");
  //~ s->lumi      = new TLatex(0.92, 0.9, "20 fb^{-1} (13 TeV)");
  //~ s->cmsprelim = new TLatex(0.75, 0.8, "Preliminary");
  //~ s->cmsprelim = new TLatex(0.2, 0.8, "Private Work");
  //~ s->cmsprelim = new TLatex(0.2, 0.8, "Preliminary");
  s->cms = new TLatex(0.2, 0.84, "CMS");
  //~ s->lumi      = new TLatex(0.525, 0.902, "L_{int} = 19.4 fb^{  -1}, SF");
  s->lumi      = new TLatex(0.92, 0.9, "19.4 fb^{-1} (8 TeV)");
  //~ s->cms       = new TLatex(0.21, 0.902, "#bf{CMS}    #sqrt{s} = 8 TeV");
  //~ s->cmsprelim = new TLatex(0.20, 0.80, "Preliminary");
  //~ s->cms = new TLatex(0.20, 0.84, "CMS");
  //~ s->excluded  = new TLatex(0.35, 0.25, "Excluded");
  //~ s->excluded  = new TLatex(0.2, 0.225, "Excluded");
  s->smooth_flag=2;
  s->smooth_points=5;
  s->second_smooth=3;
  s->PostExclusionPlotting=Draw_Fixed_Edge_CoverUp;
  s->iCLsObsExcl=0;  
  s->iCLsExpExcl=0;  
  s->iCLsExpExclm1=0;
  s->iCLsExpExclp1=0;
  s->iCLsExpExclm2=0;
  s->iCLsExpExclp2=0;
  s->iCLsObsTheom1=0;
  s->iCLsObsTheop1=0;

  //~ s->MinXsecZ=0.02;
  //~ s->MaxXsecZ=1.5;
  s->MinXsecZ=0.1;
  s->MaxXsecZ=10;
  //~ s->MaxXsecZ=20;

  SetDefault(s);

  return s;
}
