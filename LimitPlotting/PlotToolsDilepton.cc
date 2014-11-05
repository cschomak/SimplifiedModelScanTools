// $Id: PlotTools.cc,v 1.8 2012/06/26 13:58:23 auterman Exp $

/*** ------------------------------------------------------------------------------------------------------- ***
     TheBetterPlotScript, a tool to plot final results, limits and exclusion contours, based on 'PlotScript'

     Christian Autermann, Hamburg University/LPC, February 2012
 *** ------------------------------------------------------------------------------------------------------- ***/

#include "PlotTools.h"
#include "GeneratorMasses.h"

#include <cmath>
#include <algorithm>
#include <iostream>
#include <cassert>
#include <sstream>

#include "TGraph.h"
#include "TF1.h"
#include "TH2.h"
#include "TH2F.h"
#include "TObjArray.h"
#include "TPad.h"
#include "TCanvas.h"
#include "TRint.h"
#include "TROOT.h"
#include "TLatex.h"
#include "TFile.h"
#include "TStyle.h"
#include "table.h"

PlotTools * PlotTools::Clone()
{
  PlotTools * r = new PlotTools();
  for (Events::iterator it = scan_->begin(); it != scan_->end(); ++it) 
    r->addEvents( it->Clone() );
  r->Set_N_Channels(N_Channels());  
  return r;
}


void PlotTools::Area(TH2*h, const std::string& x, const std::string& y, const std::string& f) 
{
   Fill X(x);
   Fill Y(y);
   Fill F(f);
   for (Events::const_iterator it = scan_->begin(); it != scan_->end(); ++it) {
      double nr = it->Get("number");
      if ( Overview && (nr-(int)nr)==0) { 
        //std::cout << nr << ",  "<<f<< ",  "<<F(*it) << "; str="<<ToString<double>(F(*it)) <<std::endl;
        Overview->Add( nr, f, ToString(F(*it)) );
      }
      
      h->SetBinContent(h->GetXaxis()->FindBin(X(*it)), h->GetYaxis()->FindBin(Y(*it)), F(*it));
      //if (x=="chi1"&&y=="gluino"&&f=="Acceptance")
      //std::cout<<x<<"="<<X(*it)<<", "<<y<<"="<<Y(*it)<<", "<<f<<"="<<F(*it)<<std::endl;
   }
}

void PlotTools::Print(const std::string& var1, const Compare::comparator co1, double value1, const std::string& var2, const Compare::comparator co2, double value2)
{
   bool use2 = (var2!="");
   Compare Match1(var1,co1,value1);
   Compare Match2(var2,co2,value2);
   
   for (Events::const_iterator it = scan_->begin(); it != scan_->end(); ++it) {
	if (Match1(*it) && (!use2 || Match2(*it)))
	  std::cout << "neutr: "<<it->Get("neutralino2")<<", sb: "<<it->Get("sbottom")<<", ExpR: "<<it->Get("ExpR")
	            <<std::endl;
   }	
}


void PlotTools::InOutFromR(TH2*h, const std::string& x, const std::string& y, const std::string& f, int param) {
  TH2F*d=(TH2F*)h->Clone();
  Area(d,x,y,f);
  Smooth(d,param);
  for (int x = 0; x <= h->GetXaxis()->GetNbins(); ++x){
    for (int y = 0; y <= h->GetYaxis()->GetNbins(); ++y){
      double r=d->GetBinContent(x,y);
      if (r>0)
      h->SetBinContent(x,y,(r > 1.0 ? 1 : 0.01)); 
      //std::cout<<x<<", "<<y<<"; "<<r<<std::endl; 
    }
  }
  delete d;
}

void PlotTools::InOut(TH2*h, const std::string& x, const std::string& y, const std::string& f, const Compare::comparator op, const double value)
{
   Fill    X(x);
   Fill    Y(y);
   Compare F(f,op,value);
   for (Events::const_iterator it = scan_->begin(); it != scan_->end(); ++it) {
      h->SetBinContent(h->GetXaxis()->FindBin(X(*it)), h->GetYaxis()->FindBin(Y(*it)), F(*it));
   }
}

void PlotTools::Remove(const std::string& var, const Compare::comparator co, double value){
  Compare compare(var, co, value);
  int s=scan_->size();
  scan_->erase( std::remove_if(scan_->begin(),scan_->end(),compare), scan_->end());
  
  std::cout << "...removed " << s-scan_->size() << " cMSSM points, for which '"<<var<<"' "
            <<(co==Compare::greater?"> ":"< ")
            << value << std::endl;;
}


void PlotTools::Hist(TH1*h, const std::string& f) {
   Fill F(f);
   for (Events::const_iterator it = scan_->begin(); it != scan_->end(); ++it) 
     h->Fill(F(*it));
}

void PlotTools::VectorOf(std::vector<double>& v, const std::string& f) {
   Fill F(f);
   for (Events::const_iterator it = scan_->begin(); it != scan_->end(); ++it) 
     v.push_back(F(*it));
}

void PlotTools::FillEmptyPointsByInterpolation1D(const std::string& x, const std::string& y)
{
  std::cout << "...Fill Empty Points By Interpolation in x = '" <<x<<"'"<<std::flush;
  Fill X(x);
  Fill Y(y);
  
  Events newpoints;
  //first find out where to expect points
  //std::cout<< "start: TheLimits::FillEmptyPointsByInterpolation()" <<std::endl;
  double gridy=9999, miny=9999, maxy=0, gridx=9999, minx=9999, maxx=0;
  for (Events::const_iterator it=scan_->begin(); it!=scan_->end(); ++it){
    if (X(*it)<minx) minx=X(*it);
    if (X(*it)>maxx) maxx=X(*it);
    if (Y(*it)<miny) miny=Y(*it);
    if (Y(*it)>maxy) maxy=Y(*it);
    for (Events::const_iterator zt=it; zt!=scan_->end(); ++zt){
      if (X(*it)==X(*zt) ) continue;
      if ( fabs(X(*it) - X(*zt)) < gridx && 
           Y(*it)==Y(*zt)) gridx = fabs(X(*it) - X(*zt));
      if ( fabs(Y(*it) - Y(*zt) && 
           X(*it)==X(*zt)) < gridy ) gridy = fabs(Y(*it) - Y(*zt));
    }
  } 
  //Now, interpolate
  //std::cout<<minx<<"  "<<maxx<<"  "<<gridx<<"  "<<miny<<"  "<<maxy<<"  "<<gridy<<"  "<<std::endl;
  gridx=20;gridy=20;
  for (Events::const_iterator it=scan_->begin(); it!=scan_->end(); ++it){
     //find next right neighbor in x for it:
    //if (!(*it)) continue;
    Events::const_iterator nextx=scan_->end(), nexty=scan_->end();
    double dx=9999, dy=9999; 
    for (Events::const_iterator zt=scan_->begin(); zt!=scan_->end(); ++zt){
      //if (!(*zt)) continue;
      if (fabs(X(*it)-X(*zt))<0.9 || fabs(Y(*it)-Y(*zt))>0.9 ) continue;
      if ( fabs(X(*it) - X(*zt)) < dx && X(*it) < X(*zt)) {
        dx = fabs(X(*it) - X(*zt));
	nextx = zt;
      }	
      if (dx==gridx) break;	
    }
    //interpolate in x:
    if (dx!=gridx && nextx!=scan_->end()){
        //std::cout << "m0 = " <<X(*it)  << ", m12="<< Y(*it) << std::endl;
       double dist = X(*nextx) - X(*it);
       for (double r=gridx; r<dist; r+=gridx ){
         //std::cout <<X(*it)<<"/"<<Y(*it) <<"->"
	 //          <<  X(*it)*r/dist + (x(*nextx) * (1.-r/dist)) << "<- "<<x(*nextx) 
	 //          <<"/"<< y(*nextx)<<std::endl;
	 newpoints.push_back( Event( ( (*it * (r/dist)) + (*nextx * (1.-r/dist)) )));
       }	 
    }	

  }
  scan_->insert(scan_->end(), newpoints.begin(), newpoints.end());
  std::cout<< ": added " <<newpoints.size() <<" new points."<<std::endl;
}




