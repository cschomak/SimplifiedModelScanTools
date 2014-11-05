// $Id: StyleSettings_DiPhoton.cc,v 1.2 2012/06/29 20:27:21 auterman Exp $

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


style* SqGlBino_Style(){ /// Sq-Gl Bino /// ---------------------------------------------------------------------
  style * s = new style();
  s->leg=new TLegend(0.26,0.61,0.26,0.45,"#splitline{GGM bino-like #tilde{#chi}^{0}}{m_{#tilde{#chi}^{0}} = 375 GeV}");
  s->leg->SetBorderSize(0);
  s->leg->SetLineColor(0);
  s->leg->SetFillColor(10);
  s->leg->SetFillStyle(1001);
  s->leg->SetTextFont(42);
  s->leg->SetTextSize(0.03);

  s->lumi = new TLatex(0.58, 0.901, "4.6fb^{  -1}  #sqrt{s} = 7 TeV   #geq1#gamma, #geq2 jets");
  s->lumi->SetNDC(true);
  s->lumi->SetTextColor(12);
  s->lumi->SetTextFont(43);
  s->lumi->SetTextSize(20);
  s->cms = new TLatex(0.21, 0.901, "#bf{CMS}");
  s->cms->SetNDC(true);
  s->cms->SetTextColor(12);
  s->cms->SetTextFont(43);
  s->cms->SetTextSize(20);
  s->cmsprelim = new TLatex(0.21, 0.901, "#bf{CMS preliminary}");
  s->cmsprelim->SetNDC(true);
  s->cmsprelim->SetTextColor(12);
  s->cmsprelim->SetTextFont(43);
  s->cmsprelim->SetTextSize(20);
  s->excluded = new TLatex(0.3, 0.7, "excluded");
  s->excluded->SetNDC(true);
  s->excluded->SetTextColor(12);
  s->excluded->SetTextFont(43);
  s->excluded->SetTextSize(20);
  s->smooth_points=25;
  s->MinXsecZ=0.001;
  s->MaxXsecZ=0.03;
  s->iCLsObsExcl=2;  
  s->iCLsExpExcl=0;  
  s->iCLsExpExclm1=0;
  s->iCLsExpExclp1=0;
  s->iCLsObsTheom1=2;
  s->iCLsObsTheop1=2;
  return s;
}

style* SqGlWino_Style(){ /// Sq-Gl Wino /// ---------------------------------------------------------------------
  style * s = new style();
  s->leg=new TLegend(0.47,0.82,0.64,0.85,"#splitline{GGM wino-like #tilde{#chi}^{0}}{m_{#tilde{#chi}^{0}} = 375 GeV}");
  s->leg->SetBorderSize(0);
  s->leg->SetLineColor(0);
  s->leg->SetFillColor(10);
  s->leg->SetFillStyle(1001);
  s->leg->SetTextFont(42);
  s->leg->SetTextSize(0.03);

  s->lumi = new TLatex(0.58, 0.901, "4.6fb^{  -1}  #sqrt{s} = 7 TeV   #geq1#gamma, #geq2 jets");
  s->lumi->SetNDC(true);
  s->lumi->SetTextColor(12);
  s->lumi->SetTextFont(43);
  s->lumi->SetTextSize(20);
  s->cms = new TLatex(0.21, 0.901, "#bf{CMS}");
  s->cms->SetNDC(true);
  s->cms->SetTextColor(12);
  s->cms->SetTextFont(43);
  s->cms->SetTextSize(20);
  s->cmsprelim = new TLatex(0.2, 0.901, "#bf{CMS preliminary}");
  s->cmsprelim->SetNDC(true);
  s->cmsprelim->SetTextColor(12);
  s->cmsprelim->SetTextFont(43);
  s->cmsprelim->SetTextSize(20);
  s->excluded = new TLatex(0.3, 0.3, "excluded");
  s->excluded->SetNDC(true);
  s->excluded->SetTextColor(12);
  s->excluded->SetTextFont(43);
  s->excluded->SetTextSize(25);
  s->smooth_points=25;
  s->MinXsecZ=0.01;
  s->MaxXsecZ=0.5;
  
  return s;
}


