// $Id: Variable.cc,v 1.5 2012/06/26 13:58:23 auterman Exp $

/*** ------------------------------------------------------------------------------------------------------- ***
     TheBetterPlotScript, a tool to plot final results, limits and exclusion contours, based on 'PlotScript'

     Christian Autermann, Hamburg University/LPC, February 2012
 *** ------------------------------------------------------------------------------------------------------- ***/

#include "Variable.h"
#include "ConfigFile.h"

//private look-up table for the "static" event infos
static std::map<std::string,Info*> info_map;

void Info::Fill(Variable& v, ConfigFile& c)
{
  if (use_default) v.SetValue( c.read<double>(name_in_datacard, default_value) ); 
  else             v.SetValue( c.read<double>(name_in_datacard ) ); 
  v.SetInfo(this);
}


Variable ReadVariable(ConfigFile& c, const std::string& name, const std::string& name_in_datacard)
{
  Variable var;
  Info * info;
  if (info_map.find(name)!=info_map.end())
    info = info_map[name];
  else {
    info = new Info(name, name_in_datacard);
    info_map[name] = info;
  }  
  info->Fill(var, c);
  return var;
}

Variable ReadVariable(ConfigFile& c, const std::string& name, const std::string& name_in_datacard, const double default_value)
{
  Variable var;
  Info * info;
  if (info_map.find(name)!=info_map.end())
    info = info_map[name];
  else {
    info = new Info(name, name_in_datacard, default_value);
    info_map[name] = info;
  }  
  info->Fill(var, c);
  return var;
}

Info* GetInfo(const std::string& var)
{
  return info_map[var];
}