TH2 * PlotTools::GetHist(const std::string& x, const std::string& y)
{
  Fill X(x);
  Fill Y(y);
  double gridy=9999, miny=9999, maxy=0, gridx=9999, minx=9999, maxx=0;
  for (Events::const_iterator it=scan_->begin(); it!=scan_->end(); ++it){
    if (X(*it)<minx) minx=X(*it);
    if (X(*it)>maxx) maxx=X(*it);
    if (Y(*it)<miny) miny=Y(*it);
    if (Y(*it)>maxy) maxy=Y(*it);
    for (Events::const_iterator zt=it; zt!=scan_->end(); ++zt){
      if ( fabs(X(*it) - X(*zt)) < gridx && fabs(Y(*it)-Y(*zt))<0.9 && fabs(X(*it)-X(*zt))>0.9 ) 
        gridx = fabs(X(*it) - X(*zt));
      if ( fabs(Y(*it) - Y(*zt)) < gridy && fabs(X(*it)-X(*zt))<0.9 && fabs(Y(*it)-Y(*zt))>0.9 ) 
        gridy = fabs(Y(*it) - Y(*zt));
    }
  } 
  int binsx=(maxx-minx)/gridx;
  int binsy=(maxy-miny)/gridy;
  std::string titel = ";"+GetInfo(x)->GetLabel()+";"+GetInfo(y)->GetLabel();
  std::stringstream name;
  name << ++plotindex_ << "_" << GetInfo(x)->GetLabel()<<"_"<<GetInfo(y)->GetLabel();
  TH2F*h = new TH2F(name.str().c_str(),titel.c_str(),binsx+1,minx-gridx/2.,maxx+gridx/2,binsy+1,miny-gridy/2,maxy+gridy/2.);
  std::cout<<"...using binning "<<binsx+1<<", "<<minx-gridx/2.<<", "<<maxx+gridx/2.<<", "<<binsy+1<<", "<<miny-gridy/2.<<", "<<maxy+gridy/2.<<std::endl;
  return h;
}

Events::const_iterator FindPoint(const std::string& x,double ix, const std::string& y,double iy,double prec,Events *scan) 
{
  Fill X(x);
  Fill Y(y);
  for (Events::const_iterator it=scan->begin(); it!=scan->end(); ++it)
    if (fabs(X(*it)-ix)<prec && fabs(Y(*it)-iy)<prec) return it;
  return scan->end();
}

void PlotTools::FillEmptyPointsByInterpolation(const std::string& x, const std::string& y)
{
  std::cout << "...Fill Empty Points By 2D linear Interpolation in x = '" <<x<<"' and y = '"<<y<<"'"<<std::endl;
  Fill X(x);
  Fill Y(y);
  
  Events newpoints;
  //first find out where to expect points
  //std::cout<< "start: TheLimits::FillEmptyPointsByInterpolation()" <<std::endl;

  double gridy=9999, miny=9999, maxy=0, gridx=9999, minx=9999, maxx=0;
  for (Events::const_iterator it=scan_->begin(); it!=scan_->end(); ++it){
    if (X(*it)<minx) minx=X(*it);
    if (X(*it)>maxx) maxx=X(*it);
    if (Y(*it)<miny) miny=Y(*it);
    if (Y(*it)>maxy) maxy=Y(*it);
    for (Events::const_iterator zt=it; zt!=scan_->end(); ++zt){
      if ( fabs(X(*it) - X(*zt)) < gridx && fabs(Y(*it)-Y(*zt))<0.9 && fabs(X(*it)-X(*zt))>0.9 ) 
        gridx = fabs(X(*it) - X(*zt));
      if ( fabs(Y(*it) - Y(*zt)) < gridy && fabs(X(*it)-X(*zt))<0.9 && fabs(Y(*it)-Y(*zt))>0.9 ) 
        gridy = fabs(Y(*it) - Y(*zt));
    }
  } 
  //Now, interpolate
  std::cout<<"   --X-binning:: "<<minx<<" to "<<maxx<<", in "<<gridx
           << "; --Y-binning:: "<<miny<<" to "<<maxy<<", in "<<gridy<<"  "<<std::endl;

  //double gridx=20, gridy=20;
  for (Events::const_iterator it=scan_->begin(); it!=scan_->end(); ++it){
    //find next right neighbor in x for it:
    Events::const_iterator nextx=scan_->end();
    double dx=9999; 
    for (Events::const_iterator zt=scan_->begin(); zt!=scan_->end(); ++zt){
      if (fabs(X(*it)-X(*zt))<0.9 || fabs(Y(*it)-Y(*zt))>0.9 ) continue;
      if ( fabs(X(*it) - X(*zt)) < dx && X(*it) < X(*zt)) {
        dx = fabs(X(*it) - X(*zt));
	nextx = zt;
      }	
      if (dx==gridx) break;	
    }
    //interpolate in x:
    if (dx!=gridx && nextx!=scan_->end()){
        //std::cout << "m0 = " <<X(*it)  << ", m12="<< Y(*it) << std::endl;
       double distx = X(*nextx) - X(*it);
       for (double r=gridx; r<distx; r+=gridx ){
         Events::const_iterator miny=scan_->end(), maxy=scan_->end();
         //find upper and lower neighbors in 'y' for nextx
	 double current_x=X(*it)+r, dmin=9999, dmax=9999;
	 for (Events::const_iterator zt=scan_->begin(); zt!=scan_->end(); ++zt){
	   if (fabs(current_x-X(*zt))>0.9) continue;
	   if ( fabs(Y(*it) - Y(*zt)) < dmin && Y(*it) > Y(*zt)) {
	     dmin = fabs(Y(*it) - Y(*zt));
	     miny = zt;
	   }	
	   if ( fabs(Y(*it) - Y(*zt)) < dmax && Y(*it) < Y(*zt)) {
	     dmax = fabs(Y(*it) - Y(*zt));
	     maxy = zt;
	   }	
	   if (dmin==gridy && dmax==gridy) break;	
	 }
	 double disty=dmin+dmax;
	 double bias_xy=1;
	 double totdist = distx+disty*bias_xy;
	 if (miny!=scan_->end() && maxy!=scan_->end() && nextx!=scan_->end()) {
	         newpoints.push_back( Event( ( 
		                       (*it   * ((1.-r   /distx) * disty*bias_xy/totdist)) + (*nextx * ((r/distx) * disty*bias_xy/totdist)) +
	                               (*miny * (dmax/disty * distx/totdist)) + (*maxy  * ((dmin/disty) * distx/totdist))
	                           ) ) );
	   //std::cout <<"added point >> "<<X(newpoints.back())<<"/"<<Y(newpoints.back())<<std::endl;
	 	 
	   
	 }			   
         else if (nextx!=scan_->end())			 
	         newpoints.push_back( Event( ( (*it * (1.-r/distx)) + (*nextx * (r/distx)) )));

         else if (miny!=scan_->end() && maxy!=scan_->end())			 
	         newpoints.push_back( Event( ( (*miny * (dmax/disty)) + (*maxy  * ((dmin/disty))) )));
//	 std::cout<<std::endl;
//	 std::cout<<std::endl;
       }	 
    }	

  }
  scan_->insert(scan_->end(), newpoints.begin(), newpoints.end());
  std::cout<< ": added " <<newpoints.size() <<" new points."<<std::endl;
}

