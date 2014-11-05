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
	from defs import Region, defineMyColors, myColors, BasicCuts, sbottom_masses
	from math import sqrt
		
	
	lumi = 19400.
	printLumi = "19.4"
	
	n_bins = 6
	n_processes = 2
	n_nuicance_parameters = 15

	m_neutr_1_fix = True
	m_neutralino_1 = "100"
	
	
	if m_neutr_1_fix == False:
		generalSignalSample = "T6bblledge"
		path = "/user/schomakers/SimplifiedModelScans/shelvesT6bblledge"
	else:
		generalSignalSample = "T6bbslepton"
		path = "/user/schomakers/SimplifiedModelScans/shelvesT6bbllslepton"
	generalSignalLabel = "SUSY_Simplified_Model_Madgraph_FastSim_%s"%(generalSignalSample)
	
	lowMllCentrObservation = 860
	lowMllCentrTTbar = 722
	lowMllCentrTTbarSystUncertainty = 0.04
	lowMllCentrTTbarStatUncertainty = 0.037
	lowMllCentrDY = 8.2
	lowMllCentrDYUncertainty = 0.32
	
	ZPeakCentrObservation = 487
	ZPeakCentrTTbar = 355
	ZPeakCentrTTbarSystUncertainty = 0.039
	ZPeakCentrTTbarStatUncertainty = 0.054
	ZPeakCentrDY = 116
	ZPeakCentrDYUncertainty = 0.18
	
	highMllCentrObservation = 818
	highMllCentrTTbar = 768
	highMllCentrTTbarSystUncertainty = 0.04
	highMllCentrTTbarStatUncertainty = 0.036
	highMllCentrDY = 2.5
	highMllCentrDYUncertainty = 0.32
	
	lowMllForwObservation = 163
	lowMllForwTTbar = 155
	lowMllForwTTbarSystUncertainty = 0.065
	lowMllForwTTbarStatUncertainty = 0.080
	lowMllForwDY = 2.5
	lowMllForwDYUncertainty = 0.4
	
	ZPeakForwObservation = 170
	ZPeakForwTTbar = 131
	ZPeakForwTTbarSystUncertainty = 0.061
	ZPeakForwTTbarStatUncertainty = 0.092
	ZPeakForwDY = 42
	ZPeakForwDYUncertainty = 0.21
	
	highMllForwObservation = 368
	highMllForwTTbar = 430
	highMllForwTTbarSystUncertainty = 0.063
	highMllForwTTbarStatUncertainty = 0.051
	highMllForwDY = 1.1
	highMllForwDYUncertainty = 0.36
	
	regions = ["Barrel_lowMll","Barrel_highMll","Barrel_ZPeak","Endcap_lowMll","Endcap_highMll","Endcap_ZPeak",]
	uncertainties = ["ISRUncertainty","pileupUncertainty","metUncertainty","jetUncertainty","PDFUncertainty","leptonUncertainty"]
	

	step_size = 25
	m_b_min = 200
	m_b_max = 700
	if m_neutr_1_fix == False:
		m_n_min = 100
	else:
		m_n_min = 150
	m_n_max = 700
	
	TriggerEffUncertainty = 0.05
	FastSimUncertainty = 0.02
	LumiUncertainty = 0.026
	
	
	
	title = "Simplified Model Scan; m(#tilde{b}) [GeV]; m(#tilde{#chi}_{2}^{0}) [GeV]"
	
	nbins_x = (m_b_max - m_b_min)/step_size + 1
	x_min =  m_b_min - 0.5 * step_size
	x_max =  m_b_max + 0.5 * step_size
	nbins_y = (m_n_max - m_n_min)/step_size +1
	y_min =  m_n_min - 0.5 * step_size
	y_max =  m_n_max + 0.5 * step_size				
	
				
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
			if m_b >= m_n:
			#~ if m_b >= m_n and not (m_b == 350 and m_n > 250):
			#~ if m_b >= m_n and not (m_b == 320 and m_n == 260)   and not (m_b == 460 and m_n == 440)   and not (m_b == 480 and m_n == 160):
			#~ if m_b >= m_n and not (m_b == 475 and m_n == 200):
				#~ print "m_b: "+m_sbottom
				#~ print "m_n: "+m_neutralino_2
				
				if m_neutr_1_fix == False:
					m_neutralino_1 = str(m_n_min + j*step_size - 70)
					
				xsection = getattr(sbottom_masses, M_SBOTTOM).cross_section

				Pickles = {}
				Yields = {}
				MCEvents = {}
				statUncertainties = {}
				systUncertainties = {}
				PFMet = {}
				nJets = {}
				Leptonpt = {}
				Pileup = {}
				PDF= {}
				ISR= {}			
				
				
				for region in regions:

					Pickles["%s_%s_%s_EE"%(m_neutralino_1,m_sbottom,m_neutralino_2)] = loadPickles("%s/%s_%s_%s_%s_8TeV_%s_EE.pkl"%(path,generalSignalLabel,m_sbottom,m_neutralino_2,m_neutralino_1,region))
					Pickles["%s_%s_%s_EMu"%(m_neutralino_1,m_sbottom,m_neutralino_2)] = loadPickles("%s/%s_%s_%s_%s_8TeV_%s_EMu.pkl"%(path,generalSignalLabel,m_sbottom,m_neutralino_2,m_neutralino_1,region))
					Pickles["%s_%s_%s_MuMu"%(m_neutralino_1,m_sbottom,m_neutralino_2)] = loadPickles("%s/%s_%s_%s_%s_8TeV_%s_MuMu.pkl"%(path,generalSignalLabel,m_sbottom,m_neutralino_2,m_neutralino_1,region))
					
					MCEvents["EE_%s"%region] = Pickles["%s_%s_%s_EE"%(m_neutralino_1,m_sbottom,m_neutralino_2)]["EE"]["EEMCEvents"]
					MCEvents["EMu_%s"%region] = Pickles["%s_%s_%s_EMu"%(m_neutralino_1,m_sbottom,m_neutralino_2)]["EMu"]["EMuMCEvents"]
					MCEvents["MuMu_%s"%region] =  Pickles["%s_%s_%s_MuMu"%(m_neutralino_1,m_sbottom,m_neutralino_2)]["MuMu"]["MuMuMCEvents"]
					MCEvents["SFOF_%s"%region] = MCEvents["EE_%s"%region] + MCEvents["MuMu_%s"%region] - MCEvents["EMu_%s"%region]
					MCEvents["SFOF_%s"%region] = max(MCEvents["SFOF_%s"%region],0)
					
					Yields["EE_%s"%region] = Pickles["%s_%s_%s_EE"%(m_neutralino_1,m_sbottom,m_neutralino_2)]["EE"]["EEval"]
					Yields["EMu_%s"%region] = Pickles["%s_%s_%s_EMu"%(m_neutralino_1,m_sbottom,m_neutralino_2)]["EMu"]["EMuval"]
					Yields["MuMu_%s"%region] =  Pickles["%s_%s_%s_MuMu"%(m_neutralino_1,m_sbottom,m_neutralino_2)]["MuMu"]["MuMuval"]
					Yields["SFOF_%s"%region] = Yields["EE_%s"%region] + Yields["MuMu_%s"%region] - Yields["EMu_%s"%region]
					Yields["SFOF_%s"%region] = max(Yields["SFOF_%s"%region],0)

					
					if MCEvents["SFOF_%s"%region] > 0:
						statUncertainties["SFOF_%s"%region] = sqrt(MCEvents["SFOF_%s"%region])/MCEvents["SFOF_%s"%region]
					else:
						statUncertainties["SFOF_%s"%region] = 0
					
					### MET Uncertainty
					PFMet["Mean_%s"%region] = Pickles["%s_%s_%s_EE"%(m_neutralino_1,m_sbottom,m_neutralino_2)]["EE"]["EEPFMetMean"] + Pickles["%s_%s_%s_MuMu"%(m_neutralino_1,m_sbottom,m_neutralino_2)]["MuMu"]["MuMuPFMetMean"] - Pickles["%s_%s_%s_EMu"%(m_neutralino_1,m_sbottom,m_neutralino_2)]["EMu"]["EMuPFMetMean"] 
					
					PFMet["JetEnUp_%s"%region] = Pickles["%s_%s_%s_EE"%(m_neutralino_1,m_sbottom,m_neutralino_2)]["EE"]["EEPFMetJetEnUp"] + Pickles["%s_%s_%s_MuMu"%(m_neutralino_1,m_sbottom,m_neutralino_2)]["MuMu"]["MuMuPFMetJetEnUp"] - Pickles["%s_%s_%s_EMu"%(m_neutralino_1,m_sbottom,m_neutralino_2)]["EMu"]["EMuPFMetJetEnUp"]  
					PFMet["JetEnDown_%s"%region] = Pickles["%s_%s_%s_EE"%(m_neutralino_1,m_sbottom,m_neutralino_2)]["EE"]["EEPFMetJetEnDown"] + Pickles["%s_%s_%s_MuMu"%(m_neutralino_1,m_sbottom,m_neutralino_2)]["MuMu"]["MuMuPFMetJetEnDown"] - Pickles["%s_%s_%s_EMu"%(m_neutralino_1,m_sbottom,m_neutralino_2)]["EMu"]["EMuPFMetJetEnDown"]  
					
					PFMet["JetResUp_%s"%region] = Pickles["%s_%s_%s_EE"%(m_neutralino_1,m_sbottom,m_neutralino_2)]["EE"]["EEpatPFMetJetResUp"] + Pickles["%s_%s_%s_MuMu"%(m_neutralino_1,m_sbottom,m_neutralino_2)]["MuMu"]["MuMupatPFMetJetResUp"] - Pickles["%s_%s_%s_EMu"%(m_neutralino_1,m_sbottom,m_neutralino_2)]["EMu"]["EMupatPFMetJetResUp"]  
					PFMet["JetResDown_%s"%region] = Pickles["%s_%s_%s_EE"%(m_neutralino_1,m_sbottom,m_neutralino_2)]["EE"]["EEpatPFMetJetResDown"] + Pickles["%s_%s_%s_MuMu"%(m_neutralino_1,m_sbottom,m_neutralino_2)]["MuMu"]["MuMupatPFMetJetResDown"] - Pickles["%s_%s_%s_EMu"%(m_neutralino_1,m_sbottom,m_neutralino_2)]["EMu"]["EMupatPFMetJetResDown"]  
					
					PFMet["JetElectronEnUp_%s"%region] = Pickles["%s_%s_%s_EE"%(m_neutralino_1,m_sbottom,m_neutralino_2)]["EE"]["EEpatPFMetElectronEnUp"] + Pickles["%s_%s_%s_MuMu"%(m_neutralino_1,m_sbottom,m_neutralino_2)]["MuMu"]["MuMupatPFMetElectronEnUp"] - Pickles["%s_%s_%s_EMu"%(m_neutralino_1,m_sbottom,m_neutralino_2)]["EMu"]["EMupatPFMetElectronEnUp"]  
					PFMet["JetElectronEnDown_%s"%region] = Pickles["%s_%s_%s_EE"%(m_neutralino_1,m_sbottom,m_neutralino_2)]["EE"]["EEpatPFMetElectronEnDown"] + Pickles["%s_%s_%s_MuMu"%(m_neutralino_1,m_sbottom,m_neutralino_2)]["MuMu"]["MuMupatPFMetElectronEnDown"] - Pickles["%s_%s_%s_EMu"%(m_neutralino_1,m_sbottom,m_neutralino_2)]["EMu"]["EMupatPFMetElectronEnDown"]  

					PFMet["JetMuonEnUp_%s"%region] = Pickles["%s_%s_%s_EE"%(m_neutralino_1,m_sbottom,m_neutralino_2)]["EE"]["EEpatPFMetMuonEnUp"] + Pickles["%s_%s_%s_MuMu"%(m_neutralino_1,m_sbottom,m_neutralino_2)]["MuMu"]["MuMupatPFMetMuonEnUp"] - Pickles["%s_%s_%s_EMu"%(m_neutralino_1,m_sbottom,m_neutralino_2)]["EMu"]["EMupatPFMetMuonEnUp"]  
					PFMet["JetMuonEnDown_%s"%region]  = Pickles["%s_%s_%s_EE"%(m_neutralino_1,m_sbottom,m_neutralino_2)]["EE"]["EEpatPFMetMuonEnDown"] + Pickles["%s_%s_%s_MuMu"%(m_neutralino_1,m_sbottom,m_neutralino_2)]["MuMu"]["MuMupatPFMetMuonEnDown"] - Pickles["%s_%s_%s_EMu"%(m_neutralino_1,m_sbottom,m_neutralino_2)]["EMu"]["EMupatPFMetMuonEnDown"]  
					
					PFMet["JetTauEnUp_%s"%region]  = Pickles["%s_%s_%s_EE"%(m_neutralino_1,m_sbottom,m_neutralino_2)]["EE"]["EEpatPFMetTauEnUp"] + Pickles["%s_%s_%s_MuMu"%(m_neutralino_1,m_sbottom,m_neutralino_2)]["MuMu"]["MuMupatPFMetTauEnUp"] - Pickles["%s_%s_%s_EMu"%(m_neutralino_1,m_sbottom,m_neutralino_2)]["EMu"]["EMupatPFMetTauEnUp"]  
					PFMet["JetTauEnDown_%s"%region] = Pickles["%s_%s_%s_EE"%(m_neutralino_1,m_sbottom,m_neutralino_2)]["EE"]["EEpatPFMetTauEnDown"] + Pickles["%s_%s_%s_MuMu"%(m_neutralino_1,m_sbottom,m_neutralino_2)]["MuMu"]["MuMupatPFMetTauEnDown"] - Pickles["%s_%s_%s_EMu"%(m_neutralino_1,m_sbottom,m_neutralino_2)]["EMu"]["EMupatPFMetTauEnDown"]  
					
					PFMet["JetUnclusteredEnUp_%s"%region] = Pickles["%s_%s_%s_EE"%(m_neutralino_1,m_sbottom,m_neutralino_2)]["EE"]["EEpatPFMetUnclusteredEnUp"] + Pickles["%s_%s_%s_MuMu"%(m_neutralino_1,m_sbottom,m_neutralino_2)]["MuMu"]["MuMupatPFMetUnclusteredEnUp"] - Pickles["%s_%s_%s_EMu"%(m_neutralino_1,m_sbottom,m_neutralino_2)]["EMu"]["EMupatPFMetUnclusteredEnUp"]  
					PFMet["JetUnclusteredEnDown_%s"%region] = Pickles["%s_%s_%s_EE"%(m_neutralino_1,m_sbottom,m_neutralino_2)]["EE"]["EEpatPFMetUnclusteredEnDown"] + Pickles["%s_%s_%s_MuMu"%(m_neutralino_1,m_sbottom,m_neutralino_2)]["MuMu"]["MuMupatPFMetUnclusteredEnDown"] - Pickles["%s_%s_%s_EMu"%(m_neutralino_1,m_sbottom,m_neutralino_2)]["EMu"]["EMupatPFMetUnclusteredEnDown"]  
					
					if PFMet["Mean_%s"%region] > 0:
						systUncertainties["metUncertainty_%s"%region] = sqrt( max((PFMet["JetEnUp_%s"%region]-PFMet["Mean_%s"%region])/PFMet["Mean_%s"%region],(PFMet["JetEnDown_%s"%region]-PFMet["Mean_%s"%region])/PFMet["Mean_%s"%region])**2 + max((PFMet["JetResUp_%s"%region]-PFMet["Mean_%s"%region])/PFMet["Mean_%s"%region],(PFMet["JetResDown_%s"%region]-PFMet["Mean_%s"%region])/PFMet["Mean_%s"%region])**2 + max((PFMet["JetElectronEnUp_%s"%region]-PFMet["Mean_%s"%region])/PFMet["Mean_%s"%region],(PFMet["JetElectronEnDown_%s"%region]-PFMet["Mean_%s"%region])/PFMet["Mean_%s"%region])**2 + max((PFMet["JetMuonEnUp_%s"%region]-PFMet["Mean_%s"%region])/PFMet["Mean_%s"%region],(PFMet["JetMuonEnDown_%s"%region]-PFMet["Mean_%s"%region])/PFMet["Mean_%s"%region])**2 + max((PFMet["JetTauEnUp_%s"%region]-PFMet["Mean_%s"%region])/PFMet["Mean_%s"%region],(PFMet["JetTauEnDown_%s"%region]-PFMet["Mean_%s"%region])/PFMet["Mean_%s"%region])**2 + max((PFMet["JetUnclusteredEnUp_%s"%region]-PFMet["Mean_%s"%region])/PFMet["Mean_%s"%region],(PFMet["JetUnclusteredEnDown_%s"%region]-PFMet["Mean_%s"%region])/PFMet["Mean_%s"%region])**2)
					else:
						systUncertainties["metUncertainty_%s"%region] = 0
					
					### Jet Uncertainty
					
					nJets["Mean_%s"%region] = Pickles["%s_%s_%s_EE"%(m_neutralino_1,m_sbottom,m_neutralino_2)]["EE"]["EEnJetsMean"] + Pickles["%s_%s_%s_MuMu"%(m_neutralino_1,m_sbottom,m_neutralino_2)]["MuMu"]["MuMunJetsMean"] - Pickles["%s_%s_%s_EMu"%(m_neutralino_1,m_sbottom,m_neutralino_2)]["EMu"]["EMunJetsMean"] 
					
					nJets["nJetsEnUp_%s"%region] = Pickles["%s_%s_%s_EE"%(m_neutralino_1,m_sbottom,m_neutralino_2)]["EE"]["EEnJetsEnUp"] + Pickles["%s_%s_%s_MuMu"%(m_neutralino_1,m_sbottom,m_neutralino_2)]["MuMu"]["MuMunJetsEnUp"] - Pickles["%s_%s_%s_EMu"%(m_neutralino_1,m_sbottom,m_neutralino_2)]["EMu"]["EMunJetsEnUp"]  
					nJets["nJetsEnDown_%s"%region] = Pickles["%s_%s_%s_EE"%(m_neutralino_1,m_sbottom,m_neutralino_2)]["EE"]["EEnJetsEnDown"] + Pickles["%s_%s_%s_MuMu"%(m_neutralino_1,m_sbottom,m_neutralino_2)]["MuMu"]["MuMunJetsEnDown"] - Pickles["%s_%s_%s_EMu"%(m_neutralino_1,m_sbottom,m_neutralino_2)]["EMu"]["EMunJetsEnDown"]  
					
					nJets["nJetsResUp_%s"%region] = Pickles["%s_%s_%s_EE"%(m_neutralino_1,m_sbottom,m_neutralino_2)]["EE"]["EEnJetsResUp"] + Pickles["%s_%s_%s_MuMu"%(m_neutralino_1,m_sbottom,m_neutralino_2)]["MuMu"]["MuMunJetsResUp"] - Pickles["%s_%s_%s_EMu"%(m_neutralino_1,m_sbottom,m_neutralino_2)]["EMu"]["EMunJetsResUp"]  
					nJets["nJetsResDown_%s"%region] = Pickles["%s_%s_%s_EE"%(m_neutralino_1,m_sbottom,m_neutralino_2)]["EE"]["EEnJetsResDown"] + Pickles["%s_%s_%s_MuMu"%(m_neutralino_1,m_sbottom,m_neutralino_2)]["MuMu"]["MuMunJetsResDown"] - Pickles["%s_%s_%s_EMu"%(m_neutralino_1,m_sbottom,m_neutralino_2)]["EMu"]["EMunJetsResDown"]  
					
					if nJets["Mean_%s"%region] > 0:
						systUncertainties["jetUncertainty_%s"%region] = sqrt( max((nJets["nJetsEnUp_%s"%region]-nJets["Mean_%s"%region])/nJets["Mean_%s"%region],(nJets["nJetsEnDown_%s"%region]-nJets["Mean_%s"%region])/nJets["Mean_%s"%region])**2 + max((nJets["nJetsResUp_%s"%region]-nJets["Mean_%s"%region])/nJets["Mean_%s"%region],(nJets["nJetsResDown_%s"%region]-nJets["Mean_%s"%region])/nJets["Mean_%s"%region])**2 )
					else:
						systUncertainties["jetUncertainty_%s"%region] = 0
					
					### Lepton Uncertainty
					
					Leptonpt["Mean_%s"%region] = Pickles["%s_%s_%s_EE"%(m_neutralino_1,m_sbottom,m_neutralino_2)]["EE"]["EEleptonptMean"] + Pickles["%s_%s_%s_MuMu"%(m_neutralino_1,m_sbottom,m_neutralino_2)]["MuMu"]["MuMuleptonptMean"] - Pickles["%s_%s_%s_EMu"%(m_neutralino_1,m_sbottom,m_neutralino_2)]["EMu"]["EMuleptonptMean"] 
					
					Leptonpt["EEMean_%s"%region] = Pickles["%s_%s_%s_EE"%(m_neutralino_1,m_sbottom,m_neutralino_2)]["EE"]["EEleptonptMean"]
					Leptonpt["EEScaleUp_%s"%region] = Pickles["%s_%s_%s_EE"%(m_neutralino_1,m_sbottom,m_neutralino_2)]["EE"]["EEleptonptScaleUp"]
					Leptonpt["EEScaleDown_%s"%region] = Pickles["%s_%s_%s_EE"%(m_neutralino_1,m_sbottom,m_neutralino_2)]["EE"]["EEleptonptScaleUp"]
					
					if Leptonpt["EEMean_%s"%region] > 0:
						systUncertainties["EEleptonUncertainty_%s"%region] = sqrt(max(((Leptonpt["EEScaleUp_%s"%region]-Leptonpt["EEMean_%s"%region])/Leptonpt["EEMean_%s"%region])**2, ((Leptonpt["EEScaleDown_%s"%region]-Leptonpt["EEMean_%s"%region])/Leptonpt["EEMean_%s"%region])**2))
					else:
						systUncertainties["EEleptonUncertainty_%s"%region] = 0
					
					Leptonpt["MuMuMean_%s"%region] = Pickles["%s_%s_%s_MuMu"%(m_neutralino_1,m_sbottom,m_neutralino_2)]["MuMu"]["MuMuleptonptMean"]
					Leptonpt["MuMuScaleUp_%s"%region] = Pickles["%s_%s_%s_MuMu"%(m_neutralino_1,m_sbottom,m_neutralino_2)]["MuMu"]["MuMuleptonptScaleUp"]
					Leptonpt["MuMuScaleDown_%s"%region] = Pickles["%s_%s_%s_MuMu"%(m_neutralino_1,m_sbottom,m_neutralino_2)]["MuMu"]["MuMuleptonptScaleUp"]
					
					if Leptonpt["MuMuMean_%s"%region] > 0:
						systUncertainties["MuMuleptonUncertainty_%s"%region] = sqrt(max(((Leptonpt["MuMuScaleUp_%s"%region]-Leptonpt["MuMuMean_%s"%region])/Leptonpt["MuMuMean_%s"%region])**2, ((Leptonpt["MuMuScaleDown_%s"%region]-Leptonpt["MuMuMean_%s"%region])/Leptonpt["MuMuMean_%s"%region])**2))
					else:
						systUncertainties["MuMuleptonUncertainty_%s"%region] = 0
					
					Leptonpt["EMuMean_%s"%region] = Pickles["%s_%s_%s_EMu"%(m_neutralino_1,m_sbottom,m_neutralino_2)]["EMu"]["EMuleptonptMean"]
					Leptonpt["EMuScaleUp1_%s"%region] = Pickles["%s_%s_%s_EMu"%(m_neutralino_1,m_sbottom,m_neutralino_2)]["EMu"]["EMuleptonpt1ScaleUp"]
					Leptonpt["EMuScaleUp2_%s"%region] = Pickles["%s_%s_%s_EMu"%(m_neutralino_1,m_sbottom,m_neutralino_2)]["EMu"]["EMuleptonpt2ScaleUp"]
					Leptonpt["EMuScaleDown1_%s"%region] = Pickles["%s_%s_%s_EMu"%(m_neutralino_1,m_sbottom,m_neutralino_2)]["EMu"]["EMuleptonpt1ScaleUp"]
					Leptonpt["EMuScaleDown2_%s"%region] = Pickles["%s_%s_%s_EMu"%(m_neutralino_1,m_sbottom,m_neutralino_2)]["EMu"]["EMuleptonpt2ScaleUp"]
					
					if Leptonpt["EMuMean_%s"%region] > 0:
						systUncertainties["EMuleptonUncertainty_%s"%region] = sqrt( max((Leptonpt["EMuScaleUp1_%s"%region]-Leptonpt["EMuMean_%s"%region])/Leptonpt["EMuMean_%s"%region],(Leptonpt["EMuScaleUp2_%s"%region]-Leptonpt["EMuMean_%s"%region])/Leptonpt["EMuMean_%s"%region])**2 + max((Leptonpt["EMuScaleDown1_%s"%region]-Leptonpt["EMuMean_%s"%region])/Leptonpt["EMuMean_%s"%region],(Leptonpt["EMuScaleDown2_%s"%region]-Leptonpt["EMuMean_%s"%region])/Leptonpt["EMuMean_%s"%region])**2 )
					else:
						systUncertainties["EMuleptonUncertainty_%s"%region] = 0
					
					if Leptonpt["Mean_%s"%region] > 0:
						systUncertainties["leptonUncertainty_%s"%region] = sqrt((Leptonpt["EEMean_%s"%region]*systUncertainties["EEleptonUncertainty_%s"%region])**2 + (Leptonpt["MuMuMean_%s"%region]*systUncertainties["MuMuleptonUncertainty_%s"%region])**2 + (Leptonpt["EMuMean_%s"%region]*systUncertainties["EMuleptonUncertainty_%s"%region])**2)/Leptonpt["Mean_%s"%region]
					else:
						systUncertainties["leptonUncertainty_%s"%region] = 0
					
					###  Pileup Uncertainty
					Pileup["Mean_%s"%region] = Pickles["%s_%s_%s_EE"%(m_neutralino_1,m_sbottom,m_neutralino_2)]["EE"]["EEPileupMean"] + Pickles["%s_%s_%s_MuMu"%(m_neutralino_1,m_sbottom,m_neutralino_2)]["MuMu"]["MuMuPileupMean"] - Pickles["%s_%s_%s_EMu"%(m_neutralino_1,m_sbottom,m_neutralino_2)]["EMu"]["EMuPileupMean"] 
					
					Pileup["PileupUp_%s"%region] = Pickles["%s_%s_%s_EE"%(m_neutralino_1,m_sbottom,m_neutralino_2)]["EE"]["EEPileupUp"] + Pickles["%s_%s_%s_MuMu"%(m_neutralino_1,m_sbottom,m_neutralino_2)]["MuMu"]["MuMuPileupUp"] - Pickles["%s_%s_%s_EMu"%(m_neutralino_1,m_sbottom,m_neutralino_2)]["EMu"]["EMuPileupUp"]  
					Pileup["PileupDown_%s"%region] = Pickles["%s_%s_%s_EE"%(m_neutralino_1,m_sbottom,m_neutralino_2)]["EE"]["EEPileupDown"] + Pickles["%s_%s_%s_MuMu"%(m_neutralino_1,m_sbottom,m_neutralino_2)]["MuMu"]["MuMuPileupDown"] - Pickles["%s_%s_%s_EMu"%(m_neutralino_1,m_sbottom,m_neutralino_2)]["EMu"]["EMuPileupDown"]  
					
					if Pileup["Mean_%s"%region] > 0 and Pileup["PileupDown_%s"%region] > 0:
						systUncertainties["pileupUncertainty_%s"%region] = sqrt( max((Pileup["PileupUp_%s"%region]-Pileup["Mean_%s"%region])/Pileup["Mean_%s"%region],(Pileup["PileupDown_%s"%region] -Pileup["Mean_%s"%region])/Pileup["PileupDown_%s"%region])**2 )
					elif Pileup["Mean_%s"%region] > 0:
						systUncertainties["pileupUncertainty_%s"%region] = (Pileup["PileupUp_%s"%region]-Pileup["Mean_%s"%region])/Pileup["Mean_%s"%region]
					elif Pileup["PileupDown_%s"%region] > 0:
						systUncertainties["pileupUncertainty_%s"%region] = (Pileup["PileupDown_%s"%region] -Pileup["Mean_%s"%region])/Pileup["PileupDown_%s"%region]
					else:
						systUncertainties["pileupUncertainty_%s"%region] = 0
					
					### PDF Uncertainty
					PDF["CT10Mean_%s"%region] = Pickles["%s_%s_%s_EE"%(m_neutralino_1,m_sbottom,m_neutralino_2)]["EE"]["EECT10Mean"] + Pickles["%s_%s_%s_MuMu"%(m_neutralino_1,m_sbottom,m_neutralino_2)]["MuMu"]["MuMuCT10Mean"] - Pickles["%s_%s_%s_EMu"%(m_neutralino_1,m_sbottom,m_neutralino_2)]["EMu"]["EMuCT10Mean"] 
					PDF["CT10AbsMean_%s"%region] = Pickles["%s_%s_%s_EE"%(m_neutralino_1,m_sbottom,m_neutralino_2)]["EE"]["EECT10AbsMean"] + Pickles["%s_%s_%s_MuMu"%(m_neutralino_1,m_sbottom,m_neutralino_2)]["MuMu"]["MuMuCT10AbsMean"] - Pickles["%s_%s_%s_EMu"%(m_neutralino_1,m_sbottom,m_neutralino_2)]["EMu"]["EMuCT10AbsMean"] 
					PDF["CT10Up_%s"%region] = Pickles["%s_%s_%s_EE"%(m_neutralino_1,m_sbottom,m_neutralino_2)]["EE"]["EECT10Up"] + Pickles["%s_%s_%s_MuMu"%(m_neutralino_1,m_sbottom,m_neutralino_2)]["MuMu"]["MuMuCT10Up"] - Pickles["%s_%s_%s_EMu"%(m_neutralino_1,m_sbottom,m_neutralino_2)]["EMu"]["EMuCT10Up"] 
					PDF["CT10AbsUp_%s"%region] = Pickles["%s_%s_%s_EE"%(m_neutralino_1,m_sbottom,m_neutralino_2)]["EE"]["EECT10AbsUp"] + Pickles["%s_%s_%s_MuMu"%(m_neutralino_1,m_sbottom,m_neutralino_2)]["MuMu"]["MuMuCT10AbsUp"] - Pickles["%s_%s_%s_EMu"%(m_neutralino_1,m_sbottom,m_neutralino_2)]["EMu"]["EMuCT10AbsUp"] 
					PDF["CT10Down_%s"%region] = Pickles["%s_%s_%s_EE"%(m_neutralino_1,m_sbottom,m_neutralino_2)]["EE"]["EECT10Down"] + Pickles["%s_%s_%s_MuMu"%(m_neutralino_1,m_sbottom,m_neutralino_2)]["MuMu"]["MuMuCT10Down"] - Pickles["%s_%s_%s_EMu"%(m_neutralino_1,m_sbottom,m_neutralino_2)]["EMu"]["EMuCT10Down"] 
					PDF["CT10AbsDown_%s"%region] = Pickles["%s_%s_%s_EE"%(m_neutralino_1,m_sbottom,m_neutralino_2)]["EE"]["EECT10AbsDown"] + Pickles["%s_%s_%s_MuMu"%(m_neutralino_1,m_sbottom,m_neutralino_2)]["MuMu"]["MuMuCT10AbsDown"] - Pickles["%s_%s_%s_EMu"%(m_neutralino_1,m_sbottom,m_neutralino_2)]["EMu"]["EMuCT10AbsDown"] 
					
					PDF["MSTWMean_%s"%region] = Pickles["%s_%s_%s_EE"%(m_neutralino_1,m_sbottom,m_neutralino_2)]["EE"]["EEMSTWMean"] + Pickles["%s_%s_%s_MuMu"%(m_neutralino_1,m_sbottom,m_neutralino_2)]["MuMu"]["MuMuMSTWMean"] - Pickles["%s_%s_%s_EMu"%(m_neutralino_1,m_sbottom,m_neutralino_2)]["EMu"]["EMuMSTWMean"] 
					PDF["MSTWAbsMean_%s"%region] = Pickles["%s_%s_%s_EE"%(m_neutralino_1,m_sbottom,m_neutralino_2)]["EE"]["EEMSTWAbsMean"] + Pickles["%s_%s_%s_MuMu"%(m_neutralino_1,m_sbottom,m_neutralino_2)]["MuMu"]["MuMuMSTWAbsMean"] - Pickles["%s_%s_%s_EMu"%(m_neutralino_1,m_sbottom,m_neutralino_2)]["EMu"]["EMuMSTWAbsMean"] 
					PDF["MSTWUp_%s"%region] = Pickles["%s_%s_%s_EE"%(m_neutralino_1,m_sbottom,m_neutralino_2)]["EE"]["EEMSTWUp"] + Pickles["%s_%s_%s_MuMu"%(m_neutralino_1,m_sbottom,m_neutralino_2)]["MuMu"]["MuMuMSTWUp"] - Pickles["%s_%s_%s_EMu"%(m_neutralino_1,m_sbottom,m_neutralino_2)]["EMu"]["EMuMSTWUp"] 
					PDF["MSTWAbsUp_%s"%region] = Pickles["%s_%s_%s_EE"%(m_neutralino_1,m_sbottom,m_neutralino_2)]["EE"]["EEMSTWAbsUp"] + Pickles["%s_%s_%s_MuMu"%(m_neutralino_1,m_sbottom,m_neutralino_2)]["MuMu"]["MuMuMSTWAbsUp"] - Pickles["%s_%s_%s_EMu"%(m_neutralino_1,m_sbottom,m_neutralino_2)]["EMu"]["EMuMSTWAbsUp"] 
					PDF["MSTWDown_%s"%region] = Pickles["%s_%s_%s_EE"%(m_neutralino_1,m_sbottom,m_neutralino_2)]["EE"]["EEMSTWDown"] + Pickles["%s_%s_%s_MuMu"%(m_neutralino_1,m_sbottom,m_neutralino_2)]["MuMu"]["MuMuMSTWDown"] - Pickles["%s_%s_%s_EMu"%(m_neutralino_1,m_sbottom,m_neutralino_2)]["EMu"]["EMuMSTWDown"] 
					PDF["MSTWAbsDown_%s"%region] = Pickles["%s_%s_%s_EE"%(m_neutralino_1,m_sbottom,m_neutralino_2)]["EE"]["EEMSTWAbsDown"] + Pickles["%s_%s_%s_MuMu"%(m_neutralino_1,m_sbottom,m_neutralino_2)]["MuMu"]["MuMuMSTWAbsDown"] - Pickles["%s_%s_%s_EMu"%(m_neutralino_1,m_sbottom,m_neutralino_2)]["EMu"]["EMuMSTWAbsDown"] 
					
					PDF["NNPDFMean_%s"%region] = Pickles["%s_%s_%s_EE"%(m_neutralino_1,m_sbottom,m_neutralino_2)]["EE"]["EENNPDFMean"] + Pickles["%s_%s_%s_MuMu"%(m_neutralino_1,m_sbottom,m_neutralino_2)]["MuMu"]["MuMuNNPDFMean"] - Pickles["%s_%s_%s_EMu"%(m_neutralino_1,m_sbottom,m_neutralino_2)]["EMu"]["EMuNNPDFMean"] 
					PDF["NNPDFAbsMean_%s"%region] = Pickles["%s_%s_%s_EE"%(m_neutralino_1,m_sbottom,m_neutralino_2)]["EE"]["EENNPDFAbsMean"] + Pickles["%s_%s_%s_MuMu"%(m_neutralino_1,m_sbottom,m_neutralino_2)]["MuMu"]["MuMuNNPDFAbsMean"] - Pickles["%s_%s_%s_EMu"%(m_neutralino_1,m_sbottom,m_neutralino_2)]["EMu"]["EMuNNPDFAbsMean"] 
					PDF["NNPDFUp_%s"%region] = Pickles["%s_%s_%s_EE"%(m_neutralino_1,m_sbottom,m_neutralino_2)]["EE"]["EENNPDFUp"] + Pickles["%s_%s_%s_MuMu"%(m_neutralino_1,m_sbottom,m_neutralino_2)]["MuMu"]["MuMuNNPDFUp"] - Pickles["%s_%s_%s_EMu"%(m_neutralino_1,m_sbottom,m_neutralino_2)]["EMu"]["EMuNNPDFUp"] 
					PDF["NNPDFAbsUp_%s"%region] = Pickles["%s_%s_%s_EE"%(m_neutralino_1,m_sbottom,m_neutralino_2)]["EE"]["EENNPDFAbsUp"] + Pickles["%s_%s_%s_MuMu"%(m_neutralino_1,m_sbottom,m_neutralino_2)]["MuMu"]["MuMuNNPDFAbsUp"] - Pickles["%s_%s_%s_EMu"%(m_neutralino_1,m_sbottom,m_neutralino_2)]["EMu"]["EMuNNPDFAbsUp"] 
					PDF["NNPDFDown_%s"%region] = Pickles["%s_%s_%s_EE"%(m_neutralino_1,m_sbottom,m_neutralino_2)]["EE"]["EENNPDFDown"] + Pickles["%s_%s_%s_MuMu"%(m_neutralino_1,m_sbottom,m_neutralino_2)]["MuMu"]["MuMuNNPDFDown"] - Pickles["%s_%s_%s_EMu"%(m_neutralino_1,m_sbottom,m_neutralino_2)]["EMu"]["EMuNNPDFDown"] 
					PDF["NNPDFAbsDown_%s"%region] = Pickles["%s_%s_%s_EE"%(m_neutralino_1,m_sbottom,m_neutralino_2)]["EE"]["EENNPDFAbsDown"] + Pickles["%s_%s_%s_MuMu"%(m_neutralino_1,m_sbottom,m_neutralino_2)]["MuMu"]["MuMuNNPDFAbsDown"] - Pickles["%s_%s_%s_EMu"%(m_neutralino_1,m_sbottom,m_neutralino_2)]["EMu"]["EMuNNPDFAbsDown"]
					
					if PDF["CT10Mean_%s"%region] > 0 and PDF["MSTWMean_%s"%region] > 0 and PDF["NNPDFMean_%s"%region] > 0:
						systUncertainties["PDFUncertainty_%s"%region] = max(max(((PDF["CT10Up_%s"%region]/PDF["CT10AbsUp_%s"%region])-(PDF["CT10Mean_%s"%region]/PDF["CT10AbsMean_%s"%region]))/(PDF["CT10Mean_%s"%region]/PDF["CT10AbsMean_%s"%region]),abs(((PDF["CT10Down_%s"%region]/PDF["CT10AbsDown_%s"%region])-(PDF["CT10Mean_%s"%region]/PDF["CT10AbsMean_%s"%region]))/(PDF["CT10Mean_%s"%region]/PDF["CT10AbsMean_%s"%region]))),max(((PDF["MSTWUp_%s"%region]/PDF["MSTWAbsUp_%s"%region])-(PDF["MSTWMean_%s"%region]/PDF["MSTWAbsMean_%s"%region]))/(PDF["MSTWMean_%s"%region]/PDF["MSTWAbsMean_%s"%region]),abs(((PDF["MSTWDown_%s"%region]/PDF["MSTWAbsDown_%s"%region])-(PDF["MSTWMean_%s"%region]/PDF["MSTWAbsMean_%s"%region]))/(PDF["MSTWMean_%s"%region]/PDF["MSTWAbsMean_%s"%region]))),max(((PDF["NNPDFUp_%s"%region]/PDF["NNPDFAbsUp_%s"%region])-(PDF["NNPDFMean_%s"%region]/PDF["NNPDFAbsMean_%s"%region]))/(PDF["NNPDFMean_%s"%region]/PDF["NNPDFAbsMean_%s"%region]),abs(((PDF["NNPDFDown_%s"%region]/PDF["NNPDFAbsDown_%s"%region])-(PDF["NNPDFMean_%s"%region]/PDF["NNPDFAbsMean_%s"%region]))/(PDF["NNPDFMean_%s"%region]/PDF["NNPDFAbsMean_%s"%region]))))
					elif PDF["CT10Mean_%s"%region] > 0 and PDF["MSTWMean_%s"%region] > 0:
						systUncertainties["PDFUncertainty_%s"%region] = max(max(((PDF["CT10Up_%s"%region]/PDF["CT10AbsUp_%s"%region])-(PDF["CT10Mean_%s"%region]/PDF["CT10AbsMean_%s"%region]))/(PDF["CT10Mean_%s"%region]/PDF["CT10AbsMean_%s"%region]),abs(((PDF["CT10Down_%s"%region]/PDF["CT10AbsDown_%s"%region])-(PDF["CT10Mean_%s"%region]/PDF["CT10AbsMean_%s"%region]))/(PDF["CT10Mean_%s"%region]/PDF["CT10AbsMean_%s"%region]))),max(((PDF["MSTWUp_%s"%region]/PDF["MSTWAbsUp_%s"%region])-(PDF["MSTWMean_%s"%region]/PDF["MSTWAbsMean_%s"%region]))/(PDF["MSTWMean_%s"%region]/PDF["MSTWAbsMean_%s"%region]),abs(((PDF["MSTWDown_%s"%region]/PDF["MSTWAbsDown_%s"%region])-(PDF["MSTWMean_%s"%region]/PDF["MSTWAbsMean_%s"%region]))/(PDF["MSTWMean_%s"%region]/PDF["MSTWAbsMean_%s"%region]))))						
					elif PDF["CT10Mean_%s"%region] > 0 and PDF["NNPDFMean_%s"%region] > 0:
						systUncertainties["PDFUncertainty_%s"%region] = max(max(((PDF["CT10Up_%s"%region]/PDF["CT10AbsUp_%s"%region])-(PDF["CT10Mean_%s"%region]/PDF["CT10AbsMean_%s"%region]))/(PDF["CT10Mean_%s"%region]/PDF["CT10AbsMean_%s"%region]),abs(((PDF["CT10Down_%s"%region]/PDF["CT10AbsDown_%s"%region])-(PDF["CT10Mean_%s"%region]/PDF["CT10AbsMean_%s"%region]))/(PDF["CT10Mean_%s"%region]/PDF["CT10AbsMean_%s"%region]))),max(((PDF["NNPDFUp_%s"%region]/PDF["NNPDFAbsUp_%s"%region])-(PDF["NNPDFMean_%s"%region]/PDF["NNPDFAbsMean_%s"%region]))/(PDF["NNPDFMean_%s"%region]/PDF["NNPDFAbsMean_%s"%region]),abs(((PDF["NNPDFDown_%s"%region]/PDF["NNPDFAbsDown_%s"%region])-(PDF["NNPDFMean_%s"%region]/PDF["NNPDFAbsMean_%s"%region]))/(PDF["NNPDFMean_%s"%region]/PDF["NNPDFAbsMean_%s"%region]))))
					elif PDF["MSTWMean_%s"%region] > 0 and PDF["NNPDFMean_%s"%region] > 0:
						systUncertainties["PDFUncertainty_%s"%region] = max(max(((PDF["MSTWUp_%s"%region]/PDF["MSTWAbsUp_%s"%region])-(PDF["MSTWMean_%s"%region]/PDF["MSTWAbsMean_%s"%region]))/(PDF["MSTWMean_%s"%region]/PDF["MSTWAbsMean_%s"%region]),abs(((PDF["MSTWDown_%s"%region]/PDF["MSTWAbsDown_%s"%region])-(PDF["MSTWMean_%s"%region]/PDF["MSTWAbsMean_%s"%region]))/(PDF["MSTWMean_%s"%region]/PDF["MSTWAbsMean_%s"%region]))),max(((PDF["NNPDFUp_%s"%region]/PDF["NNPDFAbsUp_%s"%region])-(PDF["NNPDFMean_%s"%region]/PDF["NNPDFAbsMean_%s"%region]))/(PDF["NNPDFMean_%s"%region]/PDF["NNPDFAbsMean_%s"%region]),abs(((PDF["NNPDFDown_%s"%region]/PDF["NNPDFAbsDown_%s"%region])-(PDF["NNPDFMean_%s"%region]/PDF["NNPDFAbsMean_%s"%region]))/(PDF["NNPDFMean_%s"%region]/PDF["NNPDFAbsMean_%s"%region]))))
					elif PDF["CT10Mean_%s"%region] > 0:
						systUncertainties["PDFUncertainty_%s"%region] = max(((PDF["CT10Up_%s"%region]/PDF["CT10AbsUp_%s"%region])-(PDF["CT10Mean_%s"%region]/PDF["CT10AbsMean_%s"%region]))/(PDF["CT10Mean_%s"%region]/PDF["CT10AbsMean_%s"%region]),abs(((PDF["CT10Down_%s"%region]/PDF["CT10AbsDown_%s"%region])-(PDF["CT10Mean_%s"%region]/PDF["CT10AbsMean_%s"%region]))/(PDF["CT10Mean_%s"%region]/PDF["CT10AbsMean_%s"%region])))
					elif PDF["MSTWMean_%s"%region] > 0:
						systUncertainties["PDFUncertainty_%s"%region] = max(((PDF["MSTWUp_%s"%region]/PDF["MSTWAbsUp_%s"%region])-(PDF["MSTWMean_%s"%region]/PDF["MSTWAbsMean_%s"%region]))/(PDF["MSTWMean_%s"%region]/PDF["MSTWAbsMean_%s"%region]),abs(((PDF["MSTWDown_%s"%region]/PDF["MSTWAbsDown_%s"%region])-(PDF["MSTWMean_%s"%region]/PDF["MSTWAbsMean_%s"%region]))/(PDF["MSTWMean_%s"%region]/PDF["MSTWAbsMean_%s"%region])))
					elif PDF["NNPDFMean_%s"%region] > 0:
						systUncertainties["PDFUncertainty_%s"%region] = max(((PDF["NNPDFUp_%s"%region]/PDF["NNPDFAbsUp_%s"%region])-(PDF["NNPDFMean_%s"%region]/PDF["NNPDFAbsMean_%s"%region]))/(PDF["NNPDFMean_%s"%region]/PDF["NNPDFAbsMean_%s"%region]),abs(((PDF["NNPDFDown_%s"%region]/PDF["NNPDFAbsDown_%s"%region])-(PDF["NNPDFMean_%s"%region]/PDF["NNPDFAbsMean_%s"%region]))/(PDF["NNPDFMean_%s"%region]/PDF["NNPDFAbsMean_%s"%region])))
					else:
						systUncertainties["PDFUncertainty_%s"%region] = 0
					
					### ISR Uncertainty
					ISR["Mean_%s"%region] = Pickles["%s_%s_%s_EE"%(m_neutralino_1,m_sbottom,m_neutralino_2)]["EE"]["EEISRMean"] + Pickles["%s_%s_%s_MuMu"%(m_neutralino_1,m_sbottom,m_neutralino_2)]["MuMu"]["MuMuISRMean"] - Pickles["%s_%s_%s_EMu"%(m_neutralino_1,m_sbottom,m_neutralino_2)]["EMu"]["EMuISRMean"] 
					
					ISR["ISRUp_%s"%region] = Pickles["%s_%s_%s_EE"%(m_neutralino_1,m_sbottom,m_neutralino_2)]["EE"]["EEISRUp"] + Pickles["%s_%s_%s_MuMu"%(m_neutralino_1,m_sbottom,m_neutralino_2)]["MuMu"]["MuMuISRUp"] - Pickles["%s_%s_%s_EMu"%(m_neutralino_1,m_sbottom,m_neutralino_2)]["EMu"]["EMuISRUp"]  
					ISR["ISRDown_%s"%region] = Pickles["%s_%s_%s_EE"%(m_neutralino_1,m_sbottom,m_neutralino_2)]["EE"]["EEISRDown"] + Pickles["%s_%s_%s_MuMu"%(m_neutralino_1,m_sbottom,m_neutralino_2)]["MuMu"]["MuMuISRDown"] - Pickles["%s_%s_%s_EMu"%(m_neutralino_1,m_sbottom,m_neutralino_2)]["EMu"]["EMuISRDown"]  
					
					if ISR["Mean_%s"%region] > 0:
						systUncertainties["ISRUncertainty_%s"%region] = sqrt(max(((ISR["ISRUp_%s"%region]-ISR["Mean_%s"%region])/ISR["Mean_%s"%region])**2,((ISR["ISRDown_%s"%region]-ISR["Mean_%s"%region])/ISR["Mean_%s"%region])**2))
					else:
						systUncertainties["ISRUncertainty_%s"%region] = 0
						
					if Yields["SFOF_%s"%region] > 0:
						systUncertainties["TriggerEffUncertainty_%s"%region] = sqrt((Yields["EE_%s"%region]*TriggerEffUncertainty)**2 + (Yields["MuMu_%s"%region]*TriggerEffUncertainty)**2 + (Yields["EMu_%s"%region]*TriggerEffUncertainty)**2)/Yields["SFOF_%s"%region]
					else:
						systUncertainties["TriggerEffUncertainty_%s"%region] = 0
							
					#~ if Pickles["%s_%s_%s"%(m_neutralino_1,m_sbottom,m_neutralino_2)]["Signal"]["val"] > 0:
					### Total syst uncertainty
					systUncertainties["TotalUncertainty_%s"%region] = sqrt(systUncertainties["metUncertainty_%s"%region]**2 + systUncertainties["jetUncertainty_%s"%region]**2 + systUncertainties["leptonUncertainty_%s"%region]**2 + systUncertainties["pileupUncertainty_%s"%region]**2 + systUncertainties["PDFUncertainty_%s"%region]**2 + systUncertainties["ISRUncertainty_%s"%region]**2  + systUncertainties["TriggerEffUncertainty_%s"%region]**2 + FastSimUncertainty**2 + LumiUncertainty**2)

						
				ValueLowMllCentral = Yields["SFOF_Barrel_lowMll"]
				UncertaintyLowMllCentral = systUncertainties["TotalUncertainty_Barrel_lowMll"]
				StatUncertaintyLowMllCentral = statUncertainties["SFOF_Barrel_lowMll"]
				ValueZPeakCentral = Yields["SFOF_Barrel_ZPeak"]
				UncertaintyZPeakCentral = systUncertainties["TotalUncertainty_Barrel_ZPeak"]
				StatUncertaintyZPeakCentral = statUncertainties["SFOF_Barrel_ZPeak"]
				ValueHighMllCentral = Yields["SFOF_Barrel_highMll"]
				UncertaintyHighMllCentral = systUncertainties["TotalUncertainty_Barrel_highMll"]
				StatUncertaintyHighMllCentral = statUncertainties["SFOF_Barrel_highMll"]
	
				ValueLowMllForward = Yields["SFOF_Endcap_lowMll"]
				UncertaintyLowMllForward = systUncertainties["TotalUncertainty_Endcap_lowMll"]
				StatUncertaintyLowMllForward = statUncertainties["SFOF_Endcap_lowMll"]
				ValueZPeakForward = Yields["SFOF_Endcap_ZPeak"]
				UncertaintyZPeakForward = systUncertainties["TotalUncertainty_Endcap_ZPeak"]
				StatUncertaintyZPeakForward = statUncertainties["SFOF_Endcap_ZPeak"]
				ValueHighMllForward = Yields["SFOF_Endcap_highMll"]
				UncertaintyHighMllForward = systUncertainties["TotalUncertainty_Endcap_highMll"]
				StatUncertaintyHighMllForward = statUncertainties["SFOF_Endcap_highMll"]
				
				if ValueLowMllCentral > 0:
					firstGuesslowMll = 2 * TMath.Sqrt(UncertaintyLowMllCentral**2+lowMllCentrTTbar+lowMllCentrDY+(lowMllCentrTTbarSystUncertainty*lowMllCentrTTbar)**2+(lowMllCentrTTbarStatUncertainty*lowMllCentrTTbar)**2+(lowMllCentrDYUncertainty*lowMllCentrDY)**2) / ValueLowMllCentral
				else:
					firstGuesslowMll = 10
				if ValueHighMllCentral > 0:
					firstGuesshighMll = 2 * TMath.Sqrt(UncertaintyHighMllCentral**2+highMllCentrTTbar+highMllCentrDY+(highMllCentrTTbarSystUncertainty*highMllCentrTTbar)**2+(highMllCentrTTbarStatUncertainty*highMllCentrTTbar)**2+(highMllCentrDYUncertainty*highMllCentrDY)**2) / ValueHighMllCentral
				else:
					firstGuesshighMll = 10
				if ValueZPeakCentral > 0:
					firstGuessZPeak = 2 * TMath.Sqrt(UncertaintyZPeakCentral**2+ZPeakCentrTTbar+ZPeakCentrDY+(ZPeakCentrTTbarSystUncertainty*ZPeakCentrTTbar)**2+(ZPeakCentrTTbarStatUncertainty*ZPeakCentrTTbar)**2+(ZPeakCentrDYUncertainty*ZPeakCentrDY)**2) / ValueZPeakCentral
				else:
					firstGuessZPeak = 10
				firstGuess = min(firstGuesslowMll,firstGuesshighMll,firstGuessZPeak)
				
				if m_neutr_1_fix == False:
					Name= "SUSY_Simplified_Model_Madgraph_FastSim_T6bblledge_%s_%s_%s_8TeV"%(m_sbottom,m_neutralino_2,m_neutralino_1)
					DataCard = open("DataCards/T6bblledge/%s.txt"%Name,'w')
				else:
					Name= "SUSY_Simplified_Model_Madgraph_FastSim_T6bbllslepton_%s_%s_%s_8TeV"%(m_sbottom,m_neutralino_2,m_neutralino_1)
					DataCard = open("DataCards/T6bbllslepton/%s.txt"%Name,'w')
				DataCard.write("# sbottom = %s \n"%m_sbottom)
				DataCard.write("# neutralino 2 = %s \n"%m_neutralino_2)
				DataCard.write("# Xsection = %s \n"%xsection)
				DataCard.write("# R_firstguess = %s \n"%str(firstGuess))
				DataCard.write("imax %s number of bins \n"%n_bins)
				DataCard.write("jmax %s number of processes minus 1 \n"%n_processes)
				DataCard.write("kmax %s number of nuisance parameters \n"%n_nuicance_parameters)
				DataCard.write("---------------------------------------------------------------------------------------------------------------------------------- \n")
				DataCard.write("bin          CentrLowMll   CentrZPeak  CentrHighMll  ForwLowMll   ForwZPeak  ForwHighMll\n")
				DataCard.write("observation  %s            %s          %s            %s           %s         %s    \n"%(lowMllCentrObservation,ZPeakCentrObservation,highMllCentrObservation,lowMllForwObservation,ZPeakForwObservation,highMllForwObservation))
				DataCard.write("---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- \n")
				DataCard.write("bin                                 CentrLowMll   CentrLowMll   CentrLowMll  CentrZPeak   CentrZPeak   CentrZPeak  CentrHighMll   CentrHighMll   CentrHighMll   ForwLowMll   ForwLowMll   ForwLowMll  ForwZPeak   ForwZPeak   ForwZPeak  ForwHighMll   ForwHighMll   ForwHighMll  \n")
				DataCard.write("process                             SUSY          ZJets         OF           SUSY         ZJets        OF          SUSY           ZJets          OF             SUSY         ZJets        OF          SUSY        ZJets       OF         SUSY          ZJets         OF  \n")
				DataCard.write("process                             0             1             2            0            1            2           0              1              2              0            1            2           0           1           2          0             1             2  \n")
				DataCard.write("rate                                %s            %s            %s           %s           %s           %s          %s             %s             %s             %s           %s           %s          %s          %s          %s         %s            %s            %s  \n"%(ValueLowMllCentral,lowMllCentrDY,lowMllCentrTTbar,ValueZPeakCentral,ZPeakCentrDY,ZPeakCentrTTbar,ValueHighMllCentral,highMllCentrDY,highMllCentrTTbar,ValueLowMllForward,lowMllForwDY,lowMllForwTTbar,ValueZPeakForward,ZPeakForwDY,ZPeakForwTTbar,ValueHighMllForward,highMllForwDY,highMllForwTTbar))
				DataCard.write("-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- \n")
				DataCard.write("SigSystUncert               lnN     %s            -             -            %s           -            -           %s             -              -              %s           -            -           %s          -           -          %s            -             -   \n"%(str(1+UncertaintyLowMllCentral),str(1+UncertaintyZPeakCentral),str(1+UncertaintyHighMllCentral),str(1+UncertaintyLowMllForward),str(1+UncertaintyZPeakForward),str(1+UncertaintyHighMllForward)))
				DataCard.write("OFSystUncert                lnN     -             -             %s           -            -            %s          -              -              %s             -            -            %s          -           -           %s         -             -             %s  \n"%(str(1+lowMllCentrTTbarSystUncertainty),str(1+ZPeakCentrTTbarSystUncertainty),str(1+highMllCentrTTbarSystUncertainty),str(1+lowMllForwTTbarSystUncertainty),str(1+ZPeakForwTTbarSystUncertainty),str(1+highMllForwTTbarSystUncertainty)))
				DataCard.write("ZJetsUncert                 lnN     -             %s            -            -            %s           -           -              %s             -              -            %s           -           -           %s          -          -             %s            -   \n"%(str(1+lowMllCentrDYUncertainty),str(1+ZPeakCentrDYUncertainty),str(1+highMllCentrDYUncertainty),str(1+lowMllForwDYUncertainty),str(1+ZPeakForwDYUncertainty),str(1+highMllForwDYUncertainty)))
				DataCard.write("SigStatUncertLowMllCentr    lnN     %s            -             -            -            -            -           -              -              -              -            -            -           -           -           -          -             -             -   \n"%(str(1+StatUncertaintyLowMllCentral)))
				DataCard.write("SigStatUncertZPeakCentr     lnN     -             -             -            %s           -            -           -              -              -              -            -            -           -           -           -          -             -             -   \n"%(str(1+StatUncertaintyZPeakCentral)))
				DataCard.write("SigStatUncertHighMllCentr   lnN     -             -             -            -            -            -           %s             -              -              -            -            -           -           -           -          -             -             -   \n"%(str(1+StatUncertaintyHighMllCentral)))
				DataCard.write("SigStatUncertLowMllForw     lnN     -             -             -            -            -            -           -              -              -              %s           -            -           -           -           -          -             -             -   \n"%(str(1+StatUncertaintyLowMllForward)))
				DataCard.write("SigStatUncertZPeakForw      lnN     -             -             -            -            -            -           -              -              -              -            -            -           %s          -           -          -             -             -   \n"%(str(1+StatUncertaintyZPeakForward)))
				DataCard.write("SigStatUncertHighMllForw    lnN     -             -             -            -            -            -           -              -              -              -            -            -           -           -           -          %s            -             -   \n"%(str(1+StatUncertaintyHighMllForward)))
				DataCard.write("OFStatUncertLowMllCentr     lnN     -             -             %s           -            -            -           -              -              -              -            -            -           -           -           -          -             -             -   \n"%(str(1+lowMllCentrTTbarStatUncertainty)))
				DataCard.write("OFStatUncertZPeakCentr      lnN     -             -             -            -            -            %s          -              -              -              -            -            -           -           -           -          -             -             -   \n"%(str(1+ZPeakCentrTTbarStatUncertainty)))
				DataCard.write("OFStatUncertHighMllCentr    lnN     -             -             -            -            -            -           -              -              %s             -            -            -           -           -           -          -             -             -   \n"%(str(1+highMllCentrTTbarStatUncertainty)))
				DataCard.write("OFStatUncertLowMllForw      lnN     -             -             -            -            -            -           -              -              -              -            -            %s          -           -           -          -             -             -   \n"%(str(1+lowMllForwTTbarStatUncertainty)))
				DataCard.write("OFStatUncertZPeakForw       lnN     -             -             -            -            -            -           -              -              -              -            -            -           -           -           %s         -             -             -   \n"%(str(1+ZPeakForwTTbarStatUncertainty)))
				DataCard.write("OFStatUncertHighMllForw     lnN     -             -             -            -            -            -           -              -              -              -            -            -           -           -           -          -             -             %s  \n"%(str(1+highMllForwTTbarStatUncertainty)))
							
							
						
			j += 1		
		i += 1
			#~ canv.DrawFrame(x_min,y_min,x_max,y_max,title)
			
	

		
				
		
	
										
					
			
											
									
				

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
 
