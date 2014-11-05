####################################################################################################
# FastSim lepton scaling factors were not in included in the trees                                 #
# -> One has to run over each event to scale it properly                                           #
# For the slepton model (fixed neutralino 1): Events have to be scaled to Z/slepton BR either via  #
# the number of generated sleptons (new, has to be implemented) or the number of generated leptons #
# (with a neutralino 2 as mother) and the mother PDG ID (old)                                      #
####################################################################################################



import ROOT
import numpy as np
from ROOT import TH1F
from math import sqrt
attic = []


ROOT.gStyle.SetOptStat(0)

ptScales = {"EE":{"Barrel":"1.012","Endcap":"1.03"},"MuMu":{"Barrel":"1.004","Endcap":"1.004"}}

etaCuts = {
			"Barrel":"abs(eta1) < 1.4 && abs(eta2) < 1.4",
			"Endcap":"(((abs(eta1) < 1.4 || abs(eta1) > 1.6) && (abs(eta2) < 1.4 || abs(eta2) > 1.6)) && 1.6 <= TMath::Max(abs(eta1),abs(eta2)))",
			"BothEndcap":"abs(eta1) > 1.6 && abs(eta2) > 1.6",
			"Inclusive":"abs(eta1) < 2.4 && abs(eta2) < 2.4 && ((abs(eta1) < 1.4 || abs(eta1) > 1.6) && (abs(eta2) < 1.4 || abs(eta2) > 1.6))"
			}
			
mllCuts = {
			"lowMll":"p4.M() < 70 && p4.M() > 20",
			"ZPeak":"p4.M() < 101 && p4.M() > 81",
			"highMll":"p4.M() > 120",
			}

eventLowerMllCuts = {
			"lowMll": 20,
			"ZPeak": 81,
			"highMll":120,
			}
			
eventUpperMllCuts = {
			"lowMll": 70 ,
			"ZPeak": 101,
			"highMll":10000,
			}

def readPDFHistsFromFile(filePath, dileptonCombination, pdfSet):
	from ROOT import TH1F, TFile
	from random import randint
	from sys import maxint
	name1 = "%x"%(randint(0, maxint))	
	name2 = "%x"%(randint(0, maxint))	
	name3 = "%x"%(randint(0, maxint))	
	result = {}
	f1 = TFile(filePath,"READ")
	
	firstBin = 20
	lastBin = 300
	nBins = 280/5
	histoMean = TH1F(name1,name1, nBins, firstBin, lastBin)
	histoMean = (f1.Get("%s_%sDileptonTree_%s"%(pdfSet,dileptonCombination,"mean"))).Clone()
	result["mean"] = histoMean.Clone()
	result["up"] = f1.Get("%s_%sDileptonTree_%s"%(pdfSet,dileptonCombination,"up")).Clone(name2)
	result["down"] = f1.Get("%s_%sDileptonTree_%s"%(pdfSet,dileptonCombination,"down")).Clone(name3)
	f1.Close()
	print result
	return result

def readPDFHists(path,dileptonCombination):
	
	result = {}
	for sampleName, filePath in getFilePathsAndSampleNames(path).iteritems():
		result[sampleName] = {}
		print readPDFHistsFromFile(filePath, dileptonCombination,"CT10")
		result[sampleName]["CT10"] = readPDFHistsFromFile(filePath, dileptonCombination,"CT10")
		result[sampleName]["MSTW"] = readPDFHistsFromFile(filePath, dileptonCombination,"MSTW")
		result[sampleName]["NNPDF"] = readPDFHistsFromFile(filePath, dileptonCombination,"NNPDF")
		
	return result	

def readTreeFromFile(path, dileptonCombination):
	"""
	helper functionfrom argparse import ArgumentParser
	path: path to .root file containing simulated events
	dileptonCombination: EMu, EMu, or EMu for electron-electron, electron-muon, or muon-muon events

	returns: tree containing events for on sample and dileptonCombination
	"""
	from ROOT import TChain
	result = TChain()
	result.Add("%s/cutsV23DileptonFinalTrees/%sDileptonTree"%(path, dileptonCombination))
	return result
	
def getFilePathsAndSampleNames(path):
	"""
	helper function
	path: path to directory containing all sample files

	returns: dict of smaple names -> path of .root file (for all samples in path)
	"""
	result = []
	from glob import glob
	from re import match
	result = {}
	for filePath in glob("%s/sw538*.root"%path):
		#~ sampleName = match(".*sw538v.*\.processed.*\.(.*).root", filePath).groups()[0]
		sampleName = match(".*sw538v0477.processed\.(.*).root", filePath).groups()[0]
		#for the python enthusiats: yield sampleName, filePath is more efficient here :)
		result[sampleName] = filePath
	return result
	
def totalNumberOfGeneratedEvents(path):
	"""
	path: path to directory containing all sample files

	returns dict samples names -> number of simulated events in source sample
			(note these include events without EMu EMu EMu signature, too )
	"""
	from ROOT import TFile
	result = {}
	for sampleName, filePath in getFilePathsAndSampleNames(path).iteritems():
		rootFile = TFile(filePath, "read")
		result[sampleName] = rootFile.FindObjectAny("analysis paths").GetBinContent(1)
	return result
	
def readTrees(path, dileptonCombination):
	"""
	path: path to directory containing all sample files
	dileptonCombination: "EMu", "EMu", or pyroot"EMu" for electron-electron, electron-muon, or muon-muon events

	returns: dict of sample names ->  trees containing events (for all samples for one dileptonCombination)
	"""
	result = {}
	for sampleName, filePath in getFilePathsAndSampleNames(path).iteritems():		
		result[sampleName] = readTreeFromFile(filePath, dileptonCombination)
		
	return result
	
	
def createHistoFromTree(tree, variable, weight, nBins, firstBin, lastBin, nEvents = -1):
	"""
	tree: tree to create histo from)
	variable: variable to plot (must be a branch of the tree)
	weight: weights to apply (e.g. "var1*(var2 > 15)" will use weights from var1 and cut on var2 > 15
	nBins, firstBin, lastBin: number of bins, first bin and last bin (same as in TH1F constructor)
	nEvents: number of events to process (-1 = all)
	"""
	from ROOT import TH1F
	from random import randint
	from sys import maxint
	if nEvents < 0:
		nEvents = maxint
	#make a random name you could give something meaningfull here,
	#but that would make this less readable
	name = "%x"%(randint(0, maxint))
	result = TH1F(name, "", nBins, firstBin, lastBin)
	result.Sumw2()
	tree.Draw("%s>>%s"%(variable, name), weight, "goff", nEvents)
	return result
	
	
def setTDRStyle():
	from ROOT import TStyle
	from ROOT import kWhite
	from ROOT import kTRUE
	tdrStyle =  TStyle("tdrStyle","Style for P-TDR")
	
	# For the canvas:
	tdrStyle.SetCanvasBorderMode(0)
	tdrStyle.SetCanvasColor(kWhite)
	# For the canvas:
	tdrStyle.SetCanvasBorderMode(0)
	tdrStyle.SetCanvasColor(kWhite)
	tdrStyle.SetCanvasDefH(600) #Height of canvas
	tdrStyle.SetCanvasDefW(600)#Width of canvas
	tdrStyle.SetCanvasDefX(0)  #POsition on screen
	tdrStyle.SetCanvasDefY(0)
	
	# For the Pad:
	tdrStyle.SetPadBorderMode(0)
	# tdrStyle->SetPadBorderSize(Width_t size = 1);
	tdrStyle.SetPadColor(kWhite)
	tdrStyle.SetPadGridX(0)
	tdrStyle.SetPadGridY(0)
	tdrStyle.SetGridColor(0)
	tdrStyle.SetGridStyle(3)
	tdrStyle.SetGridWidth(1)
	
	# For the frame:
	tdrStyle.SetFrameBorderMode(0)
	tdrStyle.SetFrameBorderSize(1)
	tdrStyle.SetFrameFillColor(0)
	tdrStyle.SetFrameFillStyle(0)
	tdrStyle.SetFrameLineColor(1)
	tdrStyle.SetFrameLineStyle(1)
	tdrStyle.SetFrameLineWidth(1)
	
	# For the histo:
	# tdrStyle->SetHistFillColor(1);
	# tdrStyle->SetHistFillStyle(0);
	tdrStyle.SetHistLineColor(1)
	tdrStyle.SetHistLineStyle(0)
	tdrStyle.SetHistLineWidth(1)
	# tdrStyle->SetLegoInnerR(Float_t rad = 0.5);
	# tdrStyle->SetNumberContours(Int_t number = 20);
	
	tdrStyle.SetEndErrorSize(2)
	#  tdrStyle->SetErrorMarker(20);
	tdrStyle.SetErrorX(0.)
	
	tdrStyle.SetMarkerStyle(20)
	
	#For the fit/function:
	tdrStyle.SetOptFit(1)
	tdrStyle.SetFitFormat("5.4g")
	tdrStyle.SetFuncColor(2)
	tdrStyle.SetFuncStyle(1)
	tdrStyle.SetFuncWidth(1)
	
	#For the date:
	tdrStyle.SetOptDate(0)
	# tdrStyle->SetDateX(Float_t x = 0.01);
	# tdrStyle->SetDateY(Float_t y = 0.01);
	
	# For the statistics box:
	tdrStyle.SetOptFile(0)
	tdrStyle.SetOptStat("emr") # To display the mean and RMS:   SetOptStat("mr");
	tdrStyle.SetStatColor(kWhite)
	tdrStyle.SetStatFont(42)
	tdrStyle.SetStatFontSize(0.025)
	tdrStyle.SetStatTextColor(1)
	tdrStyle.SetStatFormat("6.4g")
	tdrStyle.SetStatBorderSize(1)
	tdrStyle.SetStatH(0.1)
	tdrStyle.SetStatW(0.15)
	# tdrStyle->SetStatStyle(Style_t style = 100.1);
	# tdrStyle->SetStatX(Float_t x = 0);
	# tdrStyle->SetStatY(Float_t y = 0);
	
	# Margins:
	tdrStyle.SetPadTopMargin(0.05)
	tdrStyle.SetPadBottomMargin(0.13)
	tdrStyle.SetPadLeftMargin(0.15)
	tdrStyle.SetPadRightMargin(0.05)
	
	# For the Global title:
	tdrStyle.SetOptTitle(0)
	tdrStyle.SetTitleFont(42)
	tdrStyle.SetTitleColor(1)
	tdrStyle.SetTitleTextColor(1)
	tdrStyle.SetTitleFillColor(10)
	tdrStyle.SetTitleFontSize(0.05)
	# tdrStyle->SetTitleH(0); # Set the height of the title box
	# tdrStyle->SetTitleW(0); # Set the width of the title box
	# tdrStyle->SetTitleX(0); # Set the position of the title box
	# tdrStyle->SetTitleY(0.985); # Set the position of the title box
	# tdrStyle->SetTitleStyle(Style_t style = 100.1);
	# tdrStyle->SetTitleBorderSize(2);
	
	# For the axis titles:
	tdrStyle.SetTitleColor(1, "XYZ")
	tdrStyle.SetTitleFont(42, "XYZ")
	tdrStyle.SetTitleSize(0.06, "XYZ")
	# tdrStyle->SetTitleXSize(Float_t size = 0.02); # Another way to set the size?
	# tdrStyle->SetTitleYSize(Float_t size = 0.02);
	tdrStyle.SetTitleXOffset(0.9)
	tdrStyle.SetTitleYOffset(1.2)
	# tdrStyle->SetTitleOffset(1.1, "Y"); # Another way to set the Offset
	
	# For the axis labels:
	tdrStyle.SetLabelColor(1, "XYZ")
	tdrStyle.SetLabelFont(42, "XYZ")
	tdrStyle.SetLabelOffset(0.007, "XYZ")
	tdrStyle.SetLabelSize(0.05, "XYZ")
	
	# For the axis:
	tdrStyle.SetAxisColor(1, "XYZ")
	tdrStyle.SetStripDecimals(kTRUE)
	tdrStyle.SetTickLength(0.03, "XYZ")
	tdrStyle.SetNdivisions(408, "XYZ")
	
	#~ tdrStyle->SetNdivisions(510, "XYZ");
	tdrStyle.SetPadTickX(1)  # To get tick marks on the opposite side of the frame
	tdrStyle.SetPadTickY(1)
	
	# Change for log plots:
	tdrStyle.SetOptLogx(0)
	tdrStyle.SetOptLogy(0)
	tdrStyle.SetOptLogz(0)
	
	# Postscript options:
	tdrStyle.SetPaperSize(20.,20.);
	# tdrStyle->SetLineScalePS(Float_t scale = 3);
	# tdrStyle->SetLineStyleString(Int_t i, const char* text);
	# tdrStyle->SetHeaderPS(const char* header);
	# tdrStyle->SetTitlePS(const char* pstitle);
	
	#tdrStyle->SetBarOffset(Float_t baroff = 0.5);
	#tdrStyle->SetBarWidth(Float_t barwidth = 0.5);
	#tdrStyle->SetPaintTextFormat(const char* format = "g");
	tdrStyle.SetPalette(1)
	#tdrStyle->SetTimeOffset(Double_t toffset);
	#tdrStyle->SetHistMinimumZero(kTRUE);
	
	
	
	
	ROOT.gROOT.ForceStyle()
	
	tdrStyle.cd()

def produceMETUncertainty(tree,cuts,dilepton):
	
	uncertaintySources = ["patPFMetJetEnUp","patPFMetJetEnDown","patPFMetJetResUp","patPFMetJetResDown","patPFMetElectronEnUp","patPFMetElectronEnDown","patPFMetMuonEnUp","patPFMetMuonEnDown","patPFMetTauEnUp","patPFMetTauEnDown","patPFMetUnclusteredEnUp","patPFMetUnclusteredEnDown"]
	colors=[ROOT.kBlue,ROOT.kGreen+3,ROOT.kGreen+3,ROOT.kGreen,ROOT.kGreen,ROOT.kOrange+2,ROOT.kOrange+2,ROOT.kPink,ROOT.kPink,ROOT.kBlack,ROOT.kBlack,ROOT.kBlue+3,ROOT.kBlue+3]
	result = 0.
	defaultTree = tree.CopyTree(cuts)
	histos = [createHistoFromTree(tree, "patPFMet", "", 40, 0, 400)]
	yields = [float(createHistoFromTree(tree, "p4.M()", cuts, 300, 0, 300).Integral())]
	for index, source in enumerate(uncertaintySources):
		if index == 0:
			cuts = cuts.replace("patPFMet",source)
		else:
			cuts = cuts.replace(uncertaintySources[index-1],source)
		yields.append(float(createHistoFromTree(tree, "p4.M()", cuts, 300, 0, 300).Integral()))
		histos.append(createHistoFromTree(tree, source, "", 40, 0, 400))
	if yields[0] > 0:
		result = sqrt( max((yields[1]-yields[0])/yields[0],(yields[1]-yields[0])/yields[0])**2 + max((yields[3]-yields[0])/yields[0],(yields[4]-yields[0])/yields[0])**2 + max((yields[5]-yields[0])/yields[0],(yields[6]-yields[0])/yields[0])**2 + max((yields[7]-yields[0])/yields[0],(yields[8]-yields[0])/yields[0])**2 + max((yields[9]-yields[0])/yields[0],(yields[10]-yields[0])/yields[0])**2 + max((yields[11]-yields[0])/yields[0],(yields[12]-yields[0])/yields[0])**2)
	else:
		result = 0
	
	
	#~ hCanvas = TCanvas("hCanvas", "Distribution", 800,800)

	#~ plotPad = ROOT.TPad("plotPad","plotPad",0,0,1,1)
	#~ ratioPad = ROOT.TPad("ratioPad","ratioPad",0,0.,1,0.3)
	#~ setTDRStyle()		
	#~ plotPad.UseCurrentStyle()
	#~ ratioPad.UseCurrentStyle()
	#~ plotPad.Draw()	
	#~ ratioPad.Draw()	
	#~ plotPad.cd()	
#~ 
#~ 
	#~ legend = TLegend(0.4, 0.4, 0.95, 0.95)
	#~ legend.SetFillStyle(0)
	#~ legend.SetBorderSize(1)
			#~ 
	#~ hCanvas.DrawFrame(0,0.1,400,1500,"; %s ; %s" %("E^{miss}_{T} [GeV]","Events / 10 GeV"))
#~ 
	#~ latex = ROOT.TLatex()
	#~ latex.SetTextSize(0.05)
	#~ latex.SetTextFont(42)
	#~ latex.SetNDC(True)
	#~ latex.DrawLatex(0.13, 0.96, "CMS Simulation,   #sqrt{s} = 8 TeV,	 #scale[0.6]{#int}Ldt = 19.4 fb^{-1}")	
	#~ 
	#~ 
	#~ for i, histo in enumerate(histos):
		#~ histo.SetLineColor(colors[i])
		#~ if i == 0:
			#~ histo.SetLineWidth(4)
			#~ legend.AddEntry(histo,"E_{T}^{miss}","l")
		#~ else:
			#~ histo.SetLineWidth(2)
			#~ legend.AddEntry(histo,uncertaintySources[i-1],"l")
		#~ histo.Draw("samehist")
			#~ 
	#~ legend.Draw("same")
	#~ hCanvas.Print("fig/metUncertainty_%s_%s.pdf"%(sampleName,dilepton))	

	
	
	
	return result,yields[0],yields[1],yields[2],yields[3],yields[4],yields[5],yields[6],yields[7],yields[8],yields[9],yields[10],yields[11],yields[12]		
	
def produceJetUncertainty(tree,cuts,dilepton):
	
	uncertaintySources = ["nJetsEnUp","nJetsEnDown","nJetsResUp","nJetsResDown"]
	colors=[ROOT.kBlack,ROOT.kBlue,ROOT.kGreen+3,ROOT.kGreen+3,ROOT.kOrange+2,ROOT.kOrange+2]

	result = 0.
	defaultTree = tree.CopyTree(cuts)
	yields = [float(createHistoFromTree(tree, "p4.M()", cuts, 300, 0, 300).Integral())]
	histos = [createHistoFromTree(tree, "nJets", "", 10, 0, 10)]
	histos.append(createHistoFromTree(tree, "nJetsSmeared", "", 10, 0, 10))

	for index, source in enumerate(uncertaintySources):
		if index == 0:
			cuts = cuts.replace("nJetsSmeared",source)
		else:
			cuts = cuts.replace(uncertaintySources[index-1],source)
		yields.append(float(createHistoFromTree(tree, "p4.M()", cuts, 300, 0, 300).Integral()))
		histos.append(createHistoFromTree(tree, source, "", 10, 0, 10))
	
	if 	yields[0] > 0:
		result = sqrt( max((yields[1]-yields[0])/yields[0],(yields[1]-yields[0])/yields[0])**2 + max((yields[3]-yields[0])/yields[0],(yields[4]-yields[0])/yields[0])**2 )
	else:
		result = 0	

	#~ hCanvas = TCanvas("hCanvas", "Distribution", 800,800)

	#~ plotPad = ROOT.TPad("plotPad","plotPad",0,0,1,1)
	#~ ratioPad = ROOT.TPad("ratioPad","ratioPad",0,0.,1,0.3)
	#~ setTDRStyle()		
	#~ plotPad.UseCurrentStyle()
	#~ ratioPad.UseCurrentStyle()
	#~ plotPad.Draw()	
	#~ ratioPad.Draw()	
	#~ plotPad.cd()	


	#~ legend = TLegend(0.5, 0.6, 0.95, 0.95)
	#~ legend.SetFillStyle(0)
	#~ legend.SetBorderSize(1)
			
	#~ hCanvas.DrawFrame(0,0.1,10,4000,"; %s ; %s" %("N_{jets}","Events"))
#~ 
	#~ latex = ROOT.TLatex()
	#~ latex.SetTextSize(0.05)
	#~ latex.SetTextFont(42)
	#~ latex.SetNDC(True)
	#~ latex.DrawLatex(0.13, 0.96, "CMS Simulation,   #sqrt{s} = 8 TeV,	 #scale[0.6]{#int}Ldt = 19.4 fb^{-1}")	
	#~ 
	#~ 
	#~ for i, histo in enumerate(histos):
		#~ histo.SetLineColor(colors[i])
		#~ if i == 0:
			#~ histo.SetLineWidth(4)
			#~ legend.AddEntry(histo,"N_{jets}","l")
		#~ elif i == 1:
			#~ histo.SetLineWidth(4)
			#~ legend.AddEntry(histo,"N_{jets} smeared","l")
		#~ else:
			#~ histo.SetLineWidth(2)
			#~ legend.AddEntry(histo,uncertaintySources[i-2],"l")
		#~ histo.Draw("samehist")
			#~ 
	#~ legend.Draw("same")
	#~ hCanvas.Print("fig/jetUncertainty_%s_%s.pdf"%(sampleName,dilepton))	


	return result,yields[0],yields[1],yields[2],yields[3],yields[4]
	
#~ def produceLeptonUncertainty(tree,cuts,dilepton):
	#~ 
	#~ uncertaintySources = ["pt1ScaleUp","pt1ScaleDown","pt2ScaleUp","pt2ScaleDown"]
	#~ result = 0.
	#~ defaultTree = tree.CopyTree(cuts)
	#~ yields = [float(createHistoFromTree(tree, "p4.M()", cuts, 300, 0, 300).Integral())]
	#~ if yields[0] > 0:
		#~ if dilepton == "EMu":
			#~ for index, source in enumerate(uncertaintySources):
				#~ if index == 0:
					#~ cuts = cuts.replace("pt1",source)
				#~ elif index == 2:
					#~ cuts = cuts.replace(uncertaintySources[1],"pt1")
					#~ cuts = cuts.replace("pt2",source)
				#~ else:
					#~ cuts = cuts.replace(uncertaintySources[index-1],source)
				#~ yields.append(float(createHistoFromTree(tree, "p4.M()", cuts, 300, 0, 300).Integral()))
			#~ result = sqrt( max((yields[1]-yields[0])/yields[0],(yields[1]-yields[0])/yields[0])**2 + max((yields[3]-yields[0])/yields[0],(yields[4]-yields[0])/yields[0])**2 )		
		#~ else:
			#~ cuts = cuts.replace("pt1","pt1ScaleUp")
			#~ cuts = cuts.replace("pt2","pt2ScaleUp")
			#~ yields.append(float(createHistoFromTree(tree, "p4.M()", cuts, 300, 0, 300).Integral()))
			#~ result = sqrt(result**2 + ((yields[1]-yields[0])/yields[0])**2)	
			#~ cuts = cuts.replace("pt1ScaleUp","pt1ScaleDown")
			#~ cuts = cuts.replace("pt2ScaleUp","pt2ScaleDown")
			#~ yields.append(float(createHistoFromTree(tree, "p4.M()", cuts, 300, 0, 300).Integral()))
			#~ result = sqrt(max(result**2 ,((yields[2]-yields[0])/yields[0])**2))
	#~ else:
		#~ result = 0
			#~ 
	#~ return result

def produceLeptonUncertaintyEMu(tree,cuts,dilepton,region):
   
	uncertaintySources = ["pt1ScaleUp","pt1ScaleDown","pt2ScaleUp","pt2ScaleDown"]
	result = 0.
	defaultTree = tree.CopyTree(cuts)
	yields = [float(createHistoFromTree(tree, "p4.M()", cuts, 300, 0, 300).Integral())]
	for index, source in enumerate(uncertaintySources):
		if index == 0:
			cuts = cuts.replace("pt1",source)
		elif index == 2:
			cuts = cuts.replace(uncertaintySources[1],"pt1")
			cuts = cuts.replace("pt2",source)
		else:
			cuts = cuts.replace(uncertaintySources[index-1],source)
		yields.append(float(createHistoFromTree(tree, "p4.M()", cuts, 300, 0, 300).Integral()))
	if yields[0] > 0:
		result = sqrt( max((yields[1]-yields[0])/yields[0],(yields[2]-yields[0])/yields[0])**2 + max((yields[3]-yields[0])/yields[0],(yields[4]-yields[0])/yields[0])**2 )
	else:
		result = 0
	return result,yields[0],yields[1],yields[2],yields[3],yields[4]
	
	  
def produceLeptonUncertaintySF(tree,cuts,dilepton,region):
   
	uncertaintySources = ["pt1ScaleUp","pt1ScaleDown","pt2ScaleUp","pt2ScaleDown"]
	result = 0.
	defaultTree = tree.CopyTree(cuts)
	yields = [float(createHistoFromTree(tree, "p4.M()", cuts, 300, 0, 300).Integral())]
	cuts = cuts.replace("pt1","pt1ScaleUp")
	cuts = cuts.replace("pt2","pt2ScaleUp")
	cuts = cuts.replace("p4.M()","p4.M()*%s"%ptScales[dilepton][region])
	yields.append(float(createHistoFromTree(tree, "p4.M()", cuts, 300, 0, 300).Integral()))
	if yields[0] > 0:
		result = sqrt(result**2 + ((yields[1]-yields[0])/yields[0])**2)
	else:
		result = 0
	cuts = cuts.replace("pt1ScaleUp","pt1ScaleDown")
	cuts = cuts.replace("pt2ScaleUp","pt2ScaleDown")
	cuts = cuts.replace("p4.M()*%s"%ptScales[dilepton][region],"p4.M()/%s"%ptScales[dilepton][region])
	yields.append(float(createHistoFromTree(tree, "p4.M()", cuts, 300, 0, 300).Integral()))
	if yields[0] > 0:
		result = sqrt(max(result**2 ,((yields[2]-yields[0])/yields[0])**2))
	else:
		result = 0
	#~ return result	
	return result,yields[0],yields[1],yields[2]
			
def produceISRUncertainty(tree,cuts,dilepton,ISR_incl_cuts):
	
	uncertaintySources = ["(sbottomWeight+(1-sbottomWeight))","(sbottomWeight-(1-sbottomWeight))"]
	result = 0.
	#~ defaultTree = tree.CopyTree(cuts)
	incl_yields_unweighted =  float(createHistoFromTree(tree, "p4.M()", ISR_incl_cuts, 300, 0, 300).Integral())
	incl_yields_weighted =  float(createHistoFromTree(tree, "p4.M()", "sbottomWeight * %s"%ISR_incl_cuts, 300, 0, 300).Integral())
	if incl_yields_weighted > 0:
		correctionFactor = incl_yields_unweighted / incl_yields_weighted
	else:
		correctionFactor = 0
		print "ISR rewweighting not possible"
	yields = [float(createHistoFromTree(tree, "p4.M()", cuts, 300, 0, 300).Integral())*correctionFactor]
	cuts = cuts.replace("sbottomWeight","(sbottomWeight+(1-sbottomWeight))")
	yields.append(float(createHistoFromTree(tree, "p4.M()", cuts, 300, 0, 300).Integral()))
	if yields[0] > 0:
		result = sqrt(result**2 + ((yields[1]-yields[0])/yields[0])**2)	
	cuts = cuts.replace("(sbottomWeight+(1-sbottomWeight))","(sbottomWeight-(1-sbottomWeight))")
	yields.append(float(createHistoFromTree(tree, "p4.M()", cuts, 300, 0, 300).Integral())*correctionFactor**2)
	if yields[0] > 0:
		result = sqrt(max(result**2 ,((yields[2]-yields[0])/yields[0])**2))
	else:
		result = 0
	
	#~ print "Incl yields unweighted: "+str(incl_yields_unweighted)
	#~ print "Incl yields ISR weighted: "+str(incl_yields_weighted)
	#~ print "Correction Factor: "+str(correctionFactor)
	#~ print "ISR weighted yields: "+str(yields[0])
	#~ print "2x ISR weighted yields: "+str(yields[2])
	#~ print "Unweighted yields: "+str(yields[1])
			
	#~ return result
	return result,yields[0],yields[1],yields[2],correctionFactor
	
