#ifndef OVERVIEW_H
#define OVERVIEW_H

#include <fstream>
#include <map>
#include <string>

#include "table.h"


template<class T> std::string ToString(T t){
  std::stringstream ss;
  ss << t;
  return ss.str();
}

class OverviewTable {
 public:
  OverviewTable():table(new Table::TTable()){}
  void Add(int point, const std::string& var, const std::string& val){
    body[point][var]=val;
    header[var]=1;
    //std::cout << point<< ", var="<<var<<"; val="<<val<<"; size="<<body.size() <<std::endl;
  }
  Table::TTable * Get();
  void Print(std::ofstream& of);
  
 private:
  std::map<int, std::map<std::string,std::string> > body;
  std::map<std::string,bool> header;
  Table::TTable * table;
};

extern OverviewTable * Overview;



#endif
