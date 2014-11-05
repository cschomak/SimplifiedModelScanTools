// $Id: StyleSettings.h,v 1.9 2012/06/29 20:27:21 auterman Exp $

/*** ------------------------------------------------------------------------------------------------------- ***
     TheBetterPlotScript, a tool to plot final results, limits and exclusion contours, based on 'PlotScript'

     Christian Autermann, Hamburg University/LPC, February 2012
 *** ------------------------------------------------------------------------------------------------------- ***/

#ifndef STYLE_SETTINGS_H
#define STYLE_SETTINGS_H

#include <iostream>

#include "TString.h"
#include "TStyle.h"
#include "TLatex.h"
#include "TGraph.h"
#include "TPad.h"
#include "TLegend.h"

class PlotTools;
struct style;
style* WinoBino_Style();
style* SqGlWino_Style();
style* SqGlBino_Style();
style* GlWino_Style();
style* GlBino_Style();
style* SMST1gg_Style();
style* SMST1lg_Style();

style* SqGlWino_Style_SD7();
style* SqGlBino_Style_SD7();
style* SqGlWino_Style_SD8();
style* SqGlBino_Style_SD8();

style* SqGlBino_78Syst_Style();
style* SqGlWino_78Syst_Style();

style* Fixed_Neutralino_Style();
style* Fixed_Edge_Style();

style* SqGlWino_DiP_Style();
style* SqGlBino_DiP_Style();
style* SqGlBino_DiP78Syst_Style();
style* SqGlWino_DiP78Syst_Style();

/* Paper Style agreement with Dongwook
TCanvas size:
//800 x 600

//black color
left: CMS, sqrt(s)=7TeV
right: L_int = 4.62 fb-1 , selection

*/
struct style{
  style(){ //Set Defaults
    PreExclusionPlotting=0;
    PostExclusionPlotting=0;
    leg=0;
    cms=0;
    cmsprelim=0;
    lumi=0;
    cmsTemperaturePlot=0;
    cmsprelimTemperaturePlot=0;
    lumiTemperaturePlot=0;
    excluded=0;
    smooth_flag=0;
    smooth_points=25;
    second_smooth=0;
    iCLsObsExcl=0;  
    iCLsExpExcl=0;  
    iCLsExpExclm1=0;
    iCLsExpExclp1=0;
    iCLsExpExclm2=0;
    iCLsExpExclp2=0;
    iCLsObsTheom1=0;
    iCLsObsTheop1=0;
    iCLsExpTheom1=0;
    iCLsExpTheop1=0;
    MinXsecZ=-999.;//let the plot find the min/max
    MaxXsecZ=-999.;  
    MinAccZ=-999.;//let the plot find the min/max
    MaxAccZ=-999.;  
    //~ lumi = new TLatex(0.50, 0.901, "4.62 fb^{  -1}  #sqrt{s} = 7 TeV   #geq1 #gamma, #geq2 jets");
    lumi = new TLatex(0.95, 0.96, "19.4 fb^{-1} (8 TeV)");
    lumi->SetNDC(true);
    lumi->SetTextColor(12);
    lumi->SetTextFont(42);
    lumi->SetTextAlign(31);
    lumi->SetTextSize(0.04);
    cms = new TLatex(0.19, 0.89, "CMS");
    cms->SetNDC(true);
    //~ cms->SetTextColor(12);
    cms->SetTextFont(61);
    cms->SetTextSize(0.055);
    //~ cmsprelim = new TLatex(0.21, 0.901, "#bf{CMS preliminary}");
    cmsprelim = new TLatex(0.19, 0.85, "Preliminary");
    cmsprelim->SetNDC(true);
    //~ cmsprelim->SetTextColor(12);
    cmsprelim->SetTextFont(52);
    cmsprelim->SetTextSize(0.03);

    //~ lumiTemperaturePlot = new TLatex(0.48, 0.906, "4.62 fb^{  -1}  #sqrt{s} = 7 TeV   #geq1 #gamma, #geq2 jets");
    lumiTemperaturePlot = new TLatex(0.95, 0.96, "19.4 fb^{-1} (8 TeV)");
    lumiTemperaturePlot->SetNDC(true);
    //~ lumiTemperaturePlot->SetTextColor(12);
    lumiTemperaturePlot->SetTextFont(42);
    lumiTemperaturePlot->SetTextSize(0.04);
    lumiTemperaturePlot->SetTextAlign(31);
    cmsTemperaturePlot = new TLatex(0.19, 0.89, "CMS");
    cmsTemperaturePlot->SetNDC(true);
    cmsTemperaturePlot->SetTextColor(12);
    cmsTemperaturePlot->SetTextFont(43);
    cmsTemperaturePlot->SetTextSize(20);
    //~ cmsprelimTemperaturePlot = new TLatex(0.21, 0.906, "#bf{CMS preliminary}");
    cmsprelimTemperaturePlot = new TLatex(0.19, 0.85, "Preliminary");
    cmsprelimTemperaturePlot->SetNDC(true);
    //~ cmsprelimTemperaturePlot->SetTextColor(12);
    cmsprelimTemperaturePlot->SetTextFont(52);
    cmsprelimTemperaturePlot->SetTextSize(0.03);
    Set505=false;
    SetMoreLogLabels=false;
    show7TeVExp=false;
    show7TeVObs=false;
    show8TeVExp=false;
    show8TeVObs=false;
  } 
  ///
  /// Please make sure, that all new variables in this class are set to proper default values in the contructor above!
  /// I.e. the default value should leave the old style unchanged.
  ///
  void (*PreExclusionPlotting)(style*, PlotTools*);
  void (*PostExclusionPlotting)(style*, TLegend*);
   
