C=c++
LD=c++
F77=g77
#O2 for optimization, g for debugging
SPECIALFLAGS=-g # -O2 -g
ROOTCFLAGS=$(shell root-config --cflags)
ROOTLIBS=$(shell root-config --libs) -lMinuit

CFLAGS = $(SPECIALFLAGS) -I. -I./include -I$(SRT_PUBLIC_CONTEXT)/include -I$(ROOTSYS)/include -Wno-deprecated
LFLAGS = $(SPECIALFLAGS) -lz 


RCXX=$(CFLAGS) $(ROOTCFLAGS)
RLXX=$(LFLAGS) $(ROOTLIBS)

#~ SRC=table.cc Overview.cc Variable.cc OldExclusionContours.cc ConfigFile.cc GeneratorMasses.cc PlotTools.cc Plotting.cc Event.cc
SRC=table.cc Overview.cc Variable.cc OldExclusionContours.cc ConfigFile.cc GeneratorMasses.cc PlotTools.cc Plotting.cc EventDilepton.cc

%.o: %.cc
		$(C) $(RCXX) -c $<

all: plotDilepton
#~ all: plotSinglePhoton8TeV
#plotSinglePhoton7TeV plotSinglePhoton8TeV plot_Combination


# common object files:
ConfigFile.o: ConfigFile.cc ConfigFile.h
		$(C) $(RCXX) -c ConfigFile.cc 

OldExclusionContours.o: OldExclusionContours.cc OldExclusionContours.h
		$(C) $(RCXX) -c OldExclusionContours.cc 

Event.o: Event.cc Event.h
		$(C) $(RCXX) -c Event.cc 

EventDiPhoton.o: EventDiPhoton.cc Event.h
		$(C) $(RCXX) -c EventDiPhoton.cc

EventDilepton.o: EventDilepton.cc Event.h
		$(C) $(RCXX) -c EventDilepton.cc  

Variable.o: Variable.cc Variable.h
		$(C) $(RCXX) -c Variable.cc 

GeneratorMasses.o: GeneratorMasses.cc GeneratorMasses.h
		$(C) $(RCXX) -c GeneratorMasses.cc 

PlotTools.o: PlotTools.cc PlotTools.h 
		$(C) $(RCXX) -c PlotTools.cc

PlotToolsDilepton.o: PlotToolsDilepton.cc PlotTools.h 
		$(C) $(RCXX) -c PlotToolsDilepton.cc

Plotting.o: Plotting.cc Plotting.h 
		$(C) $(RCXX) -c Plotting.cc 

TheLimits.o: TheLimits.cc TheLimits.h
		$(C) $(RCXX) -c TheLimits.cc 

# single photon 7 TeV specific ----------------------------------------------------------------------------------------
StyleSettings_SinglePhoton_7TeV.o: StyleSettings.h 
		$(C) $(RCXX) -c StyleSettings_SinglePhoton_7TeV.cc

plotSinglePhoton7TeV.o: StyleSettings.h 
		$(C) $(RCXX) -c plotSinglePhoton7TeV.cc 

plotSinglePhoton7TeV: $(SRC:.cc=.o) StyleSettings_SinglePhoton_7TeV.o plotSinglePhoton7TeV.o 
		$(LD) $(SRC:.cc=.o) StyleSettings_SinglePhoton_7TeV.o plotSinglePhoton7TeV.o $(RLXX) $(JCORR) -o plotSinglePhoton7TeV
		@echo '-> plotSinglePhoton7TeV executable created.'

# single photon 8 TeV specific ----------------------------------------------------------------------------------------
StyleSettings_SinglePhoton_8TeV.o: StyleSettings.h StyleSettings_SinglePhoton_8TeV.cc
		$(C) $(RCXX) -c StyleSettings_SinglePhoton_8TeV.cc