/// ----------- Gl - Bino ------------ /// ----------------------------------------------------------------------------------

void Draw_DiPhoton_GlBino_CoverUp(style * s=0) {
	TGraph*cover = new TGraph(0);
	cover->SetPoint(0, 200,  300);
	cover->SetPoint(1, 1200, 1210);
	cover->SetPoint(2, 1200, 1190);
	cover->SetPoint(3,    0,    0);
	cover->SetFillColor(kWhite);
	//cover->SetLineColor(kBlack);
	cover->Draw("f");

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
	tex.DrawLatex(0.6, 0.25, "#tilde{g} NLSP");
	gPad->RedrawAxis();
}


style* GlBino_Style(style * s=0){ 
  style * s = new style();
  s->leg=new TLegend(0.26,0.68,0.69,0.85,"#splitline{GGM bino-like #tilde{#chi}^{0}}{m_{#tilde{q}} = 2500 GeV}");
  s->leg->SetBorderSize(0);
  s->leg->SetLineColor(0);
  s->leg->SetFillColor(10);
  s->leg->SetFillStyle(1001);
  s->leg->SetTextFont(42);
  s->leg->SetTextSize(0.03);

  s->lumi = new TLatex(0.58, 0.901, "4.6fb^{  -1}  #sqrt{s} = 7 TeV   #geq1#gamma, #geq2 jets");
  s->lumi->SetNDC(true);
  s->lumi->SetTextColor(12);
  s->lumi->SetTextFont(43);
  s->lumi->SetTextSize(20);
  s->cms = new TLatex(0.21, 0.901, "#bf{CMS}");
  s->cms->SetNDC(true);
  s->cms->SetTextColor(12);
  s->cms->SetTextFont(43);
  s->cms->SetTextSize(20);
  s->cmsprelim = new TLatex(0.21, 0.901, "#bf{CMS preliminary}");
  s->cmsprelim->SetNDC(true);
  s->cmsprelim->SetTextColor(12);
  s->cmsprelim->SetTextFont(43);
  s->cmsprelim->SetTextSize(20);
  
  s->lumiTemperaturePlot = new TLatex(0.48, 0.906, "4.6fb^{  -1}  #sqrt{s} = 7 TeV   #geq1#gamma, #geq2 jets");
  s->lumiTemperaturePlot->SetNDC(true);
  s->lumiTemperaturePlot->SetTextColor(12);
  s->lumiTemperaturePlot->SetTextFont(43);
  s->lumiTemperaturePlot->SetTextSize(20);
  s->cmsTemperaturePlot = new TLatex(0.21, 0.906, "#bf{CMS}");
  s->cmsTemperaturePlot->SetNDC(true);
  s->cmsTemperaturePlot->SetTextColor(12);
  s->cmsTemperaturePlot->SetTextFont(43);
  s->cmsTemperaturePlot->SetTextSize(20);
  s->cmsprelimTemperaturePlot = new TLatex(0.21, 0.906, "#bf{CMS preliminary}");
  s->cmsprelimTemperaturePlot->SetNDC(true);
  s->cmsprelimTemperaturePlot->SetTextColor(12);
  s->cmsprelimTemperaturePlot->SetTextFont(43);
  s->cmsprelimTemperaturePlot->SetTextSize(20);

  s->excluded = new TLatex(0.3, 0.4, "excluded");
  s->excluded->SetNDC(true);
  s->excluded->SetTextColor(12);
  s->excluded->SetTextFont(43);
  s->excluded->SetTextSize(20);
  s->smooth_flag=2;
  s->smooth_points=25;
  s->PostExclusionPlotting=Draw_DiPhoton_GlBino_CoverUp;
  s->iCLsObsExcl=0;  
  s->iCLsExpExcl=0;  
  s->iCLsExpExclm1=0;
  s->iCLsExpExclp1=0;
  s->iCLsObsTheom1=0;
  s->iCLsObsTheop1=0;
  s->MinXsecZ=0.001;
  s->MaxXsecZ=0.5;

  return s;
}

