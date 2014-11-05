// $Id: Plotting.cc,v 1.2 2012/06/29 20:27:21 auterman Exp $

/*** ------------------------------------------------------------------------------------------------------- ***
     TheBetterPlotScript, a tool to plot final results, limits and exclusion contours, based on 'PlotScript'

     Christian Autermann, Hamburg University/LPC, February 2012
 *** ------------------------------------------------------------------------------------------------------- ***/


#include "Plotting.h"

#include "StyleSettings.h"
#include "OldExclusionContours.h"


void DrawPlot2D(PlotTools *PlotTool, TCanvas*canvas, TH2* h, const std::string& flag, const string& x, const std::string& y, const std::string& var, 
                const std::string& ztitel, double zmin, double zmax, style*s)
{
   TH2F *plot2D = (TH2F*)h->Clone();
   plot2D->GetZaxis()->SetTitle(ztitel.c_str());
   PlotTool->Area(plot2D, x, y, var);
   plot2D->GetZaxis()->SetTitleOffset(1.5);
   if (zmin!=-999) plot2D->SetMinimum(zmin);
   if (zmax!=-999) plot2D->SetMaximum(zmax);
   if (zmin==-999&&zmax==-999) SetZRange(plot2D);
   if (s&&s->SetMoreLogLabels) {
     plot2D->GetZaxis()->SetMoreLogLabels();
     plot2D->GetZaxis()->SetLabelSize(0.035);
     plot2D->GetZaxis()->SetTitleOffset(2.1);
     c1->SetRightMargin(0.22);  
     c1->SetLeftMargin(0.15);  
   }  

   plot2D->GetXaxis()->SetNdivisions(505);
   plot2D->Draw("colz"); 
   double tx=400;
   double ty=1.045*(plot2D->GetYaxis()->GetXmax()-plot2D->GetYaxis()->GetXmin())+plot2D->GetYaxis()->GetXmin();  

   if (s&&s->cmsprelimTemperaturePlot) s->cmsprelimTemperaturePlot->Draw();
   if (s&&s->lumiTemperaturePlot) s->lumiTemperaturePlot->Draw();
   gPad->RedrawAxis();
   string namePlot = "results/" + flag + "_"+x+"_"+y+"_"+var;
   if (plotPrelim) canvas->SaveAs((namePlot + "_prelim.pdf").c_str());
   if (plotPNG && plotPrelim) canvas->SaveAs((namePlot + "_prelim.png").c_str());
   if (plotC   && plotPrelim) canvas->SaveAs((namePlot + "_prelim.C").c_str());
   //
   plot2D->Draw("colz"); 
   if (s&&s->cmsTemperaturePlot)  s->cmsTemperaturePlot->Draw();
   if (s&&s->lumiTemperaturePlot) s->lumiTemperaturePlot->Draw();
   gPad->RedrawAxis();
   canvas->SaveAs((namePlot + ".pdf").c_str());
   if (plotPNG) canvas->SaveAs((namePlot + ".png").c_str());
   if (plotC)   canvas->SaveAs((namePlot + ".C").c_str());
}
 
void DrawHist1D(PlotTools *PlotTool, TCanvas*canvas, const std::string& flag, const string& x, const std::string& y, const std::string& var, 
                const std::string& titel, int n)
{
   std::vector<double> vec;
   PlotTool->VectorOf(vec, var);
   if (vec.size()<=0) return;
   std::sort(vec.begin(), vec.end());
   double median  = vec[vec.size()/2];
   double quant16 = vec[vec.size()/6.25];
   double quant84 = vec[vec.size()/1.2];
   double xmin    = vec.front();
   double xmax    = vec.back();
   std::string name = flag+"_"+x+"_"+y+"_"+var+"_1D";
   TH1F *h1D = new TH1F(name.c_str(),";;number of cMSSM points", n, xmin-sqrt(fabs(xmin)), xmax+sqrt(fabs(xmax)));
   h1D->GetXaxis()->SetTitle(titel.c_str());
   PlotTool->Hist(h1D, var);
   TLegend * leg = new TLegend(0.19, 0.7, 0.4, 0.88);
   leg->SetBorderSize(0);
   leg->SetFillColor(0);
   leg->SetTextSize(0.025);
   { std::stringstream ss; ss << "16% quantile: " << setprecision(3) << quant16;
   leg->AddEntry((TObject*)0,ss.str().c_str(),""); }
   { std::stringstream ss; ss << "median : " << setprecision(3) << median;
   leg->AddEntry((TObject*)0,ss.str().c_str(),""); }
   { std::stringstream ss; ss << "84% quantile: " << setprecision(3) << quant84;
   leg->AddEntry((TObject*)0,ss.str().c_str(),""); }
   h1D->Draw("h");
   leg->Draw("same");
   std::string namePlot = "results/" + flag +"_"+x+"_"+y+"_"+var+"_1D";
   c1->SaveAs((namePlot + ".pdf").c_str());
   if (plotPNG) c1->SaveAs((namePlot + ".png").c_str());
}


void DrawStandardUncertaintyPlots(PlotTools *pt, const std::string& flag, const std::string& x, const std::string& y, style*s, TH2*h)
{
   c1->SetRightMargin(0.18);  
   //Log z-scale
   c1->SetLogz(1);
   DrawPlot2D(pt,c1,h,flag,x,y,"Luminosity",        "Luminosity [pb^{-1}]", 0, 6000.);
   DrawPlot2D(pt,c1,h,flag,x,y,"SignalStatUnc",     "Rel. Signal Statistical uncertainty", 0.01, 100.);
   DrawPlot2D(pt,c1,h,flag,x,y,"SignalSysUnc",      "Rel. Signal Systematic uncertainty", 0.01, 100.);
   DrawPlot2D(pt,c1,h,flag,x,y,"SignalPDFAccUnc",   "Rel. Signal PDF Accept. uncertainty", 0.01, 100.);
   DrawPlot2D(pt,c1,h,flag,x,y,"SignalPDFXsecUnc",  "Rel. Signal PDF cross-section uncertainty", 0.01, 100.);
   DrawPlot2D(pt,c1,h,flag,x,y,"SignalScaleUnc",    "Rel. Signal Scale uncertainty", 0.01, 100.);
   DrawPlot2D(pt,c1,h,flag,x,y,"SignalJesUpUnc",    "Rel. Signal JES (up) uncertainty", 0.01, 100.);
   DrawPlot2D(pt,c1,h,flag,x,y,"SignalJesDnUnc",    "Rel. Signal JES (dn) uncertainty", 0.01, 100.);
   DrawPlot2D(pt,c1,h,flag,x,y,"SignalJerUpUnc",    "Rel. Signal JER (up) uncertainty", 0.01, 100.);
   DrawPlot2D(pt,c1,h,flag,x,y,"SignalJerDnUnc",    "Rel. Signal JER (dn) uncertainty", 0.01, 100.);
   DrawPlot2D(pt,c1,h,flag,x,y,"SignalTotalUnc",    "Rel. Signal Total uncertainty", 0.01, 100.);
}

