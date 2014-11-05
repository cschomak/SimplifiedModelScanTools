// $Id: GeneratorMasses.h,v 1.2 2012/06/26 13:58:23 auterman Exp $

/*** ------------------------------------------------------------------------------------------------------- ***
     TheBetterPlotScript, a tool to plot final results, limits and exclusion contours, based on 'PlotScript'

     Christian Autermann, Hamburg University/LPC, February 2012
 *** ------------------------------------------------------------------------------------------------------- ***/

#ifndef GENERATORMASSES_H
#define GENERATORMASSES_H

#include <vector>
#include <string>

#include "Event.h"

/// class containing additional information from generators
class GeneratorMasses {
 public:
//  GeneratorMasses(){}
  double Mzero;
  double Mhalf;
  double TanBeta;
  double Mu;
  double Azero;
  double Mtop;
  double muQ;
  double Q;
  double M1;
  double M2;
  double M3;
  double MGL;
  double MUL;
  double MB1;
  double MSN;
  double MNTAU;
  double MZ1;
  double MW1;
  double MHL;
  double MUR;
  double MB2;
  double MEL;
  double MTAU1;
  double MZ2;
  double MW2;
  double MHH;
  double MDL;
  double MT1;
  double MER;
  double MTAU2;
  double MZ3;
  double MHA;
  double MDR;
  double MT2;
  double MZ4;
  double MHp;
  bool operator==(const GeneratorMasses& o){return Mzero==o.Mzero && Mhalf==o.Mhalf && TanBeta==o.TanBeta; }
};

void ReadGeneratorMasses(std::vector<GeneratorMasses>& masses, std::string file);
void Match(std::vector<GeneratorMasses>& masses, Events& evts);


#endif
