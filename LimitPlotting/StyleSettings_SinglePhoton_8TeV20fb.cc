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

#include "StyleSettings.h"
#include "OldExclusionContours.h"
#include "Overview.h"

void SetDefault(style * s=0)
{
  if (!s) return;
  if (s->leg) {
    s->leg->SetBorderSize(0);
    s->leg->SetLineColor(0);
    s->leg->SetFillColor(10);
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
    s->cmsprelim->SetTextColor(1);
    s->cmsprelim->SetTextFont(43);
    s->cmsprelim->SetTextSize(20);
  }
  if (s->lumi) {
    s->lumi->SetNDC(true);
    s->lumi->SetTextColor(1);
    s->lumi->SetTextFont(43);
    s->lumi->SetTextSize(25);
  }
  if (s->cms) {
    s->cms->SetNDC(true);
    s->cms->SetTextColor(1);
    s->cms->SetTextFont(43);
    s->cms->SetTextSize(25);
  }
  s->lumiTemperaturePlot = new TLatex(0.52, 0.912, "L_{int} = 19.8 fb^{  -1}  #geq1 #gamma, #geq2 jets");
  s->lumiTemperaturePlot->SetNDC(true);
  s->lumiTemperaturePlot->SetTextColor(1);
  s->lumiTemperaturePlot->SetTextFont(43);
  s->lumiTemperaturePlot->SetTextSize(25);
  s->cmsTemperaturePlot = new TLatex(0.16, 0.912, "#bf{CMS preliminary} #sqrt{s} = 8 TeV");
  s->cmsTemperaturePlot->SetNDC(true);
  s->cmsTemperaturePlot->SetTextColor(1);
  s->cmsTemperaturePlot->SetTextFont(43);
  s->cmsTemperaturePlot->SetTextSize(25);
  s->cmsprelimTemperaturePlot = new TLatex(0.18, 0.912, "#bf{CMS} #sqrt{s} = 8 TeV");
  s->cmsprelimTemperaturePlot->SetNDC(true);
  s->cmsprelimTemperaturePlot->SetTextColor(1);
  s->cmsprelimTemperaturePlot->SetTextFont(43);
  s->cmsprelimTemperaturePlot->SetTextSize(25);

}

void Draw_OldBinoLimits(style * s=0, TLegend*l=0) {
  TGraph * exp7TeVBinoSqGl = Exp_7TeV_Bino2j_squark_gluino();
  TGraph * exp8TeVBinoSqGl = Exp_8TeV_Bino2j_squark_gluino();
  TGraph * exp78TeVBinoSqGl = Exp_Bino_Single78corr_squark_gluino();
  exp7TeVBinoSqGl->Draw("same");
  //exp8TeVBinoSqGl->Draw("same");
  //exp78TeVBinoSqGl->Draw("same");
  //if (l) l->AddEntry(exp78TeVBinoSqGl,"Combination 7 & 8 TeV, 9 fb^{-1}","l");
  //if (l) l->AddEntry(exp8TeVBinoSqGl, "Exp. 8 TeV, 4 fb^{-1}","l");
  if (l) l->AddEntry(exp7TeVBinoSqGl, "Exp. 7 TeV, 5 fb^{-1}","l");
}

style* SqGlBino_Style(){ /// Sq-Gl Bino /// ---------------------------------------------------------------------
  style * s = new style();
  s->leg=new TLegend(0.26,0.16,0.61,0.45,"#splitline{Bino-like #tilde{#chi}^{0} NLSP}{m_{#tilde{#chi}^{0}} = 375 GeV}");

  s->lumi      = new TLatex(0.58, 0.902, "L_{int} = 19.8 fb^{  -1} #geq1#gamma, #geq2 jets");
  s->cms       = new TLatex(0.21, 0.902, "#bf{CMS preliminary} #sqrt{s} = 8 TeV");
  s->cmsprelim = new TLatex(0.21, 0.902, "#bf{CMS}    #sqrt{s} = 8 TeV");
  s->excluded  = new TLatex(0.3,  0.7,   "Excluded");
  s->smooth_points=25;
  s->MinXsecZ=0.001;
  s->MaxXsecZ=0.03;
  s->PostExclusionPlotting=Draw_OldBinoLimits;
  
  SetDefault(s);
  return s;
}