def signalNumbers(tree,etaRegion,mllRegion,dilepton,electronScaleFactors,muonScaleFactors,additionalCut,m_neutr_1_fix):
		
	### Only to check whether the normalization is right for the slepton model for the files in which the generated slepton number is not correct
	FourGenLeptonEvents = 0
	ThreeGenLeptonEvents = 0
	OneGenLeptonNeutrinoEvents = 0
	OneGenLeptonQuarkEvents = 0
	TwoGenLeptonNeutrinoEvents = 0
	TwoGenLeptonZQuarkEvents = 0
	TwoGenLeptonSleptonEvents = 0
	FourGenLeptonEventsReweighted = 0
	ThreeGenLeptonEventsReweighted = 0
	OneGenLeptonNeutrinoEventsReweighted = 0
	OneGenLeptonQuarkEventsReweighted = 0
	TwoGenLeptonNeutrinoEventsReweighted = 0
	TwoGenLeptonZQuarkEventsReweighted = 0
	TwoGenLeptonSleptonEventsReweighted = 0
	####
	
	signalEvents = 0
	MCEvents = 0
	mll_lower_Cut = eventLowerMllCuts[mllRegion]
	mll_upper_Cut = eventUpperMllCuts[mllRegion]
	if m_neutr_1_fix == False:
		if additionalCut == "NJets3Cut":
			if dilepton == "EE":
				if etaRegion == "Barrel":
					for ev in tree:
						if ev.chargeProduct < 0 and abs(ev.eta1) < 1.4 and abs(ev.eta2) < 1.4 and ev.pt1 > 20 and ev.pt2 > 20 and ev.inv > mll_lower_Cut and ev.inv < mll_upper_Cut and ev.nJetsSmeared >= 3 and abs(ev.eta1) < 2.4 and abs(ev.eta2) < 2.4 and ev.deltaR > 0.3:
							MCEvents +=1
							if ev.nGenSUSYLeptons == 4:
								signalEvents += 9*0.0102 * ev.weight * ev.sbottomWeight * electronScaleFactors.GetBinContent(electronScaleFactors.GetXaxis().FindBin(ev.pt1),electronScaleFactors.GetYaxis().FindBin(abs(ev.eta1))) * electronScaleFactors.GetBinContent(electronScaleFactors.GetXaxis().FindBin(ev.pt2),electronScaleFactors.GetYaxis().FindBin(abs(ev.eta2)))
							elif ev.nGenSUSYLeptons == 2 and ev.nGenSUSYNeutrinos == 0:
								signalEvents += 9./2. * 0.1411 * ev.weight * ev.sbottomWeight * electronScaleFactors.GetBinContent(electronScaleFactors.GetXaxis().FindBin(ev.pt1),electronScaleFactors.GetYaxis().FindBin(abs(ev.eta1))) * electronScaleFactors.GetBinContent(electronScaleFactors.GetXaxis().FindBin(ev.pt2),electronScaleFactors.GetYaxis().FindBin(abs(ev.eta2)))
							elif ev.nGenSUSYLeptons == 2 and ev.nGenSUSYNeutrinos == 2:
								signalEvents += 9./2. * 0.0404 * ev.weight * ev.sbottomWeight * electronScaleFactors.GetBinContent(electronScaleFactors.GetXaxis().FindBin(ev.pt1),electronScaleFactors.GetYaxis().FindBin(abs(ev.eta1))) * electronScaleFactors.GetBinContent(electronScaleFactors.GetXaxis().FindBin(ev.pt2),electronScaleFactors.GetYaxis().FindBin(abs(ev.eta2)))
							elif ev.nGenSUSYLeptons == 0 and ev.nGenSUSYNeutrinos == 4:
								signalEvents += 9 * 0.04 * ev.weight * ev.sbottomWeight * electronScaleFactors.GetBinContent(electronScaleFactors.GetXaxis().FindBin(ev.pt1),electronScaleFactors.GetYaxis().FindBin(abs(ev.eta1))) * electronScaleFactors.GetBinContent(electronScaleFactors.GetXaxis().FindBin(ev.pt2),electronScaleFactors.GetYaxis().FindBin(abs(ev.eta2)))
							elif ev.nGenSUSYLeptons == 0 and ev.nGenSUSYNeutrinos == 2:
								signalEvents +=  9./2. * 0.2796 * ev.weight * ev.sbottomWeight * electronScaleFactors.GetBinContent(electronScaleFactors.GetXaxis().FindBin(ev.pt1),electronScaleFactors.GetYaxis().FindBin(abs(ev.eta1))) * electronScaleFactors.GetBinContent(electronScaleFactors.GetXaxis().FindBin(ev.pt2),electronScaleFactors.GetYaxis().FindBin(abs(ev.eta2)))
							elif ev.nGenSUSYLeptons == 0 and ev.nGenSUSYNeutrinos == 0:
								signalEvents +=  9 * 0.4887 * ev.weight * ev.sbottomWeight * electronScaleFactors.GetBinContent(electronScaleFactors.GetXaxis().FindBin(ev.pt1),electronScaleFactors.GetYaxis().FindBin(abs(ev.eta1))) * electronScaleFactors.GetBinContent(electronScaleFactors.GetXaxis().FindBin(ev.pt2),electronScaleFactors.GetYaxis().FindBin(abs(ev.eta2)))
				elif etaRegion == "Endcap":
					for ev in tree:
						if ev.chargeProduct < 0 and (((abs(ev.eta1) < 1.4 or abs(ev.eta1) > 1.6) and (abs(ev.eta2) < 1.4 or abs(ev.eta2) > 1.6)) and 1.6 <= max(abs(ev.eta1),abs(ev.eta2))) and ev.pt1 > 20 and ev.pt2 > 20 and ev.inv > mll_lower_Cut and ev.inv < mll_upper_Cut and ev.nJetsSmeared >= 3 and abs(ev.eta1) < 2.4 and abs(ev.eta2) < 2.4 and ev.deltaR > 0.3:
							MCEvents +=1
							if ev.nGenSUSYLeptons == 4:
								signalEvents += 9*0.0102 * ev.weight * ev.sbottomWeight * electronScaleFactors.GetBinContent(electronScaleFactors.GetXaxis().FindBin(ev.pt1),electronScaleFactors.GetYaxis().FindBin(abs(ev.eta1))) * electronScaleFactors.GetBinContent(electronScaleFactors.GetXaxis().FindBin(ev.pt2),electronScaleFactors.GetYaxis().FindBin(abs(ev.eta2)))
							elif ev.nGenSUSYLeptons == 2 and ev.nGenSUSYNeutrinos == 0:
								signalEvents += 9./2. * 0.1411 * ev.weight * ev.sbottomWeight * electronScaleFactors.GetBinContent(electronScaleFactors.GetXaxis().FindBin(ev.pt1),electronScaleFactors.GetYaxis().FindBin(abs(ev.eta1))) * electronScaleFactors.GetBinContent(electronScaleFactors.GetXaxis().FindBin(ev.pt2),electronScaleFactors.GetYaxis().FindBin(abs(ev.eta2)))
							elif ev.nGenSUSYLeptons == 2 and ev.nGenSUSYNeutrinos == 2:
								signalEvents += 9./2. * 0.0404 * ev.weight * ev.sbottomWeight * electronScaleFactors.GetBinContent(electronScaleFactors.GetXaxis().FindBin(ev.pt1),electronScaleFactors.GetYaxis().FindBin(abs(ev.eta1))) * electronScaleFactors.GetBinContent(electronScaleFactors.GetXaxis().FindBin(ev.pt2),electronScaleFactors.GetYaxis().FindBin(abs(ev.eta2)))
							elif ev.nGenSUSYLeptons == 0 and ev.nGenSUSYNeutrinos == 4:
								signalEvents += 9 * 0.04 * ev.weight * ev.sbottomWeight * electronScaleFactors.GetBinContent(electronScaleFactors.GetXaxis().FindBin(ev.pt1),electronScaleFactors.GetYaxis().FindBin(abs(ev.eta1))) * electronScaleFactors.GetBinContent(electronScaleFactors.GetXaxis().FindBin(ev.pt2),electronScaleFactors.GetYaxis().FindBin(abs(ev.eta2)))
							elif ev.nGenSUSYLeptons == 0 and ev.nGenSUSYNeutrinos == 2:
								signalEvents +=  9./2. * 0.2796 * ev.weight * ev.sbottomWeight * electronScaleFactors.GetBinContent(electronScaleFactors.GetXaxis().FindBin(ev.pt1),electronScaleFactors.GetYaxis().FindBin(abs(ev.eta1))) * electronScaleFactors.GetBinContent(electronScaleFactors.GetXaxis().FindBin(ev.pt2),electronScaleFactors.GetYaxis().FindBin(abs(ev.eta2)))
							elif ev.nGenSUSYLeptons == 0 and ev.nGenSUSYNeutrinos == 0:
								signalEvents +=  9 * 0.4887 * ev.weight * ev.sbottomWeight * electronScaleFactors.GetBinContent(electronScaleFactors.GetXaxis().FindBin(ev.pt1),electronScaleFactors.GetYaxis().FindBin(abs(ev.eta1))) * electronScaleFactors.GetBinContent(electronScaleFactors.GetXaxis().FindBin(ev.pt2),electronScaleFactors.GetYaxis().FindBin(abs(ev.eta2)))
			elif dilepton == "MuMu":
				if etaRegion == "Barrel":
					for ev in tree:
						if ev.chargeProduct < 0 and abs(ev.eta1) < 1.4 and abs(ev.eta2) < 1.4 and ev.pt1 > 20 and ev.pt2 > 20 and ev.inv > mll_lower_Cut and ev.inv < mll_upper_Cut and ev.nJetsSmeared >= 3 and abs(ev.eta1) < 2.4 and abs(ev.eta2) < 2.4 and ev.deltaR > 0.3:
							MCEvents +=1
							if ev.nGenSUSYLeptons == 4:
								signalEvents += 9*0.0102 * ev.weight * ev.sbottomWeight * muonScaleFactors.GetBinContent(muonScaleFactors.GetXaxis().FindBin(ev.pt1),muonScaleFactors.GetYaxis().FindBin(abs(ev.eta1))) * muonScaleFactors.GetBinContent(muonScaleFactors.GetXaxis().FindBin(ev.pt2),muonScaleFactors.GetYaxis().FindBin(abs(ev.eta2)))
							elif ev.nGenSUSYLeptons == 2 and ev.nGenSUSYNeutrinos == 0:
								signalEvents += 9./2. * 0.1411 * ev.weight * ev.sbottomWeight * muonScaleFactors.GetBinContent(muonScaleFactors.GetXaxis().FindBin(ev.pt1),muonScaleFactors.GetYaxis().FindBin(abs(ev.eta1))) * muonScaleFactors.GetBinContent(muonScaleFactors.GetXaxis().FindBin(ev.pt2),muonScaleFactors.GetYaxis().FindBin(abs(ev.eta2)))
							elif ev.nGenSUSYLeptons == 2 and ev.nGenSUSYNeutrinos == 2:
								signalEvents += 9./2. * 0.0404 * ev.weight * ev.sbottomWeight * muonScaleFactors.GetBinContent(muonScaleFactors.GetXaxis().FindBin(ev.pt1),muonScaleFactors.GetYaxis().FindBin(abs(ev.eta1))) * muonScaleFactors.GetBinContent(muonScaleFactors.GetXaxis().FindBin(ev.pt2),muonScaleFactors.GetYaxis().FindBin(abs(ev.eta2)))
							elif ev.nGenSUSYLeptons == 0 and ev.nGenSUSYNeutrinos == 4:
								signalEvents += 9 * 0.04 * ev.weight * ev.sbottomWeight * muonScaleFactors.GetBinContent(muonScaleFactors.GetXaxis().FindBin(ev.pt1),muonScaleFactors.GetYaxis().FindBin(abs(ev.eta1))) * muonScaleFactors.GetBinContent(muonScaleFactors.GetXaxis().FindBin(ev.pt2),muonScaleFactors.GetYaxis().FindBin(abs(ev.eta2)))
							elif ev.nGenSUSYLeptons == 0 and ev.nGenSUSYNeutrinos == 2:
								signalEvents +=  9./2. * 0.2796 * ev.weight * ev.sbottomWeight * muonScaleFactors.GetBinContent(muonScaleFactors.GetXaxis().FindBin(ev.pt1),muonScaleFactors.GetYaxis().FindBin(abs(ev.eta1))) * muonScaleFactors.GetBinContent(muonScaleFactors.GetXaxis().FindBin(ev.pt2),muonScaleFactors.GetYaxis().FindBin(abs(ev.eta2)))
							elif ev.nGenSUSYLeptons == 0 and ev.nGenSUSYNeutrinos == 0:
								signalEvents +=  9 * 0.4887 * ev.weight * ev.sbottomWeight * muonScaleFactors.GetBinContent(muonScaleFactors.GetXaxis().FindBin(ev.pt1),muonScaleFactors.GetYaxis().FindBin(abs(ev.eta1))) * muonScaleFactors.GetBinContent(muonScaleFactors.GetXaxis().FindBin(ev.pt2),muonScaleFactors.GetYaxis().FindBin(abs(ev.eta2)))
				elif etaRegion == "Endcap":
					for ev in tree:
						if ev.chargeProduct < 0 and (((abs(ev.eta1) < 1.4 or abs(ev.eta1) > 1.6) and (abs(ev.eta2) < 1.4 or abs(ev.eta2) > 1.6)) and 1.6 <= max(abs(ev.eta1),abs(ev.eta2))) and ev.pt1 > 20 and ev.pt2 > 20 and ev.inv > mll_lower_Cut and ev.inv < mll_upper_Cut and ev.nJetsSmeared >= 3 and abs(ev.eta1) < 2.4 and abs(ev.eta2) < 2.4 and ev.deltaR > 0.3:
							MCEvents +=1
							if ev.nGenSUSYLeptons == 4:
								signalEvents += 9*0.0102 * ev.weight * ev.sbottomWeight * muonScaleFactors.GetBinContent(muonScaleFactors.GetXaxis().FindBin(ev.pt1),muonScaleFactors.GetYaxis().FindBin(abs(ev.eta1))) * muonScaleFactors.GetBinContent(muonScaleFactors.GetXaxis().FindBin(ev.pt2),muonScaleFactors.GetYaxis().FindBin(abs(ev.eta2)))
							elif ev.nGenSUSYLeptons == 2 and ev.nGenSUSYNeutrinos == 0:
								signalEvents += 9./2. * 0.1411 * ev.weight * ev.sbottomWeight * muonScaleFactors.GetBinContent(muonScaleFactors.GetXaxis().FindBin(ev.pt1),muonScaleFactors.GetYaxis().FindBin(abs(ev.eta1))) * muonScaleFactors.GetBinContent(muonScaleFactors.GetXaxis().FindBin(ev.pt2),muonScaleFactors.GetYaxis().FindBin(abs(ev.eta2)))
							elif ev.nGenSUSYLeptons == 2 and ev.nGenSUSYNeutrinos == 2:
								signalEvents += 9./2. * 0.0404 * ev.weight * ev.sbottomWeight * muonScaleFactors.GetBinContent(muonScaleFactors.GetXaxis().FindBin(ev.pt1),muonScaleFactors.GetYaxis().FindBin(abs(ev.eta1))) * muonScaleFactors.GetBinContent(muonScaleFactors.GetXaxis().FindBin(ev.pt2),muonScaleFactors.GetYaxis().FindBin(abs(ev.eta2)))
							elif ev.nGenSUSYLeptons == 0 and ev.nGenSUSYNeutrinos == 4:
								signalEvents += 9 * 0.04 * ev.weight * ev.sbottomWeight * muonScaleFactors.GetBinContent(muonScaleFactors.GetXaxis().FindBin(ev.pt1),muonScaleFactors.GetYaxis().FindBin(abs(ev.eta1))) * muonScaleFactors.GetBinContent(muonScaleFactors.GetXaxis().FindBin(ev.pt2),muonScaleFactors.GetYaxis().FindBin(abs(ev.eta2)))
							elif ev.nGenSUSYLeptons == 0 and ev.nGenSUSYNeutrinos == 2:
								signalEvents +=  9./2. * 0.2796 * ev.weight * ev.sbottomWeight * muonScaleFactors.GetBinContent(muonScaleFactors.GetXaxis().FindBin(ev.pt1),muonScaleFactors.GetYaxis().FindBin(abs(ev.eta1))) * muonScaleFactors.GetBinContent(muonScaleFactors.GetXaxis().FindBin(ev.pt2),muonScaleFactors.GetYaxis().FindBin(abs(ev.eta2)))
							elif ev.nGenSUSYLeptons == 0 and ev.nGenSUSYNeutrinos == 0:
								signalEvents +=  9 * 0.4887 * ev.weight * ev.sbottomWeight * muonScaleFactors.GetBinContent(muonScaleFactors.GetXaxis().FindBin(ev.pt1),muonScaleFactors.GetYaxis().FindBin(abs(ev.eta1))) * muonScaleFactors.GetBinContent(muonScaleFactors.GetXaxis().FindBin(ev.pt2),muonScaleFactors.GetYaxis().FindBin(abs(ev.eta2)))
			elif dilepton == "EMu":
				if etaRegion == "Barrel":
					for ev in tree:
						if ev.chargeProduct < 0 and abs(ev.eta1) < 1.4 and abs(ev.eta2) < 1.4 and ev.pt1 > 20 and ev.pt2 > 20 and ev.inv > mll_lower_Cut and ev.inv < mll_upper_Cut and ev.nJetsSmeared >= 3 and abs(ev.eta1) < 2.4 and abs(ev.eta2) < 2.4 and ev.deltaR > 0.3:
							MCEvents +=1
							if ev.nGenSUSYLeptons == 4:
								signalEvents += 9*0.0102 * ev.weight * ev.sbottomWeight * electronScaleFactors.GetBinContent(electronScaleFactors.GetXaxis().FindBin(ev.pt1),electronScaleFactors.GetYaxis().FindBin(abs(ev.eta1))) * muonScaleFactors.GetBinContent(muonScaleFactors.GetXaxis().FindBin(ev.pt2),muonScaleFactors.GetYaxis().FindBin(abs(ev.eta2)))
							elif ev.nGenSUSYLeptons == 2 and ev.nGenSUSYNeutrinos == 0:
								signalEvents += 9./2. * 0.1411 * ev.weight * ev.sbottomWeight * electronScaleFactors.GetBinContent(electronScaleFactors.GetXaxis().FindBin(ev.pt1),electronScaleFactors.GetYaxis().FindBin(abs(ev.eta1))) * muonScaleFactors.GetBinContent(muonScaleFactors.GetXaxis().FindBin(ev.pt2),muonScaleFactors.GetYaxis().FindBin(abs(ev.eta2)))
							elif ev.nGenSUSYLeptons == 2 and ev.nGenSUSYNeutrinos == 2:
								signalEvents += 9./2. * 0.0404 * ev.weight * ev.sbottomWeight * electronScaleFactors.GetBinContent(electronScaleFactors.GetXaxis().FindBin(ev.pt1),electronScaleFactors.GetYaxis().FindBin(abs(ev.eta1))) * muonScaleFactors.GetBinContent(muonScaleFactors.GetXaxis().FindBin(ev.pt2),muonScaleFactors.GetYaxis().FindBin(abs(ev.eta2)))
							elif ev.nGenSUSYLeptons == 0 and ev.nGenSUSYNeutrinos == 4:
								signalEvents += 9 * 0.04 * ev.weight * ev.sbottomWeight * electronScaleFactors.GetBinContent(electronScaleFactors.GetXaxis().FindBin(ev.pt1),electronScaleFactors.GetYaxis().FindBin(abs(ev.eta1))) * muonScaleFactors.GetBinContent(muonScaleFactors.GetXaxis().FindBin(ev.pt2),muonScaleFactors.GetYaxis().FindBin(abs(ev.eta2)))
							elif ev.nGenSUSYLeptons == 0 and ev.nGenSUSYNeutrinos == 2:
								signalEvents +=  9./2. * 0.2796 * ev.weight * ev.sbottomWeight * electronScaleFactors.GetBinContent(electronScaleFactors.GetXaxis().FindBin(ev.pt1),electronScaleFactors.GetYaxis().FindBin(abs(ev.eta1))) * muonScaleFactors.GetBinContent(muonScaleFactors.GetXaxis().FindBin(ev.pt2),muonScaleFactors.GetYaxis().FindBin(abs(ev.eta2)))
							elif ev.nGenSUSYLeptons == 0 and ev.nGenSUSYNeutrinos == 0:
								signalEvents +=  9 * 0.4887 * ev.weight * ev.sbottomWeight * electronScaleFactors.GetBinContent(electronScaleFactors.GetXaxis().FindBin(ev.pt1),electronScaleFactors.GetYaxis().FindBin(abs(ev.eta1))) * muonScaleFactors.GetBinContent(muonScaleFactors.GetXaxis().FindBin(ev.pt2),muonScaleFactors.GetYaxis().FindBin(abs(ev.eta2)))
				elif etaRegion == "Endcap":
					for ev in tree:
						MCEvents +=1
						if ev.chargeProduct < 0 and (((abs(ev.eta1) < 1.4 or abs(ev.eta1) > 1.6) and (abs(ev.eta2) < 1.4 or abs(ev.eta2) > 1.6)) and 1.6 <= max(abs(ev.eta1),abs(ev.eta2))) and ev.pt1 > 20 and ev.pt2 > 20 and ev.inv > mll_lower_Cut and ev.inv < mll_upper_Cut and ev.nJetsSmeared >= 3 and abs(ev.eta1) < 2.4 and abs(ev.eta2) < 2.4 and ev.deltaR > 0.3:
							if ev.nGenSUSYLeptons == 4:
								signalEvents += 9*0.0102 * ev.weight * ev.sbottomWeight * electronScaleFactors.GetBinContent(electronScaleFactors.GetXaxis().FindBin(ev.pt1),electronScaleFactors.GetYaxis().FindBin(abs(ev.eta1))) * muonScaleFactors.GetBinContent(muonScaleFactors.GetXaxis().FindBin(ev.pt2),muonScaleFactors.GetYaxis().FindBin(abs(ev.eta2)))
							elif ev.nGenSUSYLeptons == 2 and ev.nGenSUSYNeutrinos == 0:
								signalEvents += 9./2. * 0.1411 * ev.weight * ev.sbottomWeight * electronScaleFactors.GetBinContent(electronScaleFactors.GetXaxis().FindBin(ev.pt1),electronScaleFactors.GetYaxis().FindBin(abs(ev.eta1))) * muonScaleFactors.GetBinContent(muonScaleFactors.GetXaxis().FindBin(ev.pt2),muonScaleFactors.GetYaxis().FindBin(abs(ev.eta2)))
							elif ev.nGenSUSYLeptons == 2 and ev.nGenSUSYNeutrinos == 2:
								signalEvents += 9./2. * 0.0404 * ev.weight * ev.sbottomWeight * electronScaleFactors.GetBinContent(electronScaleFactors.GetXaxis().FindBin(ev.pt1),electronScaleFactors.GetYaxis().FindBin(abs(ev.eta1))) * muonScaleFactors.GetBinContent(muonScaleFactors.GetXaxis().FindBin(ev.pt2),muonScaleFactors.GetYaxis().FindBin(abs(ev.eta2)))
							elif ev.nGenSUSYLeptons == 0 and ev.nGenSUSYNeutrinos == 4:
								signalEvents += 9 * 0.04 * ev.weight * ev.sbottomWeight * electronScaleFactors.GetBinContent(electronScaleFactors.GetXaxis().FindBin(ev.pt1),electronScaleFactors.GetYaxis().FindBin(abs(ev.eta1))) * muonScaleFactors.GetBinContent(muonScaleFactors.GetXaxis().FindBin(ev.pt2),muonScaleFactors.GetYaxis().FindBin(abs(ev.eta2)))
							elif ev.nGenSUSYLeptons == 0 and ev.nGenSUSYNeutrinos == 2:
								signalEvents +=  9./2. * 0.2796 * ev.weight * ev.sbottomWeight * electronScaleFactors.GetBinContent(electronScaleFactors.GetXaxis().FindBin(ev.pt1),electronScaleFactors.GetYaxis().FindBin(abs(ev.eta1))) * muonScaleFactors.GetBinContent(muonScaleFactors.GetXaxis().FindBin(ev.pt2),muonScaleFactors.GetYaxis().FindBin(abs(ev.eta2)))
							elif ev.nGenSUSYLeptons == 0 and ev.nGenSUSYNeutrinos == 0:
								signalEvents +=  9 * 0.4887 * ev.weight * ev.sbottomWeight * electronScaleFactors.GetBinContent(electronScaleFactors.GetXaxis().FindBin(ev.pt1),electronScaleFactors.GetYaxis().FindBin(abs(ev.eta1))) * muonScaleFactors.GetBinContent(muonScaleFactors.GetXaxis().FindBin(ev.pt2),muonScaleFactors.GetYaxis().FindBin(abs(ev.eta2)))
						
		elif additionalCut == "Met150Cut":
			if dilepton == "EE":
				if etaRegion == "Barrel":
					for ev in tree: 
						if ev.chargeProduct < 0 and abs(ev.eta1) < 1.4 and abs(ev.eta2) < 1.4 and ev.pt1 > 20 and ev.pt2 > 20 and ev.inv > mll_lower_Cut and ev.inv < mll_upper_Cut and ev.patPFMet > 150 and abs(ev.eta1) < 2.4 and abs(ev.eta2) < 2.4 and ev.deltaR > 0.3:
							MCEvents +=1
							if ev.nGenSUSYLeptons == 4:
								signalEvents += 9*0.0102 * ev.weight * ev.sbottomWeight * electronScaleFactors.GetBinContent(electronScaleFactors.GetXaxis().FindBin(ev.pt1),electronScaleFactors.GetYaxis().FindBin(abs(ev.eta1))) * electronScaleFactors.GetBinContent(electronScaleFactors.GetXaxis().FindBin(ev.pt2),electronScaleFactors.GetYaxis().FindBin(abs(ev.eta2)))
							elif ev.nGenSUSYLeptons == 2 and ev.nGenSUSYNeutrinos == 0:
								signalEvents += 9./2. * 0.1411 * ev.weight * ev.sbottomWeight * electronScaleFactors.GetBinContent(electronScaleFactors.GetXaxis().FindBin(ev.pt1),electronScaleFactors.GetYaxis().FindBin(abs(ev.eta1))) * electronScaleFactors.GetBinContent(electronScaleFactors.GetXaxis().FindBin(ev.pt2),electronScaleFactors.GetYaxis().FindBin(abs(ev.eta2)))
							elif ev.nGenSUSYLeptons == 2 and ev.nGenSUSYNeutrinos == 2:
								signalEvents += 9./2. * 0.0404 * ev.weight * ev.sbottomWeight * electronScaleFactors.GetBinContent(electronScaleFactors.GetXaxis().FindBin(ev.pt1),electronScaleFactors.GetYaxis().FindBin(abs(ev.eta1))) * electronScaleFactors.GetBinContent(electronScaleFactors.GetXaxis().FindBin(ev.pt2),electronScaleFactors.GetYaxis().FindBin(abs(ev.eta2)))
							elif ev.nGenSUSYLeptons == 0 and ev.nGenSUSYNeutrinos == 4:
								signalEvents += 9 * 0.04 * ev.weight * ev.sbottomWeight * electronScaleFactors.GetBinContent(electronScaleFactors.GetXaxis().FindBin(ev.pt1),electronScaleFactors.GetYaxis().FindBin(abs(ev.eta1))) * electronScaleFactors.GetBinContent(electronScaleFactors.GetXaxis().FindBin(ev.pt2),electronScaleFactors.GetYaxis().FindBin(abs(ev.eta2)))
							elif ev.nGenSUSYLeptons == 0 and ev.nGenSUSYNeutrinos == 2:
								signalEvents +=  9./2. * 0.2796 * ev.weight * ev.sbottomWeight * electronScaleFactors.GetBinContent(electronScaleFactors.GetXaxis().FindBin(ev.pt1),electronScaleFactors.GetYaxis().FindBin(abs(ev.eta1))) * electronScaleFactors.GetBinContent(electronScaleFactors.GetXaxis().FindBin(ev.pt2),electronScaleFactors.GetYaxis().FindBin(abs(ev.eta2)))
							elif ev.nGenSUSYLeptons == 0 and ev.nGenSUSYNeutrinos == 0:
								signalEvents +=  9 * 0.4887 * ev.weight * ev.sbottomWeight * electronScaleFactors.GetBinContent(electronScaleFactors.GetXaxis().FindBin(ev.pt1),electronScaleFactors.GetYaxis().FindBin(abs(ev.eta1))) * electronScaleFactors.GetBinContent(electronScaleFactors.GetXaxis().FindBin(ev.pt2),electronScaleFactors.GetYaxis().FindBin(abs(ev.eta2)))
				elif etaRegion == "Endcap":
					for ev in tree:
						if ev.chargeProduct < 0 and (((abs(ev.eta1) < 1.4 or abs(ev.eta1) > 1.6) and (abs(ev.eta2) < 1.4 or abs(ev.eta2) > 1.6)) and 1.6 <= max(abs(ev.eta1),abs(ev.eta2))) and ev.pt1 > 20 and ev.pt2 > 20 and ev.inv > mll_lower_Cut and ev.inv < mll_upper_Cut and ev.patPFMet > 150 and abs(ev.eta1) < 2.4 and abs(ev.eta2) < 2.4 and ev.deltaR > 0.3:
							MCEvents +=1
							if ev.nGenSUSYLeptons == 4:
								signalEvents += 9*0.0102 * ev.weight * ev.sbottomWeight * electronScaleFactors.GetBinContent(electronScaleFactors.GetXaxis().FindBin(ev.pt1),electronScaleFactors.GetYaxis().FindBin(abs(ev.eta1))) * electronScaleFactors.GetBinContent(electronScaleFactors.GetXaxis().FindBin(ev.pt2),electronScaleFactors.GetYaxis().FindBin(abs(ev.eta2)))
							elif ev.nGenSUSYLeptons == 2 and ev.nGenSUSYNeutrinos == 0:
								signalEvents += 9./2. * 0.1411 * ev.weight * ev.sbottomWeight * electronScaleFactors.GetBinContent(electronScaleFactors.GetXaxis().FindBin(ev.pt1),electronScaleFactors.GetYaxis().FindBin(abs(ev.eta1))) * electronScaleFactors.GetBinContent(electronScaleFactors.GetXaxis().FindBin(ev.pt2),electronScaleFactors.GetYaxis().FindBin(abs(ev.eta2)))
							elif ev.nGenSUSYLeptons == 2 and ev.nGenSUSYNeutrinos == 2:
								signalEvents += 9./2. * 0.0404 * ev.weight * ev.sbottomWeight * electronScaleFactors.GetBinContent(electronScaleFactors.GetXaxis().FindBin(ev.pt1),electronScaleFactors.GetYaxis().FindBin(abs(ev.eta1))) * electronScaleFactors.GetBinContent(electronScaleFactors.GetXaxis().FindBin(ev.pt2),electronScaleFactors.GetYaxis().FindBin(abs(ev.eta2)))
							elif ev.nGenSUSYLeptons == 0 and ev.nGenSUSYNeutrinos == 4:
								signalEvents += 9 * 0.04 * ev.weight * ev.sbottomWeight * electronScaleFactors.GetBinContent(electronScaleFactors.GetXaxis().FindBin(ev.pt1),electronScaleFactors.GetYaxis().FindBin(abs(ev.eta1))) * electronScaleFactors.GetBinContent(electronScaleFactors.GetXaxis().FindBin(ev.pt2),electronScaleFactors.GetYaxis().FindBin(abs(ev.eta2)))
							elif ev.nGenSUSYLeptons == 0 and ev.nGenSUSYNeutrinos == 2:
								signalEvents +=  9./2. * 0.2796 * ev.weight * ev.sbottomWeight * electronScaleFactors.GetBinContent(electronScaleFactors.GetXaxis().FindBin(ev.pt1),electronScaleFactors.GetYaxis().FindBin(abs(ev.eta1))) * electronScaleFactors.GetBinContent(electronScaleFactors.GetXaxis().FindBin(ev.pt2),electronScaleFactors.GetYaxis().FindBin(abs(ev.eta2)))
							elif ev.nGenSUSYLeptons == 0 and ev.nGenSUSYNeutrinos == 0:
								signalEvents +=  9 * 0.4887 * ev.weight * ev.sbottomWeight * electronScaleFactors.GetBinContent(electronScaleFactors.GetXaxis().FindBin(ev.pt1),electronScaleFactors.GetYaxis().FindBin(abs(ev.eta1))) * electronScaleFactors.GetBinContent(electronScaleFactors.GetXaxis().FindBin(ev.pt2),electronScaleFactors.GetYaxis().FindBin(abs(ev.eta2)))
			elif dilepton == "MuMu":
				if etaRegion == "Barrel":
					for ev in tree:
						if ev.chargeProduct < 0 and abs(ev.eta1) < 1.4 and abs(ev.eta2) < 1.4 and ev.pt1 > 20 and ev.pt2 > 20 and ev.inv > mll_lower_Cut and ev.inv < mll_upper_Cut and ev.patPFMet > 150 and abs(ev.eta1) < 2.4 and abs(ev.eta2) < 2.4 and ev.deltaR > 0.3:
							MCEvents +=1
							if ev.nGenSUSYLeptons == 4:
								signalEvents += 9*0.0102 * ev.weight * ev.sbottomWeight * muonScaleFactors.GetBinContent(muonScaleFactors.GetXaxis().FindBin(ev.pt1),muonScaleFactors.GetYaxis().FindBin(abs(ev.eta1))) * muonScaleFactors.GetBinContent(muonScaleFactors.GetXaxis().FindBin(ev.pt2),muonScaleFactors.GetYaxis().FindBin(abs(ev.eta2)))
							elif ev.nGenSUSYLeptons == 2 and ev.nGenSUSYNeutrinos == 0:
								signalEvents += 9./2. * 0.1411 * ev.weight * ev.sbottomWeight * muonScaleFactors.GetBinContent(muonScaleFactors.GetXaxis().FindBin(ev.pt1),muonScaleFactors.GetYaxis().FindBin(abs(ev.eta1))) * muonScaleFactors.GetBinContent(muonScaleFactors.GetXaxis().FindBin(ev.pt2),muonScaleFactors.GetYaxis().FindBin(abs(ev.eta2)))
							elif ev.nGenSUSYLeptons == 2 and ev.nGenSUSYNeutrinos == 2:
								signalEvents += 9./2. * 0.0404 * ev.weight * ev.sbottomWeight * muonScaleFactors.GetBinContent(muonScaleFactors.GetXaxis().FindBin(ev.pt1),muonScaleFactors.GetYaxis().FindBin(abs(ev.eta1))) * muonScaleFactors.GetBinContent(muonScaleFactors.GetXaxis().FindBin(ev.pt2),muonScaleFactors.GetYaxis().FindBin(abs(ev.eta2)))
							elif ev.nGenSUSYLeptons == 0 and ev.nGenSUSYNeutrinos == 4:
								signalEvents += 9 * 0.04 * ev.weight * ev.sbottomWeight * muonScaleFactors.GetBinContent(muonScaleFactors.GetXaxis().FindBin(ev.pt1),muonScaleFactors.GetYaxis().FindBin(abs(ev.eta1))) * muonScaleFactors.GetBinContent(muonScaleFactors.GetXaxis().FindBin(ev.pt2),muonScaleFactors.GetYaxis().FindBin(abs(ev.eta2)))
							elif ev.nGenSUSYLeptons == 0 and ev.nGenSUSYNeutrinos == 2:
								signalEvents +=  9./2. * 0.2796 * ev.weight * ev.sbottomWeight * muonScaleFactors.GetBinContent(muonScaleFactors.GetXaxis().FindBin(ev.pt1),muonScaleFactors.GetYaxis().FindBin(abs(ev.eta1))) * muonScaleFactors.GetBinContent(muonScaleFactors.GetXaxis().FindBin(ev.pt2),muonScaleFactors.GetYaxis().FindBin(abs(ev.eta2)))
							elif ev.nGenSUSYLeptons == 0 and ev.nGenSUSYNeutrinos == 0:
								signalEvents +=  9 * 0.4887 * ev.weight * ev.sbottomWeight * muonScaleFactors.GetBinContent(muonScaleFactors.GetXaxis().FindBin(ev.pt1),muonScaleFactors.GetYaxis().FindBin(abs(ev.eta1))) * muonScaleFactors.GetBinContent(muonScaleFactors.GetXaxis().FindBin(ev.pt2),muonScaleFactors.GetYaxis().FindBin(abs(ev.eta2)))
				elif etaRegion == "Endcap":
					for ev in tree:
						if ev.chargeProduct < 0 and (((abs(ev.eta1) < 1.4 or abs(ev.eta1) > 1.6) and (abs(ev.eta2) < 1.4 or abs(ev.eta2) > 1.6)) and 1.6 <= max(abs(ev.eta1),abs(ev.eta2))) and ev.pt1 > 20 and ev.pt2 > 20 and ev.inv > mll_lower_Cut and ev.inv < mll_upper_Cut and ev.patPFMet > 150 and abs(ev.eta1) < 2.4 and abs(ev.eta2) < 2.4 and ev.deltaR > 0.3:
							MCEvents +=1
							if ev.nGenSUSYLeptons == 4:
								signalEvents += 9*0.0102 * ev.weight * ev.sbottomWeight * muonScaleFactors.GetBinContent(muonScaleFactors.GetXaxis().FindBin(ev.pt1),muonScaleFactors.GetYaxis().FindBin(abs(ev.eta1))) * muonScaleFactors.GetBinContent(muonScaleFactors.GetXaxis().FindBin(ev.pt2),muonScaleFactors.GetYaxis().FindBin(abs(ev.eta2)))
							elif ev.nGenSUSYLeptons == 2 and ev.nGenSUSYNeutrinos == 0:
								signalEvents += 9./2. * 0.1411 * ev.weight * ev.sbottomWeight * muonScaleFactors.GetBinContent(muonScaleFactors.GetXaxis().FindBin(ev.pt1),muonScaleFactors.GetYaxis().FindBin(abs(ev.eta1))) * muonScaleFactors.GetBinContent(muonScaleFactors.GetXaxis().FindBin(ev.pt2),muonScaleFactors.GetYaxis().FindBin(abs(ev.eta2)))
							elif ev.nGenSUSYLeptons == 2 and ev.nGenSUSYNeutrinos == 2:
								signalEvents += 9./2. * 0.0404 * ev.weight * ev.sbottomWeight * muonScaleFactors.GetBinContent(muonScaleFactors.GetXaxis().FindBin(ev.pt1),muonScaleFactors.GetYaxis().FindBin(abs(ev.eta1))) * muonScaleFactors.GetBinContent(muonScaleFactors.GetXaxis().FindBin(ev.pt2),muonScaleFactors.GetYaxis().FindBin(abs(ev.eta2)))
							elif ev.nGenSUSYLeptons == 0 and ev.nGenSUSYNeutrinos == 4:
								signalEvents += 9 * 0.04 * ev.weight * ev.sbottomWeight * muonScaleFactors.GetBinContent(muonScaleFactors.GetXaxis().FindBin(ev.pt1),muonScaleFactors.GetYaxis().FindBin(abs(ev.eta1))) * muonScaleFactors.GetBinContent(muonScaleFactors.GetXaxis().FindBin(ev.pt2),muonScaleFactors.GetYaxis().FindBin(abs(ev.eta2)))
							elif ev.nGenSUSYLeptons == 0 and ev.nGenSUSYNeutrinos == 2:
								signalEvents +=  9./2. * 0.2796 * ev.weight * ev.sbottomWeight * muonScaleFactors.GetBinContent(muonScaleFactors.GetXaxis().FindBin(ev.pt1),muonScaleFactors.GetYaxis().FindBin(abs(ev.eta1))) * muonScaleFactors.GetBinContent(muonScaleFactors.GetXaxis().FindBin(ev.pt2),muonScaleFactors.GetYaxis().FindBin(abs(ev.eta2)))
							elif ev.nGenSUSYLeptons == 0 and ev.nGenSUSYNeutrinos == 0:
								signalEvents +=  9 * 0.4887 * ev.weight * ev.sbottomWeight * muonScaleFactors.GetBinContent(muonScaleFactors.GetXaxis().FindBin(ev.pt1),muonScaleFactors.GetYaxis().FindBin(abs(ev.eta1))) * muonScaleFactors.GetBinContent(muonScaleFactors.GetXaxis().FindBin(ev.pt2),muonScaleFactors.GetYaxis().FindBin(abs(ev.eta2)))
			elif dilepton == "EMu":
				if etaRegion == "Barrel":
					for ev in tree:
						if ev.chargeProduct < 0 and abs(ev.eta1) < 1.4 and abs(ev.eta2) < 1.4 and ev.pt1 > 20 and ev.pt2 > 20 and ev.inv > mll_lower_Cut and ev.inv < mll_upper_Cut and ev.patPFMet > 150 and abs(ev.eta1) < 2.4 and abs(ev.eta2) < 2.4 and ev.deltaR > 0.3:
							MCEvents +=1
							if ev.nGenSUSYLeptons == 4:
								signalEvents += 9*0.0102 * ev.weight * ev.sbottomWeight * electronScaleFactors.GetBinContent(electronScaleFactors.GetXaxis().FindBin(ev.pt1),electronScaleFactors.GetYaxis().FindBin(abs(ev.eta1))) * muonScaleFactors.GetBinContent(muonScaleFactors.GetXaxis().FindBin(ev.pt2),muonScaleFactors.GetYaxis().FindBin(abs(ev.eta2)))
							elif ev.nGenSUSYLeptons == 2 and ev.nGenSUSYNeutrinos == 0:
								signalEvents += 9./2. * 0.1411 * ev.weight * ev.sbottomWeight * electronScaleFactors.GetBinContent(electronScaleFactors.GetXaxis().FindBin(ev.pt1),electronScaleFactors.GetYaxis().FindBin(abs(ev.eta1))) * muonScaleFactors.GetBinContent(muonScaleFactors.GetXaxis().FindBin(ev.pt2),muonScaleFactors.GetYaxis().FindBin(abs(ev.eta2)))
							elif ev.nGenSUSYLeptons == 2 and ev.nGenSUSYNeutrinos == 2:
								signalEvents += 9./2. * 0.0404 * ev.weight * ev.sbottomWeight * electronScaleFactors.GetBinContent(electronScaleFactors.GetXaxis().FindBin(ev.pt1),electronScaleFactors.GetYaxis().FindBin(abs(ev.eta1))) * muonScaleFactors.GetBinContent(muonScaleFactors.GetXaxis().FindBin(ev.pt2),muonScaleFactors.GetYaxis().FindBin(abs(ev.eta2)))
							elif ev.nGenSUSYLeptons == 0 and ev.nGenSUSYNeutrinos == 4:
								signalEvents += 9 * 0.04 * ev.weight * ev.sbottomWeight * electronScaleFactors.GetBinContent(electronScaleFactors.GetXaxis().FindBin(ev.pt1),electronScaleFactors.GetYaxis().FindBin(abs(ev.eta1))) * muonScaleFactors.GetBinContent(muonScaleFactors.GetXaxis().FindBin(ev.pt2),muonScaleFactors.GetYaxis().FindBin(abs(ev.eta2)))
							elif ev.nGenSUSYLeptons == 0 and ev.nGenSUSYNeutrinos == 2:
								signalEvents +=  9./2. * 0.2796 * ev.weight * ev.sbottomWeight * electronScaleFactors.GetBinContent(electronScaleFactors.GetXaxis().FindBin(ev.pt1),electronScaleFactors.GetYaxis().FindBin(abs(ev.eta1))) * muonScaleFactors.GetBinContent(muonScaleFactors.GetXaxis().FindBin(ev.pt2),muonScaleFactors.GetYaxis().FindBin(abs(ev.eta2)))
							elif ev.nGenSUSYLeptons == 0 and ev.nGenSUSYNeutrinos == 0:
								signalEvents +=  9 * 0.4887 * ev.weight * ev.sbottomWeight * electronScaleFactors.GetBinContent(electronScaleFactors.GetXaxis().FindBin(ev.pt1),electronScaleFactors.GetYaxis().FindBin(abs(ev.eta1))) * muonScaleFactors.GetBinContent(muonScaleFactors.GetXaxis().FindBin(ev.pt2),muonScaleFactors.GetYaxis().FindBin(abs(ev.eta2)))
				elif etaRegion == "Endcap":
					for ev in tree:
						if ev.chargeProduct < 0 and (((abs(ev.eta1) < 1.4 or abs(ev.eta1) > 1.6) and (abs(ev.eta2) < 1.4 or abs(ev.eta2) > 1.6)) and 1.6 <= max(abs(ev.eta1),abs(ev.eta2))) and ev.pt1 > 20 and ev.pt2 > 20 and ev.inv > mll_lower_Cut and ev.inv < mll_upper_Cut and ev.patPFMet > 150 and abs(ev.eta1) < 2.4 and abs(ev.eta2) < 2.4 and ev.deltaR > 0.3:
							MCEvents +=1
							if ev.nGenSUSYLeptons == 4:
								signalEvents += 9*0.0102 * ev.weight * ev.sbottomWeight * electronScaleFactors.GetBinContent(electronScaleFactors.GetXaxis().FindBin(ev.pt1),electronScaleFactors.GetYaxis().FindBin(abs(ev.eta1))) * muonScaleFactors.GetBinContent(muonScaleFactors.GetXaxis().FindBin(ev.pt2),muonScaleFactors.GetYaxis().FindBin(abs(ev.eta2)))
							elif ev.nGenSUSYLeptons == 2 and ev.nGenSUSYNeutrinos == 0:
								signalEvents += 9./2. * 0.1411 * ev.weight * ev.sbottomWeight * electronScaleFactors.GetBinContent(electronScaleFactors.GetXaxis().FindBin(ev.pt1),electronScaleFactors.GetYaxis().FindBin(abs(ev.eta1))) * muonScaleFactors.GetBinContent(muonScaleFactors.GetXaxis().FindBin(ev.pt2),muonScaleFactors.GetYaxis().FindBin(abs(ev.eta2)))
							elif ev.nGenSUSYLeptons == 2 and ev.nGenSUSYNeutrinos == 2:
								signalEvents += 9./2. * 0.0404 * ev.weight * ev.sbottomWeight * electronScaleFactors.GetBinContent(electronScaleFactors.GetXaxis().FindBin(ev.pt1),electronScaleFactors.GetYaxis().FindBin(abs(ev.eta1))) * muonScaleFactors.GetBinContent(muonScaleFactors.GetXaxis().FindBin(ev.pt2),muonScaleFactors.GetYaxis().FindBin(abs(ev.eta2)))
							elif ev.nGenSUSYLeptons == 0 and ev.nGenSUSYNeutrinos == 4:
								signalEvents += 9 * 0.04 * ev.weight * ev.sbottomWeight * electronScaleFactors.GetBinContent(electronScaleFactors.GetXaxis().FindBin(ev.pt1),electronScaleFactors.GetYaxis().FindBin(abs(ev.eta1))) * muonScaleFactors.GetBinContent(muonScaleFactors.GetXaxis().FindBin(ev.pt2),muonScaleFactors.GetYaxis().FindBin(abs(ev.eta2)))
							elif ev.nGenSUSYLeptons == 0 and ev.nGenSUSYNeutrinos == 2:
								signalEvents +=  9./2. * 0.2796 * ev.weight * ev.sbottomWeight * electronScaleFactors.GetBinContent(electronScaleFactors.GetXaxis().FindBin(ev.pt1),electronScaleFactors.GetYaxis().FindBin(abs(ev.eta1))) * muonScaleFactors.GetBinContent(muonScaleFactors.GetXaxis().FindBin(ev.pt2),muonScaleFactors.GetYaxis().FindBin(abs(ev.eta2)))
							elif ev.nGenSUSYLeptons == 0 and ev.nGenSUSYNeutrinos == 0:
								signalEvents +=  9 * 0.4887 * ev.weight * ev.sbottomWeight * electronScaleFactors.GetBinContent(electronScaleFactors.GetXaxis().FindBin(ev.pt1),electronScaleFactors.GetYaxis().FindBin(abs(ev.eta1))) * muonScaleFactors.GetBinContent(muonScaleFactors.GetXaxis().FindBin(ev.pt2),muonScaleFactors.GetYaxis().FindBin(abs(ev.eta2)))
						
		else:
			if dilepton == "EE":
				if etaRegion == "Barrel":
					for ev in tree:
						if ev.chargeProduct < 0 and abs(ev.eta1) < 1.4 and abs(ev.eta2) < 1.4 and ev.pt1 > 20 and ev.pt2 > 20 and ev.inv > mll_lower_Cut and ev.inv < mll_upper_Cut and ((ev.patPFMet > 100 and ev.nJetsSmeared >= 3) or  (ev.patPFMet > 150 and ev.nJetsSmeared >=2)) and abs(ev.eta1) < 2.4 and abs(ev.eta2) < 2.4 and ev.deltaR > 0.3:
							MCEvents +=1
							if ev.nGenSUSYLeptons == 4:
								signalEvents += 9*0.0102 * ev.weight * ev.sbottomWeight * electronScaleFactors.GetBinContent(electronScaleFactors.GetXaxis().FindBin(ev.pt1),electronScaleFactors.GetYaxis().FindBin(abs(ev.eta1))) * electronScaleFactors.GetBinContent(electronScaleFactors.GetXaxis().FindBin(ev.pt2),electronScaleFactors.GetYaxis().FindBin(abs(ev.eta2)))
							elif ev.nGenSUSYLeptons == 2 and ev.nGenSUSYNeutrinos == 0:
								signalEvents += 9./2. * 0.1411 * ev.weight * ev.sbottomWeight * electronScaleFactors.GetBinContent(electronScaleFactors.GetXaxis().FindBin(ev.pt1),electronScaleFactors.GetYaxis().FindBin(abs(ev.eta1))) * electronScaleFactors.GetBinContent(electronScaleFactors.GetXaxis().FindBin(ev.pt2),electronScaleFactors.GetYaxis().FindBin(abs(ev.eta2)))
							elif ev.nGenSUSYLeptons == 2 and ev.nGenSUSYNeutrinos == 2:
								signalEvents += 9./2. * 0.0404 * ev.weight * ev.sbottomWeight * electronScaleFactors.GetBinContent(electronScaleFactors.GetXaxis().FindBin(ev.pt1),electronScaleFactors.GetYaxis().FindBin(abs(ev.eta1))) * electronScaleFactors.GetBinContent(electronScaleFactors.GetXaxis().FindBin(ev.pt2),electronScaleFactors.GetYaxis().FindBin(abs(ev.eta2)))
							elif ev.nGenSUSYLeptons == 0 and ev.nGenSUSYNeutrinos == 4:
								signalEvents += 9 * 0.04 * ev.weight * ev.sbottomWeight * electronScaleFactors.GetBinContent(electronScaleFactors.GetXaxis().FindBin(ev.pt1),electronScaleFactors.GetYaxis().FindBin(abs(ev.eta1))) * electronScaleFactors.GetBinContent(electronScaleFactors.GetXaxis().FindBin(ev.pt2),electronScaleFactors.GetYaxis().FindBin(abs(ev.eta2)))
							elif ev.nGenSUSYLeptons == 0 and ev.nGenSUSYNeutrinos == 2:
								signalEvents +=  9./2. * 0.2796 * ev.weight * ev.sbottomWeight * electronScaleFactors.GetBinContent(electronScaleFactors.GetXaxis().FindBin(ev.pt1),electronScaleFactors.GetYaxis().FindBin(abs(ev.eta1))) * electronScaleFactors.GetBinContent(electronScaleFactors.GetXaxis().FindBin(ev.pt2),electronScaleFactors.GetYaxis().FindBin(abs(ev.eta2)))
							elif ev.nGenSUSYLeptons == 0 and ev.nGenSUSYNeutrinos == 0:
								signalEvents +=  9 * 0.4887 * ev.weight * ev.sbottomWeight * electronScaleFactors.GetBinContent(electronScaleFactors.GetXaxis().FindBin(ev.pt1),electronScaleFactors.GetYaxis().FindBin(abs(ev.eta1))) * electronScaleFactors.GetBinContent(electronScaleFactors.GetXaxis().FindBin(ev.pt2),electronScaleFactors.GetYaxis().FindBin(abs(ev.eta2)))
				elif etaRegion == "Endcap":
					for ev in tree:
						if ev.chargeProduct < 0 and (((abs(ev.eta1) < 1.4 or abs(ev.eta1) > 1.6) and (abs(ev.eta2) < 1.4 or abs(ev.eta2) > 1.6)) and 1.6 <= max(abs(ev.eta1),abs(ev.eta2))) and ev.pt1 > 20 and ev.pt2 > 20 and ev.inv > mll_lower_Cut and ev.inv < mll_upper_Cut and ((ev.patPFMet > 100 and ev.nJetsSmeared >= 3) or  (ev.patPFMet > 150 and ev.nJetsSmeared >=2)) and abs(ev.eta1) < 2.4 and abs(ev.eta2) < 2.4 and ev.deltaR > 0.3:
							MCEvents +=1
							if ev.nGenSUSYLeptons == 4:
								signalEvents += 9*0.0102 * ev.weight * ev.sbottomWeight * electronScaleFactors.GetBinContent(electronScaleFactors.GetXaxis().FindBin(ev.pt1),electronScaleFactors.GetYaxis().FindBin(abs(ev.eta1))) * electronScaleFactors.GetBinContent(electronScaleFactors.GetXaxis().FindBin(ev.pt2),electronScaleFactors.GetYaxis().FindBin(abs(ev.eta2)))
							elif ev.nGenSUSYLeptons == 2 and ev.nGenSUSYNeutrinos == 0:
								signalEvents += 9./2. * 0.1411 * ev.weight * ev.sbottomWeight * electronScaleFactors.GetBinContent(electronScaleFactors.GetXaxis().FindBin(ev.pt1),electronScaleFactors.GetYaxis().FindBin(abs(ev.eta1))) * electronScaleFactors.GetBinContent(electronScaleFactors.GetXaxis().FindBin(ev.pt2),electronScaleFactors.GetYaxis().FindBin(abs(ev.eta2)))
							elif ev.nGenSUSYLeptons == 2 and ev.nGenSUSYNeutrinos == 2:
								signalEvents += 9./2. * 0.0404 * ev.weight * ev.sbottomWeight * electronScaleFactors.GetBinContent(electronScaleFactors.GetXaxis().FindBin(ev.pt1),electronScaleFactors.GetYaxis().FindBin(abs(ev.eta1))) * electronScaleFactors.GetBinContent(electronScaleFactors.GetXaxis().FindBin(ev.pt2),electronScaleFactors.GetYaxis().FindBin(abs(ev.eta2)))
							elif ev.nGenSUSYLeptons == 0 and ev.nGenSUSYNeutrinos == 4:
								signalEvents += 9 * 0.04 * ev.weight * ev.sbottomWeight * electronScaleFactors.GetBinContent(electronScaleFactors.GetXaxis().FindBin(ev.pt1),electronScaleFactors.GetYaxis().FindBin(abs(ev.eta1))) * electronScaleFactors.GetBinContent(electronScaleFactors.GetXaxis().FindBin(ev.pt2),electronScaleFactors.GetYaxis().FindBin(abs(ev.eta2)))
							elif ev.nGenSUSYLeptons == 0 and ev.nGenSUSYNeutrinos == 2:
								signalEvents +=  9./2. * 0.2796 * ev.weight * ev.sbottomWeight * electronScaleFactors.GetBinContent(electronScaleFactors.GetXaxis().FindBin(ev.pt1),electronScaleFactors.GetYaxis().FindBin(abs(ev.eta1))) * electronScaleFactors.GetBinContent(electronScaleFactors.GetXaxis().FindBin(ev.pt2),electronScaleFactors.GetYaxis().FindBin(abs(ev.eta2)))
							elif ev.nGenSUSYLeptons == 0 and ev.nGenSUSYNeutrinos == 0:
								signalEvents +=  9 * 0.4887 * ev.weight * ev.sbottomWeight * electronScaleFactors.GetBinContent(electronScaleFactors.GetXaxis().FindBin(ev.pt1),electronScaleFactors.GetYaxis().FindBin(abs(ev.eta1))) * electronScaleFactors.GetBinContent(electronScaleFactors.GetXaxis().FindBin(ev.pt2),electronScaleFactors.GetYaxis().FindBin(abs(ev.eta2)))
			elif dilepton == "MuMu":
				if etaRegion == "Barrel":
					for ev in tree:
						if ev.chargeProduct < 0 and abs(ev.eta1) < 1.4 and abs(ev.eta2) < 1.4 and ev.pt1 > 20 and ev.pt2 > 20 and ev.inv > mll_lower_Cut and ev.inv < mll_upper_Cut and ((ev.patPFMet > 100 and ev.nJetsSmeared >= 3) or  (ev.patPFMet > 150 and ev.nJetsSmeared >=2)) and abs(ev.eta1) < 2.4 and abs(ev.eta2) < 2.4 and ev.deltaR > 0.3:
							MCEvents +=1
							if ev.nGenSUSYLeptons == 4:
								signalEvents += 9*0.0102 * ev.weight * ev.sbottomWeight * muonScaleFactors.GetBinContent(muonScaleFactors.GetXaxis().FindBin(ev.pt1),muonScaleFactors.GetYaxis().FindBin(abs(ev.eta1))) * muonScaleFactors.GetBinContent(muonScaleFactors.GetXaxis().FindBin(ev.pt2),muonScaleFactors.GetYaxis().FindBin(abs(ev.eta2)))
							elif ev.nGenSUSYLeptons == 2 and ev.nGenSUSYNeutrinos == 0:
								signalEvents += 9./2. * 0.1411 * ev.weight * ev.sbottomWeight * muonScaleFactors.GetBinContent(muonScaleFactors.GetXaxis().FindBin(ev.pt1),muonScaleFactors.GetYaxis().FindBin(abs(ev.eta1))) * muonScaleFactors.GetBinContent(muonScaleFactors.GetXaxis().FindBin(ev.pt2),muonScaleFactors.GetYaxis().FindBin(abs(ev.eta2)))
							elif ev.nGenSUSYLeptons == 2 and ev.nGenSUSYNeutrinos == 2:
								signalEvents += 9./2. * 0.0404 * ev.weight * ev.sbottomWeight * muonScaleFactors.GetBinContent(muonScaleFactors.GetXaxis().FindBin(ev.pt1),muonScaleFactors.GetYaxis().FindBin(abs(ev.eta1))) * muonScaleFactors.GetBinContent(muonScaleFactors.GetXaxis().FindBin(ev.pt2),muonScaleFactors.GetYaxis().FindBin(abs(ev.eta2)))
							elif ev.nGenSUSYLeptons == 0 and ev.nGenSUSYNeutrinos == 4:
								signalEvents += 9 * 0.04 * ev.weight * ev.sbottomWeight * muonScaleFactors.GetBinContent(muonScaleFactors.GetXaxis().FindBin(ev.pt1),muonScaleFactors.GetYaxis().FindBin(abs(ev.eta1))) * muonScaleFactors.GetBinContent(muonScaleFactors.GetXaxis().FindBin(ev.pt2),muonScaleFactors.GetYaxis().FindBin(abs(ev.eta2)))
							elif ev.nGenSUSYLeptons == 0 and ev.nGenSUSYNeutrinos == 2:
								signalEvents +=  9./2. * 0.2796 * ev.weight * ev.sbottomWeight * muonScaleFactors.GetBinContent(muonScaleFactors.GetXaxis().FindBin(ev.pt1),muonScaleFactors.GetYaxis().FindBin(abs(ev.eta1))) * muonScaleFactors.GetBinContent(muonScaleFactors.GetXaxis().FindBin(ev.pt2),muonScaleFactors.GetYaxis().FindBin(abs(ev.eta2)))
							elif ev.nGenSUSYLeptons == 0 and ev.nGenSUSYNeutrinos == 0:
								signalEvents +=  9 * 0.4887 * ev.weight * ev.sbottomWeight * muonScaleFactors.GetBinContent(muonScaleFactors.GetXaxis().FindBin(ev.pt1),muonScaleFactors.GetYaxis().FindBin(abs(ev.eta1))) * muonScaleFactors.GetBinContent(muonScaleFactors.GetXaxis().FindBin(ev.pt2),muonScaleFactors.GetYaxis().FindBin(abs(ev.eta2)))
				elif etaRegion == "Endcap":
					for ev in tree:
						if ev.chargeProduct < 0 and (((abs(ev.eta1) < 1.4 or abs(ev.eta1) > 1.6) and (abs(ev.eta2) < 1.4 or abs(ev.eta2) > 1.6)) and 1.6 <= max(abs(ev.eta1),abs(ev.eta2))) and ev.pt1 > 20 and ev.pt2 > 20 and ev.inv > mll_lower_Cut and ev.inv < mll_upper_Cut and ((ev.patPFMet > 100 and ev.nJetsSmeared >= 3) or  (ev.patPFMet > 150 and ev.nJetsSmeared >=2)) and abs(ev.eta1) < 2.4 and abs(ev.eta2) < 2.4 and ev.deltaR > 0.3:
							MCEvents +=1
							if ev.nGenSUSYLeptons == 4:
								signalEvents += 9*0.0102 * ev.weight * ev.sbottomWeight * muonScaleFactors.GetBinContent(muonScaleFactors.GetXaxis().FindBin(ev.pt1),muonScaleFactors.GetYaxis().FindBin(abs(ev.eta1))) * muonScaleFactors.GetBinContent(muonScaleFactors.GetXaxis().FindBin(ev.pt2),muonScaleFactors.GetYaxis().FindBin(abs(ev.eta2)))
							elif ev.nGenSUSYLeptons == 2 and ev.nGenSUSYNeutrinos == 0:
								signalEvents += 9./2. * 0.1411 * ev.weight * ev.sbottomWeight * muonScaleFactors.GetBinContent(muonScaleFactors.GetXaxis().FindBin(ev.pt1),muonScaleFactors.GetYaxis().FindBin(abs(ev.eta1))) * muonScaleFactors.GetBinContent(muonScaleFactors.GetXaxis().FindBin(ev.pt2),muonScaleFactors.GetYaxis().FindBin(abs(ev.eta2)))
							elif ev.nGenSUSYLeptons == 2 and ev.nGenSUSYNeutrinos == 2:
								signalEvents += 9./2. * 0.0404 * ev.weight * ev.sbottomWeight * muonScaleFactors.GetBinContent(muonScaleFactors.GetXaxis().FindBin(ev.pt1),muonScaleFactors.GetYaxis().FindBin(abs(ev.eta1))) * muonScaleFactors.GetBinContent(muonScaleFactors.GetXaxis().FindBin(ev.pt2),muonScaleFactors.GetYaxis().FindBin(abs(ev.eta2)))
							elif ev.nGenSUSYLeptons == 0 and ev.nGenSUSYNeutrinos == 4:
								signalEvents += 9 * 0.04 * ev.weight * ev.sbottomWeight * muonScaleFactors.GetBinContent(muonScaleFactors.GetXaxis().FindBin(ev.pt1),muonScaleFactors.GetYaxis().FindBin(abs(ev.eta1))) * muonScaleFactors.GetBinContent(muonScaleFactors.GetXaxis().FindBin(ev.pt2),muonScaleFactors.GetYaxis().FindBin(abs(ev.eta2)))
							elif ev.nGenSUSYLeptons == 0 and ev.nGenSUSYNeutrinos == 2:
								signalEvents +=  9./2. * 0.2796 * ev.weight * ev.sbottomWeight * muonScaleFactors.GetBinContent(muonScaleFactors.GetXaxis().FindBin(ev.pt1),muonScaleFactors.GetYaxis().FindBin(abs(ev.eta1))) * muonScaleFactors.GetBinContent(muonScaleFactors.GetXaxis().FindBin(ev.pt2),muonScaleFactors.GetYaxis().FindBin(abs(ev.eta2)))
							elif ev.nGenSUSYLeptons == 0 and ev.nGenSUSYNeutrinos == 0:
								signalEvents +=  9 * 0.4887 * ev.weight * ev.sbottomWeight * muonScaleFactors.GetBinContent(muonScaleFactors.GetXaxis().FindBin(ev.pt1),muonScaleFactors.GetYaxis().FindBin(abs(ev.eta1))) * muonScaleFactors.GetBinContent(muonScaleFactors.GetXaxis().FindBin(ev.pt2),muonScaleFactors.GetYaxis().FindBin(abs(ev.eta2)))
			elif dilepton == "EMu":
				if etaRegion == "Barrel":
					for ev in tree:
						if ev.chargeProduct < 0 and abs(ev.eta1) < 1.4 and abs(ev.eta2) < 1.4 and ev.pt1 > 20 and ev.pt2 > 20 and ev.inv > mll_lower_Cut and ev.inv < mll_upper_Cut and ((ev.patPFMet > 100 and ev.nJetsSmeared >= 3) or  (ev.patPFMet > 150 and ev.nJetsSmeared >=2)) and abs(ev.eta1) < 2.4 and abs(ev.eta2) < 2.4 and ev.deltaR > 0.3:
							MCEvents +=1
							if ev.nGenSUSYLeptons == 4:
								signalEvents += 9*0.0102 * ev.weight * ev.sbottomWeight * electronScaleFactors.GetBinContent(electronScaleFactors.GetXaxis().FindBin(ev.pt1),electronScaleFactors.GetYaxis().FindBin(abs(ev.eta1))) * muonScaleFactors.GetBinContent(muonScaleFactors.GetXaxis().FindBin(ev.pt2),muonScaleFactors.GetYaxis().FindBin(abs(ev.eta2)))
							elif ev.nGenSUSYLeptons == 2 and ev.nGenSUSYNeutrinos == 0:
								signalEvents += 9./2. * 0.1411 * ev.weight * ev.sbottomWeight * electronScaleFactors.GetBinContent(electronScaleFactors.GetXaxis().FindBin(ev.pt1),electronScaleFactors.GetYaxis().FindBin(abs(ev.eta1))) * muonScaleFactors.GetBinContent(muonScaleFactors.GetXaxis().FindBin(ev.pt2),muonScaleFactors.GetYaxis().FindBin(abs(ev.eta2)))
							elif ev.nGenSUSYLeptons == 2 and ev.nGenSUSYNeutrinos == 2:
								signalEvents += 9./2. * 0.0404 * ev.weight * ev.sbottomWeight * electronScaleFactors.GetBinContent(electronScaleFactors.GetXaxis().FindBin(ev.pt1),electronScaleFactors.GetYaxis().FindBin(abs(ev.eta1))) * muonScaleFactors.GetBinContent(muonScaleFactors.GetXaxis().FindBin(ev.pt2),muonScaleFactors.GetYaxis().FindBin(abs(ev.eta2)))
							elif ev.nGenSUSYLeptons == 0 and ev.nGenSUSYNeutrinos == 4:
								signalEvents += 9 * 0.04 * ev.weight * ev.sbottomWeight * electronScaleFactors.GetBinContent(electronScaleFactors.GetXaxis().FindBin(ev.pt1),electronScaleFactors.GetYaxis().FindBin(abs(ev.eta1))) * muonScaleFactors.GetBinContent(muonScaleFactors.GetXaxis().FindBin(ev.pt2),muonScaleFactors.GetYaxis().FindBin(abs(ev.eta2)))
							elif ev.nGenSUSYLeptons == 0 and ev.nGenSUSYNeutrinos == 2:
								signalEvents +=  9./2. * 0.2796 * ev.weight * ev.sbottomWeight * electronScaleFactors.GetBinContent(electronScaleFactors.GetXaxis().FindBin(ev.pt1),electronScaleFactors.GetYaxis().FindBin(abs(ev.eta1))) * muonScaleFactors.GetBinContent(muonScaleFactors.GetXaxis().FindBin(ev.pt2),muonScaleFactors.GetYaxis().FindBin(abs(ev.eta2)))
							elif ev.nGenSUSYLeptons == 0 and ev.nGenSUSYNeutrinos == 0:
								signalEvents +=  9 * 0.4887 * ev.weight * ev.sbottomWeight * electronScaleFactors.GetBinContent(electronScaleFactors.GetXaxis().FindBin(ev.pt1),electronScaleFactors.GetYaxis().FindBin(abs(ev.eta1))) * muonScaleFactors.GetBinContent(muonScaleFactors.GetXaxis().FindBin(ev.pt2),muonScaleFactors.GetYaxis().FindBin(abs(ev.eta2)))
				elif etaRegion == "Endcap":
					for ev in tree:
						if ev.chargeProduct < 0 and (((abs(ev.eta1) < 1.4 or abs(ev.eta1) > 1.6) and (abs(ev.eta2) < 1.4 or abs(ev.eta2) > 1.6)) and 1.6 <= max(abs(ev.eta1),abs(ev.eta2))) and ev.pt1 > 20 and ev.pt2 > 20 and ev.inv > mll_lower_Cut and ev.inv < mll_upper_Cut and ((ev.patPFMet > 100 and ev.nJetsSmeared >= 3) or  (ev.patPFMet > 150 and ev.nJetsSmeared >=2)) and abs(ev.eta1) < 2.4 and abs(ev.eta2) < 2.4 and ev.deltaR > 0.3:
							MCEvents +=1
							if ev.nGenSUSYLeptons == 4:
								signalEvents += 9*0.0102 * ev.weight * ev.sbottomWeight * electronScaleFactors.GetBinContent(electronScaleFactors.GetXaxis().FindBin(ev.pt1),electronScaleFactors.GetYaxis().FindBin(abs(ev.eta1))) * muonScaleFactors.GetBinContent(muonScaleFactors.GetXaxis().FindBin(ev.pt2),muonScaleFactors.GetYaxis().FindBin(abs(ev.eta2)))
							elif ev.nGenSUSYLeptons == 2 and ev.nGenSUSYNeutrinos == 0:
								signalEvents += 9./2. * 0.1411 * ev.weight * ev.sbottomWeight * electronScaleFactors.GetBinContent(electronScaleFactors.GetXaxis().FindBin(ev.pt1),electronScaleFactors.GetYaxis().FindBin(abs(ev.eta1))) * muonScaleFactors.GetBinContent(muonScaleFactors.GetXaxis().FindBin(ev.pt2),muonScaleFactors.GetYaxis().FindBin(abs(ev.eta2)))
							elif ev.nGenSUSYLeptons == 2 and ev.nGenSUSYNeutrinos == 2:
								signalEvents += 9./2. * 0.0404 * ev.weight * ev.sbottomWeight * electronScaleFactors.GetBinContent(electronScaleFactors.GetXaxis().FindBin(ev.pt1),electronScaleFactors.GetYaxis().FindBin(abs(ev.eta1))) * muonScaleFactors.GetBinContent(muonScaleFactors.GetXaxis().FindBin(ev.pt2),muonScaleFactors.GetYaxis().FindBin(abs(ev.eta2)))
							elif ev.nGenSUSYLeptons == 0 and ev.nGenSUSYNeutrinos == 4:
								signalEvents += 9 * 0.04 * ev.weight * ev.sbottomWeight * electronScaleFactors.GetBinContent(electronScaleFactors.GetXaxis().FindBin(ev.pt1),electronScaleFactors.GetYaxis().FindBin(abs(ev.eta1))) * muonScaleFactors.GetBinContent(muonScaleFactors.GetXaxis().FindBin(ev.pt2),muonScaleFactors.GetYaxis().FindBin(abs(ev.eta2)))
							elif ev.nGenSUSYLeptons == 0 and ev.nGenSUSYNeutrinos == 2:
								signalEvents +=  9./2. * 0.2796 * ev.weight * ev.sbottomWeight * electronScaleFactors.GetBinContent(electronScaleFactors.GetXaxis().FindBin(ev.pt1),electronScaleFactors.GetYaxis().FindBin(abs(ev.eta1))) * muonScaleFactors.GetBinContent(muonScaleFactors.GetXaxis().FindBin(ev.pt2),muonScaleFactors.GetYaxis().FindBin(abs(ev.eta2)))
							elif ev.nGenSUSYLeptons == 0 and ev.nGenSUSYNeutrinos == 0:
								signalEvents +=  9 * 0.4887 * ev.weight * ev.sbottomWeight * electronScaleFactors.GetBinContent(electronScaleFactors.GetXaxis().FindBin(ev.pt1),electronScaleFactors.GetYaxis().FindBin(abs(ev.eta1))) * muonScaleFactors.GetBinContent(muonScaleFactors.GetXaxis().FindBin(ev.pt2),muonScaleFactors.GetYaxis().FindBin(abs(ev.eta2)))
	else:
		if additionalCut == "NJets3Cut":
			if dilepton == "EE":
				if etaRegion == "Barrel":
					for ev in tree:
						if ev.chargeProduct < 0 and abs(ev.eta1) < 1.4 and abs(ev.eta2) < 1.4 and ev.pt1 > 20 and ev.pt2 > 20 and ev.inv > mll_lower_Cut and ev.inv < mll_upper_Cut and ev.nJetsSmeared >= 3 and abs(ev.eta1) < 2.4 and abs(ev.eta2) < 2.4 and ev.deltaR > 0.3:
							MCEvents +=1
							if ev.nGenSUSYLeptons == 4:
								signalEvents += 9*0.0102 * ev.weight * ev.sbottomWeight * electronScaleFactors.GetBinContent(electronScaleFactors.GetXaxis().FindBin(ev.pt1),electronScaleFactors.GetYaxis().FindBin(abs(ev.eta1))) * electronScaleFactors.GetBinContent(electronScaleFactors.GetXaxis().FindBin(ev.pt2),electronScaleFactors.GetYaxis().FindBin(abs(ev.eta2)))
							elif ev.nGenSUSYLeptons == 3:
								signalEvents += 3. * 0.101 * ev.weight * ev.sbottomWeight * electronScaleFactors.GetBinContent(electronScaleFactors.GetXaxis().FindBin(ev.pt1),electronScaleFactors.GetYaxis().FindBin(abs(ev.eta1))) * electronScaleFactors.GetBinContent(electronScaleFactors.GetXaxis().FindBin(ev.pt2),electronScaleFactors.GetYaxis().FindBin(abs(ev.eta2)))
							elif ev.nGenSUSYLeptons == 1 and ev.nGenSUSYNeutrinos == 2:
								signalEvents +=  3. * 0.2 * ev.weight * ev.sbottomWeight * electronScaleFactors.GetBinContent(electronScaleFactors.GetXaxis().FindBin(ev.pt1),electronScaleFactors.GetYaxis().FindBin(abs(ev.eta1))) * electronScaleFactors.GetBinContent(electronScaleFactors.GetXaxis().FindBin(ev.pt2),electronScaleFactors.GetYaxis().FindBin(abs(ev.eta2)))
							elif ev.nGenSUSYLeptons == 1 and ev.nGenSUSYNeutrinos == 0:
								signalEvents +=  3. * 0.6991 * ev.weight * ev.sbottomWeight * electronScaleFactors.GetBinContent(electronScaleFactors.GetXaxis().FindBin(ev.pt1),electronScaleFactors.GetYaxis().FindBin(abs(ev.eta1))) * electronScaleFactors.GetBinContent(electronScaleFactors.GetXaxis().FindBin(ev.pt2),electronScaleFactors.GetYaxis().FindBin(abs(ev.eta2)))
							elif ev.nGenSUSYLeptons == 2 and ev.nGenSUSYNeutrinos == 0 and ev.nGenSUSYSleptons == 0 and ev.motherPdgId1 != 1000011 and ev.motherPdgId1 != 2000011 and ev.motherPdgId1 != 1000013 and ev.motherPdgId1 != 2000013 and ev.motherPdgId2 != 1000011 and ev.motherPdgId2 != 2000011 and ev.motherPdgId2 != 1000013 and ev.motherPdgId2 != 2000013: 
								signalEvents +=  9./2. * 0.1411 * ev.weight * ev.sbottomWeight * electronScaleFactors.GetBinContent(electronScaleFactors.GetXaxis().FindBin(ev.pt1),electronScaleFactors.GetYaxis().FindBin(abs(ev.eta1))) * electronScaleFactors.GetBinContent(electronScaleFactors.GetXaxis().FindBin(ev.pt2),electronScaleFactors.GetYaxis().FindBin(abs(ev.eta2)))
							elif ev.nGenSUSYLeptons == 2 and ev.nGenSUSYNeutrinos == 2 and ev.nGenSUSYSleptons == 0 and ev.motherPdgId1 != 1000011 and ev.motherPdgId1 != 2000011 and ev.motherPdgId1 != 1000013 and ev.motherPdgId1 != 2000013 and ev.motherPdgId2 != 1000011 and ev.motherPdgId2 != 2000011 and ev.motherPdgId2 != 1000013 and ev.motherPdgId2 != 2000013: 
								signalEvents +=  9./2. * 0.0404 * ev.weight * ev.sbottomWeight * electronScaleFactors.GetBinContent(electronScaleFactors.GetXaxis().FindBin(ev.pt1),electronScaleFactors.GetYaxis().FindBin(abs(ev.eta1))) * electronScaleFactors.GetBinContent(electronScaleFactors.GetXaxis().FindBin(ev.pt2),electronScaleFactors.GetYaxis().FindBin(abs(ev.eta2)))
							elif ev.nGenSUSYLeptons == 2 and ev.nGenSUSYNeutrinos == 0 and (ev.motherPdgId1 == 1000011 or ev.motherPdgId1 == 2000011 or ev.motherPdgId1 == 1000013 or ev.motherPdgId1 == 2000013 or ev.motherPdgId2 == 1000011 or ev.motherPdgId2 == 2000011 or ev.motherPdgId2 == 1000013 or ev.motherPdgId2 == 2000013): 
								signalEvents +=  ev.weight * ev.sbottomWeight * electronScaleFactors.GetBinContent(electronScaleFactors.GetXaxis().FindBin(ev.pt1),electronScaleFactors.GetYaxis().FindBin(abs(ev.eta1))) * electronScaleFactors.GetBinContent(electronScaleFactors.GetXaxis().FindBin(ev.pt2),electronScaleFactors.GetYaxis().FindBin(abs(ev.eta2)))
							else:
								print "Right selection not found"
								print "nGenLeptons: "+str(ev.nGenSUSYLeptons)
				elif etaRegion == "Endcap":
						for ev in tree:
							if ev.chargeProduct < 0 and (((abs(ev.eta1) < 1.4 or abs(ev.eta1) > 1.6) and (abs(ev.eta2) < 1.4 or abs(ev.eta2) > 1.6)) and 1.6 <= max(abs(ev.eta1),abs(ev.eta2))) and ev.pt1 > 20 and ev.pt2 > 20 and ev.inv > mll_lower_Cut and ev.inv < mll_upper_Cut and ev.nJetsSmeared >= 3 and abs(ev.eta1) < 2.4 and abs(ev.eta2) < 2.4 and ev.deltaR > 0.3:
								MCEvents +=1
								if ev.nGenSUSYLeptons == 4:
									signalEvents += 9*0.0102 * ev.weight * ev.sbottomWeight * electronScaleFactors.GetBinContent(electronScaleFactors.GetXaxis().FindBin(ev.pt1),electronScaleFactors.GetYaxis().FindBin(abs(ev.eta1))) * electronScaleFactors.GetBinContent(electronScaleFactors.GetXaxis().FindBin(ev.pt2),electronScaleFactors.GetYaxis().FindBin(abs(ev.eta2)))
								elif ev.nGenSUSYLeptons == 3:
									signalEvents += 3. * 0.101 * ev.weight * ev.sbottomWeight * electronScaleFactors.GetBinContent(electronScaleFactors.GetXaxis().FindBin(ev.pt1),electronScaleFactors.GetYaxis().FindBin(abs(ev.eta1))) * electronScaleFactors.GetBinContent(electronScaleFactors.GetXaxis().FindBin(ev.pt2),electronScaleFactors.GetYaxis().FindBin(abs(ev.eta2)))
								elif ev.nGenSUSYLeptons == 1 and ev.nGenSUSYNeutrinos == 2:
									signalEvents +=  3. * 0.2 * ev.weight * ev.sbottomWeight * electronScaleFactors.GetBinContent(electronScaleFactors.GetXaxis().FindBin(ev.pt1),electronScaleFactors.GetYaxis().FindBin(abs(ev.eta1))) * electronScaleFactors.GetBinContent(electronScaleFactors.GetXaxis().FindBin(ev.pt2),electronScaleFactors.GetYaxis().FindBin(abs(ev.eta2)))
								elif ev.nGenSUSYLeptons == 1 and ev.nGenSUSYNeutrinos == 0:
									signalEvents +=  3. * 0.6991 * ev.weight * ev.sbottomWeight * electronScaleFactors.GetBinContent(electronScaleFactors.GetXaxis().FindBin(ev.pt1),electronScaleFactors.GetYaxis().FindBin(abs(ev.eta1))) * electronScaleFactors.GetBinContent(electronScaleFactors.GetXaxis().FindBin(ev.pt2),electronScaleFactors.GetYaxis().FindBin(abs(ev.eta2)))
								elif ev.nGenSUSYLeptons == 2 and ev.nGenSUSYNeutrinos == 0 and ev.nGenSUSYSleptons == 0 and ev.motherPdgId1 != 1000011 and ev.motherPdgId1 != 2000011 and ev.motherPdgId1 != 1000013 and ev.motherPdgId1 != 2000013 and ev.motherPdgId2 != 1000011 and ev.motherPdgId2 != 2000011 and ev.motherPdgId2 != 1000013 and ev.motherPdgId2 != 2000013: 
									signalEvents +=  9./2. * 0.1411 * ev.weight * ev.sbottomWeight * electronScaleFactors.GetBinContent(electronScaleFactors.GetXaxis().FindBin(ev.pt1),electronScaleFactors.GetYaxis().FindBin(abs(ev.eta1))) * electronScaleFactors.GetBinContent(electronScaleFactors.GetXaxis().FindBin(ev.pt2),electronScaleFactors.GetYaxis().FindBin(abs(ev.eta2)))
								elif ev.nGenSUSYLeptons == 2 and ev.nGenSUSYNeutrinos == 2 and ev.nGenSUSYSleptons == 0 and ev.motherPdgId1 != 1000011 and ev.motherPdgId1 != 2000011 and ev.motherPdgId1 != 1000013 and ev.motherPdgId1 != 2000013 and ev.motherPdgId2 != 1000011 and ev.motherPdgId2 != 2000011 and ev.motherPdgId2 != 1000013 and ev.motherPdgId2 != 2000013: 
									signalEvents +=  9./2. * 0.0404 * ev.weight * ev.sbottomWeight * electronScaleFactors.GetBinContent(electronScaleFactors.GetXaxis().FindBin(ev.pt1),electronScaleFactors.GetYaxis().FindBin(abs(ev.eta1))) * electronScaleFactors.GetBinContent(electronScaleFactors.GetXaxis().FindBin(ev.pt2),electronScaleFactors.GetYaxis().FindBin(abs(ev.eta2)))
								elif ev.nGenSUSYLeptons == 2 and ev.nGenSUSYNeutrinos == 0 and (ev.motherPdgId1 == 1000011 or ev.motherPdgId1 == 2000011 or ev.motherPdgId1 == 1000013 or ev.motherPdgId1 == 2000013 or ev.motherPdgId2 == 1000011 or ev.motherPdgId2 == 2000011 or ev.motherPdgId2 == 1000013 or ev.motherPdgId2 == 2000013): 
									signalEvents +=  ev.weight * ev.sbottomWeight * electronScaleFactors.GetBinContent(electronScaleFactors.GetXaxis().FindBin(ev.pt1),electronScaleFactors.GetYaxis().FindBin(abs(ev.eta1))) * electronScaleFactors.GetBinContent(electronScaleFactors.GetXaxis().FindBin(ev.pt2),electronScaleFactors.GetYaxis().FindBin(abs(ev.eta2)))
								else:
									print "Right selection not found"
									print "nGenLeptons: "+str(ev.nGenSUSYLeptons)
			elif dilepton == "MuMu":
				if etaRegion == "Barrel":
					for ev in tree:
						if ev.chargeProduct < 0 and abs(ev.eta1) < 1.4 and abs(ev.eta2) < 1.4 and ev.pt1 > 20 and ev.pt2 > 20 and ev.inv > mll_lower_Cut and ev.inv < mll_upper_Cut and ev.nJetsSmeared >= 3 and abs(ev.eta1) < 2.4 and abs(ev.eta2) < 2.4 and ev.deltaR > 0.3:
							MCEvents +=1
							if ev.nGenSUSYLeptons == 4:
								signalEvents += 9*0.0102 * ev.weight * ev.sbottomWeight * electronScaleFactors.GetBinContent(electronScaleFactors.GetXaxis().FindBin(ev.pt1),electronScaleFactors.GetYaxis().FindBin(abs(ev.eta1))) * electronScaleFactors.GetBinContent(electronScaleFactors.GetXaxis().FindBin(ev.pt2),electronScaleFactors.GetYaxis().FindBin(abs(ev.eta2)))
							elif ev.nGenSUSYLeptons == 3:
								signalEvents += 3. * 0.101 * ev.weight * ev.sbottomWeight * electronScaleFactors.GetBinContent(electronScaleFactors.GetXaxis().FindBin(ev.pt1),electronScaleFactors.GetYaxis().FindBin(abs(ev.eta1))) * electronScaleFactors.GetBinContent(electronScaleFactors.GetXaxis().FindBin(ev.pt2),electronScaleFactors.GetYaxis().FindBin(abs(ev.eta2)))
							elif ev.nGenSUSYLeptons == 1 and ev.nGenSUSYNeutrinos == 2:
								signalEvents +=  3. * 0.2 * ev.weight * ev.sbottomWeight * electronScaleFactors.GetBinContent(electronScaleFactors.GetXaxis().FindBin(ev.pt1),electronScaleFactors.GetYaxis().FindBin(abs(ev.eta1))) * electronScaleFactors.GetBinContent(electronScaleFactors.GetXaxis().FindBin(ev.pt2),electronScaleFactors.GetYaxis().FindBin(abs(ev.eta2)))
							elif ev.nGenSUSYLeptons == 1 and ev.nGenSUSYNeutrinos == 0:
								signalEvents +=  3. * 0.6991 * ev.weight * ev.sbottomWeight * electronScaleFactors.GetBinContent(electronScaleFactors.GetXaxis().FindBin(ev.pt1),electronScaleFactors.GetYaxis().FindBin(abs(ev.eta1))) * electronScaleFactors.GetBinContent(electronScaleFactors.GetXaxis().FindBin(ev.pt2),electronScaleFactors.GetYaxis().FindBin(abs(ev.eta2)))
							elif ev.nGenSUSYLeptons == 2 and ev.nGenSUSYNeutrinos == 0 and ev.nGenSUSYSleptons == 0 and  ev.motherPdgId1 != 1000011 and ev.motherPdgId1 != 2000011 and ev.motherPdgId1 != 1000013 and ev.motherPdgId1 != 2000013 and ev.motherPdgId2 != 1000011 and ev.motherPdgId2 != 2000011 and ev.motherPdgId2 != 1000013 and ev.motherPdgId2 != 2000013: 
								signalEvents +=  9./2. * 0.1411 * ev.weight * ev.sbottomWeight * electronScaleFactors.GetBinContent(electronScaleFactors.GetXaxis().FindBin(ev.pt1),electronScaleFactors.GetYaxis().FindBin(abs(ev.eta1))) * electronScaleFactors.GetBinContent(electronScaleFactors.GetXaxis().FindBin(ev.pt2),electronScaleFactors.GetYaxis().FindBin(abs(ev.eta2)))
							elif ev.nGenSUSYLeptons == 2 and ev.nGenSUSYNeutrinos == 2 and ev.nGenSUSYSleptons == 0 and ev.motherPdgId1 != 1000011 and ev.motherPdgId1 != 2000011 and ev.motherPdgId1 != 1000013 and ev.motherPdgId1 != 2000013 and ev.motherPdgId2 != 1000011 and ev.motherPdgId2 != 2000011 and ev.motherPdgId2 != 1000013 and ev.motherPdgId2 != 2000013: 
								signalEvents +=  9./2. * 0.0404 * ev.weight * ev.sbottomWeight * electronScaleFactors.GetBinContent(electronScaleFactors.GetXaxis().FindBin(ev.pt1),electronScaleFactors.GetYaxis().FindBin(abs(ev.eta1))) * electronScaleFactors.GetBinContent(electronScaleFactors.GetXaxis().FindBin(ev.pt2),electronScaleFactors.GetYaxis().FindBin(abs(ev.eta2)))
							elif ev.nGenSUSYLeptons == 2 and ev.nGenSUSYNeutrinos == 0 and (ev.motherPdgId1 == 1000011 or ev.motherPdgId1 == 2000011 or ev.motherPdgId1 == 1000013 or ev.motherPdgId1 == 2000013 or ev.motherPdgId2 == 1000011 or ev.motherPdgId2 == 2000011 or ev.motherPdgId2 == 1000013 or ev.motherPdgId2 == 2000013): 
								signalEvents +=  ev.weight * ev.sbottomWeight * electronScaleFactors.GetBinContent(electronScaleFactors.GetXaxis().FindBin(ev.pt1),electronScaleFactors.GetYaxis().FindBin(abs(ev.eta1))) * electronScaleFactors.GetBinContent(electronScaleFactors.GetXaxis().FindBin(ev.pt2),electronScaleFactors.GetYaxis().FindBin(abs(ev.eta2)))
							else:
								print "Right selection not found"
								print "nGenLeptons: "+str(ev.nGenSUSYLeptons)
				elif etaRegion == "Endcap":
						for ev in tree:
							if ev.chargeProduct < 0 and (((abs(ev.eta1) < 1.4 or abs(ev.eta1) > 1.6) and (abs(ev.eta2) < 1.4 or abs(ev.eta2) > 1.6)) and 1.6 <= max(abs(ev.eta1),abs(ev.eta2))) and ev.pt1 > 20 and ev.pt2 > 20 and ev.inv > mll_lower_Cut and ev.inv < mll_upper_Cut and ev.nJetsSmeared >= 3 and abs(ev.eta1) < 2.4 and abs(ev.eta2) < 2.4 and ev.deltaR > 0.3:
								MCEvents +=1
								if ev.nGenSUSYLeptons == 4:
									signalEvents += 9*0.0102 * ev.weight * ev.sbottomWeight * electronScaleFactors.GetBinContent(electronScaleFactors.GetXaxis().FindBin(ev.pt1),electronScaleFactors.GetYaxis().FindBin(abs(ev.eta1))) * electronScaleFactors.GetBinContent(electronScaleFactors.GetXaxis().FindBin(ev.pt2),electronScaleFactors.GetYaxis().FindBin(abs(ev.eta2)))
								elif ev.nGenSUSYLeptons == 3:
									signalEvents += 3. * 0.101 * ev.weight * ev.sbottomWeight * electronScaleFactors.GetBinContent(electronScaleFactors.GetXaxis().FindBin(ev.pt1),electronScaleFactors.GetYaxis().FindBin(abs(ev.eta1))) * electronScaleFactors.GetBinContent(electronScaleFactors.GetXaxis().FindBin(ev.pt2),electronScaleFactors.GetYaxis().FindBin(abs(ev.eta2)))
								elif ev.nGenSUSYLeptons == 1 and ev.nGenSUSYNeutrinos == 2:
									signalEvents +=  3. * 0.2 * ev.weight * ev.sbottomWeight * electronScaleFactors.GetBinContent(electronScaleFactors.GetXaxis().FindBin(ev.pt1),electronScaleFactors.GetYaxis().FindBin(abs(ev.eta1))) * electronScaleFactors.GetBinContent(electronScaleFactors.GetXaxis().FindBin(ev.pt2),electronScaleFactors.GetYaxis().FindBin(abs(ev.eta2)))
								elif ev.nGenSUSYLeptons == 1 and ev.nGenSUSYNeutrinos == 0:
									signalEvents +=  3. * 0.6991 * ev.weight * ev.sbottomWeight * electronScaleFactors.GetBinContent(electronScaleFactors.GetXaxis().FindBin(ev.pt1),electronScaleFactors.GetYaxis().FindBin(abs(ev.eta1))) * electronScaleFactors.GetBinContent(electronScaleFactors.GetXaxis().FindBin(ev.pt2),electronScaleFactors.GetYaxis().FindBin(abs(ev.eta2)))
								elif ev.nGenSUSYLeptons == 2 and ev.nGenSUSYNeutrinos == 0 and ev.nGenSUSYSleptons == 0 and ev.motherPdgId1 != 1000011 and ev.motherPdgId1 != 2000011 and ev.motherPdgId1 != 1000013 and ev.motherPdgId1 != 2000013 and ev.motherPdgId2 != 1000011 and ev.motherPdgId2 != 2000011 and ev.motherPdgId2 != 1000013 and ev.motherPdgId2 != 2000013: 
									signalEvents +=  9./2. * 0.1411 * ev.weight * ev.sbottomWeight * electronScaleFactors.GetBinContent(electronScaleFactors.GetXaxis().FindBin(ev.pt1),electronScaleFactors.GetYaxis().FindBin(abs(ev.eta1))) * electronScaleFactors.GetBinContent(electronScaleFactors.GetXaxis().FindBin(ev.pt2),electronScaleFactors.GetYaxis().FindBin(abs(ev.eta2)))
								elif ev.nGenSUSYLeptons == 2 and ev.nGenSUSYNeutrinos == 2 and ev.nGenSUSYSleptons == 0 and ev.motherPdgId1 != 1000011 and ev.motherPdgId1 != 2000011 and ev.motherPdgId1 != 1000013 and ev.motherPdgId1 != 2000013 and ev.motherPdgId2 != 1000011 and ev.motherPdgId2 != 2000011 and ev.motherPdgId2 != 1000013 and ev.motherPdgId2 != 2000013: 
									signalEvents +=  9./2. * 0.0404 * ev.weight * ev.sbottomWeight * electronScaleFactors.GetBinContent(electronScaleFactors.GetXaxis().FindBin(ev.pt1),electronScaleFactors.GetYaxis().FindBin(abs(ev.eta1))) * electronScaleFactors.GetBinContent(electronScaleFactors.GetXaxis().FindBin(ev.pt2),electronScaleFactors.GetYaxis().FindBin(abs(ev.eta2)))
								elif ev.nGenSUSYLeptons == 2 and ev.nGenSUSYNeutrinos == 0 and (ev.motherPdgId1 == 1000011 or ev.motherPdgId1 == 2000011 or ev.motherPdgId1 == 1000013 or ev.motherPdgId1 == 2000013 or ev.motherPdgId2 == 1000011 or ev.motherPdgId2 == 2000011 or ev.motherPdgId2 == 1000013 or ev.motherPdgId2 == 2000013): 
									signalEvents +=  ev.weight * ev.sbottomWeight * electronScaleFactors.GetBinContent(electronScaleFactors.GetXaxis().FindBin(ev.pt1),electronScaleFactors.GetYaxis().FindBin(abs(ev.eta1))) * electronScaleFactors.GetBinContent(electronScaleFactors.GetXaxis().FindBin(ev.pt2),electronScaleFactors.GetYaxis().FindBin(abs(ev.eta2)))
								else:
									print "Right selection not found"
									print "nGenLeptons: "+str(ev.nGenSUSYLeptons)
			elif dilepton == "EMu":
				if etaRegion == "Barrel":
					for ev in tree:
						if ev.chargeProduct < 0 and abs(ev.eta1) < 1.4 and abs(ev.eta2) < 1.4 and ev.pt1 > 20 and ev.pt2 > 20 and ev.inv > mll_lower_Cut and ev.inv < mll_upper_Cut and ev.nJetsSmeared >= 3 and abs(ev.eta1) < 2.4 and abs(ev.eta2) < 2.4 and ev.deltaR > 0.3:
							MCEvents +=1
							if ev.nGenSUSYLeptons == 4:
								signalEvents += 9*0.0102 * ev.weight * ev.sbottomWeight * electronScaleFactors.GetBinContent(electronScaleFactors.GetXaxis().FindBin(ev.pt1),electronScaleFactors.GetYaxis().FindBin(abs(ev.eta1))) * electronScaleFactors.GetBinContent(electronScaleFactors.GetXaxis().FindBin(ev.pt2),electronScaleFactors.GetYaxis().FindBin(abs(ev.eta2)))
							elif ev.nGenSUSYLeptons == 3:
								signalEvents += 3. * 0.101 * ev.weight * ev.sbottomWeight * electronScaleFactors.GetBinContent(electronScaleFactors.GetXaxis().FindBin(ev.pt1),electronScaleFactors.GetYaxis().FindBin(abs(ev.eta1))) * electronScaleFactors.GetBinContent(electronScaleFactors.GetXaxis().FindBin(ev.pt2),electronScaleFactors.GetYaxis().FindBin(abs(ev.eta2)))
							elif ev.nGenSUSYLeptons == 1 and ev.nGenSUSYNeutrinos == 2:
								signalEvents +=  3. * 0.2 * ev.weight * ev.sbottomWeight * electronScaleFactors.GetBinContent(electronScaleFactors.GetXaxis().FindBin(ev.pt1),electronScaleFactors.GetYaxis().FindBin(abs(ev.eta1))) * electronScaleFactors.GetBinContent(electronScaleFactors.GetXaxis().FindBin(ev.pt2),electronScaleFactors.GetYaxis().FindBin(abs(ev.eta2)))
							elif ev.nGenSUSYLeptons == 1 and ev.nGenSUSYNeutrinos == 0:
								signalEvents +=  3. * 0.6991 * ev.weight * ev.sbottomWeight * electronScaleFactors.GetBinContent(electronScaleFactors.GetXaxis().FindBin(ev.pt1),electronScaleFactors.GetYaxis().FindBin(abs(ev.eta1))) * electronScaleFactors.GetBinContent(electronScaleFactors.GetXaxis().FindBin(ev.pt2),electronScaleFactors.GetYaxis().FindBin(abs(ev.eta2)))
							elif ev.nGenSUSYLeptons == 2 and ev.nGenSUSYNeutrinos == 0 and ev.nGenSUSYSleptons == 0 and  ev.motherPdgId1 != 1000011 and ev.motherPdgId1 != 2000011 and ev.motherPdgId1 != 1000013 and ev.motherPdgId1 != 2000013 and ev.motherPdgId2 != 1000011 and ev.motherPdgId2 != 2000011 and ev.motherPdgId2 != 1000013 and ev.motherPdgId2 != 2000013: 
								signalEvents +=  9./2. * 0.1411 * ev.weight * ev.sbottomWeight * electronScaleFactors.GetBinContent(electronScaleFactors.GetXaxis().FindBin(ev.pt1),electronScaleFactors.GetYaxis().FindBin(abs(ev.eta1))) * electronScaleFactors.GetBinContent(electronScaleFactors.GetXaxis().FindBin(ev.pt2),electronScaleFactors.GetYaxis().FindBin(abs(ev.eta2)))
							elif ev.nGenSUSYLeptons == 2 and ev.nGenSUSYNeutrinos == 2 and ev.nGenSUSYSleptons == 0 and ev.motherPdgId1 != 1000011 and ev.motherPdgId1 != 2000011 and ev.motherPdgId1 != 1000013 and ev.motherPdgId1 != 2000013 and ev.motherPdgId2 != 1000011 and ev.motherPdgId2 != 2000011 and ev.motherPdgId2 != 1000013 and ev.motherPdgId2 != 2000013: 
								signalEvents +=  9./2. * 0.0404 * ev.weight * ev.sbottomWeight * electronScaleFactors.GetBinContent(electronScaleFactors.GetXaxis().FindBin(ev.pt1),electronScaleFactors.GetYaxis().FindBin(abs(ev.eta1))) * electronScaleFactors.GetBinContent(electronScaleFactors.GetXaxis().FindBin(ev.pt2),electronScaleFactors.GetYaxis().FindBin(abs(ev.eta2)))
							elif ev.nGenSUSYLeptons == 2 and ev.nGenSUSYNeutrinos == 0 and (ev.motherPdgId1 == 1000011 or ev.motherPdgId1 == 2000011 or ev.motherPdgId1 == 1000013 or ev.motherPdgId1 == 2000013 or ev.motherPdgId2 == 1000011 or ev.motherPdgId2 == 2000011 or ev.motherPdgId2 == 1000013 or ev.motherPdgId2 == 2000013): 
								signalEvents +=  ev.weight * ev.sbottomWeight * electronScaleFactors.GetBinContent(electronScaleFactors.GetXaxis().FindBin(ev.pt1),electronScaleFactors.GetYaxis().FindBin(abs(ev.eta1))) * electronScaleFactors.GetBinContent(electronScaleFactors.GetXaxis().FindBin(ev.pt2),electronScaleFactors.GetYaxis().FindBin(abs(ev.eta2)))
							else:
								print "Right selection not found"
								print "nGenLeptons: "+str(ev.nGenSUSYLeptons)
				elif etaRegion == "Endcap":
					for ev in tree:
						if ev.chargeProduct < 0 and (((abs(ev.eta1) < 1.4 or abs(ev.eta1) > 1.6) and (abs(ev.eta2) < 1.4 or abs(ev.eta2) > 1.6)) and 1.6 <= max(abs(ev.eta1),abs(ev.eta2))) and ev.pt1 > 20 and ev.pt2 > 20 and ev.inv > mll_lower_Cut and ev.inv < mll_upper_Cut and ev.nJetsSmeared >= 3 and abs(ev.eta1) < 2.4 and abs(ev.eta2) < 2.4 and ev.deltaR > 0.3:
							MCEvents +=1
							if ev.nGenSUSYLeptons == 4:
								signalEvents += 9*0.0102 * ev.weight * ev.sbottomWeight * electronScaleFactors.GetBinContent(electronScaleFactors.GetXaxis().FindBin(ev.pt1),electronScaleFactors.GetYaxis().FindBin(abs(ev.eta1))) * electronScaleFactors.GetBinContent(electronScaleFactors.GetXaxis().FindBin(ev.pt2),electronScaleFactors.GetYaxis().FindBin(abs(ev.eta2)))
							elif ev.nGenSUSYLeptons == 3:
								signalEvents += 3. * 0.101 * ev.weight * ev.sbottomWeight * electronScaleFactors.GetBinContent(electronScaleFactors.GetXaxis().FindBin(ev.pt1),electronScaleFactors.GetYaxis().FindBin(abs(ev.eta1))) * electronScaleFactors.GetBinContent(electronScaleFactors.GetXaxis().FindBin(ev.pt2),electronScaleFactors.GetYaxis().FindBin(abs(ev.eta2)))
							elif ev.nGenSUSYLeptons == 1 and ev.nGenSUSYNeutrinos == 2:
								signalEvents +=  3. * 0.2 * ev.weight * ev.sbottomWeight * electronScaleFactors.GetBinContent(electronScaleFactors.GetXaxis().FindBin(ev.pt1),electronScaleFactors.GetYaxis().FindBin(abs(ev.eta1))) * electronScaleFactors.GetBinContent(electronScaleFactors.GetXaxis().FindBin(ev.pt2),electronScaleFactors.GetYaxis().FindBin(abs(ev.eta2)))
							elif ev.nGenSUSYLeptons == 1 and ev.nGenSUSYNeutrinos == 0:
								signalEvents +=  3. * 0.6991 * ev.weight * ev.sbottomWeight * electronScaleFactors.GetBinContent(electronScaleFactors.GetXaxis().FindBin(ev.pt1),electronScaleFactors.GetYaxis().FindBin(abs(ev.eta1))) * electronScaleFactors.GetBinContent(electronScaleFactors.GetXaxis().FindBin(ev.pt2),electronScaleFactors.GetYaxis().FindBin(abs(ev.eta2)))
							elif ev.nGenSUSYLeptons == 2 and ev.nGenSUSYNeutrinos == 0 and ev.nGenSUSYSleptons == 0 and ev.motherPdgId1 != 1000011 and ev.motherPdgId1 != 2000011 and ev.motherPdgId1 != 1000013 and ev.motherPdgId1 != 2000013 and ev.motherPdgId2 != 1000011 and ev.motherPdgId2 != 2000011 and ev.motherPdgId2 != 1000013 and ev.motherPdgId2 != 2000013: 
								signalEvents +=  9./2. * 0.1411 * ev.weight * ev.sbottomWeight * electronScaleFactors.GetBinContent(electronScaleFactors.GetXaxis().FindBin(ev.pt1),electronScaleFactors.GetYaxis().FindBin(abs(ev.eta1))) * electronScaleFactors.GetBinContent(electronScaleFactors.GetXaxis().FindBin(ev.pt2),electronScaleFactors.GetYaxis().FindBin(abs(ev.eta2)))
							elif ev.nGenSUSYLeptons == 2 and ev.nGenSUSYNeutrinos == 2 and ev.nGenSUSYSleptons == 0 and ev.motherPdgId1 != 1000011 and ev.motherPdgId1 != 2000011 and ev.motherPdgId1 != 1000013 and ev.motherPdgId1 != 2000013 and ev.motherPdgId2 != 1000011 and ev.motherPdgId2 != 2000011 and ev.motherPdgId2 != 1000013 and ev.motherPdgId2 != 2000013: 
								signalEvents +=  9./2. * 0.0404 * ev.weight * ev.sbottomWeight * electronScaleFactors.GetBinContent(electronScaleFactors.GetXaxis().FindBin(ev.pt1),electronScaleFactors.GetYaxis().FindBin(abs(ev.eta1))) * electronScaleFactors.GetBinContent(electronScaleFactors.GetXaxis().FindBin(ev.pt2),electronScaleFactors.GetYaxis().FindBin(abs(ev.eta2)))
							elif ev.nGenSUSYLeptons == 2 and ev.nGenSUSYNeutrinos == 0 and (ev.motherPdgId1 == 1000011 or ev.motherPdgId1 == 2000011 or ev.motherPdgId1 == 1000013 or ev.motherPdgId1 == 2000013 or ev.motherPdgId2 == 1000011 or ev.motherPdgId2 == 2000011 or ev.motherPdgId2 == 1000013 or ev.motherPdgId2 == 2000013): 
								signalEvents +=  ev.weight * ev.sbottomWeight * electronScaleFactors.GetBinContent(electronScaleFactors.GetXaxis().FindBin(ev.pt1),electronScaleFactors.GetYaxis().FindBin(abs(ev.eta1))) * electronScaleFactors.GetBinContent(electronScaleFactors.GetXaxis().FindBin(ev.pt2),electronScaleFactors.GetYaxis().FindBin(abs(ev.eta2)))
							else:
								print "Right selection not found"
								print "nGenLeptons: "+str(ev.nGenSUSYLeptons)
						
		elif additionalCut == "Met150Cut":
			if dilepton == "EE":
				if etaRegion == "Barrel":
					for ev in tree:
						if ev.chargeProduct < 0 and abs(ev.eta1) < 1.4 and abs(ev.eta2) < 1.4 and ev.pt1 > 20 and ev.pt2 > 20 and ev.inv > mll_lower_Cut and ev.inv < mll_upper_Cut and ev.patPFMET > 150 and abs(ev.eta1) < 2.4 and abs(ev.eta2) < 2.4 and ev.deltaR > 0.3:
							MCEvents +=1
							if ev.nGenSUSYLeptons == 4:
								signalEvents += 9*0.0102 * ev.weight * ev.sbottomWeight * electronScaleFactors.GetBinContent(electronScaleFactors.GetXaxis().FindBin(ev.pt1),electronScaleFactors.GetYaxis().FindBin(abs(ev.eta1))) * electronScaleFactors.GetBinContent(electronScaleFactors.GetXaxis().FindBin(ev.pt2),electronScaleFactors.GetYaxis().FindBin(abs(ev.eta2)))
							elif ev.nGenSUSYLeptons == 3:
								signalEvents += 3. * 0.101 * ev.weight * ev.sbottomWeight * electronScaleFactors.GetBinContent(electronScaleFactors.GetXaxis().FindBin(ev.pt1),electronScaleFactors.GetYaxis().FindBin(abs(ev.eta1))) * electronScaleFactors.GetBinContent(electronScaleFactors.GetXaxis().FindBin(ev.pt2),electronScaleFactors.GetYaxis().FindBin(abs(ev.eta2)))
							elif ev.nGenSUSYLeptons == 1 and ev.nGenSUSYNeutrinos == 2:
								signalEvents +=  3. * 0.2 * ev.weight * ev.sbottomWeight * electronScaleFactors.GetBinContent(electronScaleFactors.GetXaxis().FindBin(ev.pt1),electronScaleFactors.GetYaxis().FindBin(abs(ev.eta1))) * electronScaleFactors.GetBinContent(electronScaleFactors.GetXaxis().FindBin(ev.pt2),electronScaleFactors.GetYaxis().FindBin(abs(ev.eta2)))
							elif ev.nGenSUSYLeptons == 1 and ev.nGenSUSYNeutrinos == 0:
								signalEvents +=  3. * 0.6991 * ev.weight * ev.sbottomWeight * electronScaleFactors.GetBinContent(electronScaleFactors.GetXaxis().FindBin(ev.pt1),electronScaleFactors.GetYaxis().FindBin(abs(ev.eta1))) * electronScaleFactors.GetBinContent(electronScaleFactors.GetXaxis().FindBin(ev.pt2),electronScaleFactors.GetYaxis().FindBin(abs(ev.eta2)))
							elif ev.nGenSUSYLeptons == 2 and ev.nGenSUSYNeutrinos == 0 and ev.nGenSUSYSleptons == 0 and ev.motherPdgId1 != 1000011 and ev.motherPdgId1 != 2000011 and ev.motherPdgId1 != 1000013 and ev.motherPdgId1 != 2000013 and ev.motherPdgId2 != 1000011 and ev.motherPdgId2 != 2000011 and ev.motherPdgId2 != 1000013 and ev.motherPdgId2 != 2000013: 
								signalEvents +=  9./2. * 0.1411 * ev.weight * ev.sbottomWeight * electronScaleFactors.GetBinContent(electronScaleFactors.GetXaxis().FindBin(ev.pt1),electronScaleFactors.GetYaxis().FindBin(abs(ev.eta1))) * electronScaleFactors.GetBinContent(electronScaleFactors.GetXaxis().FindBin(ev.pt2),electronScaleFactors.GetYaxis().FindBin(abs(ev.eta2)))
							elif ev.nGenSUSYLeptons == 2 and ev.nGenSUSYNeutrinos == 2 and ev.nGenSUSYSleptons == 0 and ev.motherPdgId1 != 1000011 and ev.motherPdgId1 != 2000011 and ev.motherPdgId1 != 1000013 and ev.motherPdgId1 != 2000013 and ev.motherPdgId2 != 1000011 and ev.motherPdgId2 != 2000011 and ev.motherPdgId2 != 1000013 and ev.motherPdgId2 != 2000013: 
								signalEvents +=  9./2. * 0.0404 * ev.weight * ev.sbottomWeight * electronScaleFactors.GetBinContent(electronScaleFactors.GetXaxis().FindBin(ev.pt1),electronScaleFactors.GetYaxis().FindBin(abs(ev.eta1))) * electronScaleFactors.GetBinContent(electronScaleFactors.GetXaxis().FindBin(ev.pt2),electronScaleFactors.GetYaxis().FindBin(abs(ev.eta2)))
							elif ev.nGenSUSYLeptons == 2 and ev.nGenSUSYNeutrinos == 0 and (ev.motherPdgId1 == 1000011 or ev.motherPdgId1 == 2000011 or ev.motherPdgId1 == 1000013 or ev.motherPdgId1 == 2000013 or ev.motherPdgId2 == 1000011 or ev.motherPdgId2 == 2000011 or ev.motherPdgId2 == 1000013 or ev.motherPdgId2 == 2000013): 
								signalEvents +=  ev.weight * ev.sbottomWeight * electronScaleFactors.GetBinContent(electronScaleFactors.GetXaxis().FindBin(ev.pt1),electronScaleFactors.GetYaxis().FindBin(abs(ev.eta1))) * electronScaleFactors.GetBinContent(electronScaleFactors.GetXaxis().FindBin(ev.pt2),electronScaleFactors.GetYaxis().FindBin(abs(ev.eta2)))
							else:
								print "Right selection not found"
								print "nGenLeptons: "+str(ev.nGenSUSYLeptons)
				elif etaRegion == "Endcap":
					for ev in tree:
						if ev.chargeProduct < 0 and (((abs(ev.eta1) < 1.4 or abs(ev.eta1) > 1.6) and (abs(ev.eta2) < 1.4 or abs(ev.eta2) > 1.6)) and 1.6 <= max(abs(ev.eta1),abs(ev.eta2))) and ev.pt1 > 20 and ev.pt2 > 20 and ev.inv > mll_lower_Cut and ev.inv < mll_upper_Cut and ev.patPFMET > 150 and abs(ev.eta1) < 2.4 and abs(ev.eta2) < 2.4 and ev.deltaR > 0.3:
							MCEvents +=1
							if ev.nGenSUSYLeptons == 4:
								signalEvents += 9*0.0102 * ev.weight * ev.sbottomWeight * electronScaleFactors.GetBinContent(electronScaleFactors.GetXaxis().FindBin(ev.pt1),electronScaleFactors.GetYaxis().FindBin(abs(ev.eta1))) * electronScaleFactors.GetBinContent(electronScaleFactors.GetXaxis().FindBin(ev.pt2),electronScaleFactors.GetYaxis().FindBin(abs(ev.eta2)))
							elif ev.nGenSUSYLeptons == 3:
								signalEvents += 3. * 0.101 * ev.weight * ev.sbottomWeight * electronScaleFactors.GetBinContent(electronScaleFactors.GetXaxis().FindBin(ev.pt1),electronScaleFactors.GetYaxis().FindBin(abs(ev.eta1))) * electronScaleFactors.GetBinContent(electronScaleFactors.GetXaxis().FindBin(ev.pt2),electronScaleFactors.GetYaxis().FindBin(abs(ev.eta2)))
							elif ev.nGenSUSYLeptons == 1 and ev.nGenSUSYNeutrinos == 2:
								signalEvents +=  3. * 0.2 * ev.weight * ev.sbottomWeight * electronScaleFactors.GetBinContent(electronScaleFactors.GetXaxis().FindBin(ev.pt1),electronScaleFactors.GetYaxis().FindBin(abs(ev.eta1))) * electronScaleFactors.GetBinContent(electronScaleFactors.GetXaxis().FindBin(ev.pt2),electronScaleFactors.GetYaxis().FindBin(abs(ev.eta2)))
							elif ev.nGenSUSYLeptons == 1 and ev.nGenSUSYNeutrinos == 0:
								signalEvents +=  3. * 0.6991 * ev.weight * ev.sbottomWeight * electronScaleFactors.GetBinContent(electronScaleFactors.GetXaxis().FindBin(ev.pt1),electronScaleFactors.GetYaxis().FindBin(abs(ev.eta1))) * electronScaleFactors.GetBinContent(electronScaleFactors.GetXaxis().FindBin(ev.pt2),electronScaleFactors.GetYaxis().FindBin(abs(ev.eta2)))
							elif ev.nGenSUSYLeptons == 2 and ev.nGenSUSYNeutrinos == 0 and ev.nGenSUSYSleptons == 0 and ev.motherPdgId1 != 1000011 and ev.motherPdgId1 != 2000011 and ev.motherPdgId1 != 1000013 and ev.motherPdgId1 != 2000013 and ev.motherPdgId2 != 1000011 and ev.motherPdgId2 != 2000011 and ev.motherPdgId2 != 1000013 and ev.motherPdgId2 != 2000013: 
								signalEvents +=  9./2. * 0.1411 * ev.weight * ev.sbottomWeight * electronScaleFactors.GetBinContent(electronScaleFactors.GetXaxis().FindBin(ev.pt1),electronScaleFactors.GetYaxis().FindBin(abs(ev.eta1))) * electronScaleFactors.GetBinContent(electronScaleFactors.GetXaxis().FindBin(ev.pt2),electronScaleFactors.GetYaxis().FindBin(abs(ev.eta2)))
							elif ev.nGenSUSYLeptons == 2 and ev.nGenSUSYNeutrinos == 2 and ev.nGenSUSYSleptons == 0 and ev.motherPdgId1 != 1000011 and ev.motherPdgId1 != 2000011 and ev.motherPdgId1 != 1000013 and ev.motherPdgId1 != 2000013 and ev.motherPdgId2 != 1000011 and ev.motherPdgId2 != 2000011 and ev.motherPdgId2 != 1000013 and ev.motherPdgId2 != 2000013: 
								signalEvents +=  9./2. * 0.0404 * ev.weight * ev.sbottomWeight * electronScaleFactors.GetBinContent(electronScaleFactors.GetXaxis().FindBin(ev.pt1),electronScaleFactors.GetYaxis().FindBin(abs(ev.eta1))) * electronScaleFactors.GetBinContent(electronScaleFactors.GetXaxis().FindBin(ev.pt2),electronScaleFactors.GetYaxis().FindBin(abs(ev.eta2)))
							elif ev.nGenSUSYLeptons == 2 and ev.nGenSUSYNeutrinos == 0 and (ev.motherPdgId1 == 1000011 or ev.motherPdgId1 == 2000011 or ev.motherPdgId1 == 1000013 or ev.motherPdgId1 == 2000013 or ev.motherPdgId2 == 1000011 or ev.motherPdgId2 == 2000011 or ev.motherPdgId2 == 1000013 or ev.motherPdgId2 == 2000013): 
								signalEvents +=  ev.weight * ev.sbottomWeight * electronScaleFactors.GetBinContent(electronScaleFactors.GetXaxis().FindBin(ev.pt1),electronScaleFactors.GetYaxis().FindBin(abs(ev.eta1))) * electronScaleFactors.GetBinContent(electronScaleFactors.GetXaxis().FindBin(ev.pt2),electronScaleFactors.GetYaxis().FindBin(abs(ev.eta2)))
							else:
								print "Right selection not found"
								print "nGenLeptons: "+str(ev.nGenSUSYLeptons)
			elif dilepton == "MuMu":
				if etaRegion == "Barrel":
					for ev in tree:
						if ev.chargeProduct < 0 and abs(ev.eta1) < 1.4 and abs(ev.eta2) < 1.4 and ev.pt1 > 20 and ev.pt2 > 20 and ev.inv > mll_lower_Cut and ev.inv < mll_upper_Cut and ev.patPFMET > 150 and abs(ev.eta1) < 2.4 and abs(ev.eta2) < 2.4 and ev.deltaR > 0.3:
							MCEvents +=1
							if ev.nGenSUSYLeptons == 4:
								signalEvents += 9*0.0102 * ev.weight * ev.sbottomWeight * electronScaleFactors.GetBinContent(electronScaleFactors.GetXaxis().FindBin(ev.pt1),electronScaleFactors.GetYaxis().FindBin(abs(ev.eta1))) * electronScaleFactors.GetBinContent(electronScaleFactors.GetXaxis().FindBin(ev.pt2),electronScaleFactors.GetYaxis().FindBin(abs(ev.eta2)))
							elif ev.nGenSUSYLeptons == 3:
								signalEvents += 3. * 0.101 * ev.weight * ev.sbottomWeight * electronScaleFactors.GetBinContent(electronScaleFactors.GetXaxis().FindBin(ev.pt1),electronScaleFactors.GetYaxis().FindBin(abs(ev.eta1))) * electronScaleFactors.GetBinContent(electronScaleFactors.GetXaxis().FindBin(ev.pt2),electronScaleFactors.GetYaxis().FindBin(abs(ev.eta2)))
							elif ev.nGenSUSYLeptons == 1 and ev.nGenSUSYNeutrinos == 2:
								signalEvents +=  3. * 0.2 * ev.weight * ev.sbottomWeight * electronScaleFactors.GetBinContent(electronScaleFactors.GetXaxis().FindBin(ev.pt1),electronScaleFactors.GetYaxis().FindBin(abs(ev.eta1))) * electronScaleFactors.GetBinContent(electronScaleFactors.GetXaxis().FindBin(ev.pt2),electronScaleFactors.GetYaxis().FindBin(abs(ev.eta2)))
							elif ev.nGenSUSYLeptons == 1 and ev.nGenSUSYNeutrinos == 0:
								signalEvents +=  3. * 0.6991 * ev.weight * ev.sbottomWeight * electronScaleFactors.GetBinContent(electronScaleFactors.GetXaxis().FindBin(ev.pt1),electronScaleFactors.GetYaxis().FindBin(abs(ev.eta1))) * electronScaleFactors.GetBinContent(electronScaleFactors.GetXaxis().FindBin(ev.pt2),electronScaleFactors.GetYaxis().FindBin(abs(ev.eta2)))
							elif ev.nGenSUSYLeptons == 2 and ev.nGenSUSYNeutrinos == 0 and ev.nGenSUSYSleptons == 0 and ev.motherPdgId1 != 1000011 and ev.motherPdgId1 != 2000011 and ev.motherPdgId1 != 1000013 and ev.motherPdgId1 != 2000013 and ev.motherPdgId2 != 1000011 and ev.motherPdgId2 != 2000011 and ev.motherPdgId2 != 1000013 and ev.motherPdgId2 != 2000013: 
								signalEvents +=  9./2. * 0.1411 * ev.weight * ev.sbottomWeight * electronScaleFactors.GetBinContent(electronScaleFactors.GetXaxis().FindBin(ev.pt1),electronScaleFactors.GetYaxis().FindBin(abs(ev.eta1))) * electronScaleFactors.GetBinContent(electronScaleFactors.GetXaxis().FindBin(ev.pt2),electronScaleFactors.GetYaxis().FindBin(abs(ev.eta2)))
							elif ev.nGenSUSYLeptons == 2 and ev.nGenSUSYNeutrinos == 2 and ev.nGenSUSYSleptons == 0 and ev.motherPdgId1 != 1000011 and ev.motherPdgId1 != 2000011 and ev.motherPdgId1 != 1000013 and ev.motherPdgId1 != 2000013 and ev.motherPdgId2 != 1000011 and ev.motherPdgId2 != 2000011 and ev.motherPdgId2 != 1000013 and ev.motherPdgId2 != 2000013: 
								signalEvents +=  9./2. * 0.0404 * ev.weight * ev.sbottomWeight * electronScaleFactors.GetBinContent(electronScaleFactors.GetXaxis().FindBin(ev.pt1),electronScaleFactors.GetYaxis().FindBin(abs(ev.eta1))) * electronScaleFactors.GetBinContent(electronScaleFactors.GetXaxis().FindBin(ev.pt2),electronScaleFactors.GetYaxis().FindBin(abs(ev.eta2)))
							elif ev.nGenSUSYLeptons == 2 and ev.nGenSUSYNeutrinos == 0 and (ev.motherPdgId1 == 1000011 or ev.motherPdgId1 == 2000011 or ev.motherPdgId1 == 1000013 or ev.motherPdgId1 == 2000013 or ev.motherPdgId2 == 1000011 or ev.motherPdgId2 == 2000011 or ev.motherPdgId2 == 1000013 or ev.motherPdgId2 == 2000013): 
								signalEvents +=  ev.weight * ev.sbottomWeight * electronScaleFactors.GetBinContent(electronScaleFactors.GetXaxis().FindBin(ev.pt1),electronScaleFactors.GetYaxis().FindBin(abs(ev.eta1))) * electronScaleFactors.GetBinContent(electronScaleFactors.GetXaxis().FindBin(ev.pt2),electronScaleFactors.GetYaxis().FindBin(abs(ev.eta2)))
							else:
								print "Right selection not found"
								print "nGenLeptons: "+str(ev.nGenSUSYLeptons)
				elif etaRegion == "Endcap":
					for ev in tree:
						if ev.chargeProduct < 0 and (((abs(ev.eta1) < 1.4 or abs(ev.eta1) > 1.6) and (abs(ev.eta2) < 1.4 or abs(ev.eta2) > 1.6)) and 1.6 <= max(abs(ev.eta1),abs(ev.eta2))) and ev.pt1 > 20 and ev.pt2 > 20 and ev.inv > mll_lower_Cut and ev.inv < mll_upper_Cut and ev.patPFMET > 150 and abs(ev.eta1) < 2.4 and abs(ev.eta2) < 2.4 and ev.deltaR > 0.3:
							MCEvents +=1
							if ev.nGenSUSYLeptons == 4:
								signalEvents += 9*0.0102 * ev.weight * ev.sbottomWeight * electronScaleFactors.GetBinContent(electronScaleFactors.GetXaxis().FindBin(ev.pt1),electronScaleFactors.GetYaxis().FindBin(abs(ev.eta1))) * electronScaleFactors.GetBinContent(electronScaleFactors.GetXaxis().FindBin(ev.pt2),electronScaleFactors.GetYaxis().FindBin(abs(ev.eta2)))
							elif ev.nGenSUSYLeptons == 3:
								signalEvents += 3. * 0.101 * ev.weight * ev.sbottomWeight * electronScaleFactors.GetBinContent(electronScaleFactors.GetXaxis().FindBin(ev.pt1),electronScaleFactors.GetYaxis().FindBin(abs(ev.eta1))) * electronScaleFactors.GetBinContent(electronScaleFactors.GetXaxis().FindBin(ev.pt2),electronScaleFactors.GetYaxis().FindBin(abs(ev.eta2)))
							elif ev.nGenSUSYLeptons == 1 and ev.nGenSUSYNeutrinos == 2:
								signalEvents +=  3. * 0.2 * ev.weight * ev.sbottomWeight * electronScaleFactors.GetBinContent(electronScaleFactors.GetXaxis().FindBin(ev.pt1),electronScaleFactors.GetYaxis().FindBin(abs(ev.eta1))) * electronScaleFactors.GetBinContent(electronScaleFactors.GetXaxis().FindBin(ev.pt2),electronScaleFactors.GetYaxis().FindBin(abs(ev.eta2)))
							elif ev.nGenSUSYLeptons == 1 and ev.nGenSUSYNeutrinos == 0:
								signalEvents +=  3. * 0.6991 * ev.weight * ev.sbottomWeight * electronScaleFactors.GetBinContent(electronScaleFactors.GetXaxis().FindBin(ev.pt1),electronScaleFactors.GetYaxis().FindBin(abs(ev.eta1))) * electronScaleFactors.GetBinContent(electronScaleFactors.GetXaxis().FindBin(ev.pt2),electronScaleFactors.GetYaxis().FindBin(abs(ev.eta2)))
							elif ev.nGenSUSYLeptons == 2 and ev.nGenSUSYNeutrinos == 0 and ev.nGenSUSYSleptons == 0 and ev.motherPdgId1 != 1000011 and ev.motherPdgId1 != 2000011 and ev.motherPdgId1 != 1000013 and ev.motherPdgId1 != 2000013 and ev.motherPdgId2 != 1000011 and ev.motherPdgId2 != 2000011 and ev.motherPdgId2 != 1000013 and ev.motherPdgId2 != 2000013: 
								signalEvents +=  9./2. * 0.1411 * ev.weight * ev.sbottomWeight * electronScaleFactors.GetBinContent(electronScaleFactors.GetXaxis().FindBin(ev.pt1),electronScaleFactors.GetYaxis().FindBin(abs(ev.eta1))) * electronScaleFactors.GetBinContent(electronScaleFactors.GetXaxis().FindBin(ev.pt2),electronScaleFactors.GetYaxis().FindBin(abs(ev.eta2)))
							elif ev.nGenSUSYLeptons == 2 and ev.nGenSUSYNeutrinos == 2 and ev.nGenSUSYSleptons == 0 and ev.motherPdgId1 != 1000011 and ev.motherPdgId1 != 2000011 and ev.motherPdgId1 != 1000013 and ev.motherPdgId1 != 2000013 and ev.motherPdgId2 != 1000011 and ev.motherPdgId2 != 2000011 and ev.motherPdgId2 != 1000013 and ev.motherPdgId2 != 2000013: 
								signalEvents +=  9./2. * 0.0404 * ev.weight * ev.sbottomWeight * electronScaleFactors.GetBinContent(electronScaleFactors.GetXaxis().FindBin(ev.pt1),electronScaleFactors.GetYaxis().FindBin(abs(ev.eta1))) * electronScaleFactors.GetBinContent(electronScaleFactors.GetXaxis().FindBin(ev.pt2),electronScaleFactors.GetYaxis().FindBin(abs(ev.eta2)))
							elif ev.nGenSUSYLeptons == 2 and ev.nGenSUSYNeutrinos == 0 and (ev.motherPdgId1 == 1000011 or ev.motherPdgId1 == 2000011 or ev.motherPdgId1 == 1000013 or ev.motherPdgId1 == 2000013 or ev.motherPdgId2 == 1000011 or ev.motherPdgId2 == 2000011 or ev.motherPdgId2 == 1000013 or ev.motherPdgId2 == 2000013): 
								signalEvents +=  ev.weight * ev.sbottomWeight * electronScaleFactors.GetBinContent(electronScaleFactors.GetXaxis().FindBin(ev.pt1),electronScaleFactors.GetYaxis().FindBin(abs(ev.eta1))) * electronScaleFactors.GetBinContent(electronScaleFactors.GetXaxis().FindBin(ev.pt2),electronScaleFactors.GetYaxis().FindBin(abs(ev.eta2)))
							else:
								print "Right selection not found"
								print "nGenLeptons: "+str(ev.nGenSUSYLeptons)
			elif dilepton == "EMu":
				if etaRegion == "Barrel":
					for ev in tree:
						if ev.chargeProduct < 0 and abs(ev.eta1) < 1.4 and abs(ev.eta2) < 1.4 and ev.pt1 > 20 and ev.pt2 > 20 and ev.inv > mll_lower_Cut and ev.inv < mll_upper_Cut and ev.patPFMET > 150 and abs(ev.eta1) < 2.4 and abs(ev.eta2) < 2.4 and ev.deltaR > 0.3:
							MCEvents +=1
							if ev.nGenSUSYLeptons == 4:
								signalEvents += 9*0.0102 * ev.weight * ev.sbottomWeight * electronScaleFactors.GetBinContent(electronScaleFactors.GetXaxis().FindBin(ev.pt1),electronScaleFactors.GetYaxis().FindBin(abs(ev.eta1))) * electronScaleFactors.GetBinContent(electronScaleFactors.GetXaxis().FindBin(ev.pt2),electronScaleFactors.GetYaxis().FindBin(abs(ev.eta2)))
							elif ev.nGenSUSYLeptons == 3:
								signalEvents += 3. * 0.101 * ev.weight * ev.sbottomWeight * electronScaleFactors.GetBinContent(electronScaleFactors.GetXaxis().FindBin(ev.pt1),electronScaleFactors.GetYaxis().FindBin(abs(ev.eta1))) * electronScaleFactors.GetBinContent(electronScaleFactors.GetXaxis().FindBin(ev.pt2),electronScaleFactors.GetYaxis().FindBin(abs(ev.eta2)))
							elif ev.nGenSUSYLeptons == 1 and ev.nGenSUSYNeutrinos == 2:
								signalEvents +=  3. * 0.2 * ev.weight * ev.sbottomWeight * electronScaleFactors.GetBinContent(electronScaleFactors.GetXaxis().FindBin(ev.pt1),electronScaleFactors.GetYaxis().FindBin(abs(ev.eta1))) * electronScaleFactors.GetBinContent(electronScaleFactors.GetXaxis().FindBin(ev.pt2),electronScaleFactors.GetYaxis().FindBin(abs(ev.eta2)))
							elif ev.nGenSUSYLeptons == 1 and ev.nGenSUSYNeutrinos == 0:
								signalEvents +=  3. * 0.6991 * ev.weight * ev.sbottomWeight * electronScaleFactors.GetBinContent(electronScaleFactors.GetXaxis().FindBin(ev.pt1),electronScaleFactors.GetYaxis().FindBin(abs(ev.eta1))) * electronScaleFactors.GetBinContent(electronScaleFactors.GetXaxis().FindBin(ev.pt2),electronScaleFactors.GetYaxis().FindBin(abs(ev.eta2)))
							elif ev.nGenSUSYLeptons == 2 and ev.nGenSUSYNeutrinos == 0 and ev.nGenSUSYSleptons == 0 and ev.motherPdgId1 != 1000011 and ev.motherPdgId1 != 2000011 and ev.motherPdgId1 != 1000013 and ev.motherPdgId1 != 2000013 and ev.motherPdgId2 != 1000011 and ev.motherPdgId2 != 2000011 and ev.motherPdgId2 != 1000013 and ev.motherPdgId2 != 2000013: 
								signalEvents +=  9./2. * 0.1411 * ev.weight * ev.sbottomWeight * electronScaleFactors.GetBinContent(electronScaleFactors.GetXaxis().FindBin(ev.pt1),electronScaleFactors.GetYaxis().FindBin(abs(ev.eta1))) * electronScaleFactors.GetBinContent(electronScaleFactors.GetXaxis().FindBin(ev.pt2),electronScaleFactors.GetYaxis().FindBin(abs(ev.eta2)))
							elif ev.nGenSUSYLeptons == 2 and ev.nGenSUSYNeutrinos == 2 and ev.nGenSUSYSleptons == 0 and ev.motherPdgId1 != 1000011 and ev.motherPdgId1 != 2000011 and ev.motherPdgId1 != 1000013 and ev.motherPdgId1 != 2000013 and ev.motherPdgId2 != 1000011 and ev.motherPdgId2 != 2000011 and ev.motherPdgId2 != 1000013 and ev.motherPdgId2 != 2000013: 
								signalEvents +=  9./2. * 0.0404 * ev.weight * ev.sbottomWeight * electronScaleFactors.GetBinContent(electronScaleFactors.GetXaxis().FindBin(ev.pt1),electronScaleFactors.GetYaxis().FindBin(abs(ev.eta1))) * electronScaleFactors.GetBinContent(electronScaleFactors.GetXaxis().FindBin(ev.pt2),electronScaleFactors.GetYaxis().FindBin(abs(ev.eta2)))
							elif ev.nGenSUSYLeptons == 2 and ev.nGenSUSYNeutrinos == 0 and (ev.motherPdgId1 == 1000011 or ev.motherPdgId1 == 2000011 or ev.motherPdgId1 == 1000013 or ev.motherPdgId1 == 2000013 or ev.motherPdgId2 == 1000011 or ev.motherPdgId2 == 2000011 or ev.motherPdgId2 == 1000013 or ev.motherPdgId2 == 2000013): 
								signalEvents +=  ev.weight * ev.sbottomWeight * electronScaleFactors.GetBinContent(electronScaleFactors.GetXaxis().FindBin(ev.pt1),electronScaleFactors.GetYaxis().FindBin(abs(ev.eta1))) * electronScaleFactors.GetBinContent(electronScaleFactors.GetXaxis().FindBin(ev.pt2),electronScaleFactors.GetYaxis().FindBin(abs(ev.eta2)))
							else:
								print "Right selection not found"
								print "nGenLeptons: "+str(ev.nGenSUSYLeptons)
				elif etaRegion == "Endcap":
					for ev in tree:
						if ev.chargeProduct < 0 and (((abs(ev.eta1) < 1.4 or abs(ev.eta1) > 1.6) and (abs(ev.eta2) < 1.4 or abs(ev.eta2) > 1.6)) and 1.6 <= max(abs(ev.eta1),abs(ev.eta2))) and ev.pt1 > 20 and ev.pt2 > 20 and ev.inv > mll_lower_Cut and ev.inv < mll_upper_Cut and ev.patPFMET > 150 and abs(ev.eta1) < 2.4 and abs(ev.eta2) < 2.4 and ev.deltaR > 0.3:
							MCEvents +=1
							if ev.nGenSUSYLeptons == 4:
								signalEvents += 9*0.0102 * ev.weight * ev.sbottomWeight * electronScaleFactors.GetBinContent(electronScaleFactors.GetXaxis().FindBin(ev.pt1),electronScaleFactors.GetYaxis().FindBin(abs(ev.eta1))) * electronScaleFactors.GetBinContent(electronScaleFactors.GetXaxis().FindBin(ev.pt2),electronScaleFactors.GetYaxis().FindBin(abs(ev.eta2)))
							elif ev.nGenSUSYLeptons == 3:
								signalEvents += 3. * 0.101 * ev.weight * ev.sbottomWeight * electronScaleFactors.GetBinContent(electronScaleFactors.GetXaxis().FindBin(ev.pt1),electronScaleFactors.GetYaxis().FindBin(abs(ev.eta1))) * electronScaleFactors.GetBinContent(electronScaleFactors.GetXaxis().FindBin(ev.pt2),electronScaleFactors.GetYaxis().FindBin(abs(ev.eta2)))
							elif ev.nGenSUSYLeptons == 1 and ev.nGenSUSYNeutrinos == 2:
								signalEvents +=  3. * 0.2 * ev.weight * ev.sbottomWeight * electronScaleFactors.GetBinContent(electronScaleFactors.GetXaxis().FindBin(ev.pt1),electronScaleFactors.GetYaxis().FindBin(abs(ev.eta1))) * electronScaleFactors.GetBinContent(electronScaleFactors.GetXaxis().FindBin(ev.pt2),electronScaleFactors.GetYaxis().FindBin(abs(ev.eta2)))
							elif ev.nGenSUSYLeptons == 1 and ev.nGenSUSYNeutrinos == 0:
								signalEvents +=  3. * 0.6991 * ev.weight * ev.sbottomWeight * electronScaleFactors.GetBinContent(electronScaleFactors.GetXaxis().FindBin(ev.pt1),electronScaleFactors.GetYaxis().FindBin(abs(ev.eta1))) * electronScaleFactors.GetBinContent(electronScaleFactors.GetXaxis().FindBin(ev.pt2),electronScaleFactors.GetYaxis().FindBin(abs(ev.eta2)))
							elif ev.nGenSUSYLeptons == 2 and ev.nGenSUSYNeutrinos == 0 and ev.nGenSUSYSleptons == 0 and ev.motherPdgId1 != 1000011 and ev.motherPdgId1 != 2000011 and ev.motherPdgId1 != 1000013 and ev.motherPdgId1 != 2000013 and ev.motherPdgId2 != 1000011 and ev.motherPdgId2 != 2000011 and ev.motherPdgId2 != 1000013 and ev.motherPdgId2 != 2000013: 
								signalEvents +=  9./2. * 0.1411 * ev.weight * ev.sbottomWeight * electronScaleFactors.GetBinContent(electronScaleFactors.GetXaxis().FindBin(ev.pt1),electronScaleFactors.GetYaxis().FindBin(abs(ev.eta1))) * electronScaleFactors.GetBinContent(electronScaleFactors.GetXaxis().FindBin(ev.pt2),electronScaleFactors.GetYaxis().FindBin(abs(ev.eta2)))
							elif ev.nGenSUSYLeptons == 2 and ev.nGenSUSYNeutrinos == 2 and ev.nGenSUSYSleptons == 0 and ev.motherPdgId1 != 1000011 and ev.motherPdgId1 != 2000011 and ev.motherPdgId1 != 1000013 and ev.motherPdgId1 != 2000013 and ev.motherPdgId2 != 1000011 and ev.motherPdgId2 != 2000011 and ev.motherPdgId2 != 1000013 and ev.motherPdgId2 != 2000013: 
								signalEvents +=  9./2. * 0.0404 * ev.weight * ev.sbottomWeight * electronScaleFactors.GetBinContent(electronScaleFactors.GetXaxis().FindBin(ev.pt1),electronScaleFactors.GetYaxis().FindBin(abs(ev.eta1))) * electronScaleFactors.GetBinContent(electronScaleFactors.GetXaxis().FindBin(ev.pt2),electronScaleFactors.GetYaxis().FindBin(abs(ev.eta2)))
							elif ev.nGenSUSYLeptons == 2 and ev.nGenSUSYNeutrinos == 0 and (ev.motherPdgId1 == 1000011 or ev.motherPdgId1 == 2000011 or ev.motherPdgId1 == 1000013 or ev.motherPdgId1 == 2000013 or ev.motherPdgId2 == 1000011 or ev.motherPdgId2 == 2000011 or ev.motherPdgId2 == 1000013 or ev.motherPdgId2 == 2000013): 
								signalEvents +=  ev.weight * ev.sbottomWeight * electronScaleFactors.GetBinContent(electronScaleFactors.GetXaxis().FindBin(ev.pt1),electronScaleFactors.GetYaxis().FindBin(abs(ev.eta1))) * electronScaleFactors.GetBinContent(electronScaleFactors.GetXaxis().FindBin(ev.pt2),electronScaleFactors.GetYaxis().FindBin(abs(ev.eta2)))
							else:
								print "Right selection not found"
								print "nGenLeptons: "+str(ev.nGenSUSYLeptons)
		
		else:
			if dilepton == "EE":
				if etaRegion == "Barrel":
					for ev in tree:
						if ev.chargeProduct < 0 and abs(ev.eta1) < 1.4 and abs(ev.eta2) < 1.4 and ev.pt1 > 20 and ev.pt2 > 20 and ev.inv > mll_lower_Cut and ev.inv < mll_upper_Cut and ((ev.patPFMet > 100 and ev.nJetsSmeared >= 3) or  (ev.patPFMet > 150 and ev.nJetsSmeared >=2)) and abs(ev.eta1) < 2.4 and abs(ev.eta2) < 2.4 and ev.deltaR > 0.3:
							MCEvents +=1
							if ev.nGenSUSYLeptons == 4:
								FourGenLeptonEvents += 1
								FourGenLeptonEventsReweighted += 9*0.0102 
								signalEvents += 9*0.0102 * ev.weight * ev.sbottomWeight * electronScaleFactors.GetBinContent(electronScaleFactors.GetXaxis().FindBin(ev.pt1),electronScaleFactors.GetYaxis().FindBin(abs(ev.eta1))) * electronScaleFactors.GetBinContent(electronScaleFactors.GetXaxis().FindBin(ev.pt2),electronScaleFactors.GetYaxis().FindBin(abs(ev.eta2)))
							elif ev.nGenSUSYLeptons == 3:
								ThreeGenLeptonEvents += 1
								ThreeGenLeptonEventsReweighted += 3. * 0.101
								signalEvents += 3. * 0.101 * ev.weight * ev.sbottomWeight * electronScaleFactors.GetBinContent(electronScaleFactors.GetXaxis().FindBin(ev.pt1),electronScaleFactors.GetYaxis().FindBin(abs(ev.eta1))) * electronScaleFactors.GetBinContent(electronScaleFactors.GetXaxis().FindBin(ev.pt2),electronScaleFactors.GetYaxis().FindBin(abs(ev.eta2)))
							elif ev.nGenSUSYLeptons == 1 and ev.nGenSUSYNeutrinos == 2:
								OneGenLeptonNeutrinoEvents += 1
								OneGenLeptonNeutrinoEventsReweighted += 3. * 0.2
								signalEvents +=  3. * 0.2 * ev.weight * ev.sbottomWeight * electronScaleFactors.GetBinContent(electronScaleFactors.GetXaxis().FindBin(ev.pt1),electronScaleFactors.GetYaxis().FindBin(abs(ev.eta1))) * electronScaleFactors.GetBinContent(electronScaleFactors.GetXaxis().FindBin(ev.pt2),electronScaleFactors.GetYaxis().FindBin(abs(ev.eta2)))
							elif ev.nGenSUSYLeptons == 1 and ev.nGenSUSYNeutrinos == 0:
								OneGenLeptonQuarkEvents += 1
								OneGenLeptonQuarkEventsReweighted += 3. * 0.6991
								signalEvents +=  3. * 0.6991 * ev.weight * ev.sbottomWeight * electronScaleFactors.GetBinContent(electronScaleFactors.GetXaxis().FindBin(ev.pt1),electronScaleFactors.GetYaxis().FindBin(abs(ev.eta1))) * electronScaleFactors.GetBinContent(electronScaleFactors.GetXaxis().FindBin(ev.pt2),electronScaleFactors.GetYaxis().FindBin(abs(ev.eta2)))
							#~ elif ev.nGenSUSYLeptons == 2 and ev.nGenSUSYNeutrinos == 0 and ev.nGenSUSYSleptons == 0 and ev.motherPdgId1 != 1000011 and ev.motherPdgId1 != 2000011 and ev.motherPdgId1 != 1000013 and ev.motherPdgId1 != 2000013 and ev.motherPdgId2 != 1000011 and ev.motherPdgId2 != 2000011 and ev.motherPdgId2 != 1000013 and ev.motherPdgId2 != 2000013: 
							elif ev.nGenSUSYLeptons == 2 and ev.nGenSUSYNeutrinos == 0  and ev.motherPdgId1 != 1000011 and ev.motherPdgId1 != 2000011 and ev.motherPdgId1 != 1000013 and ev.motherPdgId1 != 2000013 and ev.motherPdgId2 != 1000011 and ev.motherPdgId2 != 2000011 and ev.motherPdgId2 != 1000013 and ev.motherPdgId2 != 2000013: 
								TwoGenLeptonZQuarkEventsReweighted += 9./2. * 0.1411
								TwoGenLeptonZQuarkEvents += 1
								signalEvents +=  9./2. * 0.1411 * ev.weight * ev.sbottomWeight * electronScaleFactors.GetBinContent(electronScaleFactors.GetXaxis().FindBin(ev.pt1),electronScaleFactors.GetYaxis().FindBin(abs(ev.eta1))) * electronScaleFactors.GetBinContent(electronScaleFactors.GetXaxis().FindBin(ev.pt2),electronScaleFactors.GetYaxis().FindBin(abs(ev.eta2)))
							#~ elif ev.nGenSUSYLeptons == 2 and ev.nGenSUSYNeutrinos == 2 and ev.nGenSUSYSleptons == 0 and ev.motherPdgId1 != 1000011 and ev.motherPdgId1 != 2000011 and ev.motherPdgId1 != 1000013 and ev.motherPdgId1 != 2000013 and ev.motherPdgId2 != 1000011 and ev.motherPdgId2 != 2000011 and ev.motherPdgId2 != 1000013 and ev.motherPdgId2 != 2000013: 
							elif ev.nGenSUSYLeptons == 2 and ev.nGenSUSYNeutrinos == 2  and ev.motherPdgId1 != 1000011 and ev.motherPdgId1 != 2000011 and ev.motherPdgId1 != 1000013 and ev.motherPdgId1 != 2000013 and ev.motherPdgId2 != 1000011 and ev.motherPdgId2 != 2000011 and ev.motherPdgId2 != 1000013 and ev.motherPdgId2 != 2000013: 
								TwoGenLeptonNeutrinoEvents += 1
								TwoGenLeptonNeutrinoEventsReweighted += 9./2. * 0.0404
								signalEvents +=  9./2. * 0.0404 * ev.weight * ev.sbottomWeight * electronScaleFactors.GetBinContent(electronScaleFactors.GetXaxis().FindBin(ev.pt1),electronScaleFactors.GetYaxis().FindBin(abs(ev.eta1))) * electronScaleFactors.GetBinContent(electronScaleFactors.GetXaxis().FindBin(ev.pt2),electronScaleFactors.GetYaxis().FindBin(abs(ev.eta2)))
							elif ev.nGenSUSYLeptons == 2 and ev.nGenSUSYNeutrinos == 0 and (ev.motherPdgId1 == 1000011 or ev.motherPdgId1 == 2000011 or ev.motherPdgId1 == 1000013 or ev.motherPdgId1 == 2000013 or ev.motherPdgId2 == 1000011 or ev.motherPdgId2 == 2000011 or ev.motherPdgId2 == 1000013 or ev.motherPdgId2 == 2000013): 
								signalEvents +=  ev.weight * ev.sbottomWeight * electronScaleFactors.GetBinContent(electronScaleFactors.GetXaxis().FindBin(ev.pt1),electronScaleFactors.GetYaxis().FindBin(abs(ev.eta1))) * electronScaleFactors.GetBinContent(electronScaleFactors.GetXaxis().FindBin(ev.pt2),electronScaleFactors.GetYaxis().FindBin(abs(ev.eta2)))
								TwoGenLeptonSleptonEvents += 1
								TwoGenLeptonSleptonEventsReweighted += 1
				elif etaRegion == "Endcap":
					for ev in tree:
						if ev.chargeProduct < 0 and (((abs(ev.eta1) < 1.4 or abs(ev.eta1) > 1.6) and (abs(ev.eta2) < 1.4 or abs(ev.eta2) > 1.6)) and 1.6 <= max(abs(ev.eta1),abs(ev.eta2))) and ev.pt1 > 20 and ev.pt2 > 20 and ev.inv > mll_lower_Cut and ev.inv < mll_upper_Cut and ((ev.patPFMet > 100 and ev.nJetsSmeared >= 3) or  (ev.patPFMet > 150 and ev.nJetsSmeared >=2)) and abs(ev.eta1) < 2.4 and abs(ev.eta2) < 2.4 and ev.deltaR > 0.3:
							MCEvents +=1
							if ev.nGenSUSYLeptons == 4:
								FourGenLeptonEvents += 1
								FourGenLeptonEventsReweighted += 9*0.0102 
								signalEvents += 9*0.0102 * ev.weight * ev.sbottomWeight * electronScaleFactors.GetBinContent(electronScaleFactors.GetXaxis().FindBin(ev.pt1),electronScaleFactors.GetYaxis().FindBin(abs(ev.eta1))) * electronScaleFactors.GetBinContent(electronScaleFactors.GetXaxis().FindBin(ev.pt2),electronScaleFactors.GetYaxis().FindBin(abs(ev.eta2)))
							elif ev.nGenSUSYLeptons == 3:
								ThreeGenLeptonEvents += 1
								ThreeGenLeptonEventsReweighted += 3. * 0.101
								signalEvents += 3. * 0.101 * ev.weight * ev.sbottomWeight * electronScaleFactors.GetBinContent(electronScaleFactors.GetXaxis().FindBin(ev.pt1),electronScaleFactors.GetYaxis().FindBin(abs(ev.eta1))) * electronScaleFactors.GetBinContent(electronScaleFactors.GetXaxis().FindBin(ev.pt2),electronScaleFactors.GetYaxis().FindBin(abs(ev.eta2)))
							elif ev.nGenSUSYLeptons == 1 and ev.nGenSUSYNeutrinos == 2:
								OneGenLeptonNeutrinoEvents += 1
								OneGenLeptonNeutrinoEventsReweighted += 3. * 0.2
								signalEvents +=  3. * 0.2 * ev.weight * ev.sbottomWeight * electronScaleFactors.GetBinContent(electronScaleFactors.GetXaxis().FindBin(ev.pt1),electronScaleFactors.GetYaxis().FindBin(abs(ev.eta1))) * electronScaleFactors.GetBinContent(electronScaleFactors.GetXaxis().FindBin(ev.pt2),electronScaleFactors.GetYaxis().FindBin(abs(ev.eta2)))
							elif ev.nGenSUSYLeptons == 1 and ev.nGenSUSYNeutrinos == 0:
								OneGenLeptonQuarkEvents += 1
								OneGenLeptonQuarkEventsReweighted += 3. * 0.6991
								signalEvents +=  3. * 0.6991 * ev.weight * ev.sbottomWeight * electronScaleFactors.GetBinContent(electronScaleFactors.GetXaxis().FindBin(ev.pt1),electronScaleFactors.GetYaxis().FindBin(abs(ev.eta1))) * electronScaleFactors.GetBinContent(electronScaleFactors.GetXaxis().FindBin(ev.pt2),electronScaleFactors.GetYaxis().FindBin(abs(ev.eta2)))
							#~ elif ev.nGenSUSYLeptons == 2 and ev.nGenSUSYNeutrinos == 0 and ev.nGenSUSYSleptons == 0 and ev.motherPdgId1 != 1000011 and ev.motherPdgId1 != 2000011 and ev.motherPdgId1 != 1000013 and ev.motherPdgId1 != 2000013 and ev.motherPdgId2 != 1000011 and ev.motherPdgId2 != 2000011 and ev.motherPdgId2 != 1000013 and ev.motherPdgId2 != 2000013: 
							elif ev.nGenSUSYLeptons == 2 and ev.nGenSUSYNeutrinos == 0  and ev.motherPdgId1 != 1000011 and ev.motherPdgId1 != 2000011 and ev.motherPdgId1 != 1000013 and ev.motherPdgId1 != 2000013 and ev.motherPdgId2 != 1000011 and ev.motherPdgId2 != 2000011 and ev.motherPdgId2 != 1000013 and ev.motherPdgId2 != 2000013: 
								TwoGenLeptonZQuarkEventsReweighted += 9./2. * 0.1411
								TwoGenLeptonZQuarkEvents += 1
								signalEvents +=  9./2. * 0.1411 * ev.weight * ev.sbottomWeight * electronScaleFactors.GetBinContent(electronScaleFactors.GetXaxis().FindBin(ev.pt1),electronScaleFactors.GetYaxis().FindBin(abs(ev.eta1))) * electronScaleFactors.GetBinContent(electronScaleFactors.GetXaxis().FindBin(ev.pt2),electronScaleFactors.GetYaxis().FindBin(abs(ev.eta2)))
							#~ elif ev.nGenSUSYLeptons == 2 and ev.nGenSUSYNeutrinos == 2 and ev.nGenSUSYSleptons == 0 and ev.motherPdgId1 != 1000011 and ev.motherPdgId1 != 2000011 and ev.motherPdgId1 != 1000013 and ev.motherPdgId1 != 2000013 and ev.motherPdgId2 != 1000011 and ev.motherPdgId2 != 2000011 and ev.motherPdgId2 != 1000013 and ev.motherPdgId2 != 2000013: 
							elif ev.nGenSUSYLeptons == 2 and ev.nGenSUSYNeutrinos == 2  and ev.motherPdgId1 != 1000011 and ev.motherPdgId1 != 2000011 and ev.motherPdgId1 != 1000013 and ev.motherPdgId1 != 2000013 and ev.motherPdgId2 != 1000011 and ev.motherPdgId2 != 2000011 and ev.motherPdgId2 != 1000013 and ev.motherPdgId2 != 2000013: 
								TwoGenLeptonNeutrinoEvents += 1
								TwoGenLeptonNeutrinoEventsReweighted += 9./2. * 0.0404
								signalEvents +=  9./2. * 0.0404 * ev.weight * ev.sbottomWeight * electronScaleFactors.GetBinContent(electronScaleFactors.GetXaxis().FindBin(ev.pt1),electronScaleFactors.GetYaxis().FindBin(abs(ev.eta1))) * electronScaleFactors.GetBinContent(electronScaleFactors.GetXaxis().FindBin(ev.pt2),electronScaleFactors.GetYaxis().FindBin(abs(ev.eta2)))
							elif ev.nGenSUSYLeptons == 2 and ev.nGenSUSYNeutrinos == 0 and (ev.motherPdgId1 == 1000011 or ev.motherPdgId1 == 2000011 or ev.motherPdgId1 == 1000013 or ev.motherPdgId1 == 2000013 or ev.motherPdgId2 == 1000011 or ev.motherPdgId2 == 2000011 or ev.motherPdgId2 == 1000013 or ev.motherPdgId2 == 2000013): 
								signalEvents +=  ev.weight * ev.sbottomWeight * electronScaleFactors.GetBinContent(electronScaleFactors.GetXaxis().FindBin(ev.pt1),electronScaleFactors.GetYaxis().FindBin(abs(ev.eta1))) * electronScaleFactors.GetBinContent(electronScaleFactors.GetXaxis().FindBin(ev.pt2),electronScaleFactors.GetYaxis().FindBin(abs(ev.eta2)))
								TwoGenLeptonSleptonEvents += 1
								TwoGenLeptonSleptonEventsReweighted += 1
			elif dilepton == "MuMu":
				if etaRegion == "Barrel":
					for ev in tree:
						if ev.chargeProduct < 0 and abs(ev.eta1) < 1.4 and abs(ev.eta2) < 1.4 and ev.pt1 > 20 and ev.pt2 > 20 and ev.inv > mll_lower_Cut and ev.inv < mll_upper_Cut and ((ev.patPFMet > 100 and ev.nJetsSmeared >= 3) or  (ev.patPFMet > 150 and ev.nJetsSmeared >=2)) and abs(ev.eta1) < 2.4 and abs(ev.eta2) < 2.4 and ev.deltaR > 0.3:
							MCEvents +=1
							if ev.nGenSUSYLeptons == 4:
								FourGenLeptonEvents += 1
								FourGenLeptonEventsReweighted += 9*0.0102 
								signalEvents += 9*0.0102 * ev.weight * ev.sbottomWeight * electronScaleFactors.GetBinContent(electronScaleFactors.GetXaxis().FindBin(ev.pt1),electronScaleFactors.GetYaxis().FindBin(abs(ev.eta1))) * electronScaleFactors.GetBinContent(electronScaleFactors.GetXaxis().FindBin(ev.pt2),electronScaleFactors.GetYaxis().FindBin(abs(ev.eta2)))
							elif ev.nGenSUSYLeptons == 3:
								ThreeGenLeptonEvents += 1
								ThreeGenLeptonEventsReweighted += 3. * 0.101
								signalEvents += 3. * 0.101 * ev.weight * ev.sbottomWeight * electronScaleFactors.GetBinContent(electronScaleFactors.GetXaxis().FindBin(ev.pt1),electronScaleFactors.GetYaxis().FindBin(abs(ev.eta1))) * electronScaleFactors.GetBinContent(electronScaleFactors.GetXaxis().FindBin(ev.pt2),electronScaleFactors.GetYaxis().FindBin(abs(ev.eta2)))
							elif ev.nGenSUSYLeptons == 1 and ev.nGenSUSYNeutrinos == 2:
								OneGenLeptonNeutrinoEvents += 1
								OneGenLeptonNeutrinoEventsReweighted += 3. * 0.2
								signalEvents +=  3. * 0.2 * ev.weight * ev.sbottomWeight * electronScaleFactors.GetBinContent(electronScaleFactors.GetXaxis().FindBin(ev.pt1),electronScaleFactors.GetYaxis().FindBin(abs(ev.eta1))) * electronScaleFactors.GetBinContent(electronScaleFactors.GetXaxis().FindBin(ev.pt2),electronScaleFactors.GetYaxis().FindBin(abs(ev.eta2)))
							elif ev.nGenSUSYLeptons == 1 and ev.nGenSUSYNeutrinos == 0:
								OneGenLeptonQuarkEvents += 1
								OneGenLeptonQuarkEventsReweighted += 3. * 0.6991
								signalEvents +=  3. * 0.6991 * ev.weight * ev.sbottomWeight * electronScaleFactors.GetBinContent(electronScaleFactors.GetXaxis().FindBin(ev.pt1),electronScaleFactors.GetYaxis().FindBin(abs(ev.eta1))) * electronScaleFactors.GetBinContent(electronScaleFactors.GetXaxis().FindBin(ev.pt2),electronScaleFactors.GetYaxis().FindBin(abs(ev.eta2)))
							#~ elif ev.nGenSUSYLeptons == 2 and ev.nGenSUSYNeutrinos == 0 and ev.nGenSUSYSleptons == 0 and ev.motherPdgId1 != 1000011 and ev.motherPdgId1 != 2000011 and ev.motherPdgId1 != 1000013 and ev.motherPdgId1 != 2000013 and ev.motherPdgId2 != 1000011 and ev.motherPdgId2 != 2000011 and ev.motherPdgId2 != 1000013 and ev.motherPdgId2 != 2000013: 
							elif ev.nGenSUSYLeptons == 2 and ev.nGenSUSYNeutrinos == 0  and ev.motherPdgId1 != 1000011 and ev.motherPdgId1 != 2000011 and ev.motherPdgId1 != 1000013 and ev.motherPdgId1 != 2000013 and ev.motherPdgId2 != 1000011 and ev.motherPdgId2 != 2000011 and ev.motherPdgId2 != 1000013 and ev.motherPdgId2 != 2000013: 
								TwoGenLeptonZQuarkEventsReweighted += 9./2. * 0.1411
								TwoGenLeptonZQuarkEvents += 1
								signalEvents +=  9./2. * 0.1411 * ev.weight * ev.sbottomWeight * electronScaleFactors.GetBinContent(electronScaleFactors.GetXaxis().FindBin(ev.pt1),electronScaleFactors.GetYaxis().FindBin(abs(ev.eta1))) * electronScaleFactors.GetBinContent(electronScaleFactors.GetXaxis().FindBin(ev.pt2),electronScaleFactors.GetYaxis().FindBin(abs(ev.eta2)))
							#~ elif ev.nGenSUSYLeptons == 2 and ev.nGenSUSYNeutrinos == 2 and ev.nGenSUSYSleptons == 0 and ev.motherPdgId1 != 1000011 and ev.motherPdgId1 != 2000011 and ev.motherPdgId1 != 1000013 and ev.motherPdgId1 != 2000013 and ev.motherPdgId2 != 1000011 and ev.motherPdgId2 != 2000011 and ev.motherPdgId2 != 1000013 and ev.motherPdgId2 != 2000013: 
							elif ev.nGenSUSYLeptons == 2 and ev.nGenSUSYNeutrinos == 2  and ev.motherPdgId1 != 1000011 and ev.motherPdgId1 != 2000011 and ev.motherPdgId1 != 1000013 and ev.motherPdgId1 != 2000013 and ev.motherPdgId2 != 1000011 and ev.motherPdgId2 != 2000011 and ev.motherPdgId2 != 1000013 and ev.motherPdgId2 != 2000013: 
								TwoGenLeptonNeutrinoEvents += 1
								TwoGenLeptonNeutrinoEventsReweighted += 9./2. * 0.0404
								signalEvents +=  9./2. * 0.0404 * ev.weight * ev.sbottomWeight * electronScaleFactors.GetBinContent(electronScaleFactors.GetXaxis().FindBin(ev.pt1),electronScaleFactors.GetYaxis().FindBin(abs(ev.eta1))) * electronScaleFactors.GetBinContent(electronScaleFactors.GetXaxis().FindBin(ev.pt2),electronScaleFactors.GetYaxis().FindBin(abs(ev.eta2)))
							elif ev.nGenSUSYLeptons == 2 and ev.nGenSUSYNeutrinos == 0 and (ev.motherPdgId1 == 1000011 or ev.motherPdgId1 == 2000011 or ev.motherPdgId1 == 1000013 or ev.motherPdgId1 == 2000013 or ev.motherPdgId2 == 1000011 or ev.motherPdgId2 == 2000011 or ev.motherPdgId2 == 1000013 or ev.motherPdgId2 == 2000013): 
								signalEvents +=  ev.weight * ev.sbottomWeight * electronScaleFactors.GetBinContent(electronScaleFactors.GetXaxis().FindBin(ev.pt1),electronScaleFactors.GetYaxis().FindBin(abs(ev.eta1))) * electronScaleFactors.GetBinContent(electronScaleFactors.GetXaxis().FindBin(ev.pt2),electronScaleFactors.GetYaxis().FindBin(abs(ev.eta2)))
								TwoGenLeptonSleptonEvents += 1
								TwoGenLeptonSleptonEventsReweighted += 1
				elif etaRegion == "Endcap":
					for ev in tree:
						if ev.chargeProduct < 0 and (((abs(ev.eta1) < 1.4 or abs(ev.eta1) > 1.6) and (abs(ev.eta2) < 1.4 or abs(ev.eta2) > 1.6)) and 1.6 <= max(abs(ev.eta1),abs(ev.eta2))) and ev.pt1 > 20 and ev.pt2 > 20 and ev.inv > mll_lower_Cut and ev.inv < mll_upper_Cut and ((ev.patPFMet > 100 and ev.nJetsSmeared >= 3) or  (ev.patPFMet > 150 and ev.nJetsSmeared >=2)) and abs(ev.eta1) < 2.4 and abs(ev.eta2) < 2.4 and ev.deltaR > 0.3:
							MCEvents +=1
							if ev.nGenSUSYLeptons == 4:
								FourGenLeptonEvents += 1
								FourGenLeptonEventsReweighted += 9*0.0102 
								signalEvents += 9*0.0102 * ev.weight * ev.sbottomWeight * electronScaleFactors.GetBinContent(electronScaleFactors.GetXaxis().FindBin(ev.pt1),electronScaleFactors.GetYaxis().FindBin(abs(ev.eta1))) * electronScaleFactors.GetBinContent(electronScaleFactors.GetXaxis().FindBin(ev.pt2),electronScaleFactors.GetYaxis().FindBin(abs(ev.eta2)))
							elif ev.nGenSUSYLeptons == 3:
								ThreeGenLeptonEvents += 1
								ThreeGenLeptonEventsReweighted += 3. * 0.101
								signalEvents += 3. * 0.101 * ev.weight * ev.sbottomWeight * electronScaleFactors.GetBinContent(electronScaleFactors.GetXaxis().FindBin(ev.pt1),electronScaleFactors.GetYaxis().FindBin(abs(ev.eta1))) * electronScaleFactors.GetBinContent(electronScaleFactors.GetXaxis().FindBin(ev.pt2),electronScaleFactors.GetYaxis().FindBin(abs(ev.eta2)))
							elif ev.nGenSUSYLeptons == 1 and ev.nGenSUSYNeutrinos == 2:
								OneGenLeptonNeutrinoEvents += 1
								OneGenLeptonNeutrinoEventsReweighted += 3. * 0.2
								signalEvents +=  3. * 0.2 * ev.weight * ev.sbottomWeight * electronScaleFactors.GetBinContent(electronScaleFactors.GetXaxis().FindBin(ev.pt1),electronScaleFactors.GetYaxis().FindBin(abs(ev.eta1))) * electronScaleFactors.GetBinContent(electronScaleFactors.GetXaxis().FindBin(ev.pt2),electronScaleFactors.GetYaxis().FindBin(abs(ev.eta2)))
							elif ev.nGenSUSYLeptons == 1 and ev.nGenSUSYNeutrinos == 0:
								OneGenLeptonQuarkEvents += 1
								OneGenLeptonQuarkEventsReweighted += 3. * 0.6991
								signalEvents +=  3. * 0.6991 * ev.weight * ev.sbottomWeight * electronScaleFactors.GetBinContent(electronScaleFactors.GetXaxis().FindBin(ev.pt1),electronScaleFactors.GetYaxis().FindBin(abs(ev.eta1))) * electronScaleFactors.GetBinContent(electronScaleFactors.GetXaxis().FindBin(ev.pt2),electronScaleFactors.GetYaxis().FindBin(abs(ev.eta2)))
							#~ elif ev.nGenSUSYLeptons == 2 and ev.nGenSUSYNeutrinos == 0 and ev.nGenSUSYSleptons == 0 and ev.motherPdgId1 != 1000011 and ev.motherPdgId1 != 2000011 and ev.motherPdgId1 != 1000013 and ev.motherPdgId1 != 2000013 and ev.motherPdgId2 != 1000011 and ev.motherPdgId2 != 2000011 and ev.motherPdgId2 != 1000013 and ev.motherPdgId2 != 2000013: 
							elif ev.nGenSUSYLeptons == 2 and ev.nGenSUSYNeutrinos == 0  and ev.motherPdgId1 != 1000011 and ev.motherPdgId1 != 2000011 and ev.motherPdgId1 != 1000013 and ev.motherPdgId1 != 2000013 and ev.motherPdgId2 != 1000011 and ev.motherPdgId2 != 2000011 and ev.motherPdgId2 != 1000013 and ev.motherPdgId2 != 2000013: 
								TwoGenLeptonZQuarkEventsReweighted += 9./2. * 0.1411
								TwoGenLeptonZQuarkEvents += 1
								signalEvents +=  9./2. * 0.1411 * ev.weight * ev.sbottomWeight * electronScaleFactors.GetBinContent(electronScaleFactors.GetXaxis().FindBin(ev.pt1),electronScaleFactors.GetYaxis().FindBin(abs(ev.eta1))) * electronScaleFactors.GetBinContent(electronScaleFactors.GetXaxis().FindBin(ev.pt2),electronScaleFactors.GetYaxis().FindBin(abs(ev.eta2)))
							#~ elif ev.nGenSUSYLeptons == 2 and ev.nGenSUSYNeutrinos == 2 and ev.nGenSUSYSleptons == 0 and ev.motherPdgId1 != 1000011 and ev.motherPdgId1 != 2000011 and ev.motherPdgId1 != 1000013 and ev.motherPdgId1 != 2000013 and ev.motherPdgId2 != 1000011 and ev.motherPdgId2 != 2000011 and ev.motherPdgId2 != 1000013 and ev.motherPdgId2 != 2000013: 
							elif ev.nGenSUSYLeptons == 2 and ev.nGenSUSYNeutrinos == 2  and ev.motherPdgId1 != 1000011 and ev.motherPdgId1 != 2000011 and ev.motherPdgId1 != 1000013 and ev.motherPdgId1 != 2000013 and ev.motherPdgId2 != 1000011 and ev.motherPdgId2 != 2000011 and ev.motherPdgId2 != 1000013 and ev.motherPdgId2 != 2000013: 
								TwoGenLeptonNeutrinoEvents += 1
								TwoGenLeptonNeutrinoEventsReweighted += 9./2. * 0.0404
								signalEvents +=  9./2. * 0.0404 * ev.weight * ev.sbottomWeight * electronScaleFactors.GetBinContent(electronScaleFactors.GetXaxis().FindBin(ev.pt1),electronScaleFactors.GetYaxis().FindBin(abs(ev.eta1))) * electronScaleFactors.GetBinContent(electronScaleFactors.GetXaxis().FindBin(ev.pt2),electronScaleFactors.GetYaxis().FindBin(abs(ev.eta2)))
							elif ev.nGenSUSYLeptons == 2 and ev.nGenSUSYNeutrinos == 0 and (ev.motherPdgId1 == 1000011 or ev.motherPdgId1 == 2000011 or ev.motherPdgId1 == 1000013 or ev.motherPdgId1 == 2000013 or ev.motherPdgId2 == 1000011 or ev.motherPdgId2 == 2000011 or ev.motherPdgId2 == 1000013 or ev.motherPdgId2 == 2000013): 
								signalEvents +=  ev.weight * ev.sbottomWeight * electronScaleFactors.GetBinContent(electronScaleFactors.GetXaxis().FindBin(ev.pt1),electronScaleFactors.GetYaxis().FindBin(abs(ev.eta1))) * electronScaleFactors.GetBinContent(electronScaleFactors.GetXaxis().FindBin(ev.pt2),electronScaleFactors.GetYaxis().FindBin(abs(ev.eta2)))
								TwoGenLeptonSleptonEvents += 1
								TwoGenLeptonSleptonEventsReweighted += 1
			elif dilepton == "EMu":
				if etaRegion == "Barrel":
					for ev in tree:
						if ev.chargeProduct < 0 and abs(ev.eta1) < 1.4 and abs(ev.eta2) < 1.4 and ev.pt1 > 20 and ev.pt2 > 20 and ev.inv > mll_lower_Cut and ev.inv < mll_upper_Cut and ((ev.patPFMet > 100 and ev.nJetsSmeared >= 3) or  (ev.patPFMet > 150 and ev.nJetsSmeared >=2)) and abs(ev.eta1) < 2.4 and abs(ev.eta2) < 2.4 and ev.deltaR > 0.3:
							MCEvents +=1
							if ev.nGenSUSYLeptons == 4:
								FourGenLeptonEvents += 1
								FourGenLeptonEventsReweighted += 9*0.0102 
								signalEvents += 9*0.0102 * ev.weight * ev.sbottomWeight * electronScaleFactors.GetBinContent(electronScaleFactors.GetXaxis().FindBin(ev.pt1),electronScaleFactors.GetYaxis().FindBin(abs(ev.eta1))) * electronScaleFactors.GetBinContent(electronScaleFactors.GetXaxis().FindBin(ev.pt2),electronScaleFactors.GetYaxis().FindBin(abs(ev.eta2)))
							elif ev.nGenSUSYLeptons == 3:
								ThreeGenLeptonEvents += 1
								ThreeGenLeptonEventsReweighted += 3. * 0.101
								signalEvents += 3. * 0.101 * ev.weight * ev.sbottomWeight * electronScaleFactors.GetBinContent(electronScaleFactors.GetXaxis().FindBin(ev.pt1),electronScaleFactors.GetYaxis().FindBin(abs(ev.eta1))) * electronScaleFactors.GetBinContent(electronScaleFactors.GetXaxis().FindBin(ev.pt2),electronScaleFactors.GetYaxis().FindBin(abs(ev.eta2)))
							elif ev.nGenSUSYLeptons == 1 and ev.nGenSUSYNeutrinos == 2:
								OneGenLeptonNeutrinoEvents += 1
								OneGenLeptonNeutrinoEventsReweighted += 3. * 0.2
								signalEvents +=  3. * 0.2 * ev.weight * ev.sbottomWeight * electronScaleFactors.GetBinContent(electronScaleFactors.GetXaxis().FindBin(ev.pt1),electronScaleFactors.GetYaxis().FindBin(abs(ev.eta1))) * electronScaleFactors.GetBinContent(electronScaleFactors.GetXaxis().FindBin(ev.pt2),electronScaleFactors.GetYaxis().FindBin(abs(ev.eta2)))
							elif ev.nGenSUSYLeptons == 1 and ev.nGenSUSYNeutrinos == 0:
								OneGenLeptonQuarkEvents += 1
								OneGenLeptonQuarkEventsReweighted += 3. * 0.6991
								signalEvents +=  3. * 0.6991 * ev.weight * ev.sbottomWeight * electronScaleFactors.GetBinContent(electronScaleFactors.GetXaxis().FindBin(ev.pt1),electronScaleFactors.GetYaxis().FindBin(abs(ev.eta1))) * electronScaleFactors.GetBinContent(electronScaleFactors.GetXaxis().FindBin(ev.pt2),electronScaleFactors.GetYaxis().FindBin(abs(ev.eta2)))
							#~ elif ev.nGenSUSYLeptons == 2 and ev.nGenSUSYNeutrinos == 0 and ev.nGenSUSYSleptons == 0 and ev.motherPdgId1 != 1000011 and ev.motherPdgId1 != 2000011 and ev.motherPdgId1 != 1000013 and ev.motherPdgId1 != 2000013 and ev.motherPdgId2 != 1000011 and ev.motherPdgId2 != 2000011 and ev.motherPdgId2 != 1000013 and ev.motherPdgId2 != 2000013: 
							elif ev.nGenSUSYLeptons == 2 and ev.nGenSUSYNeutrinos == 0  and ev.motherPdgId1 != 1000011 and ev.motherPdgId1 != 2000011 and ev.motherPdgId1 != 1000013 and ev.motherPdgId1 != 2000013 and ev.motherPdgId2 != 1000011 and ev.motherPdgId2 != 2000011 and ev.motherPdgId2 != 1000013 and ev.motherPdgId2 != 2000013: 
								TwoGenLeptonZQuarkEventsReweighted += 9./2. * 0.1411
								TwoGenLeptonZQuarkEvents += 1
								signalEvents +=  9./2. * 0.1411 * ev.weight * ev.sbottomWeight * electronScaleFactors.GetBinContent(electronScaleFactors.GetXaxis().FindBin(ev.pt1),electronScaleFactors.GetYaxis().FindBin(abs(ev.eta1))) * electronScaleFactors.GetBinContent(electronScaleFactors.GetXaxis().FindBin(ev.pt2),electronScaleFactors.GetYaxis().FindBin(abs(ev.eta2)))
							#~ elif ev.nGenSUSYLeptons == 2 and ev.nGenSUSYNeutrinos == 2 and ev.nGenSUSYSleptons == 0 and ev.motherPdgId1 != 1000011 and ev.motherPdgId1 != 2000011 and ev.motherPdgId1 != 1000013 and ev.motherPdgId1 != 2000013 and ev.motherPdgId2 != 1000011 and ev.motherPdgId2 != 2000011 and ev.motherPdgId2 != 1000013 and ev.motherPdgId2 != 2000013: 
							elif ev.nGenSUSYLeptons == 2 and ev.nGenSUSYNeutrinos == 2  and ev.motherPdgId1 != 1000011 and ev.motherPdgId1 != 2000011 and ev.motherPdgId1 != 1000013 and ev.motherPdgId1 != 2000013 and ev.motherPdgId2 != 1000011 and ev.motherPdgId2 != 2000011 and ev.motherPdgId2 != 1000013 and ev.motherPdgId2 != 2000013: 
								TwoGenLeptonNeutrinoEvents += 1
								TwoGenLeptonNeutrinoEventsReweighted += 9./2. * 0.0404
								signalEvents +=  9./2. * 0.0404 * ev.weight * ev.sbottomWeight * electronScaleFactors.GetBinContent(electronScaleFactors.GetXaxis().FindBin(ev.pt1),electronScaleFactors.GetYaxis().FindBin(abs(ev.eta1))) * electronScaleFactors.GetBinContent(electronScaleFactors.GetXaxis().FindBin(ev.pt2),electronScaleFactors.GetYaxis().FindBin(abs(ev.eta2)))
							elif ev.nGenSUSYLeptons == 2 and ev.nGenSUSYNeutrinos == 0 and (ev.motherPdgId1 == 1000011 or ev.motherPdgId1 == 2000011 or ev.motherPdgId1 == 1000013 or ev.motherPdgId1 == 2000013 or ev.motherPdgId2 == 1000011 or ev.motherPdgId2 == 2000011 or ev.motherPdgId2 == 1000013 or ev.motherPdgId2 == 2000013): 
								signalEvents +=  ev.weight * ev.sbottomWeight * electronScaleFactors.GetBinContent(electronScaleFactors.GetXaxis().FindBin(ev.pt1),electronScaleFactors.GetYaxis().FindBin(abs(ev.eta1))) * electronScaleFactors.GetBinContent(electronScaleFactors.GetXaxis().FindBin(ev.pt2),electronScaleFactors.GetYaxis().FindBin(abs(ev.eta2)))
								TwoGenLeptonSleptonEvents += 1
								TwoGenLeptonSleptonEventsReweighted += 1
				elif etaRegion == "Endcap":
					for ev in tree:
						if ev.chargeProduct < 0 and (((abs(ev.eta1) < 1.4 or abs(ev.eta1) > 1.6) and (abs(ev.eta2) < 1.4 or abs(ev.eta2) > 1.6)) and 1.6 <= max(abs(ev.eta1),abs(ev.eta2))) and ev.pt1 > 20 and ev.pt2 > 20 and ev.inv > mll_lower_Cut and ev.inv < mll_upper_Cut and ((ev.patPFMet > 100 and ev.nJetsSmeared >= 3) or  (ev.patPFMet > 150 and ev.nJetsSmeared >=2)) and abs(ev.eta1) < 2.4 and abs(ev.eta2) < 2.4 and ev.deltaR > 0.3:
							MCEvents +=1
							if ev.nGenSUSYLeptons == 4:
								FourGenLeptonEvents += 1
								FourGenLeptonEventsReweighted += 9*0.0102 
								signalEvents += 9*0.0102 * ev.weight * ev.sbottomWeight * electronScaleFactors.GetBinContent(electronScaleFactors.GetXaxis().FindBin(ev.pt1),electronScaleFactors.GetYaxis().FindBin(abs(ev.eta1))) * electronScaleFactors.GetBinContent(electronScaleFactors.GetXaxis().FindBin(ev.pt2),electronScaleFactors.GetYaxis().FindBin(abs(ev.eta2)))
							elif ev.nGenSUSYLeptons == 3:
								ThreeGenLeptonEvents += 1
								ThreeGenLeptonEventsReweighted += 3. * 0.101
								signalEvents += 3. * 0.101 * ev.weight * ev.sbottomWeight * electronScaleFactors.GetBinContent(electronScaleFactors.GetXaxis().FindBin(ev.pt1),electronScaleFactors.GetYaxis().FindBin(abs(ev.eta1))) * electronScaleFactors.GetBinContent(electronScaleFactors.GetXaxis().FindBin(ev.pt2),electronScaleFactors.GetYaxis().FindBin(abs(ev.eta2)))
							elif ev.nGenSUSYLeptons == 1 and ev.nGenSUSYNeutrinos == 2:
								OneGenLeptonNeutrinoEvents += 1
								OneGenLeptonNeutrinoEventsReweighted += 3. * 0.2
								signalEvents +=  3. * 0.2 * ev.weight * ev.sbottomWeight * electronScaleFactors.GetBinContent(electronScaleFactors.GetXaxis().FindBin(ev.pt1),electronScaleFactors.GetYaxis().FindBin(abs(ev.eta1))) * electronScaleFactors.GetBinContent(electronScaleFactors.GetXaxis().FindBin(ev.pt2),electronScaleFactors.GetYaxis().FindBin(abs(ev.eta2)))
							elif ev.nGenSUSYLeptons == 1 and ev.nGenSUSYNeutrinos == 0:
								OneGenLeptonQuarkEvents += 1
								OneGenLeptonQuarkEventsReweighted += 3. * 0.6991
								signalEvents +=  3. * 0.6991 * ev.weight * ev.sbottomWeight * electronScaleFactors.GetBinContent(electronScaleFactors.GetXaxis().FindBin(ev.pt1),electronScaleFactors.GetYaxis().FindBin(abs(ev.eta1))) * electronScaleFactors.GetBinContent(electronScaleFactors.GetXaxis().FindBin(ev.pt2),electronScaleFactors.GetYaxis().FindBin(abs(ev.eta2)))
							#~ elif ev.nGenSUSYLeptons == 2 and ev.nGenSUSYNeutrinos == 0 and ev.nGenSUSYSleptons == 0 and ev.motherPdgId1 != 1000011 and ev.motherPdgId1 != 2000011 and ev.motherPdgId1 != 1000013 and ev.motherPdgId1 != 2000013 and ev.motherPdgId2 != 1000011 and ev.motherPdgId2 != 2000011 and ev.motherPdgId2 != 1000013 and ev.motherPdgId2 != 2000013: 
							elif ev.nGenSUSYLeptons == 2 and ev.nGenSUSYNeutrinos == 0  and ev.motherPdgId1 != 1000011 and ev.motherPdgId1 != 2000011 and ev.motherPdgId1 != 1000013 and ev.motherPdgId1 != 2000013 and ev.motherPdgId2 != 1000011 and ev.motherPdgId2 != 2000011 and ev.motherPdgId2 != 1000013 and ev.motherPdgId2 != 2000013: 
								TwoGenLeptonZQuarkEventsReweighted += 9./2. * 0.1411
								TwoGenLeptonZQuarkEvents += 1
								signalEvents +=  9./2. * 0.1411 * ev.weight * ev.sbottomWeight * electronScaleFactors.GetBinContent(electronScaleFactors.GetXaxis().FindBin(ev.pt1),electronScaleFactors.GetYaxis().FindBin(abs(ev.eta1))) * electronScaleFactors.GetBinContent(electronScaleFactors.GetXaxis().FindBin(ev.pt2),electronScaleFactors.GetYaxis().FindBin(abs(ev.eta2)))
							#~ elif ev.nGenSUSYLeptons == 2 and ev.nGenSUSYNeutrinos == 2 and ev.nGenSUSYSleptons == 0 and ev.motherPdgId1 != 1000011 and ev.motherPdgId1 != 2000011 and ev.motherPdgId1 != 1000013 and ev.motherPdgId1 != 2000013 and ev.motherPdgId2 != 1000011 and ev.motherPdgId2 != 2000011 and ev.motherPdgId2 != 1000013 and ev.motherPdgId2 != 2000013: 
							elif ev.nGenSUSYLeptons == 2 and ev.nGenSUSYNeutrinos == 2  and ev.motherPdgId1 != 1000011 and ev.motherPdgId1 != 2000011 and ev.motherPdgId1 != 1000013 and ev.motherPdgId1 != 2000013 and ev.motherPdgId2 != 1000011 and ev.motherPdgId2 != 2000011 and ev.motherPdgId2 != 1000013 and ev.motherPdgId2 != 2000013: 
								TwoGenLeptonNeutrinoEvents += 1
								TwoGenLeptonNeutrinoEventsReweighted += 9./2. * 0.0404
								signalEvents +=  9./2. * 0.0404 * ev.weight * ev.sbottomWeight * electronScaleFactors.GetBinContent(electronScaleFactors.GetXaxis().FindBin(ev.pt1),electronScaleFactors.GetYaxis().FindBin(abs(ev.eta1))) * electronScaleFactors.GetBinContent(electronScaleFactors.GetXaxis().FindBin(ev.pt2),electronScaleFactors.GetYaxis().FindBin(abs(ev.eta2)))
							elif ev.nGenSUSYLeptons == 2 and ev.nGenSUSYNeutrinos == 0 and (ev.motherPdgId1 == 1000011 or ev.motherPdgId1 == 2000011 or ev.motherPdgId1 == 1000013 or ev.motherPdgId1 == 2000013 or ev.motherPdgId2 == 1000011 or ev.motherPdgId2 == 2000011 or ev.motherPdgId2 == 1000013 or ev.motherPdgId2 == 2000013): 
								signalEvents +=  ev.weight * ev.sbottomWeight * electronScaleFactors.GetBinContent(electronScaleFactors.GetXaxis().FindBin(ev.pt1),electronScaleFactors.GetYaxis().FindBin(abs(ev.eta1))) * electronScaleFactors.GetBinContent(electronScaleFactors.GetXaxis().FindBin(ev.pt2),electronScaleFactors.GetYaxis().FindBin(abs(ev.eta2)))
								TwoGenLeptonSleptonEvents += 1
								TwoGenLeptonSleptonEventsReweighted += 1
	
	#~ print "ZZ to 4l Events: "+str(FourGenLeptonEvents)
	#~ print "ZZ to 4l Events Reweighted: "+str(FourGenLeptonEventsReweighted)
	#~ print "Slepton + Z to 2l Events: "+str(ThreeGenLeptonEvents)
	#~ print "Slepton + Z to 2l Events Reweighted: "+str(ThreeGenLeptonEventsReweighted)
	#~ print "Slepton + Z to 2nu Events: "+str(OneGenLeptonNeutrinoEvents)
	#~ print "Slepton + Z to 2nu EventsReweighted: "+str(OneGenLeptonNeutrinoEventsReweighted)
	#~ print "Slepton + Z to 2q Events: "+str(OneGenLeptonQuarkEvents)
	#~ print "Slepton + Z to 2q EventsReweighted: "+str(OneGenLeptonQuarkEventsReweighted)
	#~ print "Z to 2l + Z to 2q Events: "+str(TwoGenLeptonZQuarkEvents)
	#~ print "Z to 2l + Z to 2q EventsReweighted: "+str(TwoGenLeptonZQuarkEventsReweighted)
	#~ print "Z to 2l + Z to 2nu Events: "+str(TwoGenLeptonNeutrinoEvents)
	#~ print "Z to 2l + Z to 2nu EventsReweighted: "+str(TwoGenLeptonNeutrinoEventsReweighted)
	#~ print "2 Slepton Events: "+str(TwoGenLeptonSleptonEvents)
	return signalEvents, MCEvents
	
