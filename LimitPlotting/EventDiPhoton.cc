// $Id: EventDiPhoton.cc,v 1.3 2012/06/29 20:27:21 auterman Exp $

/*** ------------------------------------------------------------------------------------------------------- ***
     TheBetterPlotScript, a tool to plot final results, limits and exclusion contours, based on 'PlotScript'

     Christian Autermann, Hamburg University/LPC, February 2012
 *** ------------------------------------------------------------------------------------------------------- ***/

#include "Event.h"
#include "ConfigFile.h"
#include "GeneratorMasses.h"

#include <fstream>
#include <sstream>
#include <iostream>
#include <algorithm>
#include <cmath>


void ReadEvent(Event& evt, ConfigFile& config)
{
  //If no default value is specified here, and a data-card does not contain the requested variable, 
  //the event is skipped, after an error message [void ReadEvents(Events& evts, const std::string& filelist)].
  //                           <Variable Name>, <Name in Cfg File>
  evt.Add( ReadVariable(config, "gluino",      "gluino" ) );
  evt.Add( ReadVariable(config, "squark",      "squark" ) );
  evt.Add( ReadVariable(config, "chi1",        "chi1" ) );
  evt.Add( ReadVariable(config, "cha1",        "cha1", -1 ) );
  evt.Add( ReadVariable(config, "Xsection",    "Xsection.NLO" ) );
  evt.Add( ReadVariable(config, "Luminosity",  "Luminosity" ) );
  evt.Add( ReadVariable(config, "signal",      "signal" ) );
  evt.Add( ReadVariable(config, "contamination","signal.contamination", 0 ) );
  evt.Add( ReadVariable(config, "Acceptance",  "signal.acceptance" ) );

  evt.Add( ReadVariable(config, "ObsRasym",    "CLs observed asymptotic", -9999999 ) );
  evt.Add( ReadVariable(config, "ExpRasym",    "CLs expected asymptotic", -9999999 ) );
  evt.Add( ReadVariable(config, "ExpRasymM1",  "CLs expected m1sigma asymptotic", -9999999 ) );
  evt.Add( ReadVariable(config, "ExpRasymP1",  "CLs expected p1sigma asymptotic", -9999999 ) );
  evt.Add( ReadVariable(config, "ExpRasymM2",  "CLs expected m2sigma asymptotic", -9999999 ) );
  evt.Add( ReadVariable(config, "ExpRasymP2",  "CLs expected p2sigma asymptotic", -9999999 ) );
  //"Optional" variables with default values:
  
  //evt.Add( ReadVariable(config, "ObsR",        "CLs observed",         -9999999 ) );
  //evt.Add( ReadVariable(config, "ExpR",        "CLs expected",         -9999999 ) );
  //evt.Add( ReadVariable(config, "ExpRM1",      "CLs expected m1sigma", -9999999 ) );
  //evt.Add( ReadVariable(config, "ExpRP1",      "CLs expected p1sigma", -9999999 ) );
  //evt.Add( ReadVariable(config, "ExpRM2",      "CLs expected m2sigma", -9999999 ) );
  //evt.Add( ReadVariable(config, "ExpRP2",      "CLs expected p2sigma", -9999999 ) );

  //The fully freq. CLs seem not to be available!? Use asymptotic instead...
  evt.Add( ReadVariable(config, "ObsR",    "CLs observed asymptotic", -9999999 ) );
  evt.Add( ReadVariable(config, "ExpR",    "CLs expected asymptotic", -9999999 ) );
  evt.Add( ReadVariable(config, "ExpRM1",  "CLs expected m1sigma asymptotic", -9999999 ) );
  evt.Add( ReadVariable(config, "ExpRP1",  "CLs expected p1sigma asymptotic", -9999999 ) );
  evt.Add( ReadVariable(config, "ExpRM2",  "CLs expected m2sigma asymptotic", -9999999 ) );
  evt.Add( ReadVariable(config, "ExpRP2",  "CLs expected p2sigma asymptotic", -9999999 ) );

  evt.Add( ReadVariable(config, "u_signal_scale", "signal.scale.uncertainty", 0 ) );
  evt.Add( ReadVariable(config, "u_signal_pdf",   "signal.PDF.uncertainty",   0 ) );
  
}