void PlotTools::ExpandGrid(const std::string& x, const std::string& y )
{
  std::cout << "...Expand Grid By Interpolation in x = '" <<x<<"' and y ='"<<y<<"' by factor 2"<<std::endl;
  Fill X(x);
  Fill Y(y);

  Events new_grid;
  for (Events::iterator it=scan_->begin(); it!=scan_->end(); ++it){
    double dx=9999, dy=9999;
    Events::iterator next_x=scan_->end(), next_y=scan_->end();
    //x
    for (Events::iterator nx=scan_->begin(); nx!=scan_->end(); ++nx)
      if ( X(*it) < X(*nx) && fabs( X(*it)-X(*nx))<dx && Y(*it) == Y(*nx)) {
        dx=fabs(X(*it)-X(*nx));
	next_x=nx;
      }
    //y  
    for (Events::iterator ny=scan_->begin(); ny!=scan_->end(); ++ny)
      if ( Y(*it) < Y(*ny) && fabs( Y(*it) - Y(*ny))<dy && X(*it) == X(*ny)) {
        dy=fabs(Y(*it)-Y(*ny) );
	next_y=ny;
      }
    if (next_y!=scan_->end()) {  
	Event  ny((*it + *next_y) * 0.5);
	new_grid.push_back( ny );

//	std::cout
//	<< "l<>x:"<<x(*it)<< ",y:"<<y(*it)<<", sigma"<<(*it)->NLOXsection
//	<< " <>x:"<<x(ny) << ",y:"<<y(ny)<<", sigma="<<ny->NLOXsection
//	<< " r<>x:"<<x(*next_y)<< ",y:"<<y(*next_y)<<", sigma="<<(*next_y)->NLOXsection
//	<<std::endl;
	
    }
    if (next_x!=scan_->end()) {  
	Event  nx((*it + *next_x) * 0.5);
	new_grid.push_back( nx );
    }
    if (next_x!=scan_->end() && next_y!=scan_->end()) {  
	Event  nxy((*next_x + *next_y) * 0.5);
	new_grid.push_back( nxy );
    }  
      
  } 
  scan_->insert(scan_->end(), new_grid.begin(), new_grid.end());
}


std::vector<TGraph*> GetContours(TH2*h, int ncont) {
	if (!h)
		return std::vector<TGraph*>();
	TH2 * plot = (TH2*) h->Clone();
	FillEmptyPoints(plot);
	plot->SetContour(ncont);
	plot->SetFillColor(1);
	plot->Draw("CONT Z List");
	gPad->Update();
	TObjArray *contours = (TObjArray*) gROOT->GetListOfSpecials()->FindObject("contours");
	if (!contours) {
		std::cerr << "ERROR: Found no contours! Is the histogram empty?" << std::endl;
		return std::vector<TGraph*>();
	}
	int ncontours = contours->GetSize();
	std::vector<TGraph*> result;
	for (int i = 0; i < ncontours; ++i) {
		TList *list = (TList*) contours->At(i);
		TGraph* curv = (TGraph*) list->First();
		if (curv)
			result.push_back(curv);
		for (int j = 0; j < list->GetSize(); j++) {
			curv = (TGraph*) list->After(curv); // Get Next graph
			if (curv)
				result.push_back(curv);
		}
	}
	delete plot;
	std::sort(result.begin(), result.end(), sort_TGraph());
	return result;
}

TGraph * PlotTools::GetContour(TH2*h, int ncont, int flag) {
	std::vector<TGraph*> gs = GetContours(h, ncont);
	//assert(gs.size()>flag && "ERROR: Requested a non-existing contour index! Check with ExclusionTestContours first!");
	return (gs.size() > flag ? (TGraph*) gs[flag]->Clone() : new TGraph(0));
}



TGraph * PlotTools::GetContour(TH2*h, const std::string& x, const std::string& y, const std::string& func, 
                    int ncont, int flag, int color, int style, TH2*o) {
	InOutFromR(h, x, y, func, 3);
        FillEmptyPoints(h,0.5);
	if (o) h = BinWiseOr(h,o);
	TGraph * graph = GetContour(h, ncont, flag);
	graph->SetLineColor(color);
	graph->SetLineStyle(style);
	graph->SetName(func.c_str());
	graph->SetTitle(func.c_str());
	return graph;
}

/*
void PlotTools::Print(double(*f)(const T*), double(*x)(const T*), double(*y)(const T*),
	TGraph*g, double p) {
	for (typename std::vector<T*>::const_iterator it = scan_->begin(); it != scan_->end(); ++it) {
		for (int j = 0; j < g->GetN(); ++j) {
			double gx, gy;
			g->GetPoint(j, gx, gy);
			if ((x(*it) - gx) * (x(*it) - gx) + (y(*it) - gy) * (y(*it) - gy) < p * p)
				std::cout << x(*it) << ", " << y(*it) << " :: " << f(*it) << std::endl;
		}
	}

}

void PlotTools::Print(double(*f)(const T*), double(*x1)(const T*), double(*x2)(const T*),
	double(*x3)(const T*), double(*x4)(const T*), TGraph*g, double p) {
	for (typename std::vector<T*>::const_iterator it = scan_->begin(); it != scan_->end(); ++it) {
		for (int j = 0; j < g->GetN(); ++j) {
			double gx, gy;
			g->GetPoint(j, gx, gy);
			if ((x1(*it) - gx) * (x1(*it) - gx) + (x2(*it) - gy) * (x2(*it) - gy) < p * p)
				std::cout << x1(*it) << ", " << x2(*it) << ", " << x3(*it) << ", " << x4(*it)
					<< " :: " << f(*it) << std::endl;
		}
	}

}
*/