def signalYields(tree,cuts,scalingLumi,dilepton):
	histo = createHistoFromTree(tree, "p4.M()", cuts, 300, 0, 300)
	histo.Scale(scalingLumi)
	yields = float(histo.Integral())
	return yields
			
def produceSignalEfficiency(tree,cuts,weight,dilepton):
	yields = [float(createHistoFromTree(tree, "p4.M()", cuts, 300, 0, 300).Integral())]
	result = yields[0]/weight
	return result
			
def statisticalUncertainty(tree,cuts,dilepton):
	histo = createHistoFromTree(tree, "p4.M()", cuts, 300, 0, 300)
	errInt = ROOT.Double()
	Int = histo.IntegralAndError(0,histo.GetNbinsX()+1,errInt)
	if Int > 0:
		err = float(errInt)/float(Int)
	else:
		err = 0
	return err		

def producePileupUncertainty(tree,cuts,dilepton):
	
	uncertaintySources = ["weightUp*","weightDown*"]
	colors=[ROOT.kBlack,ROOT.kBlue,ROOT.kRed]

	result = 0.
	defaultTree = tree.CopyTree(cuts)
	totalWeight = 0
	totalWeightUp = 0
	totalWeightDown = 0
	for event in tree:
		#~ print event.weight, event.weightUp, event.weightDown
		totalWeight = totalWeight + event.weight
		totalWeightUp = totalWeightUp + event.weightUp
		totalWeightDown = totalWeightDown + event.weightDown
	#~ print totalWeight/tree.GetEntries(), totalWeightUp/tree.GetEntries(), totalWeightDown/tree.GetEntries()	
	#~ print cuts
	yields = [float(createHistoFromTree(tree, "p4.M()", cuts, 300, 0, 300).Integral())]
	histos = [createHistoFromTree(tree, "p4.M()", cuts, 60, 0, 300)]
	for index, source in enumerate(uncertaintySources):
		if index == 0:
			cuts = cuts.replace("weight*",source)
		else:
			cuts = cuts.replace(uncertaintySources[index-1],source)
		#~ print cuts
		yields.append(float(createHistoFromTree(tree, "p4.M()", cuts, 300, 0, 300).Integral()))
		histos.append(createHistoFromTree(tree, "p4.M()", cuts, 60, 0, 300))

	#~ print yields
	if yields[0] > 0 and yields[2] > 0:
		result = sqrt( max((yields[1]-yields[0])/yields[0],(yields[2]-yields[0])/yields[2])**2  )		
	elif yields[0] > 0:
		result = (yields[1]-yields[0])/yields[0]
	elif yields[2] > 0:
		result = (yields[2]-yields[0])/yields[2]
	else:
		result = 0
			

	#~ hCanvas = TCanvas("hCanvas", "Distribution", 800,800)

	#~ plotPad = ROOT.TPad("plotPad","plotPad",0,0,1,1)
	#~ ratioPad = ROOT.TPad("ratioPad","ratioPad",0,0.,1,0.3)
	#~ setTDRStyle()		
	#~ plotPad.UseCurrentStyle()
	#~ ratioPad.UseCurrentStyle()
	#~ plotPad.Draw()	
	#~ ratioPad.Draw()	
	#~ plotPad.cd()	