  TLegend * leg, *legTemperaturePlot;
  TLatex * cms, *cmsprelim, *lumi, *excluded, * cmsTemperaturePlot, *cmsprelimTemperaturePlot, *lumiTemperaturePlot ;
  int smooth_flag;
  int smooth_points, second_smooth;
  int iCLsObsExcl;  
  int iCLsExpExcl;  
  int iCLsExpExclm1;
  int iCLsExpExclp1;
  int iCLsExpExclm2;
  int iCLsExpExclp2;
  int iCLsObsTheom1;
  int iCLsObsTheop1;
  int iCLsExpTheom1;
  int iCLsExpTheop1;
  double MinXsecZ;
  double MaxXsecZ;
  double MinAccZ;
  double MaxAccZ;
  bool Set505;
  bool SetMoreLogLabels;
  bool show7TeVExp;
  bool show7TeVObs;
  bool show8TeVExp;
  bool show8TeVObs;

};




  
namespace util {

  //!  Encapsulates different pad and histogram styles
  //!
  //!  \author   Matthias Schroeder (www.desy.de/~matsch)
  //!  \date     2010/03/09
  //!  $Id: StyleSettings.h,v 1.9 2012/06/29 20:27:21 auterman Exp $
  // -------------------------------------------------------------------------------------
  class StyleSettings {
  public:
    enum Style { Screen, Presentation, Paper };
    
    static Style style() {
      Style st = Screen;
      TString mode = gStyle->GetTitle();
      if( mode == "Presentation" ) st = Presentation;
      else if( mode == "Paper" ) st = Paper;
      return st;
    }
    static void screen() { setStyle("Screen",true); }
    static void screenNoTitle() { setStyle("Screen",false); }
    static void paper() { setStyle("Paper",true); }
    static void paperNoTitle() { setStyle("Paper",false); }
    static void presentation() { setStyle("Presentation",true); }
    static void presentationNoTitle() { setStyle("Presentation",false); }
    static void cms() { setStyle("CMS",false); }
    static int color(int i) {
      int col[5] = { 1, 2, 4, 7, 8 };
      return (i>=0 && i<5) ? col[i] : 1;
    }
    static int lineWidth() {
      int width = 1;
      TString mode = "Presentation";
      if( mode.CompareTo(gStyle->GetTitle()) == 0 ) {
	width = 2;
      }
      return width;
    }
    