void CalculateVariablesOnTheFly(Event& evt)
{
  evt.Add( Variable(0, new Info("ObsRtheoryM1","") ) );
  evt.Add( Variable(evt.Get("ObsR")*evt.Get("Xsection"), new Info("ObsXsecLimit","") ) );
  evt.Add( Variable(evt.Get("ExpR")*evt.Get("Xsection"), new Info("ExpXsecLimit","") ) );
  evt.Add( Variable(evt.Get("ObsRasym")*evt.Get("Xsection"), new Info("ObsXsecLimitasym","") ) );
  evt.Add( Variable(evt.Get("ExpRasym")*evt.Get("Xsection"), new Info("ExpXsecLimitasym","") ) );

  double NLO = evt.Get("u_signal_scale");
  double PDF = evt.Get("u_signal_pdf");
  if (NLO>1) NLO-=1.0;
  if (PDF>1) PDF-=1.0;
  double scl = sqrt(pow(NLO,2)+pow(PDF,2));
  //std::cout <<"sq: "<<evt.Get("squark") <<", gl: "<<evt.Get("gluino") <<", chi1: "<<evt.Get("chi1") <<", cha1: "<<evt.Get("cha1")
  //          <<"; NLO="<<NLO<<", PDF="<<PDF<<std::endl;
  evt.Add( Variable( evt.Get("ObsR")*(1.+scl), new Info("ObsRTheoM1","") ) );
  evt.Add( Variable( evt.Get("ObsR")*(1.-scl), new Info("ObsRTheoP1","") ) );
  evt.Add( Variable( evt.Get("ExpR")*(1.+scl), new Info("ExpRTheoM1","") ) );
  evt.Add( Variable( evt.Get("ExpR")*(1.-scl), new Info("ExpRTheoP1","") ) );

  evt.Add( Variable( evt.Get("ObsR")-evt.Get("ExpRM2"), new Info("ObsRmM2","") ) );
  evt.Add( Variable( evt.Get("ObsR")-evt.Get("ExpRP2"), new Info("ObsRmP2","") ) );
  evt.Add( Variable( (evt.Get("ExpRM2")!=0?evt.Get("ObsR")/evt.Get("ExpRM2"):0), new Info("ObsRdM2","") ) );
  evt.Add( Variable( (evt.Get("ExpRP2")!=0?evt.Get("ObsR")/evt.Get("ExpRP2"):0), new Info("ObsRdP2","") ) );

}

void AddGeneratorVariables(Event& evt, GeneratorMasses& p)
{
}

void ReadEvents(Events& evts, const std::string& filelist)
{
   std::cout << "...reading " << filelist<< std::flush;
   std::ifstream masses_file;
   masses_file.open(filelist.c_str());
   std::string file;
   while (1) {
      masses_file >> file;
      if (!masses_file.good()) break;
      ConfigFile config(file);
      Event evt;
      try {
        ReadEvent(evt, config);
        CalculateVariablesOnTheFly(evt);
	
	///@@Quick and dirty fix of the binning problem in the '2012-06-22-09-36-GMSB_gBino_7TeV_2j/filelist.txt' scan:
        if ( filelist=="20120622/gB_1jet/filelist.txt" && evt.Get("gluino") < 1020.)
          evt.Set("gluino", evt.Get("gluino") - 10.0);
	///@@The scan should be regenerated!  

      }
      catch(...) {
        std::cerr<<"Catched exception: skipping bad event!"<<std::endl;
	continue;
      }	
      evts.push_back(evt);
   }
   std::cout << ": "<< evts.size() << std::endl;
   //check
   masses_file.close();
}

//private lookup-table of class Event
std::map<const std::string, unsigned> Event::VariableIndex_;


void Event::Add(Variable var)
{
   vars_.push_back(var);
   if (VariableIndex_.find(var.GetInfo()->name)==VariableIndex_.end())
     VariableIndex_[var.GetInfo()->name] = vars_.size()-1;
}

void FindFirst(Events::iterator& first, Events::iterator& last, const std::string& var, const double value )
{
  for ( ;first!=last; first++) if ( first->Get(var)==value ) break;
}
void FindLast(Events::iterator first, Events::iterator& last, const std::string& var, const double value )
{
  for ( ;first<=last; first++) if ( first->Get(var)!=value ) break;
  last = first;
}

void GetEvents(Events::iterator& a, Events::iterator& b, const std::string& var, const double value )
{
  FindFirst(a, b, var, value);
  FindLast( a, b, var, value);
}

const Event Event::operator*(const double f) const {
	Event res(*this);
	for (std::vector<Variable>::iterator it=res.vars_.begin(); it != res.vars_.end(); ++it)
		it->SetValue( it->GetValue() * f);
	return res;
}

const Event Event::operator+(const Event& f) const {
	Event res(*this);
	std::vector<Variable>::iterator it = res.vars_.begin();
	std::vector<Variable>::const_iterator fi = f.vars_.begin();
	for (; it != res.vars_.end(); ++it, ++fi)
		it->SetValue( it->GetValue() + fi->GetValue() );
	return res;
}