TH2 * BinWiseOr(TH2*h1, TH2*h2) {
	TH2 * res = (TH2*) h1->Clone();
	for (int x = 0; x <= res->GetXaxis()->GetNbins(); ++x)
		for (int y = 0; y <= res->GetYaxis()->GetNbins(); ++y)
			if (h2->GetBinContent(x, y) > h1->GetBinContent(x, y))
				res->SetBinContent(x, y, h2->GetBinContent(x, y));
	return res;
}



bool sort_TGraph::operator()(const TGraph*g1, const TGraph*g2) {
	return g1->GetN() > g2->GetN();
}

TGraph * MakeBand(TGraph *g1, TGraph *g2, bool b) {
	//std::cout<<"MAKE BAND!"<<b<<std::endl;
	TGraph * res = new TGraph(g1->GetN() + g2->GetN() + 1);
	int p = 0;
	double firstx, firsty;
	for (int i = 0; i < g1->GetN(); ++i) {
		double x, y;
		g1->GetPoint(i, x, y);
		res->SetPoint(p++, x, y);
		if (i == 0) {
			firstx = x;
			firsty = y;
		}
	}
	for (int i = g2->GetN() - 1; i >= 0; --i) {
		double x, y;
		g2->GetPoint(i, x, y);
		res->SetPoint(p++, x, y);
	}
	res->SetPoint(p++, firstx, firsty);
	if (res->GetN() == 0)
		return res;
	res->SetLineColor(g2->GetLineColor());
	res->SetFillColor(g2->GetLineColor());
	res->SetFillStyle(1001);
	return res;
}

//~ void drawCmsPrel(double intLumi) {
	//~ TLatex* lat = new TLatex(0.46, 0.84, "CMS");
	//~ lat->SetNDC(true);
	//~ lat->SetTextSize(0.04);
	//~ lat->Draw("same");
//~ 
	//~ TLatex* lat2 = new TLatex(0.46, 0.77, Form("#sqrt{s} = 7 TeV,  #int#it{L}dt = %.2ffb^{-1}",
												//~ intLumi/1000.));
	//~ lat2->SetNDC(true);
	//~ lat2->SetTextSize(0.04);
	//~ lat2->Draw("same");
//~ }

void Smooth(TH2 * h, int N) {
	TH2F * old = (TH2F*) h->Clone();

	double gauss[N];
	double sigma = (double) N / 4.;
	double sum = 0;
	double lim = (double) N / 2.;
	TF1 *fb = new TF1("fb", "gaus(0)", -lim, lim);
	fb->SetParameter(0, 1. / (sqrt(2 * 3.1415) * sigma));
	fb->SetParameter(1, 0);
	fb->SetParameter(2, sigma);
	for (int i = 0; i < N; ++i) {
		gauss[i] = fb->Integral(-lim + i, -lim + i + 1);
		sum += gauss[i];
	}
	for (int i = 0; i < N; ++i)
		gauss[i] /= sum;

	for (int x = 0; x < h->GetXaxis()->GetNbins(); ++x) {
		for (int y = 0; y < h->GetYaxis()->GetNbins(); ++y) {
		double av=0, norm=0;
		int xpoints = 0;
		for (int jx = x - N / 2; jx <= x + N / 2; ++jx) {
		int ypoints = 0;
		for (int jy = y - N / 2; jy <= y + N / 2; ++jy) {
		   if (jx>=0 && jy>=0 && old->GetBinContent( (jx<0?0:jx), (jy<0?0:jy) )>0) {
		   double g = sqrt( pow(gauss[ypoints],2) +  pow(gauss[ypoints],2));
		   norm += g;
		   av += g * old->GetBinContent( jx, jy );
		   }	 
		}}
                if (h->GetBinContent(x, y)>0)
		h->SetBinContent(x, y, av/norm);
	}}
	delete old;
}

void Smooth(TGraph * g, int N, int flag) {
	TGraph * old = (TGraph*) g->Clone();
	//int N = (n%2==0?n+1:n);
	if (N > 2 * g->GetN())
		N = 2 * g->GetN() - 1;

	double gauss[N];
	double sigma = (double) N / 4.;
	double sum = 0;
	double lim = (double) N / 2.;
	TF1 *fb = new TF1("fb", "gaus(0)", -lim, lim);
	fb->SetParameter(0, 1. / (sqrt(2 * 3.1415) * sigma));
	fb->SetParameter(1, 0);
	fb->SetParameter(2, sigma);
	for (int i = 0; i < N; ++i) {
		gauss[i] = fb->Integral(-lim + i, -lim + i + 1);
		sum += gauss[i];
	}
	for (int i = 0; i < N; ++i)
		gauss[i] /= sum;

	for (int i = 0; i < g->GetN(); ++i) {
		double avy = 0., avx = 0., x, x0, y, y0;
		int points = 0;
		for (int j = i - N / 2; j <= i + N / 2; ++j) {
			if (j < 0) {
				old->GetPoint(0, x, y);
		        }		
			else if (j >= g->GetN()) {
				old->GetPoint(old->GetN() - 1, x, y);
			}	
			else 
			  old->GetPoint(j, x, y);
			avy += y * gauss[points];
			avx += x * gauss[points];
			
			if (i == j) {
				x0 = x;
				y0 = y;
			}	
			++points;
		}
		if      ((flag==1 && i - N / 2 < 0 ) || (flag==2 && i + N / 2 >= g->GetN()))
			g->SetPoint(i, x0, avy);
		else if ((flag==1 && i + N / 2 >= g->GetN()) || (flag==2 && i - N / 2 < 0 ))
			g->SetPoint(i, avx, y0);
		else
			g->SetPoint(i, avx, avy);
	}
	delete old;
}

/*
void Smooth2D(TGraph * g, int N) {
	TGraph * old = Close2D(g);
	if (N > 2 * g->GetN())
		N = 2 * g->GetN() - 1;

	double gauss[N];
	double sigma = (double) N / 4.;
	double sum = 0;
	double lim = (double) N / 2.;
	TF1 *fb = new TF1("fb", "gaus(0)", -lim, lim);
	fb->SetParameter(0, 1. / (sqrt(2 * 3.1415) * sigma));
	fb->SetParameter(1, 0);
	fb->SetParameter(2, sigma);
	for (int i = 0; i < N; ++i) {
		gauss[i] = fb->Integral(-lim + i, -lim + i + 1);
		sum += gauss[i];
	}
	for (int i = 0; i < N; ++i)
		gauss[i] /= sum;

	for (int i = 0; i < g->GetN(); ++i) {
		double avy = 0., avx = 0, x, x0, y;
		int points = 0;
		for (int j = i - N / 2; j <= i + N / 2; ++j) {
			//if      (j<0)          old->GetPoint(old->GetN()+j, x, y);
			//else if (j>=g->GetN()) old->GetPoint(j-old->GetN(), x, y);
			if (j < 0)
				old->GetPoint(0, x, y);
			else if (j >= g->GetN())
				old->GetPoint(old->GetN() - 1, x, y);
			else
				old->GetPoint(j, x, y);
			if (i == j)
				x0 = x;
			avy += y * gauss[points];
			avx += x * gauss[points];
			++points;
		}
		g->SetPoint(i, avx, avy);
	}
	delete old;
}

TGraph * Close2D(TGraph * g) {
	TGraph * f = new TGraph(0);
	if (g->GetN() == 0)
		return f;
	double x, y;
	g->GetPoint(0, x, y);
	g->SetPoint(g->GetN(), x, y);

	int i = 0;
	for (; i < g->GetN(); ++i) {
		g->GetPoint(i, x, y);
		//if (x<450&&y<450) break;
	}
	int p = 0;
	for (int j = i + 1; j != i; ++j) {
		if (j >= g->GetN())
			j = 0;
		g->GetPoint(j, x, y);
		//if (y<110+(x-120)*390/442||(x<330&&y<1000)||(x<500&&y<600)) continue;
		f->SetPoint(p++, x, y);
	}
	return f;
}
*/