plotSinglePhoton8TeV.o: plotSinglePhoton8TeV.cc plot.h   
		$(C) $(RCXX) -c plotSinglePhoton8TeV.cc 

plotSinglePhoton8TeV: $(SRC:.cc=.o) StyleSettings_SinglePhoton_8TeV.o plotSinglePhoton8TeV.o 
		$(LD) $(SRC:.cc=.o) StyleSettings_SinglePhoton_8TeV.o plotSinglePhoton8TeV.o $(RLXX) $(JCORR) -o plotSinglePhoton8TeV
		@echo '-> plotSinglePhoton8TeV executable created.'

# single photon 8 TeV, 20 fb-1 specific ----------------------------------------------------------------------------------------
StyleSettings_SinglePhoton_8TeV20fb.o: StyleSettings.h StyleSettings_SinglePhoton_8TeV20fb.cc
		$(C) $(RCXX) -c StyleSettings_SinglePhoton_8TeV20fb.cc

plotSinglePhoton8TeV20fb.o: plotSinglePhoton8TeV20fb.cc plot.h   
		$(C) $(RCXX) -c plotSinglePhoton8TeV20fb.cc 

plotSinglePhoton8TeV20fb: $(SRC:.cc=.o) StyleSettings_SinglePhoton_8TeV20fb.o plotSinglePhoton8TeV20fb.o 
		$(LD) $(SRC:.cc=.o) StyleSettings_SinglePhoton_8TeV20fb.o plotSinglePhoton8TeV20fb.o $(RLXX) $(JCORR) -o plotSinglePhoton8TeV20fb
		@echo '-> plotSinglePhoton8TeV20fb executable created.'

# Dilepton 8 TeV specific ----------------------------------------------------------------------------------------
StyleSettings_Dilepton.o: StyleSettings.h StyleSettings_Dilepton.cc
		$(C) $(RCXX) -c StyleSettings_Dilepton.cc

plotDilepton.o: plotDilepton.cc plot.h   
		$(C) $(RCXX) -c plotDilepton.cc 

plotDilepton: $(SRC:.cc=.o) EventDilepton.o StyleSettings_Dilepton.o plotDilepton.o 
		$(LD) $(SRC:.cc=.o) StyleSettings_Dilepton.o plotDilepton.o $(RLXX) $(JCORR) -o plotDilepton
		@echo '-> plotDilepton executable created.'

# Combination specific ----------------------------------------------------------------------------------------
StyleSettings_Combination.o: StyleSettings.h StyleSettings_Combination.cc
		$(C) $(RCXX) -c StyleSettings_Combination.cc

plot_Combination.o: plot_Combination.cc plot.h StyleSettings_Combination.cc
		$(C) $(RCXX) -c plot_Combination.cc 

plot_Combination: $(SRC:.cc=.o) Event.o StyleSettings_Combination.o  plot_Combination.o 
		$(LD) $(SRC:.cc=.o) StyleSettings_Combination.o plot_Combination.o $(RLXX) $(JCORR) -o plot_Combination
		@echo '-> plot_Combination executable created.'

# di photon specific           ----------------------------------------------------------------------------------------
StyleSettings_DiPhoton.o: StyleSettings.h
		$(C) $(RCXX) -c StyleSettings_DiPhoton.cc

plotDiPhoton.o: plotDiPhoton.cc plot.h
		$(C) $(RCXX) -c plotDiPhoton.cc 

plotDiPhoton: $(SRC:.cc=.o) EventDiPhoton.o StyleSettings_DiPhoton.o Plotting.o plotDiPhoton.o 
		$(LD) $(SRC:.cc=.o) StyleSettings_DiPhoton.o EventDiPhoton.o plotDiPhoton.o Plotting.o $(RLXX) $(JCORR) -o plotDiPhoton
		@echo '-> plotDiPhoton executable created.'

clean:
		@rm -f *.o 
		@rm -f plotSinglePhoton7TeV plotSinglePhoton8TeV