/// ----------- Gl - Wino ------------ /// ----------------------------------------------------------------------------------
void Draw_DiPhoton_GlWino_CoverUp(style * s=0) {
	TGraph*cover = new TGraph(0);
	cover->SetPoint(0, 300,  350);
	cover->SetPoint(1, 950, 1000);
	cover->SetPoint(2, 1000, 1000);
	cover->SetPoint(3,    0,    0);
	cover->SetFillColor(kWhite);
	//cover->SetLineColor(kBlack);
	cover->Draw("f");

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
  s->leg=new TLegend(0.42,0.20,0.89,0.46,"#splitline{GGM wino-like #tilde{#chi}^{0}}{m_{#tilde{q}} = 2500 GeV}");
  s->leg->SetBorderSize(0);
  s->leg->SetLineColor(0);
  s->leg->SetFillColor(10);
  s->leg->SetFillStyle(1001);
  s->leg->SetTextFont(42);
  s->leg->SetTextSize(0.03);

  s->lumi = new TLatex(0.58, 0.901, "4.6fb^{  -1}  #sqrt{s} = 7 TeV   #geq1#gamma, #geq2 jets");
  s->lumi->SetNDC(true);
  s->lumi->SetTextColor(12);
  s->lumi->SetTextFont(43);
  s->lumi->SetTextSize(20);
  s->cms = new TLatex(0.21, 0.901, "#bf{CMS}");
  s->cms->SetNDC(true);
  s->cms->SetTextColor(12);
  s->cms->SetTextFont(43);
  s->cms->SetTextSize(20);
  s->cmsprelim = new TLatex(0.21, 0.901, "#bf{CMS preliminary}");
  s->cmsprelim->SetNDC(true);
  s->cmsprelim->SetTextColor(12);
  s->cmsprelim->SetTextFont(43);
  s->cmsprelim->SetTextSize(20);
  s->excluded = new TLatex(0.5, 0.55, "excluded");
  s->excluded->SetNDC(true);
  s->excluded->SetTextColor(12);
  s->excluded->SetTextFont(43);
  s->excluded->SetTextSize(20);
  s->smooth_flag=2;
  s->smooth_points=25;
  s->PostExclusionPlotting=Draw_DiPhoton_GlWino_CoverUp;
  s->iCLsObsExcl=0;  
  s->iCLsExpExcl=0;  
  s->iCLsExpExclm1=0;
  s->iCLsExpExclp1=0;
  s->iCLsObsTheom1=0;
  s->iCLsObsTheop1=0;

  s->MinXsecZ=0.01;
  s->MaxXsecZ=20;

  return s;
}

/// Cha - Chi /// -----------------------------------------------------------------------
void DrawWinoBinoDiagonalCut(style * s=0) {
	TGraph*cover = new TGraph(0);
	cover->SetPoint(0,   0,   0);
	cover->SetPoint(1, 1200, 1200);
	cover->SetPoint(2,   0, 1200);
	cover->SetPoint(3,   0,   0);
	cover->SetFillColor(kGray);
	cover->Draw("f");

	TLatex tex;
	tex.SetTextSize(0.025);
	tex.SetTextFont(62);
	tex.SetNDC(true);
	tex.DrawLatex(0.25, 0.6, "bino m_{#tilde{#chi}^{0}} > wino m_{#tilde{#chi}}");
	gPad->RedrawAxis();
}