void Cut(TGraph * &g, const char f, const char c, double cut)
{
  double x, y;
  TGraph * old = (TGraph*)g->Clone();
  g=new TGraph(1);
  int i=0;
  for (int p=0; p<old->GetN(); ++p) {
    old->GetPoint(p,x,y);
    //std::cout<< "y="<< y<<", "<<f<<" = "<<x<<" "<<c<<" "<<cut<<" N=" <<g->GetN();
    if (c=='>' && f=='x' && x>cut) continue;
    if (c=='<' && f=='x' && x<cut) continue;
    if (c=='>' && f=='y' && y>cut) continue;
    if (c=='<' && f=='y' && y<cut) continue;
    g->SetPoint(i++,x,y);
    //std::cout << " <> "<<g->GetN()<<std::endl;
  }
  g->SetLineColor(old->GetLineColor());
  g->SetLineStyle(old->GetLineStyle());
  g->SetLineWidth(old->GetLineWidth());
  delete old;
}

void FillEmptyPoints(TH2*h, double by) {
	for (int x = 0; x <= h->GetXaxis()->GetNbins(); ++x){
		for (int y = 0; y <= h->GetYaxis()->GetNbins(); ++y){
			if(h->GetBinContent(x, y) == 0 ){
			     //std::cout <<x<<", "<<y<<": "<<h->GetBinContent(x, y)<<std::endl;
				h->SetBinContent(x, y, by);
			}
		}
	}


}


TCanvas * GetLimitTemplateCanvas(std::string file,std::string key)
{
  TFile f(file.c_str());
  return (TCanvas*)f.Get(key.c_str());
}

void SetZRange(TH2 * h, TH2*h2) {
    //cout<<"Find optimal z range..."<<endl;
    double maxValue = 0, minValue = 0;

    maxValue = h->GetBinContent(h->GetMaximumBin());
    minValue = h->GetBinContent(h->GetMinimumBin());
    if (minValue == 0) {
        minValue = 9999;
        for (int x = 1; x <= h->GetNbinsX() + 1; x++) {
            for (int y = 1; y <= h->GetNbinsY() + 1; y++) {
                //cout<<"x:"<<x<<endl;
                //cout<<"y:"<<y<<endl;
                double bincontent = h->GetBinContent(x, y);
                //cout<<"bincontent:"<<bincontent<<endl;

                if (minValue > bincontent && bincontent > 0) {

                    minValue = bincontent;
                }
            }
        }

    }
    minValue = minValue * 0.9;
    maxValue = maxValue * 1.1;
    //    cout<<"maximum value:"<<maxValue<<endl;
    //    cout<<"minimum value:"<<minValue<<endl;
    h->GetZaxis()->SetRangeUser(minValue, maxValue);
    if (h2)     h2->GetZaxis()->SetRangeUser(minValue, maxValue);


}

