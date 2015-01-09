C=g++
LD=g++

#O2 for optimization, g for debugging, pg for profiling
SPECIALFLAGS= -g #-g -Wall -pg#-O2
ROOTAUXCFLAGS=$(shell root-config --auxcflags)
ROOTCFLAGS=$(shell root-config --cflags)
ROOTLIBS=$(shell root-config --libs) #-lMath # -lMinuit
CFLAGS = $(SPECIALFLAGS) -Wall $(ROOTAUXCFLAGS)
LFLAGS = $(SPECIALFLAGS) 

RCXX=$(SPECIALFLAGS) -Wno-deprecated -Wall $(ROOTCFLAGS) 
RLXX=$(LFLAGS) $(ROOTLIBS) 

SRC=ConfigFile.cc FindNextR.cc

%.o: %.cc
		$(C) $(RCXX) -c $<

all: FindNextR

clean:
	@rm -f *.o 
	@rm -f FindNextR 


ConfigFile.o: ConfigFile.cc ConfigFile.h
		$(C) $(RCXX) -c ConfigFile.cc 

FindNextR.o: FindNextR.cc
	$(C) $(RCXX) -c FindNextR.cc

FindNextR: $(SRC:.cc=.o)
	$(LD) $(SRC:.cc=.o) $(RLXX) -o FindNextR
	@echo '-> executable FindNextR created.'