#~ 
#~ 
	#~ legend = TLegend(0.5, 0.6, 0.95, 0.95)
	#~ legend.SetFillStyle(0)
	#~ legend.SetBorderSize(1)
			#~ 
	#~ hCanvas.DrawFrame(20,0.1,300,250,"; %s ; %s" %("m_{ll}","Events"))
#~ 
	#~ latex = ROOT.TLatex()
	#~ latex.SetTextSize(0.05)
	#~ latex.SetTextFont(42)
	#~ latex.SetNDC(True)
	#~ latex.DrawLatex(0.13, 0.96, "CMS Simulation,   #sqrt{s} = 8 TeV,	 #scale[0.6]{#int}Ldt = 19.4 fb^{-1}")	
	#~ 
	#~ 
	#~ for i, histo in enumerate(histos):
		#~ histo.SetLineColor(colors[i])
		#~ if i == 0:
			#~ histo.SetLineWidth(1)
			#~ legend.AddEntry(histo,"default","l")
		#~ else:
			#~ histo.SetLineWidth(1)
			#~ legend.AddEntry(histo,uncertaintySources[i-2],"l")
		#~ histo.Draw("samehist")
			#~ 
	#~ legend.Draw("same")
	#~ hCanvas.Print("fig/pileUpUncertainty_%s_%s.pdf"%(sampleName,dilepton))	

	return result,yields[0],yields[1],yields[2]	
	
	