void DrawStandardPlots(PlotTools *pt, const std::string& flag, const std::string& x, const std::string& y, style*s, TH2*h)
{
   //gStyle->SetPadRightMargin(0.2);
   //gStyle->SetPadLeftMargin(0.2);
   //gStyle->SetTitleOffset(1.3, "xyz");
   //gStyle->SetTitleOffset(1.9, "y");
   //gStyle->SetNdivisions(505);
   gStyle->SetTitleFont(43, "xyz");
   gStyle->SetTitleSize(32, "xyz");
   c1->UseCurrentStyle();

   //Require an observed CLs limit:
   //pt->Remove("Acceptance", Compare::less,    s->MinAccZ);
   //pt->Remove("Acceptance", Compare::greater, s->MaxAccZ);
   //Fill the holes by 2D interpolation in gl-sq
   //pt->FillEmptyPointsByInterpolation(x, y);
   
   //Log z-scale
   c1->SetLogz(1);
   DrawPlot2D(pt,c1,h,flag,x,y,"Xsection",          "NLO cross section [pb]");

   //Linear z-scale
   c1->SetLogz(0);
   DrawPlot2D(pt,c1,h,flag,x,y,"Acceptance",        "Acceptance", s->MinAccZ, s->MaxAccZ, s );
   DrawPlot2D(pt,c1,h,flag,x,y,"AcceptancePercent", "Acceptance [%]", s->MinAccZ*100., s->MaxAccZ*100., s );
   DrawPlot2D(pt,c1,h,flag,x,y,"AcceptanceCorrected",    "Acceptance corr. f. sig. cont. [%]", s->MinAccZ*100., s->MaxAccZ*100., s );
   DrawPlot2D(pt,c1,h,flag,x,y,"ContaminationRelToSignal", "Signal contamination / Signal yield [%]" );

   //1D Histograms
   DrawHist1D(pt,c1,flag,x,y,"SignalStatUnc",	  "Rel. Signal Statistical uncertainty", 20);
   DrawHist1D(pt,c1,flag,x,y,"SignalSysUnc",	  "Rel. Signal Systematic uncertainty", 20);
   DrawHist1D(pt,c1,flag,x,y,"SignalPDFAccUnc",   "Rel. Signal PDF Accept. uncertainty", 20);
   DrawHist1D(pt,c1,flag,x,y,"SignalPDFXsecUnc",  "Rel. Signal PDF cross-section uncertainty", 20);
   DrawHist1D(pt,c1,flag,x,y,"SignalScaleUnc",    "Rel. Signal Scale uncertainty", 20);

   //DrawHist1D(pt,c1,flag,x,y,"ObsRmM2", "ObsR - ExpR-2sigma", 20);
   //DrawHist1D(pt,c1,flag,x,y,"ObsRmP2", "ObsR - ExpR+2sigma", 20);
   //DrawHist1D(pt,c1,flag,x,y,"ObsRdM2", "ObsR / ExpR-2sigma", 20);
   //DrawHist1D(pt,c1,flag,x,y,"ObsRdP2", "ObsR / ExpR+2sigma", 20);
}

void DrawStandardLimitPlots(PlotTools *pt, const std::string& flag, const std::string& x, const std::string& y, style*s, TH2*h)
{
   c1->UseCurrentStyle();

   //Require an observed CLs limit:
//   pt->Remove("ObsXsecLimit", Compare::less, s->MinXsecZ);
   //Fill possible holes by 2D interpolation in gl-sq
//   pt->FillEmptyPointsByInterpolation(x, y);
   
   
   //Log z-scale
   c1->SetLogz(1);
   //DrawPlot2D(pt,c1,h,flag+"_FixedBinning",x,y,"ObsXsecLimit",      "Observed cross section limit [pb]",0.001,0.02);
   DrawPlot2D(pt,c1,h,flag,x,y,"R_firstguess",      "R (first guess)", s->MinXsecZ, s->MaxXsecZ, s );
   DrawPlot2D(pt,c1,h,flag,x,y,"ObsXsecLimit",      "95% CL cross section upper limit [pb]", s->MinXsecZ, s->MaxXsecZ, s );
   DrawPlot2D(pt,c1,h,flag,x,y,"ExpXsecLimit",      "Expected cross section limit [pb]", s->MinXsecZ, s->MaxXsecZ, s);
   //DrawPlot2D(pt,c1,h,flag,x,y,"ObsNsignalLimit",   "Observed limit on number signal events");
   //DrawPlot2D(pt,c1,h,flag,x,y,"ExpNsignalLimit",   "Expected limit on number signal events");
   DrawPlot2D(pt,c1,h,flag,x,y,"ObsXsecLimitasym",  "Observed asympt. cross section limit [pb]", s->MinXsecZ, s->MaxXsecZ, s);
   DrawPlot2D(pt,c1,h,flag,x,y,"ExpXsecLimitasym",  "Expected asympt. cross section limit [pb]", s->MinXsecZ, s->MaxXsecZ, s);

   //Linear z-scale
   c1->SetLogz(1);
   //DrawPlot2D(pt,c1,h,flag,x,y,"ObsR",              "Observed R", 0.5, 2.);
   //DrawPlot2D(pt,c1,h,flag,x,y,"ExpR",              "Expected R", 0.5, 2.);
   DrawPlot2D(pt,c1,h,flag,x,y,"ObsR",              "Observed R", -999, -999, s);
   DrawPlot2D(pt,c1,h,flag,x,y,"ExpR",              "Expected R", -999, -999, s);
   //DrawPlot2D(pt,c1,h,flag,x,y,"ObsDivExp",         "Observed / Expected", 0.0, 2.);
}


void DrawStandardPlotsPerBin(PlotTools *pt, const std::string& flag, const std::string& x, const std::string& y, style*s, TH2*h)
{
   for (int bin=0; bin<nchannels; ++bin) {
      std::stringstream binlabel, binl;
      binlabel << ", bin "<<bin;
      binl     << bin;
      const std::string bl = binlabel.str();
      const std::string b  = binl.str();
      c1->SetLogz(1);
  
      DrawPlot2D(pt,c1,h,flag,x,y,"signal_"+b,          	"Signal event yield"+bl, 0.01, 100.);
      DrawPlot2D(pt,c1,h,flag,x,y,"signal_"+b+"_acceptance", 	"Acceptance [%]"+bl, 0.01, 100.);
      DrawPlot2D(pt,c1,h,flag,x,y,"signal_"+b+"_contamination", "Signal contamination [%]"+bl, 0.01, 100.);
      DrawPlot2D(pt,c1,h,flag,x,y,"signal_"+b+"_stat_UP",	"Signal Stat. UP [%]"+bl, 0.01, 100.);	
      DrawPlot2D(pt,c1,h,flag,x,y,"signal_"+b+"_stat_DN",	"Signal Stat. DN [%]"+bl, 0.01, 100.);	
      DrawPlot2D(pt,c1,h,flag,x,y,"signal_"+b+"_syst_UP",	"Signal Syst. UP [%]"+bl, 0.01, 100.);	
      DrawPlot2D(pt,c1,h,flag,x,y,"signal_"+b+"_syst_DN",	"Signal Syst. DN [%]"+bl, 0.01, 100.);	
      DrawPlot2D(pt,c1,h,flag,x,y,"signal_"+b+"_theory_UP",	"Signal Theory UP [%]"+bl, 0.01, 100.);	
      DrawPlot2D(pt,c1,h,flag,x,y,"signal_"+b+"_theory_DN",	"Signal Theory DN [%]"+bl, 0.01, 100.);	
      DrawPlot2D(pt,c1,h,flag,x,y,"signal_"+b+"_trigger_UP",	"Signal trigger UP [%]"+bl, 0.01, 100.);   
      DrawPlot2D(pt,c1,h,flag,x,y,"signal_"+b+"_trigger_DN", 	"Signal trigger DN [%]"+bl, 0.01, 100.);   

      //1D Histograms
      DrawHist1D(pt,c1,flag,x,y,"signal_"+b+"_contamination", "Signal contamination [%]"+bl, 20);
      DrawHist1D(pt,c1,flag,x,y,"signal_"+b+"_stat_UP",       "Signal Stat. UP [%]"+bl, 20);  
      DrawHist1D(pt,c1,flag,x,y,"signal_"+b+"_stat_DN",       "Signal Stat. DN [%]"+bl, 20);  
      DrawHist1D(pt,c1,flag,x,y,"signal_"+b+"_syst_UP",       "Signal Syst. UP [%]"+bl, 20);  
      DrawHist1D(pt,c1,flag,x,y,"signal_"+b+"_syst_DN",       "Signal Syst. DN [%]"+bl, 20);  
      DrawHist1D(pt,c1,flag,x,y,"signal_"+b+"_theory_UP",     "Signal Acc. PDF UP [%]"+bl, 20);       
      DrawHist1D(pt,c1,flag,x,y,"signal_"+b+"_theory_DN",     "Signal Acc. PDF DN [%]"+bl, 20);       
      DrawHist1D(pt,c1,flag,x,y,"signal_"+b+"_trigger_UP",    "Signal trigger UP [%]"+bl, 20);   
      DrawHist1D(pt,c1,flag,x,y,"signal_"+b+"_trigger_DN",    "Signal trigger DN [%]"+bl, 20);   
   }
   
}

