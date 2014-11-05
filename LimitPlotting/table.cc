#include "table.h"
#include <iomanip>
#include <sstream>

namespace Table {

std::string TTable::hline(char c,char r) const {

  if (style_==TeX) return "\\\\ \\hline";
  
  std::stringstream ss;
  for (int i=0; i<(delimiter_.size())/2; ++i) ss<<c;
  ss<<r;
  for (int i=0; i<(delimiter_.size()-1)/2; ++i) ss<<c;
  std::stringstream os;
  std::vector<TColumnBase*>::const_iterator it=table_.begin();
  os.fill('-');
  os<<std::endl<<std::setw((*it)->Width())<<"";
  ++it;
  for (;it!=table_.end();++it){
    os << ss.str() << std::setw((*it)->Width()) << "";
  }
  return os.str();
}


std::ostream& operator<<( std::ostream& os, const TTable& tab )
{
    //determine current style
    if (tab.GetTable()->size()==0) return os;
    std::string delimiter = tab.GetDelimiter();
    bool tex   = (tab.GetStyle()==TeX);
    bool empty = (tab.GetStyle()==Empty);
    //header
    if (tab.GetHeader()!="") os<<tab.GetHeader()<<std::endl;
    if (tex) {
      delimiter = " & ";
      os << "\\begin{tabular}{";
      for (unsigned i=0; i<tab.GetTable()->size(); ++i) os << "c";
      os << "}" <<std::endl;
    }  
    //column-headers
    std::vector<TColumnBase*>::const_iterator it=tab.GetTable()->begin();
    if (!empty){
      os<<std::setw((*it)->Width())<<(*it)->GetHeader();
      ++it;
      for (;it!=tab.GetTable()->end();++it){
        os <<delimiter<<std::setw((*it)->Width())<<(*it)->GetHeader();
      }
      //draw a line below the header
      os<<tab.hline()<<std::endl;
    } 
    else  //empty style: define at least the column width's
      for (;it!=tab.GetTable()->end();++it) (*it)->Width();
    //all rows of the table
    for (unsigned l=0; l<tab.Length(); ++l){
      //all columns of current row
      it=tab.GetTable()->begin();
      os<<std::setw((*it)->GetCurrentWidth())<<std::left<<(*it)->Str(l);
      ++it;
      for (;it!=tab.GetTable()->end();++it){
	os<<delimiter<<std::setw((*it)->GetCurrentWidth()) <<(*it)->Str(l);
      }
      if (tex) os<<"\\\\";
      os<<std::endl;
    }
    //caption
    if (!tex && tab.GetCaption()!="")
       os<<tab.GetCaption()<<std::endl;
    if (tex) {
       os<<"\\label{tab:xyz}"<<std::endl;
       if (tab.GetCaption()!="") os<<"\\caption{"<<tab.GetCaption()<<"}"<<std::endl;
       os<<"\\end{tabular}"<<std::endl;
      }  
    return os;
  }
}