style* WinoBino_Style(){ 
  style * s = new style();
  s->leg=new TLegend(0.4,0.68,0.89,0.88,"GGM    m_{#tilde{q}} =  m_{#tilde{g}} = 5 TeV");
  s->leg->SetBorderSize(0);
  s->leg->SetLineColor(0);
  s->leg->SetFillColor(10);
  s->leg->SetFillStyle(1001);
  s->leg->SetTextFont(42);
  s->leg->SetTextSize(0.03);

  s->lumi = new TLatex(0.6, 0.901, "4.6fb^{  -1}  #sqrt{s} = 7 TeV   #geq1#gamma, #geq2 jets");
  s->lumi->SetNDC(true);
  s->lumi->SetTextColor(12);
  s->lumi->SetTextFont(43);
  s->lumi->SetTextSize(20);
  s->cms = new TLatex(0.21, 0.901, "#bf{CMS}");
  s->cms->SetNDC(true);
  s->cms->SetTextColor(12);
  s->cms->SetTextFont(43);
  s->cms->SetTextSize(20);
  s->cmsprelim = new TLatex(0.21, 0.901, "#bf{CMS preliminary}");
  s->cmsprelim->SetNDC(true);
  s->cmsprelim->SetTextColor(12);
  s->cmsprelim->SetTextFont(43);
  s->cmsprelim->SetTextSize(20);
  s->excluded = new TLatex(0.6, 0.4, "excluded");
  s->excluded->SetNDC(true);
  s->excluded->SetTextColor(12);
  s->excluded->SetTextFont(43);
  s->excluded->SetTextSize(20);
  s->smooth_flag=2;
  s->smooth_points=15;
  s->PostExclusionPlotting=DrawWinoBinoDiagonalCut;
  s->iCLsObsExcl=1;  
  s->iCLsExpExcl=1;  
  s->iCLsExpExclm1=1;
  s->iCLsExpExclp1=1;
  s->iCLsObsTheom1=1;
  s->iCLsObsTheop1=1;
  s->iCLsExpTheom1=1;
  s->iCLsExpTheop1=1;  
  return s;
}

/// ------  SMS T1 gg /// -------------------------------------------------------
void Draw_DiPhoton_T1gg_CoverUp(style * s=0) {

	TGraph*cover = new TGraph(0);
	cover->SetPoint(0, 50,     75);
	cover->SetPoint(1, 2500, 2575);
	cover->SetPoint(2, 2500, 1000);
	cover->SetPoint(3,    0,    0);
	cover->SetFillColor(kWhite);
	cover->Draw("f");


	TGraph*cover2 = new TGraph(0);
	cover2->SetPoint(0, 1200, 1200);
	cover2->SetPoint(1, 2500, 9000);
	cover2->SetPoint(2, 2500, 2500);
	cover2->SetPoint(3, 1200, 1200);
	cover2->SetFillColor(kWhite);
	cover2->Draw("f");

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
	tex.DrawLatex(0.6, 0.25, "#tilde{g} NLSP");
	gPad->RedrawAxis();
}


style* SMST1gg_Style(){ 
  style * s = new style();
  s->leg=new TLegend(0.31,0.69,0.69,0.84,"SMS #gamma#gamma");
  s->leg->SetBorderSize(0);
  s->leg->SetLineColor(0);
  s->leg->SetFillColor(10);
  s->leg->SetFillStyle(1001);
  s->leg->SetTextFont(42);
  s->leg->SetTextSize(0.03);

  s->lumi = new TLatex(0.58, 0.901, "4.6fb^{  -1}  #sqrt{s} = 7 TeV   #geq1#gamma, #geq2 jets");
  s->lumi->SetNDC(true);
  s->lumi->SetTextColor(12);
  s->lumi->SetTextFont(43);
  s->lumi->SetTextSize(20);
  s->cms = new TLatex(0.21, 0.901, "#bf{CMS}");
  s->cms->SetNDC(true);
  s->cms->SetTextColor(12);
  s->cms->SetTextFont(43);
  s->cms->SetTextSize(20);
  s->cmsprelim = new TLatex(0.21, 0.901, "#bf{CMS preliminary}");
  s->cmsprelim->SetNDC(true);
  s->cmsprelim->SetTextColor(12);
  s->cmsprelim->SetTextFont(43);
  s->cmsprelim->SetTextSize(20);
  s->excluded=0;
  s->smooth_flag=2;
  s->smooth_points=30;
  s->PostExclusionPlotting=Draw_DiPhoton_T1gg_CoverUp;
  s->iCLsObsExcl=0;  
  s->iCLsExpExcl=0;  
  s->iCLsExpExclm1=0;
  s->iCLsExpExclp1=0;
  s->iCLsObsTheom1=0;
  s->iCLsObsTheop1=0;

  s->Set505=true;
  s->MinXsecZ=0.001;
  s->MaxXsecZ=2;

  return s;
}
  