void Draw_OldWinoLimits(style * s=0, TLegend*l=0) {
  TGraph * exp7TeVWinoSqGl = Exp_7TeV_Wino2j_squark_gluino();
  TGraph * exp8TeVWinoSqGl = Exp_8TeV_Wino2j_squark_gluino();
  TGraph * exp78TeVWinoSqGl = Exp_Wino_Single78corr_squark_gluino();
  exp7TeVWinoSqGl->Draw("same");
  //exp8TeVWinoSqGl->Draw("same");
  //exp78TeVWinoSqGl->Draw("same");
  //if (l) l->AddEntry(exp78TeVWinoSqGl,"Combination 7 & 8 TeV, 9 fb^{-1}","l");
  //if (l) l->AddEntry(exp8TeVWinoSqGl, "Exp. 8 TeV, 4 fb^{-1}","l");
  if (l) l->AddEntry(exp7TeVWinoSqGl, "Exp. 7 TeV, 5 fb^{-1}","l");
}

style* SqGlWino_Style(){ /// Sq-Gl Wino /// ---------------------------------------------------------------------
  style * s = new style();
  s->leg       = new TLegend(0.50,0.55,0.83,0.85,"#splitline{Wino-like #tilde{#chi}^{0} NLSP}{m_{#tilde{#chi}^{0}} = 375 GeV}");
  s->lumi      = new TLatex(0.58, 0.902, "L_{int} = 19.8 fb^{  -1} #geq1#gamma, #geq2 jets");
  s->cms       = new TLatex(0.21, 0.902, "#bf{CMS preliminary} #sqrt{s} = 8 TeV");
  s->cmsprelim = new TLatex(0.2,  0.902, "#bf{CMS}    #sqrt{s} = 8 TeV");
  s->excluded  = new TLatex(0.3,  0.3,   "Excluded");
  s->smooth_points=25;
  s->MinXsecZ=0.01;
  s->MaxXsecZ=1.;
  s->MinAccZ=0;
  s->MaxAccZ=0.1;
  s->PostExclusionPlotting=Draw_OldWinoLimits;
  
  SetDefault(s);
  return s;
}


/// ----------- Gl - Bino ------------ /// ----------------------------------------------------------------------------------

void Draw_GlBino_CoverUp(style * s=0, TLegend*l=0) {
	TGraph*cover = new TGraph(0);
	cover->SetPoint(0, 200,  300);
	cover->SetPoint(1, 880,   920);
	cover->SetPoint(2, 900,   900);
	cover->SetPoint(3,    0,    0);
	cover->SetFillColor(kWhite);
	//cover->SetLineColor(kBlack);
	cover->Draw("f");

	TGraph*gluinoNLSP = new TGraph(0);
	gluinoNLSP->SetPoint(0, 50, 55);
	gluinoNLSP->SetPoint(1, 3000, 3005);
	gluinoNLSP->SetPoint(2, 3000, 50);
	gluinoNLSP->SetPoint(3, 50, 50);
	gluinoNLSP->SetFillColor(kGray);
	gluinoNLSP->Draw("f");

	TLatex tex;
	tex.SetTextSize(0.03);
	tex.SetTextFont(62);
	tex.SetNDC(true);
	tex.DrawLatex(0.6, 0.25, "#tilde{g} NLSP");
	gPad->RedrawAxis();
}


style* GlBino_Style(){ 
  style * s = new style();
  s->leg       = new TLegend(0.26,0.71,0.69,0.85,"Bino-like #tilde{#chi}^{0} NLSP");
  s->lumi      = new TLatex(0.58, 0.902, "L_{int} = 19.8 fb^{  -1}   #geq1#gamma, #geq2 jets");
  s->cms       = new TLatex(0.21, 0.902, "#bf{CMS preliminary}    #sqrt{s} = 8 TeV");
  s->cmsprelim = new TLatex(0.21, 0.902, "#bf{CMS}    #sqrt{s} = 8 TeV");
  s->excluded  = new TLatex(0.3, 0.4, "Excluded");
  s->smooth_flag=2;
  s->smooth_points=25;
  s->PostExclusionPlotting=Draw_GlBino_CoverUp;
  s->iCLsObsExcl=1;  
  s->iCLsExpExcl=1;  
  s->iCLsExpExclm1=0;
  s->iCLsExpExclp1=0;
  s->iCLsObsTheom1=0;
  s->iCLsObsTheop1=0;
  s->MinXsecZ=0.001;
  s->MaxXsecZ=0.5;
  s->MinAccZ=0;
  s->MaxAccZ=0.8;

  SetDefault(s);
  return s;
}

/// ----------- Gl - Wino ------------ /// ----------------------------------------------------------------------------------
void Draw_GlWino_CoverUp(style * s=0, TLegend*l=0) {
	TGraph*cover = new TGraph(0);
	cover->SetPoint(0, 300,  350);
	cover->SetPoint(1, 950, 1000);
	cover->SetPoint(2, 1000, 1000);
	cover->SetPoint(3,    0,    0);
	cover->SetFillColor(kWhite);
	//cover->SetLineColor(kBlack);
//	cover->Draw("f");

	TGraph*gluinoNLSP = new TGraph(0);
	gluinoNLSP->SetPoint(0, 50, 50);
	gluinoNLSP->SetPoint(1, 3000, 3000);
	gluinoNLSP->SetPoint(2, 3000, 50);
	gluinoNLSP->SetPoint(3, 50, 50);
	gluinoNLSP->SetFillColor(kGray);
	gluinoNLSP->Draw("f");

	TLatex tex;
	tex.SetTextSize(0.03);
	tex.SetTextFont(62);
	tex.SetNDC(true);
	tex.DrawLatex(0.8, 0.5, "#tilde{g} NLSP");
	gPad->RedrawAxis();
}