  private:
    static void setStyle(const TString &mode, bool spaceForTitle) {
      // Set title of current style object
      gStyle->SetTitle(mode);

      // Zero horizontal error bars
      gStyle->SetErrorX(0);

      //  For 'colz' TH2
      gStyle->SetPalette(1);
    
      //  For the canvas
      gStyle->SetCanvasBorderMode(0);
      gStyle->SetCanvasColor(kWhite);
      gStyle->SetCanvasDefH(800); //Height of canvas
      gStyle->SetCanvasDefW(800); //Width of canvas
      gStyle->SetCanvasDefX(0);   //Position on screen
      gStyle->SetCanvasDefY(0);
    
      //  For the frame
      gStyle->SetFrameBorderMode(0);
      gStyle->SetFrameBorderSize(1);
      gStyle->SetFrameFillColor(kBlack);
      gStyle->SetFrameFillStyle(0);
      gStyle->SetFrameLineColor(kBlack);
      gStyle->SetFrameLineStyle(0);
      gStyle->SetFrameLineWidth(1);
    
      //  For the Pad
      gStyle->SetPadBorderMode(0);
      gStyle->SetPadColor(kWhite);
      gStyle->SetPadGridX(false);
      gStyle->SetPadGridY(false);
      gStyle->SetGridColor(0);
      gStyle->SetGridStyle(3);
      gStyle->SetGridWidth(1);

      //  Margins
      if( mode == "Presentation" ) {
	if( spaceForTitle ) {
	  gStyle->SetPadTopMargin(0.11);
	  gStyle->SetPadBottomMargin(0.18);
	  gStyle->SetPadLeftMargin(0.25);
	  gStyle->SetPadRightMargin(0.04);
	} else {
	  gStyle->SetPadTopMargin(0.05);
	  gStyle->SetPadBottomMargin(0.18);
	  gStyle->SetPadLeftMargin(0.19);
	  gStyle->SetPadRightMargin(0.04);
	}
      } else if( mode == "Paper" || mode == "CMS"  ) {
	if( spaceForTitle ) {
	  gStyle->SetPadTopMargin(0.06);
	  gStyle->SetPadBottomMargin(0.18);
	  gStyle->SetPadLeftMargin(0.2);
	  gStyle->SetPadRightMargin(0.04);
	} else {
	  gStyle->SetPadTopMargin(0.05);
	  gStyle->SetPadBottomMargin(0.17);
	  gStyle->SetPadLeftMargin(0.18);
	  gStyle->SetPadRightMargin(0.04);
	}
      } else {
	if( spaceForTitle ) {
	  gStyle->SetPadTopMargin(0.10);
	  gStyle->SetPadBottomMargin(0.14);
	  gStyle->SetPadLeftMargin(0.18);
	  gStyle->SetPadRightMargin(0.04);
	} else {
	  gStyle->SetPadTopMargin(0.08);
	  gStyle->SetPadBottomMargin(0.14);
	  gStyle->SetPadLeftMargin(0.18);
	  gStyle->SetPadRightMargin(0.04);
	}
      }

      //  For the histo:
      gStyle->SetHistLineColor(kBlack);
      gStyle->SetHistLineStyle(0);
      gStyle->SetHistLineWidth(1);
    
      //  For the statistics box:
      if( mode == "Screen" ) {
	gStyle->SetOptStat("eMR");
	gStyle->SetStatColor(kWhite);
	gStyle->SetStatFont(42);
	gStyle->SetStatFontSize(0.03);
	gStyle->SetStatTextColor(1);
	gStyle->SetStatFormat("6.4g");
	gStyle->SetStatBorderSize(1);
	gStyle->SetStatX(0.94);              
	gStyle->SetStatY(0.86);              
	gStyle->SetStatH(0.16);
	gStyle->SetStatW(0.22);
      } else {
	gStyle->SetOptStat(0);
      }
    
      //  For the Global title:
      gStyle->SetOptTitle(1);
      gStyle->SetTitleFont(42,"");
      gStyle->SetTitleColor(1);
      gStyle->SetTitleTextColor(1);
      gStyle->SetTitleFillColor(0);
      gStyle->SetTitleFontSize(0.1);
      gStyle->SetTitleAlign(23);
      gStyle->SetTitleX(0.6);
      gStyle->SetTitleH(0.05);
      gStyle->SetTitleBorderSize(0);

      //  For the axis
      gStyle->SetAxisColor(1,"XYZ");
      gStyle->SetTickLength(0.03,"XYZ");
      gStyle->SetNdivisions(510,"XYZ");
      if( mode == "CMS" ) {
	gStyle->SetPadTickX(0);
	gStyle->SetPadTickY(0);
      } else {
	gStyle->SetPadTickX(1);
	gStyle->SetPadTickY(1);
      }
      gStyle->SetStripDecimals(kFALSE);
    
      //  For the axis labels and titles
      gStyle->SetTitleColor(1,"XYZ");
      gStyle->SetLabelColor(1,"XYZ");
      if( mode == "Presentation" ) {
	// For the axis labels:
	gStyle->SetLabelFont(42,"XYZ");
	gStyle->SetLabelOffset(0.007,"XYZ");
	gStyle->SetLabelSize(0.045,"XYZ");
      
	// For the axis titles:
	gStyle->SetTitleFont(42,"XYZ");
	gStyle->SetTitleSize(0.06,"XYZ");
	gStyle->SetTitleXOffset(1.2);
	if( spaceForTitle ) gStyle->SetTitleYOffset(2.0);
	else                gStyle->SetTitleYOffset(1.5);
      } else if ( mode == "Paper" || mode == "CMS" ) {
	// For the axis labels:
	gStyle->SetLabelFont(42,"XYZ");
	gStyle->SetLabelOffset(0.007,"XYZ");
	gStyle->SetLabelSize(0.04,"XYZ");
      
	// For the axis titles:
	gStyle->SetTitleFont(42,"XYZ");
	gStyle->SetTitleSize(0.045,"XYZ");
	gStyle->SetTitleXOffset(1.5);
	if( spaceForTitle ) gStyle->SetTitleYOffset(2.1);
	else                gStyle->SetTitleYOffset(1.8);
      } else {
	// For the axis labels:
	gStyle->SetLabelFont(42,"XYZ");
	gStyle->SetLabelOffset(0.007,"XYZ");
	gStyle->SetLabelSize(0.035,"XYZ");
      
	// For the axis titles:
	gStyle->SetTitleFont(42,"XYZ");
	gStyle->SetTitleSize(0.04,"XYZ");
	gStyle->SetTitleXOffset(1.5);
	if( spaceForTitle ) gStyle->SetTitleYOffset(2.1);
	else                gStyle->SetTitleYOffset(1.8);
      }


      //  For the legend
      gStyle->SetLegendBorderSize(0);

      //  For the statistics box
      if( mode == "Presentation" ) {
	if( spaceForTitle ) {
	  gStyle->SetStatFontSize(0.04);
	  gStyle->SetStatX(0.92);              
	  gStyle->SetStatY(0.86);              
	  gStyle->SetStatH(0.2);
	  gStyle->SetStatW(0.3);
	} else {
	  gStyle->SetStatFontSize(0.04);
	  gStyle->SetStatX(0.92);              
	  gStyle->SetStatY(0.92);              
	  gStyle->SetStatH(0.2);
	  gStyle->SetStatW(0.3);
	}
      } else {
	if( spaceForTitle ) {
	  gStyle->SetStatFontSize(0.03);
	  gStyle->SetStatX(0.92);              
	  gStyle->SetStatY(0.86);              
	  gStyle->SetStatH(0.16);
	  gStyle->SetStatW(0.22);
	} else {
	  gStyle->SetStatFontSize(0.03);
	  gStyle->SetStatX(0.92);              
	  gStyle->SetStatY(0.92);              
	  gStyle->SetStatH(0.16);
	  gStyle->SetStatW(0.22);
	}
      }

      std::cout << "Adjusted gStyle for " << std::flush;
      if( mode == "Screen" ) std::cout << "screen viewing" << std::flush;
      else if( mode == "Paper" ) std::cout << "papers" << std::flush;
      else if( mode == "CMS" ) std::cout << "CMS PAS" << std::flush;
      else std::cout << "presentations" << std::flush;
      std::cout << " and " << std::flush;
      if( spaceForTitle ) std::cout << "histograms with title." << std::endl;
      else std::cout << "histograms without title." << std::endl;
    }
  };  
}


#endif