TGraph * InOutPlot(PlotTools *PlotTool, TCanvas*canvas, std::string flag, const std::string& x, const std::string& y, const std::string& R, TH2*h, unsigned idx, int color, int style)
{
   canvas->cd();
   
   PlotTool->InOutFromR(h, x, y, R, 3);
   FillEmptyPoints(h,0.5);
   h->GetZaxis()->SetTitleOffset(1.5);
   h->SetMinimum(-0);h->SetMaximum(1.);
   std::vector<TGraph*> contours = GetContours(h, 3);
   /// :::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
   h->Draw("colz");
   int col = kBlue - 10;
   for (std::vector<TGraph*>::iterator cont = contours.begin(); cont != contours.end(); ++cont) {
   	   if (!*cont) continue;
   	   double x, y;
   	   (*cont)->GetPoint(0, x, y);
   	   (*cont)->SetLineColor(col);
   	   (*cont)->Draw("l");
   	   TLatex l;
   	   l.SetTextSize(0.04);
   	   l.SetTextColor(col++);
   	   char val[20];
   	   sprintf(val, "%d", (int) (cont - contours.begin()));
   	   l.DrawLatex(x, y, val);
   	   if (cont-contours.begin()>13) break;
   }
   //drawCmsPrel(PlotTool->SingleValue(Luminosity), METCut);
   string nameXsPlot = "results/" + flag + "_"+x+"_"+y+"_"+"InOut"+R;
   canvas->SaveAs((nameXsPlot + ".pdf").c_str());
   if (plotPNG) canvas->SaveAs((nameXsPlot + ".png").c_str());
   delete h;
   TGraph * res = (contours.size()>idx?(TGraph*)contours[idx]->Clone():0);
   if (res) {res->SetLineColor(color);
             res->SetLineStyle(style);}
   return res;
}