style* GlWino_Style(){ 
  style * s = new style();
  s->leg       = new TLegend(0.25,0.65,0.68,0.85,"Wino-like #tilde{#chi}^{0} NLSP");
  s->lumi      = new TLatex(0.58, 0.902, "L_{int} = 19.8 fb^{  -1}   #geq1#gamma, #geq2 jets");
  s->cms       = new TLatex(0.21, 0.902, "#bf{CMS preliminary}    #sqrt{s} = 8 TeV");
  s->cmsprelim = new TLatex(0.21, 0.902, "#bf{CMS}    #sqrt{s} = 8 TeV");
  s->excluded  = new TLatex(0.29, 0.3, "Excluded");
  s->smooth_flag=2;
  s->smooth_points=15;
  s->second_smooth=5;
  s->PostExclusionPlotting=Draw_GlWino_CoverUp;
  s->iCLsObsExcl=1;  
  s->iCLsExpExcl=1;  
  s->iCLsExpExclm1=0;
  s->iCLsExpExclp1=0;
  s->iCLsObsTheom1=0;
  s->iCLsObsTheop1=0;

  s->MinXsecZ=0.01;
  s->MaxXsecZ=20;

  SetDefault(s);

  return s;
}

/// Cha - Chi /// -----------------------------------------------------------------------
void DrawWinoBinoDiagonalCut(style * s=0, TLegend*l=0) {
	TGraph*cover = new TGraph(0);
	cover->SetPoint(0,   0,   0);
	cover->SetPoint(1, 1200, 1200);
	cover->SetPoint(2, 1200, 0);
	cover->SetPoint(3,   0,   0);
	cover->SetFillColor(kGray);
	cover->Draw("f");

	TLatex tex;
	tex.SetTextSize(0.025);
	tex.SetTextFont(62);
	tex.SetNDC(true);
	tex.DrawLatex(0.6, 0.25, "bino m_{#tilde{#chi}^{0}} > wino m_{#tilde{#chi}}");
	gPad->RedrawAxis();
}


style* WinoBino_Style(){ 
  style * s = new style();
  s->leg = new TLegend(0.4,0.68,0.89,0.88,"GGM    m_{#tilde{q}} =  m_{#tilde{g}} = 5 TeV");
  s->leg->SetBorderSize(0);
  s->leg->SetLineColor(0);
  s->leg->SetFillColor(10);
  s->leg->SetFillStyle(1001);
  s->leg->SetTextFont(42);
  s->leg->SetTextSize(0.03);

  s->lumi = new TLatex(0.6, 0.901, "4.04 fb^{  -1}  #sqrt{s} = 8 TeV #geq1#gamma, #geq2 jets");
  s->lumi->SetNDC(true);
  s->lumi->SetTextColor(12);
  s->lumi->SetTextFont(43);
  s->lumi->SetTextSize(20);
  s->cms = new TLatex(0.21, 0.901, "#bf{CMS preliminary}");
  s->cms->SetNDC(true);
  s->cms->SetTextColor(12);
  s->cms->SetTextFont(43);
  s->cms->SetTextSize(20);
  s->cmsprelim = new TLatex(0.21, 0.901, "#bf{CMS}");
  s->cmsprelim->SetNDC(true);
  s->cmsprelim->SetTextColor(12);
  s->cmsprelim->SetTextFont(43);
  s->cmsprelim->SetTextSize(20);
  s->excluded = new TLatex(0.6, 0.4, "Excluded");
  s->excluded->SetNDC(true);
  s->excluded->SetTextColor(12);
  s->excluded->SetTextFont(43);
  s->excluded->SetTextSize(20);
  s->smooth_flag=2;
  s->smooth_points=15;
  s->PostExclusionPlotting=DrawWinoBinoDiagonalCut;
  s->iCLsObsExcl=1;  
  s->iCLsExpExcl=1;  
  s->iCLsExpExclm1=0;
  s->iCLsExpExclp1=0;
  s->iCLsObsTheom1=1;
  s->iCLsObsTheop1=1;
  s->iCLsExpTheom1=0;
  s->iCLsExpTheop1=0;  

  SetDefault(s);

  return s;
}