//~ TGraph* RA2Observed_36pb(){
   //~ TGraph *graph = new TGraph(129);
   //~ graph->SetName("RA2obs36pb-1");
   //~ graph->SetLineWidth(2);
   //~ graph->SetLineColor(2);
   //~ //graph->SetMarkerColor(kBlue);
   //~ //graph->SetMarkerStyle(21);
   //~ graph->SetPoint(0,5.0495,310.1631);
   //~ graph->SetPoint(1,11.74816,310.4632);
   //~ graph->SetPoint(2,15.1485,310.6155);
   //~ graph->SetPoint(3,25.2475,311.1183);
   //~ graph->SetPoint(4,35.3465,311.6649);
   //~ graph->SetPoint(5,45.4455,312.2464);
   //~ graph->SetPoint(6,55.5445,312.8517);
   //~ graph->SetPoint(7,65.6435,314.0822);
   //~ graph->SetPoint(8,72.34216,314.4794);
   //~ graph->SetPoint(9,75.7425,314.681);
   //~ graph->SetPoint(10,85.8415,315.2521);
   //~ graph->SetPoint(11,95.9405,315.7525);
   //~ graph->SetPoint(12,106.0395,316.1319);
   //~ graph->SetPoint(13,111.0419,316.3099);
   //~ graph->SetPoint(14,118.9463,316.574);
   //~ graph->SetPoint(15,126.809,316.8055);
   //~ graph->SetPoint(16,134.6602,316.9935);
   //~ graph->SetPoint(17,142.391,317.0885);
   //~ graph->SetPoint(18,150.0371,317.1153);
   //~ graph->SetPoint(19,157.6431,317.083);
   //~ graph->SetPoint(20,165.2306,316.9916);
   //~ graph->SetPoint(21,172.8219,316.8398);
   //~ graph->SetPoint(22,180.4643,316.5894);
   //~ graph->SetPoint(23,188.1975,316.1463);
   //~ graph->SetPoint(24,195.9831,315.5341);
   //~ graph->SetPoint(25,203.7808,314.8385);
   //~ graph->SetPoint(26,211.6241,314.0626);
   //~ graph->SetPoint(27,219.5504,313.1768);
   //~ graph->SetPoint(28,227.5694,312.1695);
   //~ graph->SetPoint(29,235.6705,311.0451);
   //~ graph->SetPoint(30,243.8317,309.7729);
   //~ graph->SetPoint(31,252.0689,308.2953);
   //~ graph->SetPoint(32,260.3968,306.633);
   //~ graph->SetPoint(33,268.7516,304.8153);
   //~ graph->SetPoint(34,277.0685,302.9772);
   //~ graph->SetPoint(35,285.3594,301.1464);
   //~ graph->SetPoint(36,293.6694,299.2467);
   //~ graph->SetPoint(37,301.9481,297.3159);
   //~ graph->SetPoint(38,310.1957,295.4541);
   //~ graph->SetPoint(39,318.4017,293.6261);
   //~ graph->SetPoint(40,326.4774,291.6738);
   //~ graph->SetPoint(41,334.4459,289.6291);
   //~ graph->SetPoint(42,342.3069,287.5337);
   //~ graph->SetPoint(43,350.0281,285.2399);
   //~ graph->SetPoint(44,357.7132,282.7821);
   //~ graph->SetPoint(45,365.3344,280.2042);
   //~ graph->SetPoint(46,372.8757,277.5876);
   //~ graph->SetPoint(47,380.3562,274.8286);
   //~ graph->SetPoint(48,387.7977,271.9229);
   //~ graph->SetPoint(49,395.1593,268.9235);
   //~ graph->SetPoint(50,402.479,265.9061);
   //~ graph->SetPoint(51,409.8034,263.0235);
   //~ graph->SetPoint(52,417.2037,260.2826);
   //~ graph->SetPoint(53,424.6658,257.6606);
   //~ graph->SetPoint(54,432.1837,255.2158);
   //~ graph->SetPoint(55,439.7824,252.8498);
   //~ graph->SetPoint(56,447.5324,250.4784);
   //~ graph->SetPoint(57,455.4155,248.1665);
   //~ graph->SetPoint(58,463.3538,246.2746);
   //~ graph->SetPoint(59,471.3743,245.2733);
   //~ graph->SetPoint(60,479.507,244.2944);
   //~ graph->SetPoint(61,487.8013,243.3518);
   //~ graph->SetPoint(62,496.218,242.4536);
   //~ graph->SetPoint(63,504.7242,241.5342);
   //~ graph->SetPoint(64,513.3662,240.6189);
   //~ graph->SetPoint(65,522.0385,239.6953);
   //~ graph->SetPoint(66,530.7206,238.6674);
   //~ graph->SetPoint(67,539.48,237.6134);
   //~ graph->SetPoint(68,548.2746,236.5566);
   //~ graph->SetPoint(69,557.0962,235.3967);
   //~ graph->SetPoint(70,565.9632,234.1824);
   //~ graph->SetPoint(71,574.7531,232.9209);
   //~ graph->SetPoint(72,583.4856,231.5781);
   //~ graph->SetPoint(73,592.156,230.2697);
   //~ graph->SetPoint(74,600.7259,228.9881);
   //~ graph->SetPoint(75,609.2435,227.7199);
   //~ graph->SetPoint(76,617.6929,226.4691);
   //~ graph->SetPoint(77,626.0509,225.2237);
   //~ graph->SetPoint(78,634.3124,223.98);
   //~ graph->SetPoint(79,642.4827,222.75);
   //~ graph->SetPoint(80,650.5691,221.544);
   //~ graph->SetPoint(81,658.5175,220.3382);
   //~ graph->SetPoint(82,666.3535,219.0978);
   //~ graph->SetPoint(83,674.1138,217.8704);
   //~ graph->SetPoint(84,681.8143,216.6541);
   //~ graph->SetPoint(85,689.4894,215.5348);
   //~ graph->SetPoint(86,697.0822,214.5147);
   //~ graph->SetPoint(87,704.5665,213.4809);
   //~ graph->SetPoint(88,711.978,212.4004);
   //~ graph->SetPoint(89,719.3595,211.3256);
   //~ graph->SetPoint(90,726.7282,210.2617);
   //~ graph->SetPoint(91,734.1006,209.2146);
   //~ graph->SetPoint(92,741.5407,208.2153);
   //~ graph->SetPoint(93,748.9617,207.2553);
   //~ graph->SetPoint(94,756.3621,206.2401);
   //~ graph->SetPoint(95,763.78,205.2225);
   //~ graph->SetPoint(96,771.1957,204.2703);
   //~ graph->SetPoint(97,778.5801,203.3733);
   //~ graph->SetPoint(98,785.9729,202.5053);
   //~ graph->SetPoint(99,793.357,201.6465);
   //~ graph->SetPoint(100,800.7564,200.737);
   //~ graph->SetPoint(101,808.1959,199.817);
   //~ graph->SetPoint(102,815.6238,198.9176);
   //~ graph->SetPoint(103,823.1019,198.0622);
   //~ graph->SetPoint(104,830.5421,197.2352);
   //~ graph->SetPoint(105,837.9428,196.3364);
   //~ graph->SetPoint(106,845.343,195.4146);
   //~ graph->SetPoint(107,852.7249,194.535);
   //~ graph->SetPoint(108,860.1103,193.7117);
   //~ graph->SetPoint(109,867.5219,192.9445);
   //~ graph->SetPoint(110,874.943,192.182);
   //~ graph->SetPoint(111,882.3249,191.4043);
   //~ graph->SetPoint(112,889.72,190.5342);
   //~ graph->SetPoint(113,897.1798,189.6625);
   //~ graph->SetPoint(114,904.669,188.9112);
   //~ graph->SetPoint(115,912.1216,188.286);
   //~ graph->SetPoint(116,924.0585,187.7087);
   //~ graph->SetPoint(117,927.4588,187.1887);
   //~ graph->SetPoint(118,934.1575,186.734);
   //~ graph->SetPoint(119,944.2565,186.3506);
   //~ graph->SetPoint(120,950.9552,186.0668);
   //~ graph->SetPoint(121,954.3555,185.9011);
   //~ graph->SetPoint(122,964.4545,185.7932);
   //~ graph->SetPoint(123,974.5535,185.6966);
   //~ graph->SetPoint(124,977.9538,185.6463);
   //~ graph->SetPoint(125,984.6525,185.6906);
   //~ graph->SetPoint(126,994.7515,185.8363);
   //~ graph->SetPoint(127,1001.45,186.0129);
   //~ graph->SetPoint(128,1004.851,186.2132);
   //~ return graph;