def produceScalingUncertainty(tree,cuts):
	
	uncertaintySources = ["IDScaleFactorUp*","IDScaleFactorDown*","GSFScaleFactorUp*","GSFScaleFactorDown*","trackingScaleFactorUp*","trackingScaleFactorDown*","isolationScaleFactorUp*","isolationScaleFactorDown*"]
	result = 0.
	defaultTree = tree.CopyTree(cuts)
	yields = [float(createHistoFromTree(tree, "p4.M()", cuts, 300, 0, 300).Integral())]
	for index, source in enumerate(uncertaintySources):
		if index == 0:
			cuts = cuts.replace("IDScaleFactor*",source)
		elif index == 2:
			cuts = cuts.replace(uncertaintySources[1],"IDScaleFactor*")
			cuts = cuts.replace("GSFScaleFactor*",source)
		elif index == 4:
			cuts = cuts.replace(uncertaintySources[3],"GSFScaleFactor*")
			cuts = cuts.replace("trackingScaleFactor*",source)
		elif index == 6:
			cuts = cuts.replace(uncertaintySources[5],"trackingScaleFactor*")
			cuts = cuts.replace("isolationScaleFactor*",source)
		else:
			cuts = cuts.replace(uncertaintySources[index-1],source)
		yields.append(float(createHistoFromTree(tree, "p4.M()", cuts, 300, 0, 300).Integral()))

	if yields[0] > 0:
		result = sqrt( max((yields[1]-yields[0])/yields[0],(yields[1]-yields[0])/yields[0])**2 + max((yields[3]-yields[0])/yields[0],(yields[4]-yields[0])/yields[0])**2 + max((yields[5]-yields[0])/yields[0],(yields[6]-yields[0])/yields[0])**2 + max((yields[7]-yields[0])/yields[0],(yields[8]-yields[0])/yields[0])**2 )
	else:
		result = 0
	return result	
	
	
