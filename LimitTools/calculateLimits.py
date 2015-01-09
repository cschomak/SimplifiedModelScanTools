#! /usr/bin/env python

import ROOT

from messageLogger import messageLogger as log
from optparse import OptionParser
import os


def loadPickles(path):
	from glob import glob
	import pickle
	result = {}
	for pklPath in glob(path):
		pklFile = open(pklPath, "r")
		result.update(pickle.load(pklFile))
	return result
	
			   
def writeDataCards():
	#~ from ROOT import TCanvas, TPad, TH1F, TH2F, TH1I, THStack, TLegend, TMath, TF1
	import pickle

	lumi = 19400.
	printLumi = "19.4"
	BR = "10"
	baseDir = "/user/schomakers/LimitTools/SimplifiedModelLimits/"
	
	
	#~ regions = ["signalCentral"]
	regions = ["signalCentral_mll_20_70"]
	#~ regions = ["signalCentral","signalCentral_100_met_cut","signalCentral_150_met_cut","signalCentral_2_jet_cut","signalCentral_3_jet_cut"]
	
	#set cmssw environment
	os.chdir("%s"%(baseDir))
	os.system ("mycmssw611")
	
	for region in regions:
	
		step_size = 20
		m_b_min = 200
		m_b_max = 700
		m_n_min = 100
		m_n_max = 700
		
		Pickles = {}
		
		m_neutr_1_fix = False
		m_neutralino_1 = "200"
		
			
		run = 0
		i = 0
		while m_b_min + i*step_size <= m_b_max:
			m_b = m_b_min + i*step_size
			M_SBOTTOM = "m_b_"+str(m_b_min + i*step_size)
			m_sbottom = str(m_b_min + i*step_size)
			j = 0
			
			while m_n_min + j*step_size <= m_n_max:
				#~ print i
				m_n = m_n_min + j*step_size
				m_neutralino_2 = str(m_n_min + j*step_size)
				#~ if m_b >= m_n:
				if m_b >= m_n and not (m_b == 320 and m_n == 260)   and not (m_b == 460 and m_n == 440)   and not (m_b == 480 and m_n == 160):
					print "m_b: "+m_sbottom
					print "m_n: "+m_neutralino_2
					
					if m_neutr_1_fix == False:
						m_neutralino_1 = str(m_n_min + j*step_size - 70)
					
					Name= "SF-OF_counts_SUSY_SimplifiedModel_Madgraph_FastSim_Dilepton_Edge_BR_%s_m_n_1_%s_m_b_%s_m_n_2_%s_8TeV_Scan_%s"%(BR,m_neutralino_1,m_sbottom,m_neutralino_2,region)
					
					os.system ("./../limit_V2 DataCards/%s.txt"%(Name))
					os.system ("rm roostats-*")
					os.system ("rm *.root")
					os.system ("rm *.log")
					os.system ("mv %s.txt.result.txt results/%s.result.txt"%(Name,Name))
					os.system ("rm %s.*"%Name)
		

	
				j += 1		
			i += 1

									
				

# This method just waits for a button to be pressed
def waitForInput():
    raw_input("Press any key to continue!")
    return

# entry point
#-------------
if (__name__ == "__main__"):
    # use option parser to allow verbose mode
    parser = OptionParser()
    parser.add_option("-v", "--verbose", dest="verbose", action="store_true", default=False,
                                  help="talk about everything")
    #~ parser.add_option("-b", "--base_path", dest="base_path", default="/user/schomakers/AnalysisData/PAT/Histos/sw532v0474/cutsV22DileptonTriggerSignal/TTJets/processedTrees_Simulation",
                                  #~ help="path to the directory containing simulated events")
    #~ parser.add_option("-n", "--nEvents", dest="nEvents", default="-1",
                                  #~ help="number of events to read (default = -1 = all). use smaller numbers for tests")
    (opts, args) = parser.parse_args()
    if (opts.verbose):
        # print out all output
        log.outputLevel = 5
    else:
        # ignore output with "debug" level
        log.outputLevel = 4

    # start
    #~ plot(opts.base_path, int(opts.nEvents), opts.observable)
    writeDataCards()
 