//~ }
//~ 
//~ TGraph* RA2Observed_1fb( ){
   //~ TGraph *graph = new TGraph(142);
   //~ graph->SetName("RA2Observed_1fb");
   //~ //graph->SetFillColor(84);
   //~ graph->SetLineColor(4);
   //~ graph->SetLineWidth(2);
   //~ graph->SetPoint(0,9.3545,530.8102);
   //~ graph->SetPoint(1,28.0635,531.1779);
   //~ graph->SetPoint(2,46.7725,531.6358);
   //~ graph->SetPoint(3,65.4815,532.0616);
   //~ graph->SetPoint(4,84.1905,532.3566);
   //~ graph->SetPoint(5,102.8995,532.5857);
   //~ graph->SetPoint(6,121.6085,532.8385);
   //~ graph->SetPoint(7,140.3175,533.1734);
   //~ graph->SetPoint(8,159.0265,533.4716);
   //~ graph->SetPoint(9,177.7355,533.7125);
   //~ graph->SetPoint(10,196.4445,533.8776);
   //~ graph->SetPoint(11,202.5548,533.952);
   //~ graph->SetPoint(12,215.1535,533.9265);
   //~ graph->SetPoint(13,226.7336,533.7988);
   //~ graph->SetPoint(14,241.4028,533.4416);
   //~ graph->SetPoint(15,255.7853,532.8942);
   //~ graph->SetPoint(16,270.0309,532.211);
   //~ graph->SetPoint(17,284.2032,531.4031);
   //~ graph->SetPoint(18,298.3673,530.4844);
   //~ graph->SetPoint(19,312.5865,529.4698);
   //~ graph->SetPoint(20,326.86,528.2411);
   //~ graph->SetPoint(21,341.1577,526.8409);
   //~ graph->SetPoint(22,355.6028,525.3188);
   //~ graph->SetPoint(23,370.1567,523.5435);
   //~ graph->SetPoint(24,384.7527,521.542);
   //~ graph->SetPoint(25,399.4452,519.3732);
   //~ graph->SetPoint(26,414.1731,517.083);
   //~ graph->SetPoint(27,428.9056,514.7088);
   //~ graph->SetPoint(28,443.5651,512.1308);
   //~ graph->SetPoint(29,458.0544,509.3979);
   //~ graph->SetPoint(30,472.4889,506.6755);
   //~ graph->SetPoint(31,486.8745,503.878);
   //~ graph->SetPoint(32,501.0482,500.9315);
   //~ graph->SetPoint(33,515.0864,497.8097);
   //~ graph->SetPoint(34,528.9452,494.5141);
   //~ graph->SetPoint(35,542.5491,491.0698);
   //~ graph->SetPoint(36,555.8684,487.5259);
   //~ graph->SetPoint(37,568.9826,483.8063);
   //~ graph->SetPoint(38,581.8623,479.9445);
   //~ graph->SetPoint(39,594.5836,475.8509);
   //~ graph->SetPoint(40,607.1106,471.5485);
   //~ graph->SetPoint(41,619.6138,467.1725);
   //~ graph->SetPoint(42,632.1034,462.5079);
   //~ graph->SetPoint(43,644.419,457.5307);
   //~ graph->SetPoint(44,656.6832,452.2999);
   //~ graph->SetPoint(45,668.8675,446.7048);
   //~ graph->SetPoint(46,680.9216,440.8055);
   //~ graph->SetPoint(47,693.0034,434.7815);
   //~ graph->SetPoint(48,705.1123,428.4665);
   //~ graph->SetPoint(49,717.0246,421.7536);
   //~ graph->SetPoint(50,728.8271,414.8725);
   //~ graph->SetPoint(51,740.5452,407.9118);
   //~ graph->SetPoint(52,752.2063,400.9078);
   //~ graph->SetPoint(53,763.813,393.8012);
   //~ graph->SetPoint(54,775.2835,386.658);
   //~ graph->SetPoint(55,786.6203,379.6697);
   //~ graph->SetPoint(56,797.9809,372.8602);
   //~ graph->SetPoint(57,809.2867,366.2262);
   //~ graph->SetPoint(58,820.5688,359.7902);
   //~ graph->SetPoint(59,831.83,353.5514);
   //~ graph->SetPoint(60,842.9681,347.599);
   //~ graph->SetPoint(61,854.0611,342.0535);
   //~ graph->SetPoint(62,865.2407,336.9501);
   //~ graph->SetPoint(63,876.5266,332.1052);
   //~ graph->SetPoint(64,887.8125,327.6087);
   //~ graph->SetPoint(65,899.2651,323.4389);
   //~ graph->SetPoint(66,910.8541,319.6399);
   //~ graph->SetPoint(67,922.6579,316.1359);
   //~ graph->SetPoint(68,934.5443,312.7348);
   //~ graph->SetPoint(69,946.5207,309.5606);
   //~ graph->SetPoint(70,958.7432,306.566);
   //~ graph->SetPoint(71,971.0644,303.5431);
   //~ graph->SetPoint(72,983.4808,300.6029);
   //~ graph->SetPoint(73,996.0139,297.7569);
   //~ graph->SetPoint(74,1008.588,295.0146);
   //~ graph->SetPoint(75,1021.303,292.3768);
   //~ graph->SetPoint(76,1034.246,289.8707);
   //~ graph->SetPoint(77,1047.344,287.3773);
   //~ graph->SetPoint(78,1060.593,284.8191);
   //~ graph->SetPoint(79,1073.889,282.067);
   //~ graph->SetPoint(80,1087.125,279.3118);
   //~ graph->SetPoint(81,1100.461,276.721);
   //~ graph->SetPoint(82,1113.957,274.2374);
   //~ graph->SetPoint(83,1127.526,271.8241);
   //~ graph->SetPoint(84,1141.144,269.3706);
   //~ graph->SetPoint(85,1154.81,267.0183);
   //~ graph->SetPoint(86,1168.672,264.7348);
   //~ graph->SetPoint(87,1182.73,262.4094);
   //~ graph->SetPoint(88,1196.815,260.0646);
   //~ graph->SetPoint(89,1210.926,257.9047);
   //~ graph->SetPoint(90,1225.106,255.7935);
   //~ graph->SetPoint(91,1239.32,253.6809);
   //~ graph->SetPoint(92,1253.419,251.6196);
   //~ graph->SetPoint(93,1267.43,249.7076);
   //~ graph->SetPoint(94,1281.33,247.7397);
   //~ graph->SetPoint(95,1295.073,245.87);
   //~ graph->SetPoint(96,1308.773,244.0911);
   //~ graph->SetPoint(97,1322.309,242.3672);
   //~ graph->SetPoint(98,1335.615,240.8862);
   //~ graph->SetPoint(99,1348.77,239.6794);
   //~ graph->SetPoint(100,1361.757,238.4351);
   //~ graph->SetPoint(101,1374.465,237.1694);
   //~ graph->SetPoint(102,1386.971,236.058);
   //~ graph->SetPoint(103,1399.327,235.09);
   //~ graph->SetPoint(104,1411.594,234.2493);
   //~ graph->SetPoint(105,1423.834,233.5167);
   //~ graph->SetPoint(106,1436.155,232.9704);
   //~ graph->SetPoint(107,1448.601,232.38);
   //~ graph->SetPoint(108,1461.038,231.6991);
   //~ graph->SetPoint(109,1473.496,231.0203);
   //~ graph->SetPoint(110,1486.048,230.4148);
   //~ graph->SetPoint(111,1498.817,229.8798);
   //~ graph->SetPoint(112,1511.801,229.2072);
   //~ graph->SetPoint(113,1524.823,228.3754);
   //~ graph->SetPoint(114,1537.858,227.5037);
   //~ graph->SetPoint(115,1551.025,226.6422);
   //~ graph->SetPoint(116,1564.221,225.545);
   //~ graph->SetPoint(117,1577.349,224.4837);
   //~ graph->SetPoint(118,1590.397,223.5006);
   //~ graph->SetPoint(119,1603.357,222.5873);
   //~ graph->SetPoint(120,1616.137,221.5018);
   //~ graph->SetPoint(121,1628.653,220.5172);
   //~ graph->SetPoint(122,1640.917,219.6712);
   //~ graph->SetPoint(123,1652.864,218.9957);
   //~ graph->SetPoint(124,1664.567,218.4112);
   //~ graph->SetPoint(125,1676.159,217.8846);
   //~ graph->SetPoint(126,1687.559,217.257);
   //~ graph->SetPoint(127,1698.741,216.7841);
   //~ graph->SetPoint(128,1709.896,216.4198);
   //~ graph->SetPoint(129,1724.346,216.091);
   //~ graph->SetPoint(130,1730.582,215.786);
   //~ graph->SetPoint(131,1736.819,215.491);
   //~ graph->SetPoint(132,1749.291,215.1913);
   //~ graph->SetPoint(133,1761.89,214.8721);
   //~ graph->SetPoint(134,1768,214.619);
   //~ graph->SetPoint(135,1774.111,214.3438);
   //~ graph->SetPoint(136,1786.709,213.9373);
   //~ graph->SetPoint(137,1805.418,213.3678);
   //~ graph->SetPoint(138,1824.127,212.7668);
   //~ graph->SetPoint(139,1836.726,212.2368);
   //~ graph->SetPoint(140,1842.836,211.7081);
   //~ graph->SetPoint(141,1861.545,211.0896);
   //~ return graph;