#~ def producePDFUncertainty(sampleName,path,dilepton):
	#~ from ROOT import TH1F, TFile
#~ 
	#~ result = 0.
	#~ 
	#~ pdfHists = readPDFHists(path,dilepton)
	#~ 
	#~ pdfHists = {}
	#~ yields = {}
	#~ uncertHistsUp = {}
	#~ uncertHistsDown = {}
	#~ f1 = TFile("%s/sw538v0477.processed.%s.root"%(path,sampleName),"READ")
	#~ for pdfSet in ["CT10","MSTW","NNPDF"]:
		#~ pdfHists[pdfSet] = {}
		#~ yields[pdfSet] = {}
		#~ for type in ["mean","up","down"]:
			#~ pdfHists[pdfSet][type] = f1.Get("%s_%sDileptonTree_%s"%(pdfSet,dilepton,type)).Clone()
			#~ yields[pdfSet][type] = f1.Get("%s_%sDileptonTree_%s"%(pdfSet,dilepton,type)).Integral()
		#~ uncertHistsUp[pdfSet] = pdfHists[pdfSet]["up"].Clone()
		#~ uncertHistsUp[pdfSet].Add(pdfHists[pdfSet]["mean"].Clone(),-1)
		#~ uncertHistsUp[pdfSet].Divide(pdfHists[pdfSet]["mean"].Clone())	
		#~ uncertHistsDown[pdfSet] = pdfHists[pdfSet]["down"].Clone()
		#~ uncertHistsDown[pdfSet].Add(pdfHists[pdfSet]["mean"].Clone(),-1)
		#~ uncertHistsDown[pdfSet].Divide(pdfHists[pdfSet]["mean"].Clone())	
	#~ 
	 #~ 
	#~ integratedUncertainty = max(max((yields["CT10"]["up"]-yields["CT10"]["mean"])/yields["CT10"]["mean"],abs((yields["CT10"]["down"]-yields["CT10"]["mean"])/yields["CT10"]["mean"]) ), max( max((yields["MSTW"]["up"]-yields["MSTW"]["mean"])/yields["MSTW"]["mean"],abs((yields["MSTW"]["down"]-yields["MSTW"]["mean"])/yields["MSTW"]["mean"]) ), max((yields["NNPDF"]["up"]-yields["NNPDF"]["mean"])/yields["NNPDF"]["mean"],abs((yields["NNPDF"]["down"]-yields["NNPDF"]["mean"])/yields["NNPDF"]["mean"]) ) ) )
	#~ 
	#~ 
	#~ envelopeDown = TH1F("envelopeDown","envelopeDown",int(280/5),20,300)
	#~ envelopeUp = TH1F("envelopeUp","envelopeUp",int(280/5),20,300)
	#~ 
	#~ for i in range(0,envelopeDown.GetNbinsX()+1):
		#~ envelopeDown.SetBinContent(i,float(min(uncertHistsDown["CT10"].GetBinContent(i),min(uncertHistsDown["MSTW"].GetBinContent(i),uncertHistsDown["NNPDF"].GetBinContent(i)))))
		#~ envelopeUp.SetBinContent(i,max(uncertHistsUp["CT10"].GetBinContent(i),max(uncertHistsUp["MSTW"].GetBinContent(i),uncertHistsUp["NNPDF"].GetBinContent(i))))
