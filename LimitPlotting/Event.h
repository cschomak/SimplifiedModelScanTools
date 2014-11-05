// $Id: Event.h,v 1.2 2012/06/26 13:58:23 auterman Exp $

/*** ------------------------------------------------------------------------------------------------------- ***
     TheBetterPlotScript, a tool to plot final results, limits and exclusion contours, based on 'PlotScript'

     Christian Autermann, Hamburg University/LPC, February 2012
 *** ------------------------------------------------------------------------------------------------------- ***/

#ifndef EVENT_H
#define EVENT_H

#include <map>
#include <vector>
#include <string>
#include <algorithm>

#include "Variable.h"


const static int nchannels=6;


class GeneratorMasses;

///Container for all variables per SUSY point
class Event{
 public:
  Event(){}
  //Event(Event& e){vars_=e.vars_; VariableIndex_=e.GetVariableIndex();}
  Event(Event*e){vars_=e->vars_; //VariableIndex_=e->GetVariableIndex();
    for (std::map<const std::string, unsigned>::const_iterator it=GetVariableBegin();it!=GetVariableEnd();++it)
      VariableIndex_[it->first]=it->second;
  }
 
  double Get(const std::string& variable) const {
    std::map<const std::string, unsigned>::const_iterator it = VariableIndex_.find(variable);
    return (it!=VariableIndex_.end()?vars_[it->second].GetValue():-1);}
  void   Set(const std::string& variable, double v) {vars_[VariableIndex_[variable] ].SetValue( v );}
  void   Add(Variable var); //yes, cp argument: read function doesn't cp
  Event * Clone();

  //For Interpolations:
  const Event operator*(const double f) const;
  const Event operator+(const Event& f) const;

  std::vector<Variable> vars_;
  std::map<const std::string, unsigned> GetVariableIndex() const {return VariableIndex_;}
  std::map<const std::string, unsigned>::const_iterator GetVariableBegin() const {return VariableIndex_.begin();}
  std::map<const std::string, unsigned>::const_iterator GetVariableEnd() const {return VariableIndex_.end();}
  
 private:
//  std::vector<Variable> vars_;
  static std::map<const std::string, unsigned> VariableIndex_;
}; 

///Collection of Events
typedef std::vector<Event> Events;

/// Helper class to access Variables by functor 
class Fill{
 public:
  Fill(const std::string& variable):variable(variable){}
  double operator()(const Event& evt) const { return evt.Get(variable);}
 private:
  const std::string variable;
};

/// Helper class to access Variables by functor 
class Compare{
 public:
  enum comparator { less, greater, equal };
  Compare(const std::string& variable, const comparator op, const double value):variable(variable),op(op),value(value){}
  bool operator()(const Event& evt) const { 
    if (op==less)         return evt.Get(variable)<value;
    else if (op==greater) return evt.Get(variable)>value;
    else if (op==equal)   return evt.Get(variable)==value;
    return false;
  }
 private:
  const std::string variable;
  const comparator op;
  const double value;
};

/// Helper class to acess to sort events 
class sort_by{
  public:
   sort_by(const std::string& x):f_(x){}
   bool operator()(const Event& a, const Event& b){ return f_(a)<f_(b); }
  private:
   Fill f_;
};

void ReadEvent(Event& evt, ConfigFile& config);
void ReadEvents(Events& evts, const std::string& file);
void CalculateVariablesOnTheFly(Event& evt);
void AddGeneratorVariables(Event& evt, GeneratorMasses& p);
void GetEvents(Events::iterator& a, Events::iterator& b, const std::string& var, const double value );

#endif