void DrawExclusion(PlotTools *PlotTool, std::string flag, const std::string& x, const std::string& y, 
                   TH1*hp, TH1*h,TH1*old_hp, TH1*old_h, style*s)
{
   //Require an observed CLs limit:
   //PlotTool->Remove("ObsR", Compare::less, 0.0);
   //PlotTool->FillEmptyPointsByInterpolation1D(x, y);
   
  
 
   TH2F *hs = (TH2F*)h->Clone();
   TH2F *hplot = (TH2F*)hp->Clone();
   TH2F *old_hs = (TH2F*)old_h->Clone();
   TH2F *old_hplot = (TH2F*)old_hp->Clone();
   hs->GetZaxis()->SetTitle("");

   if (s->PreExclusionPlotting) s->PreExclusionPlotting(s, PlotTool );

   //In/Out Plot
   hplot->GetZaxis()->SetTitle("Observed in/out");
   TGraph * gCLsObsExcl	  = InOutPlot(PlotTool,c1,flag,x,y,"ObsR",(TH2F*)h->Clone(), s->iCLsObsExcl, kBlue, 1);

   hplot->GetZaxis()->SetTitle("Expected in/out");
   TGraph * gCLsExpExcl   = InOutPlot(PlotTool,c1,flag,x,y,"ExpR",(TH2F*)h->Clone(), s->iCLsExpExcl, kOrange + 9, 9);

   hplot->GetZaxis()->SetTitle("Expected -1 #sigma_{experimental} in/out");
   TGraph * gCLsExpExclm1 = InOutPlot(PlotTool,c1,flag,x,y,"ExpRM1",(TH2F*)h->Clone(), s->iCLsExpExclm1, kOrange - 3, 3);

   hplot->GetZaxis()->SetTitle("Expected +1 #sigma_{experimental} in/out");
   TGraph * gCLsExpExclp1 = InOutPlot(PlotTool,c1,flag,x,y,"ExpRP1",(TH2F*)h->Clone(), s->iCLsExpExclp1, kOrange - 3, 3);

   hplot->GetZaxis()->SetTitle("Expected -2 #sigma_{experimental} in/out");
   TGraph * gCLsExpExclm2= InOutPlot(PlotTool,c1,flag,x,y,"ExpRM2",(TH2F*)h->Clone(), s->iCLsExpExclm2, kOrange - 2, 3);

   hplot->GetZaxis()->SetTitle("Expected +2 #sigma_{experimental} in/out");
   TGraph * gCLsExpExclp2 = InOutPlot(PlotTool,c1,flag,x,y,"ExpRP2",(TH2F*)h->Clone(), s->iCLsExpExclp2, kOrange - 2, 3);

   hplot->GetZaxis()->SetTitle("Observed -1 #sigma_{theory} in/out");
   TGraph * gCLsObsTheom1 = InOutPlot(PlotTool,c1,flag,x,y,"ObsRTheoM1",(TH2F*)h->Clone(), s->iCLsObsTheom1, kBlue, 3);

   hplot->GetZaxis()->SetTitle("Observed +1 #sigma_{theory} in/out");
   TGraph * gCLsObsTheop1 = InOutPlot(PlotTool,c1,flag,x,y,"ObsRTheoP1",(TH2F*)h->Clone(), s->iCLsObsTheop1, kBlue, 3);
   


   {
   //Exclusion Contours
   //gStyle->SetPadRightMargin(0.08);
   //gStyle->SetPadLeftMargin(0.2);
   //gStyle->SetTitleOffset(1.3, "xyz");
   //gStyle->SetTitleOffset(1.9, "y");
   //gStyle->SetNdivisions(505);
   //gStyle->SetTitleFont(43, "xyz");
   //gStyle->SetTitleSize(32, "xyz");
   
   //Compromise agreed on with Dongwook:
   gStyle->SetOptStat(0);
   gStyle->SetPalette(1);
   gStyle->SetPadRightMargin(0.08);
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
   c1->UseCurrentStyle();
   c1->SetLogz(0);
   c1->SetTopMargin(0.11);

   
   
   gCLsObsExcl->SetLineWidth(3);
   gCLsExpExcl->SetLineWidth(3);
   

   TGraph* gObsUnsmoothed = (TGraph*)gCLsObsExcl->Clone();
   TGraph* gObsUnsmooth = (TGraph*)gCLsObsExcl->Clone();
   TGraph* gObsUnsmoothExpExcl = (TGraph*)gCLsExpExcl->Clone();
   TGraph* gObsUnsmoothExpExclp1 = (TGraph*)gCLsExpExclp1->Clone();
   TGraph* gObsUnsmoothExpExclm1 = (TGraph*)gCLsExpExclm1->Clone();
   TGraph* gObsUnsmoothExpExclp2 = (TGraph*)gCLsExpExclp2->Clone();
   TGraph* gObsUnsmoothExpExclm2 = (TGraph*)gCLsExpExclm2->Clone();
   Smooth(gCLsObsExcl,     s->smooth_points, s->smooth_flag);
   Smooth(gCLsExpExcl,     s->smooth_points, s->smooth_flag);
   Smooth(gCLsExpExclm1,   s->smooth_points, s->smooth_flag);
   Smooth(gCLsExpExclp1,   s->smooth_points, s->smooth_flag);
   Smooth(gCLsExpExclm2,   s->smooth_points, s->smooth_flag);
   Smooth(gCLsExpExclp2,   s->smooth_points, s->smooth_flag);
   Smooth(gCLsObsTheom1,   s->smooth_points, s->smooth_flag);
   Smooth(gCLsObsTheop1,   s->smooth_points, s->smooth_flag);
   if (s->second_smooth) {
     Smooth(gCLsObsExcl,     s->second_smooth, s->smooth_flag);
     Smooth(gCLsExpExcl,     s->second_smooth, s->smooth_flag);
     Smooth(gCLsExpExclm1,   s->second_smooth, s->smooth_flag);
     Smooth(gCLsExpExclp1,   s->second_smooth, s->smooth_flag);
     Smooth(gCLsExpExclm2,   s->second_smooth, s->smooth_flag);
     Smooth(gCLsExpExclp2,   s->second_smooth, s->smooth_flag);
     Smooth(gCLsObsTheom1,   s->second_smooth, s->smooth_flag);
     Smooth(gCLsObsTheop1,   s->second_smooth, s->smooth_flag);
   }

   TGraph * gCLs1Sigma = MakeBand(gCLsExpExclm1, gCLsExpExclp1);
   gCLs1Sigma->SetFillStyle(1001);
   gCLs1Sigma->SetFillColor(kOrange - 3);
   TGraph * gCLs2Sigma = MakeBand(gCLsExpExclm2, gCLsExpExclp2);
   gCLs2Sigma->SetFillStyle(1001);
   gCLs2Sigma->SetFillColor(kOrange - 4);
   hplot->GetYaxis()->SetTitleOffset(1.9);
   hplot->GetXaxis()->SetTitleOffset(1.1);
   //Drawing the contours
   hplot->Draw("h");
   gCLs2Sigma->Draw("f");
   gCLs1Sigma->Draw("f");
   gCLsObsExcl->Draw("l");
   //~ gObsUnsmooth->Draw("l");
   gCLsExpExcl->Draw("l");
   //~ gObsUnsmoothExpExcl->Draw("l");
   //~ gObsUnsmoothExpExclp1->Draw("l");
   //~ gObsUnsmoothExpExclm1->Draw("l");
//   gCLsExpTheom1->Draw("l");
   gCLsObsTheom1->Draw("l");
//   gCLsExpTheop1->Draw("l");
   gCLsObsTheop1->Draw("l");

   //Legends
   TLegend* leg = s->leg;
   TH1F * legdummy = 0;
   leg->AddEntry(gCLsObsExcl, "Observed", "l");
   leg->AddEntry(gCLsObsTheop1, "Observed #pm1#sigma theory", "l");
   TH1F* legExp = (TH1F*)gCLs1Sigma->Clone();
   legExp->SetLineStyle(gCLsExpExcl->GetLineStyle());
   legExp->SetLineColor(gCLsExpExcl->GetLineColor());
   legExp->SetLineWidth(gCLsExpExcl->GetLineWidth());
   leg->AddEntry(legExp, "Expected #pm1#sigma exp.", "lf");
   leg->AddEntry(gCLs2Sigma, "Expected #pm2#sigma exp.", "f");
   //leg->AddEntry(gCLsExpTheop1, "Exp. limit #pm1#sigma signal theory", "l");

   if (s->PostExclusionPlotting) s->PostExclusionPlotting(s,leg);
   if (s->excluded) s->excluded->Draw();
   leg->Draw();
   s->lumi->Draw();
   s->cms->Draw();
   s->cmsprelim->Draw();

   gPad->RedrawAxis();
   string nameExcl = "results/"+ flag + "_"+x+"_"+y+"_Exclusion_";
   c1->SaveAs((nameExcl + ".pdf").c_str());
   if (plotPNG) c1->SaveAs((nameExcl + ".png").c_str());
   if (plotROOT) c1->SaveAs((nameExcl + "canvas.C").c_str());
   if (plotC  ) {
     h->GetZaxis()->SetTitle("");
     h->Draw("h");
     gCLsObsExcl->SetName("Observed limit");
     gCLsObsExcl->SetTitle("Observed limit");
     gCLsObsExcl->Draw("l");
     gCLsExpExcl->SetName("Expected limit");
     gCLsExpExcl->SetTitle("Expected limit");
     gCLsExpExcl->Draw("l");
     c1->SaveAs((nameExcl + ".C").c_str());
   }
   
   

   ///------------------------------------------------------------------------------------
   /// same, but preliminary:
   gCLs1Sigma->Draw("f");
   gCLsObsExcl->Draw("l");
   gCLsExpExcl->Draw("l");
   gCLsObsTheom1->Draw("l");
   gCLsObsTheop1->Draw("l");
   if (s->excluded) s->excluded->Draw();
   if (s->PostExclusionPlotting) s->PostExclusionPlotting(s,0);   
   leg->Draw();
   s->lumi->Draw();
   s->cmsprelim->Draw();
   gPad->RedrawAxis();
   nameExcl = "results/"+ flag + "_"+x+"_"+y+"_Exclusion_prelim";
   if (plotPrelim) c1->SaveAs((nameExcl + ".pdf").c_str());
   
    {
	   gStyle->SetOptStat(0);
	   gStyle->SetPalette(1);
	   gStyle->SetPadRightMargin(0.08);
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
	   c1->UseCurrentStyle();
	   c1->SetLogz(0);
	   c1->SetTopMargin(0.11);
	   
	   //~ TGraph*cover = new TGraph(0);
	   //~ cover->SetPoint(0, 0,  0);
	   //~ cover->SetPoint(1, 0, 1000);
	   //~ cover->SetPoint(2, 1000, 1000);
	   //~ cover->SetPoint(3, 1000,    0);
	   //~ cover->SetFillColor(kWhite);
	   //~ cover->Draw("f");
	   
	   //~ TGraph*Fixed_Edge = new TGraph(0);
		//~ Fixed_Edge->SetPoint(0, 50, 50);
		//~ Fixed_Edge->SetPoint(1, 3000, 3000);
		//~ Fixed_Edge->SetPoint(2, 50, 3000);
		//~ Fixed_Edge->SetPoint(3, 50, 50);
		//~ Fixed_Edge->SetFillColor(kGray);
		//~ Fixed_Edge->Draw("f");
	
	   //~ TGraph *Obs8TeV = new TGraph(23);
	   //~ Obs8TeV->SetName("Observed 8 TeV limit");
	   //~ Obs8TeV->SetTitle("Observed 8 TeV limit");
	   //~ Obs8TeV->SetFillColor(100);
	//~ 
	   //~ Obs8TeV->SetLineColor(1);
	   //~ Obs8TeV->SetLineWidth(3);
	   //~ Obs8TeV->SetPoint(0,343.75,100);
	   //~ Obs8TeV->SetPoint(1,343.75,112.5);
	   //~ Obs8TeV->SetPoint(2,343.75,125);
	   //~ Obs8TeV->SetPoint(3,343.6045,137.3544999);
	   //~ Obs8TeV->SetPoint(4,342.7837813,149.0337812);
	   //~ Obs8TeV->SetPoint(5,340.6937847,159.4437847);
	   //~ Obs8TeV->SetPoint(6,337.3545,168.6044999);
	   //~ Obs8TeV->SetPoint(7,333.3399966,177.0899966);
	   //~ Obs8TeV->SetPoint(8,329.0145034,185.2645034);
	   //~ Obs8TeV->SetPoint(9,324.0337812,192.7837812);
	   //~ Obs8TeV->SetPoint(10,317.7837812,199.0337812);
	   //~ Obs8TeV->SetPoint(11,310.2645034,204.0145034);
	   //~ Obs8TeV->SetPoint(12,302.0899966,208.3399966);
	   //~ Obs8TeV->SetPoint(13,293.6044999,212.3545);
	   //~ Obs8TeV->SetPoint(14,284.4437847,215.6937847);
	   //~ Obs8TeV->SetPoint(15,274.0337812,217.7837813);
	   //~ Obs8TeV->SetPoint(16,262.3544999,218.6045);
	   //~ Obs8TeV->SetPoint(17,250.1197198,218.6045);
	   //~ Obs8TeV->SetPoint(18,238.3465809,217.8095615);
	   //~ Obs8TeV->SetPoint(19,227.8055396,215.8392028);
	   //~ Obs8TeV->SetPoint(20,219.1515959,212.8960939);
	   //~ Obs8TeV->SetPoint(21,210.9088591,210.0175204);
	   //~ Obs8TeV->SetPoint(22,200,208.2979194);
	   //~ 
	   //~ TH1F *Graph_Obs8TeV = new TH1F("Graph_Obs8TeV","Observed limit",100,185.625,358.125);
	   //~ Graph_Obs8TeV->SetMinimum(88.13955);
	   //~ Graph_Obs8TeV->SetMaximum(230.4649);
	   //~ Graph_Obs8TeV->SetDirectory(0);
	   //~ Graph_Obs8TeV->SetStats(0);
	   //~ Graph_Obs8TeV->SetLineStyle(0);
	   //~ Graph_Obs8TeV->GetXaxis()->SetNdivisions(505);
	   //~ Graph_Obs8TeV->GetXaxis()->SetLabelFont(42);
	   //~ Graph_Obs8TeV->GetXaxis()->SetLabelOffset(0.007);
	   //~ Graph_Obs8TeV->GetXaxis()->SetTitleSize(32);
	   //~ Graph_Obs8TeV->GetXaxis()->SetTitleFont(43);
	   //~ Graph_Obs8TeV->GetYaxis()->SetLabelFont(42);
	   //~ Graph_Obs8TeV->GetYaxis()->SetLabelOffset(0.007);
	   //~ Graph_Obs8TeV->GetYaxis()->SetTitleSize(32);
	   //~ Graph_Obs8TeV->GetYaxis()->SetTitleOffset(1.5);
	   //~ Graph_Obs8TeV->GetYaxis()->SetTitleFont(43);
	   //~ Graph_Obs8TeV->GetZaxis()->SetLabelFont(42);
	   //~ Graph_Obs8TeV->GetZaxis()->SetLabelOffset(0.007);
	   //~ Graph_Obs8TeV->GetZaxis()->SetTitleSize(32);
	   //~ Graph_Obs8TeV->GetZaxis()->SetTitleOffset(1.2);
	   //~ Graph_Obs8TeV->GetZaxis()->SetTitleFont(43);
	   //~ Obs8TeV->SetHistogram(Graph_Obs8TeV);
	   //~ 
	   //~ Obs8TeV->Draw("l");
	   //~ 
	   //~ TGraph * Exp8TeV = new TGraph(41);
	   //~ Exp8TeV->SetName("Expected 8 TeV limit");
	   //~ Exp8TeV->SetTitle("Expected 8 TeV limit");
	   //~ Exp8TeV->SetFillColor(100);
	//~ 
	   //~ Exp8TeV->SetLineColor(kOrange + 9);
	   //~ Exp8TeV->SetLineStyle(9);
	   //~ Exp8TeV->SetLineWidth(3);
	   //~ Exp8TeV->SetPoint(0,422.3134321,100);
	   //~ Exp8TeV->SetPoint(1,425,106.9027168);
	   //~ Exp8TeV->SetPoint(2,428.1937847,115.5562153);
	   //~ Exp8TeV->SetPoint(3,430.2837813,125.9662188);
	   //~ Exp8TeV->SetPoint(4,431.1045,137.6455001);
	   //~ Exp8TeV->SetPoint(5,431.25,150);
	   //~ Exp8TeV->SetPoint(6,431.1045,162.3544999);
	   //~ Exp8TeV->SetPoint(7,430.2837813,174.0337812);
	   //~ Exp8TeV->SetPoint(8,428.1937847,184.4437847);
	   //~ Exp8TeV->SetPoint(9,425,193.75);
	   //~ Exp8TeV->SetPoint(10,421.6607153,202.9107153);
	   //~ Exp8TeV->SetPoint(11,418.75,212.5);
	   //~ Exp8TeV->SetPoint(12,415.6937847,221.9437847);
	   //~ Exp8TeV->SetPoint(13,411.5337813,230.2837812);
	   //~ Exp8TeV->SetPoint(14,406.1045,237.3545);
	   //~ Exp8TeV->SetPoint(15,400,243.75);
	   //~ Exp8TeV->SetPoint(16,393.75,250);
	   //~ Exp8TeV->SetPoint(17,387.3545,256.1045);
	   //~ Exp8TeV->SetPoint(18,380.4292813,261.6792813);
	   //~ Exp8TeV->SetPoint(19,372.7645034,266.5145034);
	   //~ Exp8TeV->SetPoint(20,364.5899966,270.8399966);
	   //~ Exp8TeV->SetPoint(21,356.1044999,274.8545);
	   //~ Exp8TeV->SetPoint(22,346.9437847,278.1937847);
	   //~ Exp8TeV->SetPoint(23,336.5337812,280.2837813);
	   //~ Exp8TeV->SetPoint(24,324.8544999,281.1302802);
	   //~ Exp8TeV->SetPoint(25,312.5,281.3954181);
	   //~ Exp8TeV->SetPoint(26,300.1197198,281.4748135);
	   //~ Exp8TeV->SetPoint(27,288.4663008,280.7041682);
	   //~ Exp8TeV->SetPoint(28,278.6521205,277.8192331);
	   //~ Exp8TeV->SetPoint(29,271.2403284,272.4595163);
	   //~ Exp8TeV->SetPoint(30,265.2476175,265.9264469);
	   //~ Exp8TeV->SetPoint(31,259.0735531,259.7523825);
	   //~ Exp8TeV->SetPoint(32,252.3949836,253.930952);
	   //~ Exp8TeV->SetPoint(33,246.069048,247.6050164);
	   //~ Exp8TeV->SetPoint(34,240.2476175,240.9264469);
	   //~ Exp8TeV->SetPoint(35,234.0735531,234.7523825);
	   //~ Exp8TeV->SetPoint(36,227.3949836,228.930952);
	   //~ Exp8TeV->SetPoint(37,221.069048,222.6050164);
	   //~ Exp8TeV->SetPoint(38,216.0159851,216.0977273);
	   //~ Exp8TeV->SetPoint(39,210.192052,211.0095194);
	   //~ Exp8TeV->SetPoint(40,200,208.4434195);
	   //~ 
	   //~ TH1F *Graph_Exp8TeV = new TH1F("Graph_Exp8TeV","Expected limit",100,176.875,454.375);
	   //~ Graph_Exp8TeV->SetMinimum(81.85252);
	   //~ Graph_Exp8TeV->SetMaximum(299.6223);
	   //~ Graph_Exp8TeV->SetDirectory(0);
	   //~ Graph_Exp8TeV->SetStats(0);
	   //~ Graph_Exp8TeV->SetLineStyle(0);
	   //~ Graph_Exp8TeV->GetXaxis()->SetNdivisions(505);
	   //~ Graph_Exp8TeV->GetXaxis()->SetLabelFont(42);
	   //~ Graph_Exp8TeV->GetXaxis()->SetLabelOffset(0.007);
	   //~ Graph_Exp8TeV->GetXaxis()->SetTitleSize(32);
	   //~ Graph_Exp8TeV->GetXaxis()->SetTitleFont(43);
	   //~ Graph_Exp8TeV->GetYaxis()->SetLabelFont(42);
	   //~ Graph_Exp8TeV->GetYaxis()->SetLabelOffset(0.007);
	   //~ Graph_Exp8TeV->GetYaxis()->SetTitleSize(32);
	   //~ Graph_Exp8TeV->GetYaxis()->SetTitleOffset(1.5);
	   //~ Graph_Exp8TeV->GetYaxis()->SetTitleFont(43);
	   //~ Graph_Exp8TeV->GetZaxis()->SetLabelFont(42);
	   //~ Graph_Exp8TeV->GetZaxis()->SetLabelOffset(0.007);
	   //~ Graph_Exp8TeV->GetZaxis()->SetTitleSize(32);
	   //~ Graph_Exp8TeV->GetZaxis()->SetTitleOffset(1.2);
	   //~ Graph_Exp8TeV->GetZaxis()->SetTitleFont(43);
	   //~ Exp8TeV->SetHistogram(Graph_Exp8TeV);
	   //~ 
	   //~ Exp8TeV->Draw("l");
	   //~ 
	   //~ TGraph * Exp13TeVDirect = new TGraph(30);
	   //~ Exp13TeVDirect->SetName("Expected limit");
	   //~ Exp13TeVDirect->SetTitle("Expected limit");
	   //~ Exp13TeVDirect->SetFillColor(100);
	//~ 
	   //~ Exp13TeVDirect->SetLineColor(kRed);
	   //~ Exp13TeVDirect->SetLineStyle(9);
	   //~ Exp13TeVDirect->SetLineWidth(3);
	   //~ Exp13TeVDirect->SetPoint(0,382.3617189,100);
	   //~ Exp13TeVDirect->SetPoint(1,384.3062154,110.9956622);
	   //~ Exp13TeVDirect->SetPoint(2,387.5,119.4027168);
	   //~ Exp13TeVDirect->SetPoint(3,390.5482846,127.9107153);
	   //~ Exp13TeVDirect->SetPoint(4,391.8175625,137.5);
	   //~ Exp13TeVDirect->SetPoint(5,390.5482846,147.0892847);
	   //~ Exp13TeVDirect->SetPoint(6,387.5,156.25);
	   //~ Exp13TeVDirect->SetPoint(7,384.1607153,165.4107153);
	   //~ Exp13TeVDirect->SetPoint(8,381.25,175);
	   //~ Exp13TeVDirect->SetPoint(9,378.1937847,184.4437847);
	   //~ Exp13TeVDirect->SetPoint(10,373.8882812,192.6382812);
	   //~ Exp13TeVDirect->SetPoint(11,367.7837812,199.0337812);
	   //~ Exp13TeVDirect->SetPoint(12,360.2645034,204.0145034);
	   //~ Exp13TeVDirect->SetPoint(13,352.0899966,208.3399966);
	   //~ Exp13TeVDirect->SetPoint(14,343.6044999,212.3545);
	   //~ Exp13TeVDirect->SetPoint(15,334.5892847,215.8392847);
	   //~ Exp13TeVDirect->SetPoint(16,325,218.75);
	   //~ Exp13TeVDirect->SetPoint(17,315.4107153,221.6607153);
	   //~ Exp13TeVDirect->SetPoint(18,306.25,225);
	   //~ Exp13TeVDirect->SetPoint(19,296.9437847,228.1937847);
	   //~ Exp13TeVDirect->SetPoint(20,286.6792813,230.1382812);
	   //~ Exp13TeVDirect->SetPoint(21,275.8207187,230.1382812);
	   //~ Exp13TeVDirect->SetPoint(22,265.5562153,228.1937847);
	   //~ Exp13TeVDirect->SetPoint(23,256.25,225);
	   //~ Exp13TeVDirect->SetPoint(24,247.0635045,221.6607153);
	   //~ Exp13TeVDirect->SetPoint(25,237.3803622,218.7757803);
	   //~ Exp13TeVDirect->SetPoint(26,227.6600395,215.9847028);
	   //~ Exp13TeVDirect->SetPoint(27,219.1515959,212.8960939);
	   //~ Exp13TeVDirect->SetPoint(28,210.9088591,210.0175204);
	   //~ Exp13TeVDirect->SetPoint(29,200,208.2979194);
	   //~ 
	   //~ TH1F *Graph_Exp13TeVDirect = new TH1F("Graph_Exp13TeVDirect","Expected limit",100,180.8182,410.9993);
	   //~ Graph_Exp13TeVDirect->SetMinimum(86.98617);
	   //~ Graph_Exp13TeVDirect->SetMaximum(243.1521);
	   //~ Graph_Exp13TeVDirect->SetDirectory(0);
	   //~ Graph_Exp13TeVDirect->SetStats(0);
	   //~ Graph_Exp13TeVDirect->SetLineStyle(0);
	   //~ Graph_Exp13TeVDirect->GetXaxis()->SetNdivisions(505);
	   //~ Graph_Exp13TeVDirect->GetXaxis()->SetLabelFont(42);
	   //~ Graph_Exp13TeVDirect->GetXaxis()->SetLabelOffset(0.007);
	   //~ Graph_Exp13TeVDirect->GetXaxis()->SetTitleSize(32);
	   //~ Graph_Exp13TeVDirect->GetXaxis()->SetTitleFont(43);
	   //~ Graph_Exp13TeVDirect->GetYaxis()->SetLabelFont(42);
	   //~ Graph_Exp13TeVDirect->GetYaxis()->SetLabelOffset(0.007);
	   //~ Graph_Exp13TeVDirect->GetYaxis()->SetTitleSize(32);
	   //~ Graph_Exp13TeVDirect->GetYaxis()->SetTitleOffset(1.5);
	   //~ Graph_Exp13TeVDirect->GetYaxis()->SetTitleFont(43);
	   //~ Graph_Exp13TeVDirect->GetZaxis()->SetLabelFont(42);
	   //~ Graph_Exp13TeVDirect->GetZaxis()->SetLabelOffset(0.007);
	   //~ Graph_Exp13TeVDirect->GetZaxis()->SetTitleSize(32);
	   //~ Graph_Exp13TeVDirect->GetZaxis()->SetTitleOffset(1.2);
	   //~ Graph_Exp13TeVDirect->GetZaxis()->SetTitleFont(43);
	   //~ Exp13TeVDirect->SetHistogram(Graph_Exp13TeVDirect);
	   //~ 
	   //~ Exp13TeVDirect->Draw("l");
	   //~ 
	   //~ TGraph * Exp13TeVEff = new TGraph(59);
	   //~ Exp13TeVEff->SetName("Expected limit");
	   //~ Exp13TeVEff->SetTitle("Expected limit");
	   //~ Exp13TeVEff->SetFillColor(100);
	//~ 
	   //~ Exp13TeVEff->SetLineColor(kBlue);
	   //~ Exp13TeVEff->SetLineStyle(9);
	   //~ Exp13TeVEff->SetLineWidth(3);
	   //~ Exp13TeVEff->SetPoint(0,519.8617189,100);
	   //~ Exp13TeVEff->SetPoint(1,521.8062154,110.9956622);
	   //~ Exp13TeVEff->SetPoint(2,525,119.4027168);
	   //~ Exp13TeVEff->SetPoint(3,528.1937847,128.0562153);
	   //~ Exp13TeVEff->SetPoint(4,530.2837813,138.4662188);
	   //~ Exp13TeVEff->SetPoint(5,530.9589999,150);
	   //~ Exp13TeVEff->SetPoint(6,530.2837813,161.5337812);
	   //~ Exp13TeVEff->SetPoint(7,528.1937847,171.9437847);
	   //~ Exp13TeVEff->SetPoint(8,525,181.25);
	   //~ Exp13TeVEff->SetPoint(9,521.6607153,190.4107153);
	   //~ Exp13TeVEff->SetPoint(10,518.75,200);
	   //~ Exp13TeVEff->SetPoint(11,515.8392847,209.5892847);
	   //~ Exp13TeVEff->SetPoint(12,512.5,218.75);
	   //~ Exp13TeVEff->SetPoint(13,509.3062154,228.0562153);
	   //~ Exp13TeVEff->SetPoint(14,507.0707187,238.3207187);
	   //~ Exp13TeVEff->SetPoint(15,505.4292813,249.1792813);
	   //~ Exp13TeVEff->SetPoint(16,503.1937847,259.4437847);
	   //~ Exp13TeVEff->SetPoint(17,499.8545,268.6044999);
	   //~ Exp13TeVEff->SetPoint(18,495.8399966,277.0899966);
	   //~ Exp13TeVEff->SetPoint(19,491.5145034,285.2645034);
	   //~ Exp13TeVEff->SetPoint(20,486.6792813,292.9292813);
	   //~ Exp13TeVEff->SetPoint(21,481.1045,299.8545);
	   //~ Exp13TeVEff->SetPoint(22,475,306.25);
	   //~ Exp13TeVEff->SetPoint(23,468.75,312.5);
	   //~ Exp13TeVEff->SetPoint(24,462.3545,318.6045);
	   //~ Exp13TeVEff->SetPoint(25,455.2837812,324.0337813);
	   //~ Exp13TeVEff->SetPoint(26,446.7982846,328.0482846);
	   //~ Exp13TeVEff->SetPoint(27,436.6792813,330.4292813);
	   //~ Exp13TeVEff->SetPoint(28,425.8207187,332.0707187);
	   //~ Exp13TeVEff->SetPoint(29,415.5562153,334.3062154);
	   //~ Exp13TeVEff->SetPoint(30,406.3955001,337.3545);
	   //~ Exp13TeVEff->SetPoint(31,397.9100034,339.7275659);
	   //~ Exp13TeVEff->SetPoint(32,389.5899966,339.7275659);
	   //~ Exp13TeVEff->SetPoint(33,381.25,337.2089999);
	   //~ Exp13TeVEff->SetPoint(34,372.9100034,333.3399966);
	   //~ Exp13TeVEff->SetPoint(35,364.5899966,329.1600034);
	   //~ Exp13TeVEff->SetPoint(36,356.1044999,325.1455001);
	   //~ Exp13TeVEff->SetPoint(37,347.0635045,321.6607153);
	   //~ Exp13TeVEff->SetPoint(38,337.3803622,318.7757803);
	   //~ Exp13TeVEff->SetPoint(39,327.6600395,315.9847028);
	   //~ Exp13TeVEff->SetPoint(40,318.5545086,312.7248135);
	   //~ Exp13TeVEff->SetPoint(41,310.1594096,308.7603835);
	   //~ Exp13TeVEff->SetPoint(42,302.5662639,303.7854519);
	   //~ Exp13TeVEff->SetPoint(43,296.069048,297.6050164);
	   //~ Exp13TeVEff->SetPoint(44,290.2476175,290.9264469);
	   //~ Exp13TeVEff->SetPoint(45,284.0735531,284.7523825);
	   //~ Exp13TeVEff->SetPoint(46,277.3949836,278.930952);
	   //~ Exp13TeVEff->SetPoint(47,271.069048,272.6050164);
	   //~ Exp13TeVEff->SetPoint(48,265.2476175,265.9264469);
	   //~ Exp13TeVEff->SetPoint(49,259.0735531,259.7523825);
	   //~ Exp13TeVEff->SetPoint(50,252.3949836,253.930952);
	   //~ Exp13TeVEff->SetPoint(51,246.069048,247.6050164);
	   //~ Exp13TeVEff->SetPoint(52,240.2476175,240.9264469);
	   //~ Exp13TeVEff->SetPoint(53,234.0735531,234.7523825);
	   //~ Exp13TeVEff->SetPoint(54,227.3949836,228.930952);
	   //~ Exp13TeVEff->SetPoint(55,221.069048,222.6050164);
	   //~ Exp13TeVEff->SetPoint(56,216.0159851,216.0977273);
	   //~ Exp13TeVEff->SetPoint(57,210.192052,211.0095194);
	   //~ Exp13TeVEff->SetPoint(58,200,208.4434195);
	   //~ 
	   //~ TH1F *Graph_Exp13TeVEff = new TH1F("Graph_Exp13TeVEff","Expected limit",100,166.9041,564.0549);
	   //~ Graph_Exp13TeVEff->SetMinimum(76.02724);
	   //~ Graph_Exp13TeVEff->SetMaximum(363.7003);
	   //~ Graph_Exp13TeVEff->SetDirectory(0);
	   //~ Graph_Exp13TeVEff->SetStats(0);
	   //~ Graph_Exp13TeVEff->SetLineStyle(0);
	   //~ Graph_Exp13TeVEff->GetXaxis()->SetNdivisions(505);
	   //~ Graph_Exp13TeVEff->GetXaxis()->SetLabelFont(42);
	   //~ Graph_Exp13TeVEff->GetXaxis()->SetLabelOffset(0.007);
	   //~ Graph_Exp13TeVEff->GetXaxis()->SetTitleSize(32);
	   //~ Graph_Exp13TeVEff->GetXaxis()->SetTitleFont(43);
	   //~ Graph_Exp13TeVEff->GetYaxis()->SetLabelFont(42);
	   //~ Graph_Exp13TeVEff->GetYaxis()->SetLabelOffset(0.007);
	   //~ Graph_Exp13TeVEff->GetYaxis()->SetTitleSize(32);
	   //~ Graph_Exp13TeVEff->GetYaxis()->SetTitleOffset(1.5);
	   //~ Graph_Exp13TeVEff->GetYaxis()->SetTitleFont(43);
	   //~ Graph_Exp13TeVEff->GetZaxis()->SetLabelFont(42);
	   //~ Graph_Exp13TeVEff->GetZaxis()->SetLabelOffset(0.007);
	   //~ Graph_Exp13TeVEff->GetZaxis()->SetTitleSize(32);
	   //~ Graph_Exp13TeVEff->GetZaxis()->SetTitleOffset(1.2);
	   //~ Graph_Exp13TeVEff->GetZaxis()->SetTitleFont(43);
	   //~ Exp13TeVEff->SetHistogram(Graph_Exp13TeVEff);
	   //~ 
	   //~ Exp13TeVEff->Draw("l");
	   //~ 
	   //~ TLegend* legSMS = s->leg;
	   //~ std::string header = legSMS->GetHeader();
	   //~ legSMS->Clear();
	   //~ legSMS->SetHeader(header.c_str());
	   //~ legSMS->AddEntry(Obs8TeV,   "Obs. 8 TeV", "l");
	   //~ legSMS->AddEntry(Exp8TeV,   "Exp. 8 TeV", "l");
	   //~ legSMS->AddEntry(Exp13TeVDirect,   "Exp. 13 TeV, SF BG from MC ", "l");
	   //~ legSMS->AddEntry(Exp13TeVEff,   "Exp. 13 TeV, Extrapolation Meth.", "l");
	   //~ legSMS->Draw();
	   //~ s->lumiTemperaturePlot->Draw();
	   //~ s->cms->Draw();
	   //~ s->cmsprelim->Draw();
	   //~ gPad->RedrawAxis();
	   //~ string nameExcl = "results/8_and_13TeV_Exclusion_Limits";
	   //~ c1->SaveAs((nameExcl + ".pdf").c_str());
   }


   ///------------------------------------------------------------------------------------
   /// Exclusion plot SMS style with x-sect limit
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
   c1->UseCurrentStyle();
   c1->SetLogz(1);
   

   TH2F *plot2D = (TH2F*)old_hp->Clone();
   plot2D->GetZaxis()->SetTitle("95% CL cross section upper limit [pb]");
   PlotTool->Area(plot2D, x, y, "ObsXsecLimit");
   plot2D->GetZaxis()->SetTitleOffset(1.5);
   if (s->MinXsecZ!=-999) plot2D->SetMinimum(s->MinXsecZ);
   if (s->MaxXsecZ!=-999) plot2D->SetMaximum(s->MaxXsecZ);
   if (s->MinXsecZ==-999&&s->MaxXsecZ==-999) SetZRange(plot2D);
   if (s&&s->SetMoreLogLabels) {
     plot2D->GetZaxis()->SetMoreLogLabels();
     plot2D->GetZaxis()->SetLabelSize(0.035);
     plot2D->GetZaxis()->SetTitleOffset(2.1);
     c1->SetRightMargin(0.22);  
     c1->SetLeftMargin(0.15);  
   }  
   plot2D->Draw("colz"); 
   gCLsObsExcl->SetLineWidth(3);
   gCLsObsExcl->SetLineColor(kBlack);
   gCLsObsTheom1->SetLineColor(kBlack);
   gCLsObsTheop1->SetLineColor(kBlack);
   gCLsObsTheom1->SetLineStyle(3);
   gCLsObsTheop1->SetLineStyle(3);
   gCLsObsTheom1->SetLineWidth(2);
   gCLsObsTheop1->SetLineWidth(2);
   gCLsExpExclm1->SetLineWidth(2);
   gCLsExpExclp1->SetLineWidth(2);
   gCLsExpExclm2->SetLineWidth(2);
   gCLsExpExclp2->SetLineWidth(2);
   gCLsExpExcl->SetLineWidth(3);
   gCLsExpExcl->SetLineStyle(9);
   gCLsExpExcl->SetLineColor(kOrange + 9);
   gCLsExpExclm1->SetLineColor(kOrange + 9);
   gCLsExpExclp1->SetLineColor(kOrange + 9);
   gCLsExpExclm2->SetLineColor(kOrange + 8);
   gCLsExpExclp2->SetLineColor(kOrange + 8);
   gCLsExpExclm1->Draw("l");
   gCLsExpExclp1->Draw("l");
   gCLsExpExclm2->Draw("l");
   gCLsExpExclp2->Draw("l");
   gCLsObsExcl->Draw("l");
   gCLsExpExcl->Draw("l");
   gCLsObsTheom1->Draw("l");
   gCLsObsTheop1->Draw("l");
   if (s->excluded) s->excluded->Draw();
   TLegend* legSMS = s->legTemperaturePlot;
   std::string header = legSMS->GetHeader();
   legSMS->Clear();
   legSMS->SetHeader(header.c_str());
   legSMS->AddEntry(gCLsObsExcl,   "Observed", "l");
   legSMS->AddEntry(gCLsObsTheop1, "Observed #pm1#sigma theory", "l");
   legSMS->AddEntry(gCLsExpExcl,   "Expected", "l");
   legSMS->AddEntry(gCLsExpExclm1, "Expected #pm1#sigma exp.", "l");
   legSMS->AddEntry(gCLsExpExclm2, "Expected #pm2#sigma exp.", "l");
   if (s->PostExclusionPlotting)  s->PostExclusionPlotting(s,legSMS);   
   legSMS->Draw();
   s->lumiTemperaturePlot->Draw();
   s->cmsTemperaturePlot->Draw();
   //~ s->cmsprelimTemperaturePlot->Draw();
   gPad->RedrawAxis();
   nameExcl = "results/"+ flag + "_"+x+"_"+y+"_Exclusion_witXsecLimit";
   c1->SaveAs((nameExcl + ".pdf").c_str());
   }
   
 
   
}