//~ }
//~ 
//~ 
//~ TGraph* Atlas0l24j_1fb( ){
   //~ TGraph *graph = new TGraph(1);
   //~ graph->SetName("Atlas0l24j_1fb");
   //~ //graph->SetFillColor(84);
   //~ graph->SetLineColor(4);
   //~ graph->SetLineWidth(2);
   //~ int i=0;
   //~ graph->SetPoint(i++,147.0, 462.4);
   //~ graph->SetPoint(i++,196.4,	  450.3);
   //~ graph->SetPoint(i++,241.0,	  442.6);
   //~ graph->SetPoint(i++,296.1,	  436.1);
   //~ graph->SetPoint(i++,335.0,	  430.1);
   //~ graph->SetPoint(i++,382.0,     421.8);
   //~ graph->SetPoint(i++,429.0,     412.0);
   //~ graph->SetPoint(i++,463.9,     407.6);
   //~ graph->SetPoint(i++,523.0,     399.1);
   //~ graph->SetPoint(i++,551.1,     393.3);
   //~ graph->SetPoint(i++,617.0,     382.7);
   //~ graph->SetPoint(i++,639.8,     379.1);
   //~ graph->SetPoint(i++,711.0,     367.8);
   //~ graph->SetPoint(i++,726.0,     364.8);
   //~ graph->SetPoint(i++,785.1,     350.6);
   //~ graph->SetPoint(i++,805.0,     345.3);
   //~ graph->SetPoint(i++,841.8,     336.3);
   //~ graph->SetPoint(i++,887.6,     322.1);
   //~ graph->SetPoint(i++,899.0,     318.4);
   //~ graph->SetPoint(i++,945.1,     307.8);
   //~ graph->SetPoint(i++,993.0,     297.0);
   //~ graph->SetPoint(i++,1005.4,    293.6);
   //~ graph->SetPoint(i++,1038.6,    279.3);
   //~ graph->SetPoint(i++,1087.0 ,   267.2);
   //~ graph->SetPoint(i++,1096.7 ,   265.1);
   //~ graph->SetPoint(i++,1174.6,    250.8);
   //~ graph->SetPoint(i++,1181.0,    249.5);
   //~ graph->SetPoint(i++,1227.9,    236.6);
   //~ graph->SetPoint(i++,1275.0,    227.1);
   //~ graph->SetPoint(i++,1337.1,    222.3);
   //~ graph->SetPoint(i++,1369.0,    217.7);
   //~ graph->SetPoint(i++,1425.6,    208.1);
   //~ graph->SetPoint(i++,1463.0,    204.3);
   //~ graph->SetPoint(i++,1557.0,    206.1);
   //~ graph->SetPoint(i++,1651.0,    205.1);
   //~ graph->SetPoint(i++,1745.0,    198.4);
   //~ graph->SetPoint(i++,1836.5,    193.8);
   //~ graph->SetPoint(i++,1839.0,    193.7);
   //~ graph->SetPoint(i++,1845.6,    193.8);
   //~ graph->SetPoint(i++,1933.0,    195.6);
   //~ graph->SetPoint(i++,1968.7,    193.8);
   //~ graph->SetPoint(i++,2027.0,    190.5);
   //~ graph->SetPoint(i++,2121.0,    191.8);
   //~ graph->SetPoint(i++,2215.0 ,   188.2);
   //~ graph->SetPoint(i++,2309.0 ,   187.2);
   //~ graph->SetPoint(i++,2403.0 ,   186.5);
   //~ graph->SetPoint(i++,2497.0 ,   186.1);
   //~ graph->SetPoint(i++,2591.0 ,   186.0);
   //~ graph->SetPoint(i++,2685.0 ,   186.5);
   //~ graph->SetPoint(i++,2779.0 ,   183.9);
   //~ graph->SetPoint(i++,2856.8 ,   179.6);
   //~ graph->SetPoint(i++,2873.0 ,   178.0);
   //~ graph->SetPoint(i++,2967.0 ,   169.8);
   //~ graph->SetPoint(i++,3030.3,	 165.3 );
   //~ return graph;		      
//~ }   
//~ 
//~ ////////////////////////////////////////////
//~ TGraph* gl_LEP(){//gl-sq
    //~ double sq[] = {0,0,100,100};
    //~ double gl[] = {0,2000,2000,0};
    //~ TGraph* res = new TGraph(4,gl,sq);
    //~ res->SetFillColor(kBlue);
    //~ return res;
//~ }
//~ 
//~ TGraph* sq_TEV(){//gl-sq
    //~ double sq[] = {0,2000,2000,330,250,300,200,150,100,0};
    //~ double gl[] = {0,0,190,190,260,300,500,560,500,500};
//~ 
    //~ TGraph* res = new TGraph(10,gl,sq);
    //~ res->SetFillColor(kGreen+2);
    //~ return res;
//~ }
//~ 
//~ TGraph* sq_CDF(){//gl-sq
    //~ double sq[] = {0,2000,2000,480,460,420,410,380,390,290,0};
    //~ double gl[] = {0,0,280,280,300,310,330,340,440,320,320};
    //~ TGraph* res = new TGraph(11,gl,sq);
    //~ res->SetFillColor(kOrange+5);
    //~ return res;
//~ }
//~ TGraph* sq_DEZ(){//gl-sq
    //~ double sq[] = {0,2000,2000,460,430,400,390,290,0};
    //~ double gl[] = {0,0,305,305,320,350,440,320,320};
    //~ TGraph* res = new TGraph(9,gl,sq);
    //~ res->SetFillColor(kYellow-5);
    //~ return res;
//~ }
//~ 
//~ TGraph* glsq_NoSol(){//sq-gl
    //~ gStyle->SetHatchesSpacing(2.0);
    //~ gStyle->SetHatchesLineWidth(1);
//~ //    double sq[] = {83,83,110,1297.6,0,   0};
//~ //    double gl[] = { 0,63,120,1466,  1466,0};   
    //~ double sq[] = {83,83,110,1602.3,0,   0};
    //~ double gl[] = { 0,63,120,1800,  1800,0};
    //~ TGraph* res = new TGraph(6,gl,sq);
    //~ res->SetLineColor(1);
    //~ res->SetLineWidth(2);
    //~ res->SetFillStyle(3354);
    //~ return res;
//~ }
//~ 
//~ 
//~ TGraph* glsq_NoSol_aux(){//sq-gl : aux for drawing
    //~ double sq[] = {83,83,110,1602.3,0};
    //~ double gl[] = { 0,63,120,1800  ,1800};
    //~ TGraph* res = new TGraph(5,gl,sq);
    //~ res->SetLineColor(1);
    //~ res->SetLineWidth(1);
    //~ res->SetFillColor(0);
    //~ return res;
//~ }

