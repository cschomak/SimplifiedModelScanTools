// $Id: GeneratorMasses.cc,v 1.2 2012/06/26 13:58:23 auterman Exp $

/*** ------------------------------------------------------------------------------------------------------- ***
     TheBetterPlotScript, a tool to plot final results, limits and exclusion contours, based on 'PlotScript'

     Christian Autermann, Hamburg University/LPC, February 2012
 *** ------------------------------------------------------------------------------------------------------- ***/


#include "GeneratorMasses.h"

#include <fstream>
#include <iostream>
#include <cmath>


void ReadGeneratorMasses(std::vector<GeneratorMasses>& masses, std::string file)
{
   std::cout<<"Reading Generator Mass Info..."<<std::endl;
   std::ifstream masses_file;
   masses_file.open(file.c_str());
   while (1) {
      GeneratorMasses p;
      masses_file >> p.Mzero
                  >> p.Mhalf
                  >> p.TanBeta
                  >> p.Mu  
                  >> p.Azero
                  >> p.Mtop  
                  >> p.muQ	  
                  >> p.Q	  
                  >> p.M1	  
                  >> p.M2
                  >> p.M3	  
                  >> p.MGL	  
                  >> p.MUL	  
                  >> p.MB1	  
                  >> p.MSN	  
                  >> p.MNTAU	  
                  >> p.MZ1	  
                  >> p.MW1	  
                  >> p.MHL	  
                  >> p.MUR	  
                  >> p.MB2	  
                  >> p.MEL	  
                  >> p.MTAU1	  
                  >> p.MZ2	  
                  >> p.MW2	  
                  >> p.MHH	  
                  >> p.MDL	  
                  >> p.MT1	  
                  >> p.MER	  
                  >> p.MTAU2	  
                  >> p.MZ3	  
                  >> p.MHA	  
                  >> p.MDR	  
                  >> p.MT2	  
                  >> p.MZ4	  
                  >> p.MHp;

      if (!masses_file.good()) break;
      //std::cout << p.Mzero<<", "<<p.Mhalf<<", "<<p.MGL<<", "<<p.MUL<<std::endl;
      if (fabs(p.Mu)!=1.) {
         std::cerr << "ERROR: check lines in file '"<<file<<"' near m0=" << p.Mzero << ", m1/2=" << p.Mhalf << std::endl;
         exit(1);
      }	
      masses.push_back( p );
   }
   std::cout << file<<": "<<masses.size()<<std::endl;
}

std::vector<GeneratorMasses>::iterator Get (std::vector<GeneratorMasses>& masses, double m0, double m12, double tb)
{
  GeneratorMasses p;
  p.Mzero=m0;
  p.Mhalf=m12;
  p.TanBeta=tb;
  return std::find(masses.begin(), masses.end(), p);
}

void Match(std::vector<GeneratorMasses>& masses, Events& evts)
{
  std::cout<<"Matching Susy-Scan and Generator Mass Info..."<<std::endl;
  for (Events::iterator evt=evts.begin(); evt!=evts.end(); ++evt){
     std::vector<GeneratorMasses>::iterator point = Get(masses, evt->Get("Mzero"), evt->Get("Mhalf"), evt->Get("TanBeta") );
     if (point!=masses.end())
       AddGeneratorVariables( *evt, *point );
     else {
       //std::cerr<<"WARNING: No generator information for point (Mzero="<<evt->Get("Mzero")
       //         <<", Mhalf="<<evt->Get("Mhalf")<<", TanBeta="<<evt->Get("TanBeta")<<") found!"<<std::endl;  
     }		
  }
}