void GetPlotTools(PlotTools*& plotTools, std::string filename, const std::string& x, const std::string& y, std::string GeneratorFile, unsigned factor)
{
  if (!c1) c1 = new TCanvas("c_squ", "c_squ", 900, 800);
  c1->cd();
 
  Events * events = new Events();
  ReadEvents(*events, filename);
  
  //plotting helper functions
  plotTools = new PlotTools(events);

  //Require an observed CLs limit:
  plotTools->Remove("ObsR", Compare::less, 0.00001);
  plotTools->Remove("Xsection", Compare::less, 0.0);

  //Fill the holes by 2D interpolation in gl-sq
  plotTools->FillEmptyPointsByInterpolation(x, y);
  plotTools->FillEmptyPointsByInterpolation(x, y);

  //Make grid in Mzero, Mhalf finer by factors of 2 by linear interpolation
  for (int i=2; i<=factor; i*=2)
    plotTools->ExpandGrid(x, y);
  // New 'pseudo' points are added, therefore the binning of all plots has to be made finer by a factor
  // of 2 in x and y for each "ExpandGrid
  
  //Add generator information of particles masses if a file is given
  if (GeneratorFile!="") {
    std::vector<GeneratorMasses> GenMasses;
    ReadGeneratorMasses(GenMasses, GeneratorFile);
    Match( GenMasses, *events);
  }  
} 