#~ 
	#~ hCanvas = TCanvas("hCanvas", "Distribution", 800,800)
#~ 
	#~ plotPad = ROOT.TPad("plotPad","plotPad",0,0,1,1)
	#~ ratioPad = ROOT.TPad("ratioPad","ratioPad",0,0.,1,0.3)
	#~ setTDRStyle()		
	#~ plotPad.UseCurrentStyle()
	#~ ratioPad.UseCurrentStyle()
	#~ plotPad.Draw()	
	#~ ratioPad.Draw()	
	#~ plotPad.cd()	
#~ 
#~ 
	#~ legend = TLegend(0.5, 0.65, 0.95, 0.95)
	#~ legend.SetFillStyle(0)
	#~ legend.SetBorderSize(1)
			#~ 
	#~ hCanvas.DrawFrame(20,-0.25,300,0.35,"; %s ; %s" %("m_{ll} [GeV]","rel. PDF Uncert."))
#~ 
	#~ latex = ROOT.TLatex()
	#~ latex.SetTextSize(0.05)
	#~ latex.SetTextFont(42)
	#~ latex.SetNDC(True)
	#~ latex.DrawLatex(0.13, 0.96, "CMS Simulation,   #sqrt{s} = 8 TeV,	 #scale[0.6]{#int}Ldt = 19.4 fb^{-1}")
#~ 
	#~ uncertHistsUp["CT10"].SetLineColor(ROOT.kRed)		
	#~ uncertHistsDown["CT10"].SetLineColor(ROOT.kRed)		
	#~ uncertHistsUp["MSTW"].SetLineColor(ROOT.kGreen+3)		
	#~ uncertHistsDown["MSTW"].SetLineColor(ROOT.kGreen+3)		
	#~ uncertHistsUp["NNPDF"].SetLineColor(ROOT.kOrange)		
	#~ uncertHistsDown["NNPDF"].SetLineColor(ROOT.kOrange)		
	#~ envelopeDown.SetLineColor(ROOT.kBlue)
	#~ envelopeUp.SetLineColor(ROOT.kBlue)
#~ 
	#~ uncertHistsUp["CT10"].Rebin(2)		
	#~ uncertHistsDown["CT10"].Rebin(2)		
	#~ uncertHistsUp["MSTW"].Rebin(2)		
	#~ uncertHistsDown["MSTW"].Rebin(2)		
	#~ uncertHistsUp["NNPDF"].Rebin(2)		
	#~ uncertHistsDown["NNPDF"].Rebin(2)		
	#~ envelopeDown.Rebin(2)
	#~ envelopeUp.Rebin(2)
	#~ 
	#~ 
	#~ legend.AddEntry(uncertHistsUp["CT10"],"CT10","l")
	#~ legend.AddEntry(uncertHistsUp["MSTW"],"MSTW 2008","l")
	#~ legend.AddEntry(uncertHistsUp["NNPDF"],"NNPDF 2.3","l")
	#~ legend.AddEntry(envelopeUp,"envelope","l")
	#~ 
	#~ uncertHistsUp["CT10"].Draw("samehist")		
	#~ uncertHistsDown["CT10"].Draw("samehist")		
	#~ uncertHistsUp["MSTW"].Draw("samehist")		
	#~ uncertHistsDown["MSTW"].Draw("samehist")			
	#~ uncertHistsUp["NNPDF"].Draw("samehist")			
	#~ uncertHistsDown["NNPDF"].Draw("samehist")			
	#~ envelopeDown.Draw("samehist")	
	#~ envelopeUp.Draw("samehist")	
	#~ 
	#~ legend.Draw("same")
#~ 
	#~ hCanvas.Print("pdfUncertainty_%s.pdf"%sampleName)	
	#~ 
	#~ 
	#~ return integratedUncertainty
def producePDFUncertainty(sampleName,path,dilepton):
	from ROOT import TH1F, TFile

	result = 0.
	
	#~ pdfHists = readPDFHists(path,dilepton)
	
	pdfHists = {}
	yields = {}
	uncertHistsUp = {}
	uncertHistsDown = {}
	f1 = TFile("%s/sw538v0477.processed.%s.root"%(path,sampleName),"READ")
	for pdfSet in ["CT10","MSTW","NNPDF"]:
		pdfHists[pdfSet] = {}
		yields[pdfSet] = {}
		for type in ["mean","up","down"]:
			pdfHists[pdfSet][type] = f1.Get("%s_%sDileptonTree_%s"%(pdfSet,dilepton,type)).Clone()
			yields[pdfSet][type] = f1.Get("%s_%sDileptonTree_%s"%(pdfSet,dilepton,type)).Integral()
		uncertHistsUp[pdfSet] = pdfHists[pdfSet]["up"].Clone()
		uncertHistsUp[pdfSet].Add(pdfHists[pdfSet]["mean"].Clone(),-1)
		uncertHistsUp[pdfSet+"Rel"]=uncertHistsUp[pdfSet].Clone()
		uncertHistsUp[pdfSet+"Rel"].Divide(pdfHists[pdfSet]["mean"].Clone())	
		uncertHistsDown[pdfSet] = pdfHists[pdfSet]["down"].Clone()
		uncertHistsDown[pdfSet].Add(pdfHists[pdfSet]["mean"].Clone(),-1)
		uncertHistsDown[pdfSet+"Rel"]=uncertHistsDown[pdfSet].Clone()
		uncertHistsDown[pdfSet+"Rel"].Divide(pdfHists[pdfSet]["mean"].Clone())	
		
		#~ uncertHistsDown[pdfSet].Divide(pdfHists[pdfSet]["mean"].Clone())	
	
	 
	integratedUncertainty = max(max((yields["CT10"]["up"]-yields["CT10"]["mean"])/yields["CT10"]["mean"],abs((yields["CT10"]["down"]-yields["CT10"]["mean"])/yields["CT10"]["mean"]) ), max( max((yields["MSTW"]["up"]-yields["MSTW"]["mean"])/yields["MSTW"]["mean"],abs((yields["MSTW"]["down"]-yields["MSTW"]["mean"])/yields["MSTW"]["mean"]) ), max((yields["NNPDF"]["up"]-yields["NNPDF"]["mean"])/yields["NNPDF"]["mean"],abs((yields["NNPDF"]["down"]-yields["NNPDF"]["mean"])/yields["NNPDF"]["mean"]) ) ) )
	
	
	envelopeDown = TH1F("envelopeDown","envelopeDown",int(280/5),20,300)
	envelopeUp = TH1F("envelopeUp","envelopeUp",int(280/5),20,300)
	U = TH1F("U","U",int(280/5),20,300)
	D = TH1F("D","D",int(280/5),20,300)
	M = TH1F("D","D",int(280/5),20,300)
	
	for i in range(0,envelopeDown.GetNbinsX()+1):
		D.SetBinContent(i,min(pdfHists["CT10"]["mean"].GetBinContent(i)+uncertHistsDown["CT10"].GetBinContent(i),min(pdfHists["MSTW"]["mean"].GetBinContent(i)+uncertHistsDown["MSTW"].GetBinContent(i),pdfHists["NNPDF"]["mean"].GetBinContent(i)+uncertHistsDown["NNPDF"].GetBinContent(i))))
		U.SetBinContent(i,max(pdfHists["CT10"]["mean"].GetBinContent(i)+uncertHistsUp["CT10"].GetBinContent(i),max(pdfHists["MSTW"]["mean"].GetBinContent(i)+uncertHistsUp["MSTW"].GetBinContent(i),pdfHists["NNPDF"]["mean"].GetBinContent(i)+uncertHistsUp["NNPDF"].GetBinContent(i))))
	
	M = D.Clone()
	M.Add(U.Clone(),1)
	#~ M.Add(M.Clone(),0.5)
	for i in range(0,envelopeDown.GetNbinsX()+1):
		M.SetBinContent(i,M.GetBinContent(i)/2)
	envelopeUp = U.Clone()
	envelopeUp.Add(M.Clone(),-1)
	envelopeUp.Divide(M.Clone())
	
	envelopeDown = envelopeUp.Clone()
	envelopeDown.Add(envelopeUp.Clone(),-2)
		
	#~ hCanvas = TCanvas("hCanvas", "Distribution", 800,800)
	#~ plotPad = ROOT.TPad("plotPad","plotPad",0,0,1,1)
	#~ ratioPad = ROOT.TPad("ratioPad","ratioPad",0,0.,1,0.3)
	#~ setTDRStyle()		
	#~ plotPad.UseCurrentStyle()
	#~ ratioPad.UseCurrentStyle()
	#~ plotPad.Draw()	
	#~ ratioPad.Draw()	
	#~ plotPad.cd()	

#~ 
	#~ legend = TLegend(0.5, 0.65, 0.95, 0.95)
	#~ legend.SetFillStyle(0)
	#~ legend.SetBorderSize(1)
			#~ 
	#~ hCanvas.DrawFrame(20,-0.5,300,0.5,"; %s ; %s" %("m_{ll} [GeV]","rel. PDF Uncert."))
#~ 
	#~ latex = ROOT.TLatex()
	#~ latex.SetTextSize(0.05)
	#~ latex.SetTextFont(42)
	#~ latex.SetNDC(True)
	#~ latex.DrawLatex(0.13, 0.96, "CMS Simulation,   #sqrt{s} = 8 TeV,	 #scale[0.6]{#int}Ldt = 19.4 fb^{-1}")

	#~ uncertHistsUp["CT10Rel"].SetLineColor(ROOT.kRed)		
	#~ uncertHistsDown["CT10Rel"].SetLineColor(ROOT.kRed)		
	#~ uncertHistsUp["MSTWRel"].SetLineColor(ROOT.kGreen+3)		
	#~ uncertHistsDown["MSTWRel"].SetLineColor(ROOT.kGreen+3)		
	#~ uncertHistsUp["NNPDFRel"].SetLineColor(ROOT.kOrange)		
	#~ uncertHistsDown["NNPDFRel"].SetLineColor(ROOT.kOrange)		
	#~ envelopeDown.SetLineColor(ROOT.kBlue)
	#~ envelopeUp.SetLineColor(ROOT.kBlue)

	#~ uncertHistsUp["CT10"].Rebin(2)		
	#~ uncertHistsDown["CT10"].Rebin(2)		
	#~ uncertHistsUp["MSTW"].Rebin(2)		
	#~ uncertHistsDown["MSTW"].Rebin(2)		
	#~ uncertHistsUp["NNPDF"].Rebin(2)		
	#~ uncertHistsDown["NNPDF"].Rebin(2)		
	#~ envelopeDown.Rebin(2)
	#~ envelopeUp.Rebin(2)
	
	
	#~ legend.AddEntry(uncertHistsUp["CT10"],"CT10","l")
	#~ legend.AddEntry(uncertHistsUp["MSTW"],"MSTW 2008","l")
	#~ legend.AddEntry(uncertHistsUp["NNPDF"],"NNPDF 2.3","l")
	#~ legend.AddEntry(envelopeUp,"envelope","l")
	#~ 
	#~ uncertHistsUp["CT10Rel"].Draw("samehist")		
	#~ uncertHistsDown["CT10Rel"].Draw("samehist")		
	#~ uncertHistsUp["MSTWRel"].Draw("samehist")		
	#~ uncertHistsDown["MSTWRel"].Draw("samehist")			
	#~ uncertHistsUp["NNPDFRel"].Draw("samehist")			
	#~ uncertHistsDown["NNPDFRel"].Draw("samehist")			
	#~ envelopeDown.Draw("samehist")	
	#~ envelopeUp.Draw("samehist")	
	#~ 
	#~ legend.Draw("same")
#~ 
	#~ hCanvas.Print("fig/pdfUncertainty_%s.pdf"%sampleName)	
	
	
	return integratedUncertainty
	
def producePDFUncertainty2(sampleName,path,dilepton):
	from ROOT import TH1F, TFile

	result = 0.
	
	#~ pdfHists = readPDFHists(path,dilepton)
	
	pdfHists = {}
	yields = {}
	absYields = {}
	relative = {}
	uncertHistsUp = {}
	uncertHistsDown = {}
	#~ print path
	#~ print sampleName
	f1 = TFile("%s/sw538v0477.processed.%s.root"%(path,sampleName),"READ")
	f2 = TFile("/user/schomakers/trees/pdfTest/pdfNominatorTest.cutsV23DileptonPDFUncertaintyNominator.%s.root"%(sampleName),"READ")
	for pdfSet in ["CT10","MSTW","NNPDF"]:
		yields[pdfSet] = {}
		absYields[pdfSet] = {}
		relative[pdfSet] = {}
		for type in ["mean","up","down"]:
			#~ print type 
			yields[pdfSet][type] = f1.Get("%s_%sDileptonTree_%s"%(pdfSet,dilepton,type)).Integral()
			absYields[pdfSet][type] = f2.Get("%s_Tree_%s"%(pdfSet,type)).Integral()
			relative[pdfSet][type] = yields[pdfSet][type]/absYields[pdfSet][type]
			#~ print yields[pdfSet][type]
			#~ print absYields[pdfSet][type]
			#~ print relative[pdfSet][type]
		
		#~ uncertHistsDown[pdfSet].Divide(pdfHists[pdfSet]["mean"].Clone())	
	
	 
	#~ integratedUncertainty = max(max((yields["CT10"]["up"]-yields["CT10"]["mean"])/yields["CT10"]["mean"],abs((yields["CT10"]["down"]-yields["CT10"]["mean"])/yields["CT10"]["mean"]) ), max( max((yields["MSTW"]["up"]-yields["MSTW"]["mean"])/yields["MSTW"]["mean"],abs((yields["MSTW"]["down"]-yields["MSTW"]["mean"])/yields["MSTW"]["mean"]) ), max((yields["NNPDF"]["up"]-yields["NNPDF"]["mean"])/yields["NNPDF"]["mean"],abs((yields["NNPDF"]["down"]-yields["NNPDF"]["mean"])/yields["NNPDF"]["mean"]) ) ) )
	integratedUncertainty = max(max((relative["CT10"]["up"]-relative["CT10"]["mean"])/relative["CT10"]["mean"],abs((relative["CT10"]["down"]-relative["CT10"]["mean"])/relative["CT10"]["mean"]) ), max( max((relative["MSTW"]["up"]-relative["MSTW"]["mean"])/relative["MSTW"]["mean"],abs((relative["MSTW"]["down"]-relative["MSTW"]["mean"])/relative["MSTW"]["mean"]) ), max((relative["NNPDF"]["up"]-relative["NNPDF"]["mean"])/relative["NNPDF"]["mean"],abs((relative["NNPDF"]["down"]-relative["NNPDF"]["mean"])/relative["NNPDF"]["mean"]) ) ) )
	
	return integratedUncertainty,yields["CT10"]["mean"],absYields["CT10"]["mean"],yields["CT10"]["up"],absYields["CT10"]["up"],yields["CT10"]["down"],absYields["CT10"]["down"],yields["MSTW"]["mean"],absYields["MSTW"]["mean"],yields["MSTW"]["up"],absYields["MSTW"]["up"],yields["MSTW"]["down"],absYields["MSTW"]["down"],yields["NNPDF"]["mean"],absYields["NNPDF"]["mean"],yields["NNPDF"]["up"],absYields["NNPDF"]["up"],yields["NNPDF"]["down"],absYields["NNPDF"]["down"]


		
