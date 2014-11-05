#include "Overview.h"
#include "iostream"

OverviewTable * Overview = 0;

Table::TTable*  OverviewTable::Get()
{
//  std::cerr<<"Table::TTable*  OverviewTable::Get()  "<<header.size()<<std::endl;
  //Create headers
  table->AddColumn<std::string>("Point");
  int ncolums=0;
  for (std::map<std::string,bool>::const_iterator it=header.begin();it!=header.end();++it){
      //std::cerr<<it->first<<"  ";
      table->AddColumn<std::string>(it->first);
  }  
  ncolums=header.size();

  for (std::map<int, std::map<std::string,std::string> >::const_iterator it=body.begin();it!=body.end();++it) {
    //std::cerr<<std::endl<<it->first<<"  ";
    *table << ToString(it->first);
    int i=0;
    for (std::map<std::string,bool>::const_iterator v=header.begin();v!=header.end();++v){
      std::map<std::string,std::string>::const_iterator elem=it->second.find(v->first);
      if (elem==it->second.end()){
         //std::cerr<<"      ";
         *table << "";
      }	 
      else  {  
         //std::cerr<<elem->second<<"   ";
         *table << elem->second;
      }
    }	 
  }
  return table;
}

void OverviewTable::Print(std::ofstream& of) 
{
  Get();
  of << *table;
}