/// ------  SMS T1 gg /// -------------------------------------------------------
void Draw_T1gg_CoverUp(style * s=0, TLegend*l=0) {

	TGraph*cover = new TGraph(0);
	cover->SetPoint(0, 50,     75);
	cover->SetPoint(1, 2500, 2575);
	cover->SetPoint(2, 2500, 1000);
	cover->SetPoint(3,    0,    0);
	cover->SetFillColor(kWhite);
	//cover->Draw("f");


	TGraph*cover2 = new TGraph(0);
	cover2->SetPoint(0, 1200, 1200);
	cover2->SetPoint(1, 2500, 9000);
	cover2->SetPoint(2, 2500, 2500);
	cover2->SetPoint(3, 1200, 1200);
	cover2->SetFillColor(kWhite);
	//cover2->Draw("f");

	TGraph*gluinoNLSP = new TGraph(0);
	gluinoNLSP->SetPoint(0, 50, 50);
	gluinoNLSP->SetPoint(1, 3000, 3000);
	gluinoNLSP->SetPoint(2, 50, 3000);
	gluinoNLSP->SetPoint(3, 50, 50);
	gluinoNLSP->SetFillColor(kGray);
	gluinoNLSP->Draw("f");

	TLatex tex;
	tex.SetTextSize(0.03);
	tex.SetTextFont(42);
	tex.SetNDC(true);
	tex.DrawLatex(0.25, 0.58, "#tilde{g} NLSP");
	gPad->RedrawAxis();
}


style* SMST1gg_Style(){ 
  style * s = new style();
  s->leg       = new TLegend(0.22,0.68,0.59,0.88,"SMS #gamma#gamma");
  s->lumi      = new TLatex(0.57, 0.902, "L_{int} = 19.8 fb^{  -1} #geq1#gamma, #geq2 jets");
  s->cms       = new TLatex(0.21, 0.902, "#bf{CMS preliminary} #sqrt{s} = 8 TeV");
  s->cmsprelim = new TLatex(0.21, 0.902, "#bf{CMS}    #sqrt{s} = 8 TeV");
  s->excluded=0;
  s->smooth_flag=2;
  s->smooth_points=10;
  s->PostExclusionPlotting=Draw_T1gg_CoverUp;
  s->iCLsObsExcl=1;  
  s->iCLsExpExcl=1;  
  s->iCLsExpExclm1=1;
  s->iCLsExpExclp1=1;
  s->iCLsObsTheom1=1;
  s->iCLsObsTheop1=1;

  s->Set505=true;
  s->MinXsecZ=0.0001;
  s->MaxXsecZ=5;
  s->MinAccZ=0;
  s->MaxAccZ=1;

  SetDefault(s);

  return s;
}

/// SMS T1 lg /// -------------------------------------------------------
void DrawNeutrNNLSP(style * s=0, TLegend*l=0) {
	TGraph*gluinoNLSP = new TGraph(0);
	gluinoNLSP->SetPoint(0, 50, 50);
	gluinoNLSP->SetPoint(1, 3000, 3000);
	gluinoNLSP->SetPoint(2, 50, 3000);
	gluinoNLSP->SetPoint(3, 50, 50);
	gluinoNLSP->SetFillColor(kGray);
	gluinoNLSP->Draw("f");

	TLatex tex;
	tex.SetTextSize(0.03);
	tex.SetTextFont(42);
	tex.SetNDC(true);
	tex.DrawLatex(0.25, 0.58, "#tilde{g} NLSP");
	gPad->RedrawAxis();
}

  
style* SMST1lg_Style(){ 
  style * s = new style();
  s->leg       = new TLegend(0.22,0.68,0.59,0.88,"SMS #gamma + X");
  s->lumi      = new TLatex(0.57, 0.902, "L_{int} = 19.8 fb^{  -1} #geq1#gamma, #geq2 jets");
  s->cms       = new TLatex(0.21, 0.902, "#bf{CMS preliminary} #sqrt{s} = 8 TeV");
  s->cmsprelim = new TLatex(0.21, 0.902, "#bf{CMS}    #sqrt{s} = 8 TeV");
  s->excluded=0;
  s->smooth_flag=2;
  s->smooth_points=10;
  s->PostExclusionPlotting=DrawNeutrNNLSP;
  s->iCLsObsExcl=1;  
  s->iCLsExpExcl=1;  
  s->iCLsExpExclm1=1;
  s->iCLsExpExclp1=3;
  s->iCLsObsTheom1=1;
  s->iCLsObsTheop1=1;
  s->iCLsExpTheom1=1;
  s->iCLsExpTheop1=1;  
  s->MinXsecZ=0.001;
  s->MaxXsecZ=2;
  s->MinAccZ=0;
  s->MaxAccZ=0.2;

  SetDefault(s);

  return s;
}

