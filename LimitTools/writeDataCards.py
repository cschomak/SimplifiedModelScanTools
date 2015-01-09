#! /usr/bin/env python

import ROOT

from messageLogger import messageLogger as log
from optparse import OptionParser


def loadPickles(path):
	from glob import glob
	import pickle
	result = {}
	for pklPath in glob(path):
		pklFile = open(pklPath, "r")
		result.update(pickle.load(pklFile))
	return result
	
			   
def writeDataCards():
	from ROOT import TCanvas, TPad, TH1F, TH2F, TH1I, THStack, TLegend, TMath, TF1
	import pickle

	lumi = 19400.
	printLumi = "19.4"
	BR = "10"
	
	n_bins = 1
	n_processes = 2
	n_nuicance_parameters = 3
	
	
	
	TTbar_err = 0.076
	DY_err = 0.07
	
	
	picklePath = "/user/schomakers/GridScan/shelves"
	
	#~ regions = ["signalCentral"]
	regions = ["signalCentral_mll_20_70"]
	#~ regions = ["signalCentral","signalCentral_100_met_cut","signalCentral_150_met_cut","signalCentral_2_jet_cut","signalCentral_3_jet_cut"]
	
	for region in regions:
		
		if region == "signalCentral_mll_20_70":
			region_label = "Central Signal Region"
			observation = 860
			TTbar = 719.12
			DY = 10.34
			region_label_2 = "20 GeV < m_{ll} < 70 GeV"
		elif region == "signalCentral_2_jet_cut":
			region_label = "Central Region"
			region_label_2 = "n_{Jets} #ge 2"
		elif region == "signalCentral_3_jet_cut":
			region_label = "Central Region"
			region_label_2 = "n_{Jets} #ge 3"
		elif region == "signalCentral_100_met_cut":
			region_label = "Central Region"
			region_label_2 = "#slash{E}_{T} > 100 GeV"
		elif region == "signalCentral_150_met_cut":
			region_label = "Central Region"
			region_label_2 = "#slash{E}_{T} > 150 GeV"
		elif "signalCentral" in region:
			observation = 2680.0
			TTbar = 2326.03
			DY = 66.556
			region_label = "Central Signal Region"
			region_label_2 = ""

	
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
					#~ print "%s/%s.pkl"%(picklePath,Name)
					Pickles["%s_%s_%s"%(m_neutralino_1,m_sbottom,m_neutralino_2)] = loadPickles("%s/%s.pkl"%(picklePath,Name))
		
					Value = Pickles["%s_%s_%s"%(m_neutralino_1,m_sbottom,m_neutralino_2)]["Signal"]["val"]
					
					if Pickles["%s_%s_%s"%(m_neutralino_1,m_sbottom,m_neutralino_2)]["Signal"]["val"] > 0:
						#~ err = 1.5
						err = 1 + Pickles["%s_%s_%s"%(m_neutralino_1,m_sbottom,m_neutralino_2)]["Signal"]["err"] / Pickles["%s_%s_%s"%(m_neutralino_1,m_sbottom,m_neutralino_2)]["Signal"]["val"]
					else:
						err = 0
					
					firstGuess = 2 * TMath.Sqrt(err**2+TTbar+DY+(TTbar_err*TTbar)**2+(DY_err*DY)**2) / Value
					
					DataCard = open("DataCards/%s.txt"%Name,'w')
					DataCard.write("# R_firstguess = %s \n"%str(firstGuess))
					DataCard.write("imax %s number of bins \n"%n_bins)
					DataCard.write("jmax %s number of processes minus 1 \n"%n_processes)
					DataCard.write("kmax %s number of nuisance parameters \n"%n_nuicance_parameters)
					DataCard.write("---------------------------------------------------------------------------------------------------------------------------------- \n")
					DataCard.write("bin          Central \n")
					DataCard.write("observation  %s \n"%observation)
					DataCard.write("---------------------------------------------------------------------------------------------------------------------------------- \n")
					DataCard.write("bin                                 Central   Central   Central \n")
					DataCard.write("process                             SUSY      ZJets     ttJets \n")
					DataCard.write("process                             0         1         2      \n")
					DataCard.write("rate                                %s       %s         %s \n"%(Value,DY,TTbar))
					DataCard.write("---------------------------------------------------------------------------------------------------------------------------------- \n")
					DataCard.write("Stat_signal             lnN         %s       -         -      \n"%str(err))
					DataCard.write("R_SF/OF                 lnN         -         -         %s \n"%(str(1+TTbar_err)))
					DataCard.write("ZJets_stat              lnN         -         %s      - \n"%(str(1+DY_err)))

	
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
 