if (__name__ == "__main__"):
	setTDRStyle()
	
	from sys import argv
	import pickle	
	from ROOT import TCanvas, TPad, TH1F, TH1I, THStack, TLegend, TF1, TH2F, TH2D, TFile
	import ratios
	from defs import sbottom_masses
	from math import sqrt
	
	ElectronFactors = TFile("electron_FastSim_EWKino.root")
	MuonFactors = TFile("muon_FastSim_EWKino.root")
	
	ElectronScaleFactors = ElectronFactors.Get("SF")
	MuonScaleFactors = MuonFactors.Get("SF")
	

	lumi = 19400
		
	step_size = 25
	m_b_min = int(argv[3])
	m_b_max = int(argv[3])
	m_n_max = 700
		
	m_neutr_1_fix = False
	if m_neutr_1_fix == False:
		MultiQuarkScaleFactor = "((nGenSUSYLeptons == 0 && nGenSUSYNeutrinos == 0) * 9 * 0.4887)"
		NeutrinoQuarkScaleFactor = "((nGenSUSYLeptons == 0 && nGenSUSYNeutrinos == 2) * 9./2. * 0.2796)"
		MultiNeutrinoScaleFactor = "((nGenSUSYLeptons == 0 && nGenSUSYNeutrinos == 4) * 9 * 0.04)"
		DileptonNeutrinoScaleFactor = "((nGenSUSYLeptons == 2 && nGenSUSYNeutrinos == 2) * 9./2. * 0.0404)"
		DileptonQuarkScaleFactor = "((nGenSUSYLeptons == 2 && nGenSUSYNeutrinos == 0) * 9./2. * 0.1411)"
		MultileptonScaleFactor = "((nGenSUSYLeptons == 4)*9*0.0102)"
		path = "/user/schomakers/trees/sw538v0477/GridScanZDecay"
		m_n_min = 100
	else:
		SleptonNeutrinoScaleFactor = "((nGenSUSYLeptons == 1 && nGenSUSYNeutrinos == 2) * 3. * 0.2)"
		SleptonQuarkScaleFactor = "((nGenSUSYLeptons == 1 && nGenSUSYNeutrinos == 0) * 3. * 0.6991)"
		SleptonLeptonScaleFactor = "((nGenSUSYLeptons == 3) * 3. * 0.101)"
		#~ DileptonQuarkScaleFactor = "((nGenSUSYLeptons == 2 && nGenSUSYNeutrinos == 0 && nGenSUSYSleptons == 0 && motherPdgId1 != 1000011 && motherPdgId1 != 2000011 && motherPdgId1 != 1000013 && motherPdgId1 != 2000013 && motherPdgId2 != 1000011 && motherPdgId2 != 2000011 && motherPdgId2 != 1000013 && motherPdgId2 != 2000013 ) * 9./2. * 0.1411)"
		#~ DileptonNeutrinoScaleFactor = "((nGenSUSYLeptons == 2 && nGenSUSYNeutrinos == 2 && nGenSUSYSleptons == 0 && motherPdgId1 != 1000011 && motherPdgId1 != 2000011 && motherPdgId1 != 1000013 && motherPdgId1 != 2000013 && motherPdgId2 != 1000011 && motherPdgId2 != 2000011 && motherPdgId2 != 1000013 && motherPdgId2 != 2000013 ) * 9./2. * 0.0404)"
		DileptonQuarkScaleFactor = "((nGenSUSYLeptons == 2 && nGenSUSYNeutrinos == 0 && motherPdgId1 != 1000011 && motherPdgId1 != 2000011 && motherPdgId1 != 1000013 && motherPdgId1 != 2000013 && motherPdgId2 != 1000011 && motherPdgId2 != 2000011 && motherPdgId2 != 1000013 && motherPdgId2 != 2000013 ) * 9./2. * 0.1411)"
		DileptonNeutrinoScaleFactor = "((nGenSUSYLeptons == 2 && nGenSUSYNeutrinos == 2 && motherPdgId1 != 1000011 && motherPdgId1 != 2000011 && motherPdgId1 != 1000013 && motherPdgId1 != 2000013 && motherPdgId2 != 1000011 && motherPdgId2 != 2000011 && motherPdgId2 != 1000013 && motherPdgId2 != 2000013 ) * 9./2. * 0.0404)"
		DiSleptonScaleFactor = "(nGenSUSYLeptons == 2 && nGenSUSYNeutrinos == 0 && (motherPdgId1 == 1000011 || motherPdgId1 == 2000011 || motherPdgId1 == 1000013 || motherPdgId1 == 2000013 || motherPdgId2 == 1000011 || motherPdgId2 == 2000011 || motherPdgId2 == 1000013 || motherPdgId2 == 2000013 ) )"
		MultileptonScaleFactor = "((nGenSUSYLeptons == 4)*9*0.0102)"
		path = "/user/schomakers/trees/sw538v0477/GridScanSlepton"
		m_n_min = 150
		m_neutralino_1 = "100"

	ptCut = "pt1 > 20 && pt2 > 20"
	ptCutLabel = "20"
	mllCut = mllCuts[argv[2]]
	variable = "p4.M()"
	etaCut = etaCuts[argv[1]]
	additionalCut = ""
	if additionalCut == "NJets3Cut":
		suffix = argv[1]+"_"+argv[2]+"_NJets3Cut"
		cuts = "weight*sbottomWeight*(chargeProduct < 0 && %s && %s && %s &&  nJetsSmeared >= 3 && abs(eta1) < 2.4 && abs(eta2) < 2.4 && deltaR > 0.3)"%(ptCut,etaCut,mllCut)
	elif additionalCut == "Met150Cut":
		suffix = argv[1]+"_"+argv[2]+"_Met150Cut"
		cuts = "weight*sbottomWeight*(chargeProduct < 0 && %s && %s && %s && patPFMet > 150 && abs(eta1) < 2.4 && abs(eta2) < 2.4 && deltaR > 0.3)"%(ptCut,etaCut,mllCut)
	else:
		suffix = argv[1]+"_"+argv[2]
		cuts = "weight*sbottomWeight*(chargeProduct < 0 && %s && %s && %s && ((patPFMet > 100 && nJetsSmeared >= 3) ||  (patPFMet > 150 && nJetsSmeared >=2)) && abs(eta1) < 2.4 && abs(eta2) < 2.4 && deltaR > 0.3)"%(ptCut,etaCut,mllCut)
	
	if m_neutr_1_fix == False:
		ISR_incl_cuts = "weight*(%s+%s+%s+%s+%s+%s)"%(MultiQuarkScaleFactor,NeutrinoQuarkScaleFactor,MultiNeutrinoScaleFactor,DileptonNeutrinoScaleFactor,DileptonQuarkScaleFactor,MultileptonScaleFactor)
		cuts = "%s *(%s+%s+%s+%s+%s+%s)"%(cuts,MultiQuarkScaleFactor,NeutrinoQuarkScaleFactor,MultiNeutrinoScaleFactor,DileptonNeutrinoScaleFactor,DileptonQuarkScaleFactor,MultileptonScaleFactor)
	else:
		ISR_incl_cuts = "weight*(%s+%s+%s+%s+%s+%s+%s)"%(SleptonNeutrinoScaleFactor,SleptonQuarkScaleFactor,SleptonLeptonScaleFactor,DileptonQuarkScaleFactor,DileptonNeutrinoScaleFactor,DiSleptonScaleFactor,MultileptonScaleFactor)
		cuts = "%s *(%s+%s+%s+%s+%s+%s+%s)"%(cuts,SleptonNeutrinoScaleFactor,SleptonQuarkScaleFactor,SleptonLeptonScaleFactor,DileptonQuarkScaleFactor,DileptonNeutrinoScaleFactor,DiSleptonScaleFactor,MultileptonScaleFactor)
			
	if argv[1] == "Barrel":
		EETriggerEff = 0.971
		EMuTriggerEff = 0.941
		MuMuTriggerEff = 0.97
	elif "Endcap" in argv[1]:
		EETriggerEff = 0.974
		EMuTriggerEff = 0.873
		MuMuTriggerEff = 0.967
	elif argv[1] == "Inclusive":
		EETriggerEff = 0.972
		EMuTriggerEff = 0.927
		MuMuTriggerEff = 0.969
	
	triggerEffUncertainty = 0.05
	lumiUncertainty = 0.026
	
	#~ if argv[1] == "Endcap":
		#~ FastSimUncertainty = 0.02
	#~ else:
		#~ FastSimUncertainty = 0.1
	FastSimUncertainty = 0.02
	
	
	
	
	totalEvents = totalNumberOfGeneratedEvents(path)
	
	i = 0
	while m_b_min + i*step_size <= m_b_max:
		m_b = m_b_min + i*step_size
		M_SBOTTOM = "m_b_"+str(m_b_min + i*step_size)
		m_sbottom = str(m_b_min + i*step_size)
		j = 0
		while m_n_min + j*step_size <= m_n_max:
			m_n_2 = m_n_min + j*step_size
			m_neutralino_2 = str(m_n_min + j*step_size)
			if m_b >= m_n_2:		
			#~ if m_b >= m_n_2 and not (m_b == 225 and m_n_2 == 150):
			#~ if m_b >= m_n_2 and not (m_b == 450 and m_n_2 == 150) and not (m_b == 450 and m_n_2 == 400) and not (m_b == 475 and m_n_2 == 175) and not (m_b == 525 and m_n_2 == 350):
				print "m_b: "+m_sbottom
				print "m_n: "+m_neutralino_2
				
				if m_neutr_1_fix == False:
					#~ m_neutralino_1 = "m_n_1_"+str(m_n_min + j*step_size - 70)
					m_neutralino_1 = str(m_n_min + j*step_size - 70)


				EMutrees = readTrees(path, "EMu")	
				EEtrees = readTrees(path, "EE")	
				MuMutrees = readTrees(path, "MuMu")	
			
			
				if m_neutr_1_fix == False:
					sampleName = "SUSY_Simplified_Model_Madgraph_FastSim_T6bblledge_%s_%s_%s_8TeV"%(m_sbottom,m_neutralino_2,m_neutralino_1)
					fileName = "SUSY_Simplified_Model_Madgraph_FastSim_T6bblledge_%s_%s_%s_8TeV"%(m_sbottom,m_neutralino_2,m_neutralino_1)
				else:
					sampleName = "SUSY_Simplified_Model_Madgraph_FastSim_T6bbslepton_%s_%s_%s_8TeV"%(m_sbottom,m_neutralino_2,m_neutralino_1)
					fileName = "SUSY_Simplified_Model_Madgraph_FastSim_T6bbslepton_%s_%s_%s_8TeV"%(m_sbottom,m_neutralino_2,m_neutralino_1)

				xsection = getattr(sbottom_masses, M_SBOTTOM).cross_section
				
				scalingLumi = lumi*xsection/totalEvents[sampleName]
				weight = 1./totalEvents[sampleName]
				for sample, tree in EEtrees.iteritems():
					if sample == sampleName:
						EEISRUncertainty,EEISRMean,EEISRUp,EEISRDown,EEISRCorrectionFactor = produceISRUncertainty(tree,cuts,"EE",ISR_incl_cuts)
						EEsignalNumber, EEMCEvents = signalNumbers(tree,argv[1],argv[2],"EE",ElectronScaleFactors,MuonScaleFactors,additionalCut,m_neutr_1_fix)
						EEsignalYield = EEsignalNumber * EETriggerEff * scalingLumi * EEISRCorrectionFactor
						EEsignalEfficiency = EEsignalNumber * EETriggerEff * weight
						EEstatUncertainty = statisticalUncertainty(tree,cuts,"EE")
						EEmetUncertainty,EEPFMetMean,EEPFMetJetEnUp,EEPFMetJetEnDown,EEpatPFMetJetResUp,EEpatPFMetJetResDown,EEpatPFMetElectronEnUp,EEpatPFMetElectronEnDown,EEpatPFMetMuonEnUp,EEpatPFMetMuonEnDown,EEpatPFMetTauEnUp,EEpatPFMetTauEnDown,EEpatPFMetUnclusteredEnUp,EEpatPFMetUnclusteredEnDown = produceMETUncertainty(tree,cuts,"EE")
						EEjetUncertainty,EEnJetsMean,EEnJetsEnUp,EEnJetsEnDown,EEnJetsResUp,EEnJetsResDown = produceJetUncertainty(tree,cuts,"EE")
						EEleptonUncertainty,EEleptonptMean,EEleptonptScaleUp,EEleptonptScaleDown = produceLeptonUncertaintySF(tree,cuts,"EE",argv[1])
						EEpileupUncertainty,EEPileupMean,EEPileupUp,EEPileupDown = producePileupUncertainty(tree,cuts,"EE")
						#~ EEscalingUncertainty = produceScalingUncertainty(tree,cuts)
						#~ EEpdfUncertainty = producePDFUncertainty(sample,path,"EE")
						EEpdfUncertainty,EECT10Mean,EECT10AbsMean,EECT10Up,EECT10AbsUp,EECT10Down,EECT10AbsDown,EEMSTWMean,EEMSTWAbsMean,EEMSTWUp,EEMSTWAbsUp,EEMSTWDown,EEMSTWAbsDown,EENNPDFMean,EENNPDFAbsMean,EENNPDFUp,EENNPDFAbsUp,EENNPDFDown,EENNPDFAbsDown = producePDFUncertainty2(sample,path,"EE")
						EEsystUncertainty = sqrt(EEmetUncertainty**2+EEjetUncertainty**2+EEleptonUncertainty**2+EEpileupUncertainty**2+EEpdfUncertainty**2+EEISRUncertainty**2+triggerEffUncertainty**2+lumiUncertainty**2+FastSimUncertainty**2)
						counts = {}
						#~ counts["EE"] = {"EEval":EEsignalYield,"EEsignalEfficiency":EEsignalEfficiency,"EEstatUncertainty":EEstatUncertainty,"EETotSystUncertainty":EEsystUncertainty,"EEmetUncertainty":EEmetUncertainty,"EEjetUncertainty":EEjetUncertainty,"EEleptonUncertainty":EEleptonUncertainty,"EEpileupUncertainty":EEpileupUncertainty,"EEscalingUncertainty":EEscalingUncertainty,"EEpdfUncertainty":EEpdfUncertainty,"EEpdfUncertainty2":EEpdfUncertainty2,"EEISRUncertainty":EEISRUncertainty}
						counts["EE"] = {"EEMCEvents":EEMCEvents,"EEval":EEsignalYield,"EEsignalEfficiency":EEsignalEfficiency,"EEstatUncertainty":EEstatUncertainty,"EETotSystUncertainty":EEsystUncertainty,
						"EEmetUncertainty":EEmetUncertainty,"EEPFMetMean":EEPFMetMean,"EEPFMetJetEnUp":EEPFMetJetEnUp,"EEPFMetJetEnDown":EEPFMetJetEnDown,"EEpatPFMetJetResUp":EEpatPFMetJetResUp,"EEpatPFMetJetResDown":EEpatPFMetJetResDown,"EEpatPFMetElectronEnUp":EEpatPFMetElectronEnUp,"EEpatPFMetElectronEnDown":EEpatPFMetElectronEnDown,"EEpatPFMetMuonEnUp":EEpatPFMetMuonEnUp,"EEpatPFMetMuonEnDown":EEpatPFMetMuonEnDown,"EEpatPFMetTauEnUp":EEpatPFMetTauEnUp,"EEpatPFMetTauEnDown":EEpatPFMetTauEnDown,"EEpatPFMetUnclusteredEnUp":EEpatPFMetUnclusteredEnUp,"EEpatPFMetUnclusteredEnDown":EEpatPFMetUnclusteredEnDown,
						"EEjetUncertainty":EEjetUncertainty,"EEnJetsMean":EEnJetsMean,"EEnJetsEnUp":EEnJetsEnUp,"EEnJetsEnDown":EEnJetsEnDown,"EEnJetsResUp":EEnJetsResUp,"EEnJetsResDown":EEnJetsResDown,
						"EEleptonUncertainty":EEleptonUncertainty,"EEleptonptMean":EEleptonptMean,"EEleptonptScaleUp":EEleptonptScaleUp,"EEleptonptScaleDown":EEleptonptScaleDown,
						"EEpileupUncertainty":EEpileupUncertainty,"EEPileupMean":EEPileupMean,"EEPileupUp":EEPileupUp,"EEPileupDown":EEPileupDown,
						"EEpdfUncertainty":EEpdfUncertainty,"EECT10Mean":EECT10Mean,"EECT10AbsMean":EECT10AbsMean,"EECT10Up":EECT10Up,"EECT10AbsUp":EECT10AbsUp,"EECT10Down":EECT10Down,"EECT10AbsDown":EECT10AbsDown,"EEMSTWMean":EEMSTWMean,"EEMSTWAbsMean":EEMSTWAbsMean,"EEMSTWUp":EEMSTWUp,"EEMSTWAbsUp":EEMSTWAbsUp,"EEMSTWDown":EEMSTWDown,"EEMSTWAbsDown":EEMSTWAbsDown,"EENNPDFMean":EENNPDFMean,"EENNPDFAbsMean":EENNPDFAbsMean,"EENNPDFUp":EENNPDFUp,"EENNPDFAbsUp":EENNPDFAbsUp,"EENNPDFDown":EENNPDFDown,"EENNPDFAbsDown":EENNPDFAbsDown,
						"EEISRUncertainty":EEISRUncertainty,"EEISRMean":EEISRMean,"EEISRUp":EEISRUp,"EEISRDown":EEISRDown}
						if m_neutr_1_fix == False:
							outFilePkl = open("shelvesZDecayLeptonScaling/%s_%s_EE.pkl"%(fileName,suffix),"w")
						else:
							#~ print "shelvesSleptonLeptonScaling/%s_%s_EE.pkl"%(fileName,suffix)
							outFilePkl = open("shelvesSleptonLeptonScalingReweighted/%s_%s_EE.pkl"%(fileName,suffix),"w")
						pickle.dump(counts, outFilePkl)
						outFilePkl.close()
				for sample, tree in EMutrees.iteritems():
					if sample == sampleName:
						EMuISRUncertainty,EMuISRMean,EMuISRUp,EMuISRDown, EMuISRCorrectionFactor = produceISRUncertainty(tree,cuts,"EMu",ISR_incl_cuts)
						EMusignalNumber, EMuMCEvents = signalNumbers(tree,argv[1],argv[2],"EMu",ElectronScaleFactors,MuonScaleFactors,additionalCut,m_neutr_1_fix)
						EMusignalYield = EMusignalNumber * EMuTriggerEff * scalingLumi * EMuISRCorrectionFactor
						EMusignalEfficiency = EMusignalNumber * EMuTriggerEff * weight
						EMustatUncertainty = statisticalUncertainty(tree,cuts,"EMu")
						EMumetUncertainty,EMuPFMetMean,EMuPFMetJetEnUp,EMuPFMetJetEnDown,EMupatPFMetJetResUp,EMupatPFMetJetResDown,EMupatPFMetElectronEnUp,EMupatPFMetElectronEnDown,EMupatPFMetMuonEnUp,EMupatPFMetMuonEnDown,EMupatPFMetTauEnUp,EMupatPFMetTauEnDown,EMupatPFMetUnclusteredEnUp,EMupatPFMetUnclusteredEnDown = produceMETUncertainty(tree,cuts,"EMu")
						EMujetUncertainty,EMunJetsMean,EMunJetsEnUp,EMunJetsEnDown,EMunJetsResUp,EMunJetsResDown = produceJetUncertainty(tree,cuts,"EMu")
						EMuleptonUncertainty,EMuleptonptMean,EMuleptonpt1ScaleUp,EMuleptonpt2ScaleUp,EMuleptonpt1ScaleDown,EMuleptonpt2ScaleDown = produceLeptonUncertaintyEMu(tree,cuts,"EMu",argv[1])
						EMupileupUncertainty,EMuPileupMean,EMuPileupUp,EMuPileupDown = producePileupUncertainty(tree,cuts,"EMu")
						#~ EMuscalingUncertainty = produceScalingUncertainty(tree,cuts)
						#~ EMupdfUncertainty = producePDFUncertainty(sample,path,"EMu")
						EMupdfUncertainty,EMuCT10Mean,EMuCT10AbsMean,EMuCT10Up,EMuCT10AbsUp,EMuCT10Down,EMuCT10AbsDown,EMuMSTWMean,EMuMSTWAbsMean,EMuMSTWUp,EMuMSTWAbsUp,EMuMSTWDown,EMuMSTWAbsDown,EMuNNPDFMean,EMuNNPDFAbsMean,EMuNNPDFUp,EMuNNPDFAbsUp,EMuNNPDFDown,EMuNNPDFAbsDown = producePDFUncertainty2(sample,path,"EMu")
						EMusystUncertainty = sqrt(EMumetUncertainty**2+EMujetUncertainty**2+EMuleptonUncertainty**2+EMupileupUncertainty**2+EMupdfUncertainty**2+EMuISRUncertainty**2+triggerEffUncertainty**2+lumiUncertainty**2+FastSimUncertainty**2)
						counts = {}
						#~ counts["EMu"] = {"EMuval":EMusignalYield,"EMusignalEfficiency":EMusignalEfficiency,"EMustatUncertainty":EMustatUncertainty,"EMuTotSystUncertainty":EMusystUncertainty,"EMumetUncertainty":EMumetUncertainty,"EMujetUncertainty":EMujetUncertainty,"EMuleptonUncertainty":EMuleptonUncertainty,"EMupileupUncertainty":EMupileupUncertainty,"EMuscalingUncertainty":EMuscalingUncertainty,"EMupdfUncertainty":EMupdfUncertainty,"EMupdfUncertainty2":EMupdfUncertainty2,"EMuISRUncertainty":EMuISRUncertainty}
						counts["EMu"] = {"EMuMCEvents":EMuMCEvents,"EMuval":EMusignalYield,"EMusignalEfficiency":EMusignalEfficiency,"EMustatUncertainty":EMustatUncertainty,"EMuTotSystUncertainty":EMusystUncertainty,
						"EMumetUncertainty":EMumetUncertainty,"EMuPFMetMean":EMuPFMetMean,"EMuPFMetJetEnUp":EMuPFMetJetEnUp,"EMuPFMetJetEnDown":EMuPFMetJetEnDown,"EMupatPFMetJetResUp":EMupatPFMetJetResUp,"EMupatPFMetJetResDown":EMupatPFMetJetResDown,"EMupatPFMetElectronEnUp":EMupatPFMetElectronEnUp,"EMupatPFMetElectronEnDown":EMupatPFMetElectronEnDown,"EMupatPFMetMuonEnUp":EMupatPFMetMuonEnUp,"EMupatPFMetMuonEnDown":EMupatPFMetMuonEnDown,"EMupatPFMetTauEnUp":EMupatPFMetTauEnUp,"EMupatPFMetTauEnDown":EMupatPFMetTauEnDown,"EMupatPFMetUnclusteredEnUp":EMupatPFMetUnclusteredEnUp,"EMupatPFMetUnclusteredEnDown":EMupatPFMetUnclusteredEnDown,
						"EMujetUncertainty":EMujetUncertainty,"EMunJetsMean":EMunJetsMean,"EMunJetsEnUp":EMunJetsEnUp,"EMunJetsEnDown":EMunJetsEnDown,"EMunJetsResUp":EMunJetsResUp,"EMunJetsResDown":EMunJetsResDown,
						"EMuleptonUncertainty":EMuleptonUncertainty,"EMuleptonptMean":EMuleptonptMean,"EMuleptonpt1ScaleUp":EMuleptonpt1ScaleUp,"EMuleptonpt2ScaleUp":EMuleptonpt2ScaleUp,"EMuleptonpt1ScaleDown":EMuleptonpt1ScaleDown,"EMuleptonpt2ScaleDown":EMuleptonpt2ScaleDown,
						"EMupileupUncertainty":EMupileupUncertainty,"EMuPileupMean":EMuPileupMean,"EMuPileupUp":EMuPileupUp,"EMuPileupDown":EMuPileupDown,
						"EMupdfUncertainty":EMupdfUncertainty,"EMuCT10Mean":EMuCT10Mean,"EMuCT10AbsMean":EMuCT10AbsMean,"EMuCT10Up":EMuCT10Up,"EMuCT10AbsUp":EMuCT10AbsUp,"EMuCT10Down":EMuCT10Down,"EMuCT10AbsDown":EMuCT10AbsDown,"EMuMSTWMean":EMuMSTWMean,"EMuMSTWAbsMean":EMuMSTWAbsMean,"EMuMSTWUp":EMuMSTWUp,"EMuMSTWAbsUp":EMuMSTWAbsUp,"EMuMSTWDown":EMuMSTWDown,"EMuMSTWAbsDown":EMuMSTWAbsDown,"EMuNNPDFMean":EMuNNPDFMean,"EMuNNPDFAbsMean":EMuNNPDFAbsMean,"EMuNNPDFUp":EMuNNPDFUp,"EMuNNPDFAbsUp":EMuNNPDFAbsUp,"EMuNNPDFDown":EMuNNPDFDown,"EMuNNPDFAbsDown":EMuNNPDFAbsDown,
						"EMuISRUncertainty":EMuISRUncertainty,"EMuISRMean":EMuISRMean,"EMuISRUp":EMuISRUp,"EMuISRDown":EMuISRDown}
						if m_neutr_1_fix == False:
							outFilePkl = open("shelvesZDecayLeptonScaling/%s_%s_EMu.pkl"%(fileName,suffix),"w")
						else:
							outFilePkl = open("shelvesSleptonLeptonScalingReweighted/%s_%s_EMu.pkl"%(fileName,suffix),"w")
						pickle.dump(counts, outFilePkl)
						outFilePkl.close()
				for sample, tree in MuMutrees.iteritems():
					if sample == sampleName:
						MuMuISRUncertainty,MuMuISRMean,MuMuISRUp,MuMuISRDown,MuMuISRCorrectionFactor = produceISRUncertainty(tree,cuts,"MuMu",ISR_incl_cuts)
						MuMusignalNumber, MuMuMCEvents = signalNumbers(tree,argv[1],argv[2],"MuMu",ElectronScaleFactors,MuonScaleFactors,additionalCut,m_neutr_1_fix)
						MuMusignalYield = MuMusignalNumber * MuMuTriggerEff * scalingLumi * MuMuISRCorrectionFactor
						MuMusignalEfficiency = MuMusignalNumber * MuMuTriggerEff * weight
						MuMustatUncertainty = statisticalUncertainty(tree,cuts,"MuMu")
						MuMumetUncertainty,MuMuPFMetMean,MuMuPFMetJetEnUp,MuMuPFMetJetEnDown,MuMupatPFMetJetResUp,MuMupatPFMetJetResDown,MuMupatPFMetElectronEnUp,MuMupatPFMetElectronEnDown,MuMupatPFMetMuonEnUp,MuMupatPFMetMuonEnDown,MuMupatPFMetTauEnUp,MuMupatPFMetTauEnDown,MuMupatPFMetUnclusteredEnUp,MuMupatPFMetUnclusteredEnDown = produceMETUncertainty(tree,cuts,"MuMu")
						MuMujetUncertainty,MuMunJetsMean,MuMunJetsEnUp,MuMunJetsEnDown,MuMunJetsResUp,MuMunJetsResDown = produceJetUncertainty(tree,cuts,"MuMu")
						MuMuleptonUncertainty,MuMuleptonptMean,MuMuleptonptScaleUp,MuMuleptonptScaleDown = produceLeptonUncertaintySF(tree,cuts,"MuMu",argv[1])
						MuMupileupUncertainty,MuMuPileupMean,MuMuPileupUp,MuMuPileupDown = producePileupUncertainty(tree,cuts,"MuMu")
						#~ MuMuscalingUncertainty = produceScalingUncertainty(tree,cuts)
						#~ MuMupdfUncertainty = producePDFUncertainty(sample,path,"MuMu")
						MuMupdfUncertainty,MuMuCT10Mean,MuMuCT10AbsMean,MuMuCT10Up,MuMuCT10AbsUp,MuMuCT10Down,MuMuCT10AbsDown,MuMuMSTWMean,MuMuMSTWAbsMean,MuMuMSTWUp,MuMuMSTWAbsUp,MuMuMSTWDown,MuMuMSTWAbsDown,MuMuNNPDFMean,MuMuNNPDFAbsMean,MuMuNNPDFUp,MuMuNNPDFAbsUp,MuMuNNPDFDown,MuMuNNPDFAbsDown = producePDFUncertainty2(sample,path,"MuMu")
						MuMusystUncertainty = sqrt(MuMumetUncertainty**2+MuMujetUncertainty**2+MuMuleptonUncertainty**2+MuMupileupUncertainty**2+MuMupdfUncertainty**2+MuMuISRUncertainty**2+triggerEffUncertainty**2+lumiUncertainty**2+FastSimUncertainty**2)
						counts = {}
						#~ counts["MuMu"] = {"MuMuval":MuMusignalYield,"MuMusignalEfficiency":MuMusignalEfficiency,"MuMustatUncertainty":MuMustatUncertainty,"MuMuTotSystUncertainty":MuMusystUncertainty,"MuMumetUncertainty":MuMumetUncertainty,"MuMujetUncertainty":MuMujetUncertainty,"MuMuleptonUncertainty":MuMuleptonUncertainty,"MuMupileupUncertainty":MuMupileupUncertainty,"MuMuscalingUncertainty":MuMuscalingUncertainty,"MuMupdfUncertainty":MuMupdfUncertainty,"MuMupdfUncertainty2":MuMupdfUncertainty2,"MuMuISRUncertainty":MuMuISRUncertainty}
						counts["MuMu"] = {"MuMuMCEvents":MuMuMCEvents,"MuMuval":MuMusignalYield,"MuMusignalEfficiency":MuMusignalEfficiency,"MuMustatUncertainty":MuMustatUncertainty,"MuMuTotSystUncertainty":MuMusystUncertainty,
						"MuMumetUncertainty":MuMumetUncertainty,"MuMuPFMetMean":MuMuPFMetMean,"MuMuPFMetJetEnUp":MuMuPFMetJetEnUp,"MuMuPFMetJetEnDown":MuMuPFMetJetEnDown,"MuMupatPFMetJetResUp":MuMupatPFMetJetResUp,"MuMupatPFMetJetResDown":MuMupatPFMetJetResDown,"MuMupatPFMetElectronEnUp":MuMupatPFMetElectronEnUp,"MuMupatPFMetElectronEnDown":MuMupatPFMetElectronEnDown,"MuMupatPFMetMuonEnUp":MuMupatPFMetMuonEnUp,"MuMupatPFMetMuonEnDown":MuMupatPFMetMuonEnDown,"MuMupatPFMetTauEnUp":MuMupatPFMetTauEnUp,"MuMupatPFMetTauEnDown":MuMupatPFMetTauEnDown,"MuMupatPFMetUnclusteredEnUp":MuMupatPFMetUnclusteredEnUp,"MuMupatPFMetUnclusteredEnDown":MuMupatPFMetUnclusteredEnDown,
						"MuMujetUncertainty":MuMujetUncertainty,"MuMunJetsMean":MuMunJetsMean,"MuMunJetsEnUp":MuMunJetsEnUp,"MuMunJetsEnDown":MuMunJetsEnDown,"MuMunJetsResUp":MuMunJetsResUp,"MuMunJetsResDown":MuMunJetsResDown,
						"MuMuleptonUncertainty":MuMuleptonUncertainty,"MuMuleptonptMean":MuMuleptonptMean,"MuMuleptonptScaleUp":MuMuleptonptScaleUp,"MuMuleptonptScaleDown":MuMuleptonptScaleDown,
						"MuMupileupUncertainty":MuMupileupUncertainty,"MuMuPileupMean":MuMuPileupMean,"MuMuPileupUp":MuMuPileupUp,"MuMuPileupDown":MuMuPileupDown,
						"MuMupdfUncertainty":MuMupdfUncertainty,"MuMuCT10Mean":MuMuCT10Mean,"MuMuCT10AbsMean":MuMuCT10AbsMean,"MuMuCT10Up":MuMuCT10Up,"MuMuCT10AbsUp":MuMuCT10AbsUp,"MuMuCT10Down":MuMuCT10Down,"MuMuCT10AbsDown":MuMuCT10AbsDown,"MuMuMSTWMean":MuMuMSTWMean,"MuMuMSTWAbsMean":MuMuMSTWAbsMean,"MuMuMSTWUp":MuMuMSTWUp,"MuMuMSTWAbsUp":MuMuMSTWAbsUp,"MuMuMSTWDown":MuMuMSTWDown,"MuMuMSTWAbsDown":MuMuMSTWAbsDown,"MuMuNNPDFMean":MuMuNNPDFMean,"MuMuNNPDFAbsMean":MuMuNNPDFAbsMean,"MuMuNNPDFUp":MuMuNNPDFUp,"MuMuNNPDFAbsUp":MuMuNNPDFAbsUp,"MuMuNNPDFDown":MuMuNNPDFDown,"MuMuNNPDFAbsDown":MuMuNNPDFAbsDown,
						"MuMuISRUncertainty":MuMuISRUncertainty,"MuMuISRMean":MuMuISRMean,"MuMuISRUp":MuMuISRUp,"MuMuISRDown":MuMuISRDown}
						if m_neutr_1_fix == False:
							outFilePkl = open("shelvesZDecayLeptonScaling/%s_%s_MuMu.pkl"%(fileName,suffix),"w")
						else:
							outFilePkl = open("shelvesSleptonLeptonScalingReweighted/%s_%s_MuMu.pkl"%(fileName,suffix),"w")
						pickle.dump(counts, outFilePkl)
						outFilePkl.close()
				
				#~ counts = {}
				#~ SFYield = EEsignalYield + MuMusignalYield
				#~ if SFYield > 0:
					#~ SFUncertainty = sqrt((EEsignalYield*EEsystUncertainty)**2 + (MuMusignalYield*MuMusystUncertainty)**2)/SFYield
					#~ SFStatUncertainty = sqrt((EEsignalYield*EEstatUncertainty)**2 + (MuMusignalYield*MuMustatUncertainty)**2)/SFYield
				#~ else: 
					#~ SFUncertainty = 0
					#~ SFStatUncertainty = 0
					#~ 
				#~ SFOFYield = EEsignalYield + MuMusignalYield - EMusignalYield
				#~ if SFOFYield > 0:
					#~ SFOFUncertainty = sqrt((EEsignalYield*EEsystUncertainty)**2 + (MuMusignalYield*MuMusystUncertainty)**2 + (EMusignalYield*MuMusystUncertainty)**2)/SFOFYield
					#~ SFOFStatUncertainty = sqrt((EEsignalYield*EEstatUncertainty)**2 + (MuMusignalYield*MuMustatUncertainty)**2 + (EMusignalYield*MuMustatUncertainty)**2)/SFOFYield
				#~ else:
					#~ SFOFUncertainty = 0
					#~ SFOFStatUncertainty = 0
					#~ 
				#~ counts["Signal"] = {"SFYield":SFYield,"SFUncertainty":SFUncertainty,"SFStatUncertainty":SFStatUncertainty,"SFOFYield":SFOFYield,"SFOFUncertainty":SFOFUncertainty,"SFOFStatUncertainty":SFOFStatUncertainty,"EEYield":EEsignalYield,"EEsystUncertainty":EEsystUncertainty,"EEstatncertainty":EEstatUncertainty,"MuMuYield":MuMusignalYield,"MuMusystUncertainty":MuMusystUncertainty,"MuMustatUncertainty":MuMustatUncertainty,"EMuYield":EMusignalYield,"EMusystUncertainty":EMusystUncertainty,"EMustatUncertainty":EMustatUncertainty}		
				#~ if m_neutr_1_fix == False:
					#~ outFilePkl = open("shelvesZDecayLeptonScaling/%s_%s.pkl"%(fileName,suffix),"w")
				#~ else:
					#~ outFilePkl = open("shelvesSleptonLeptonScaling/%s_%s.pkl"%(fileName,suffix),"w")
				#~ pickle.dump(counts, outFilePkl)
				#~ outFilePkl.close()
			
			j += 1
		i += 1
		
