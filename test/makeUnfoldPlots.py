#!/usr/bin/python
import sys,os
import array
import ROOT
import time
import math
from optparse import OptionParser

DEBUG=1

ROOT.gROOT.SetBatch()
ROOT.gStyle.SetOptStat(0)
ROOT.gStyle.SetOptTitle(0)

if(DEBUG>0):print "----- BEGIN -----"

if(DEBUG>0):print "-PARSING OPTIONS-"
usage = "usage: %prog [options] arg1 arg2"
parser=OptionParser(usage=usage)
parser.add_option("","--inputDat" ,dest='inputDat',type='string',help="Input Configuration file",default="")
#parser.add_option("","--inputDatMC" ,dest='inputDatMC',type='string',help="Input Configuration file for MC",default="")

(options,args)=parser.parse_args()

print "inserting in path cwd"
sys.path.insert(0,os.getcwd())
print "inserting in path cwd/python"
sys.path.insert(0,os.getcwd()+'/python')
from common import *
from commonRatio import MergeBins,ReadRatioDat
from commonRatio import sqrtSum,makeBands,Ratio

if(DEBUG>0): print "--> load dat file: "+options.inputDat

config=read_dat(options.inputDat)

if(DEBUG>0):
	print "--------- DATA CONFIG -----------"
	PrintDat(config)

#if(DEBUG>0): print "--> load dat file: "+options.inputDatMC

#if options.inputDatMC != "":
#	configMC=read_dat(options.inputDatMC)
doMC=True
#else:
#	doMC=False
#	configMC={}
#if(DEBUG>0):
#	print "--------- DATA MC CONFIG -----------"
#	PrintDat(configMC)

WorkDir=ReadFromDat(config,"WorkDir","./","-->Set Default WDIR")

PtCuts=ReadFromDat(config,"PtCuts",[0,100,200,300],"--> Default PtCuts")

HtCuts=ReadFromDat(config,"HtCuts",[0,100,200,300],"--> Default HtCuts")

nJetsCuts=ReadFromDat(config,"nJetsCuts",[1,3],"--> Default nJetsCuts")

SigPhId=ReadFromDat(config,"SigPhId",[0,0.011],"--> Default SigPhId")

BkgPhId=ReadFromDat(config,"BkgPhId",[0.011,0.014],"--> Default BkgPhId")

inputFileNameUnfold=WorkDir + "/UnfoldedDistributions.root"  

#if doMC:
#	WorkDirMC=ReadFromDat(configMC,"WorkDir","./","-->Set Default WDIR")
#	inputFileMC=WorkDirMC+ReadFromDat(configMC,"outputFileName","output","-->Default Output Name") + ".root"

ROOT.gSystem.Load("libGAnalysis.so") ##for syst names
file= ROOT.TFile.Open(inputFileNameUnfold)
#if doMC:
#	fileMC=ROOT.TFile.Open(inputFileMC)

#def makeBands(h1,h2,type="Mean"):
#	H=h1.Clone(h1.GetName()+"_band")
#	for i in range(1,h1.GetNbinsX()+1):
#		if type=="First":
#			H.SetBinContent(i, h1.GetBinContent(i))
#			H.SetBinError  (i, math.fabs(h1.GetBinContent(i)-h2.GetBinContent(i) ))
#		else: #type = "Mean"
#			H.SetBinContent(i, (h1.GetBinContent(i)+h2.GetBinContent(i) )/2.0)
#			H.SetBinError  (i, math.fabs(h1.GetBinContent(i)-h2.GetBinContent(i) )/2.0)
#	return H

#epsilon=0.0001
#def sqrtSum(h1,h2):
#	for i in range (1,h2.GetNbinsX()+1):
#		if h1.GetBinError(i)  > epsilon and h2.GetBinError(i)  > epsilon:
#			e=math.sqrt( h1.GetBinError(i)**2 + h2.GetBinError(i)**2 )
#		elif h1.GetBinError(i) <= epsilon and h2.GetBinError(i) <= epsilon:
#			e=epsilon
#		elif h1.GetBinError(i) > epsilon:
#			e=h1.GetBinError(i)
#		elif h2.GetBinError(i) > epsilon:
#			e=h2.GetBinError(i)
#		elif ROOT.TMath.IsNaN( h1.GetBinError(i) ) or ROOT.TMath.IsNaN( h2.GetBinError(i) ):
#			e=epsilon
#		else:
#			print "-- assertion error -- %f -- %f -- %f"%(h1.GetBinError(i),h2.GetBinError(i),epsilon)
#			e=epsilon
#		h1.SetBinError(i, e)

#def Ratio(H,H1,NoErrorH=False):
#	R=H1.Clone(H1.GetName()+"_ratio")
#	hTmp=H.Clone("tmp")
#	#in order to account error properly in ratios
#	if NoErrorH:
#		for i in range(1,hTmp.GetNbinsX()+1):
#			hTmp.SetBinError(i,0)
#	R.Divide(hTmp)
#	return R

#LOOP OVER THE BINs
for jpt in [30.0,300.0]:
  for h in range(0,len(HtCuts)):
	for nj in range(0,len(nJetsCuts)):
		if nJetsCuts[nj] != 1 and HtCuts[h] !=0:continue;	
		if jpt!=30 and ( HtCuts[h]!=0 or nJetsCuts[nj]!=1):continue;

		Bin="Ht_"+str(HtCuts[h])+"_nJets_"+str(nJetsCuts[nj])+"_JPt_"+str(jpt)
	
		#GET HISTOS
		H=file.Get("b_Ht_%.1f_nJets_%.1f_JPt_%.1f"%(HtCuts[h],nJetsCuts[nj],jpt))
		H_PUUP    =file.Get("b_Ht_%.1f_nJets_%.1f_JPt_%.1f%s"%(HtCuts[h],nJetsCuts[nj],jpt,ROOT.Analyzer.SystName(ROOT.Analyzer.PUUP)))
		H_PUDN    =file.Get("b_Ht_%.1f_nJets_%.1f_JPt_%.1f%s"%(HtCuts[h],nJetsCuts[nj],jpt,ROOT.Analyzer.SystName(ROOT.Analyzer.PUDN)))
		H_JESUP   =file.Get("b_Ht_%.1f_nJets_%.1f_JPt_%.1f%s"%(HtCuts[h],nJetsCuts[nj],jpt,ROOT.Analyzer.SystName(ROOT.Analyzer.JESUP)))
		H_JESDN   =file.Get("b_Ht_%.1f_nJets_%.1f_JPt_%.1f%s"%(HtCuts[h],nJetsCuts[nj],jpt,ROOT.Analyzer.SystName(ROOT.Analyzer.JESDN)))
		H_SIGSHAPE=file.Get("b_Ht_%.1f_nJets_%.1f_JPt_%.1f%s"%(HtCuts[h],nJetsCuts[nj],jpt,ROOT.Analyzer.SystName(ROOT.Analyzer.SIGSHAPE)))
		H_BKGSHAPE=file.Get("b_Ht_%.1f_nJets_%.1f_JPt_%.1f%s"%(HtCuts[h],nJetsCuts[nj],jpt,ROOT.Analyzer.SystName(ROOT.Analyzer.BKGSHAPE)))
		H_BIAS   =file.Get("b_Ht_%.1f_nJets_%.1f_JPt_%.1f%s"%(HtCuts[h],nJetsCuts[nj],jpt,"_BIAS"))
		H_LUMIUP = H.Clone("b_Ht_%.1f_nJets_%.1f_JPt_%.1f%s"%(HtCuts[h],nJetsCuts[nj],jpt,ROOT.Analyzer.SystName(ROOT.Analyzer.LUMIUP)))
		H_LUMIDN = H.Clone("b_Ht_%.1f_nJets_%.1f_JPt_%.1f%s"%(HtCuts[h],nJetsCuts[nj],jpt,ROOT.Analyzer.SystName(ROOT.Analyzer.LUMIDN)))
		H_LUMIUP.Scale(1.+.026)
		H_LUMIDN.Scale(1.-.026)
		H_JERUP   =file.Get("b_Ht_%.1f_nJets_%.1f_JPt_%.1f%s"%(HtCuts[h],nJetsCuts[nj],jpt,ROOT.Analyzer.SystName(ROOT.Analyzer.JERUP)))
		H_JERDN   =file.Get("b_Ht_%.1f_nJets_%.1f_JPt_%.1f%s"%(HtCuts[h],nJetsCuts[nj],jpt,ROOT.Analyzer.SystName(ROOT.Analyzer.JERDN)))
		H_UNFOLD   =file.Get("b_Ht_%.1f_nJets_%.1f_JPt_%.1f%s"%(HtCuts[h],nJetsCuts[nj],jpt,ROOT.Analyzer.SystName(ROOT.Analyzer.UNFOLD)))
	
		H_PU=makeBands(H_PUUP,H_PUDN)
		H_JES=makeBands(H_JESUP,H_JESDN)
		H_JER=makeBands(H_JERUP,H_JERDN)
		H_SIG=makeBands(H,H_SIGSHAPE,"First")
		H_BKG=makeBands(H,H_BKGSHAPE,"First")
		H_BIAS=makeBands(H,H_BIAS,"First")
		H_LUM=makeBands(H_LUMIUP,H_LUMIDN)
		H_UNFOLD=makeBands(H,H_UNFOLD,"First")
		
		if doMC:
			#print "Going to take MC file: "+"gammaPtGEN_VPt_0_8000_Ht_%.0f_8000_phid_0.000_0.011_nJets_%.0f"%(HtCuts[h],nJetsCuts[nj])
			#H_MC=file.Get("gammaPtGEN_VPt_0_8000_Ht_%.0f_8000_phid_0.000_0.011_nJets_%.0f"%(HtCuts[h],nJetsCuts[nj])); ## phid doesnt count
			H_MC=file.Get("mc_Ht_%.1f_nJets_%.1f_JPt_%.1f"%(HtCuts[h],nJetsCuts[nj],jpt)); ## phid doesnt count
			#for i in range(1,H_MC.GetNbinsX()+1):
			#	H_MC.SetBinContent(i, H_MC.GetBinContent(i)/H_MC.GetBinWidth(i) )
			#	H_MC.SetBinError  (i, H_MC.GetBinError  (i)/H_MC.GetBinWidth(i) )
			H_MC.SetLineColor(ROOT.kBlue)
			#H_MC.SetLineStyle(ROOT.kDashed)
			H_MC.SetLineWidth(2)
			#alreday scaled for lumi in Unfold
			#H_MC.Scale( ReadFromDat(config,"Lumi",1,"Default Lumi=1fb"))
		
		H_TOT=H.Clone("H_TOT")
		sqrtSum(H_TOT,H_PU)
		sqrtSum(H_TOT,H_JES)
		sqrtSum(H_TOT,H_JER)
		#sqrtSum(H_TOT,H_SIG)
		#sqrtSum(H_TOT,H_BKG)
		sqrtSum(H_TOT,H_BIAS)
		sqrtSum(H_TOT,H_LUM)
		sqrtSum(H_TOT,H_UNFOLD)
		for i in range(0,H_TOT.GetNbinsX()+1):
			print "H_TOT: Bin=%d Content=%f Error=%f "%(i,H_TOT.GetBinContent(i),H_TOT.GetBinError(i))
			print "H_PU: Bin=%d Content=%f Error=%f "%(i,H_PU.GetBinContent(i),H_PU.GetBinError(i))
			print "H_JES: Bin=%d Content=%f Error=%f "%(i,H_JES.GetBinContent(i),H_JES.GetBinError(i))
			print "H_JER: Bin=%d Content=%f Error=%f "%(i,H_JER.GetBinContent(i),H_JER.GetBinError(i))
			print "H_SIG: Bin=%d Content=%f Error=%f "%(i,H_SIG.GetBinContent(i),H_SIG.GetBinError(i))
			print "H_BIAS: Bin=%d Content=%f Error=%f "%(i,H_BIAS.GetBinContent(i),H_BIAS.GetBinError(i))
			print "H_BKG: Bin=%d Content=%f Error=%f "%(i,H_BKG.GetBinContent(i),H_BKG.GetBinError(i))
			print "H_LUM: Bin=%d Content=%f Error=%f "%(i,H_LUM.GetBinContent(i),H_LUM.GetBinError(i))
			print "H_UNFOLD: Bin=%d Content=%f Error=%f "%(i,H_UNFOLD.GetBinContent(i),H_UNFOLD.GetBinError(i))
			print "H: Bin=%d Content=%f Error=%f "%(i,H.GetBinContent(i),H.GetBinError(i))
		
		## CANVAS
		C=ROOT.TCanvas("C","C")
		C.SetLogx()
		C.SetLogy()
		
		## PLOT STYLE
		H.SetMarkerStyle(20)
		H.SetMarkerColor(ROOT.kBlack)
		H.SetLineColor(ROOT.kBlack)
	
		H_PU.SetMarkerStyle(0)
		H_PU.SetFillColor  (ROOT.kBlue-4)
		H_PU.SetMarkerColor(ROOT.kBlue-4)
		H_PU.SetLineColor  (ROOT.kBlue-4)
		H_PU.SetFillStyle(3001)
		
		H_JES.SetMarkerStyle(0)
		H_JES.SetFillColor  (ROOT.kGreen-4)
		H_JES.SetMarkerColor(ROOT.kGreen-4)
		H_JES.SetLineColor  (ROOT.kGreen-4)
		H_JES.SetFillStyle(3003)
		
		H_SIG.SetMarkerStyle(0)
		H_SIG.SetFillColor  (ROOT.kMagenta+2)
		H_SIG.SetMarkerColor(ROOT.kMagenta+2)
		H_SIG.SetLineColor  (ROOT.kMagenta+2)
		H_SIG.SetFillStyle(3004)
		
		H_BKG.SetMarkerStyle(0)
		H_BKG.SetFillColor  (ROOT.kRed-4)
		H_BKG.SetMarkerColor(ROOT.kRed-4)
		H_BKG.SetLineColor  (ROOT.kRed-4)
		H_BKG.SetFillStyle(3005)

		H_BIAS.SetMarkerStyle(0)
		H_BIAS.SetFillColor  (ROOT.kGray+2)
		H_BIAS.SetMarkerColor(ROOT.kGray+2)
		H_BIAS.SetLineColor  (ROOT.kGray+2)
		H_BIAS.SetFillStyle(3001)

		H_UNFOLD.SetMarkerStyle(0)
		H_UNFOLD.SetFillColor  (ROOT.kGreen+2)
		H_UNFOLD.SetMarkerColor(ROOT.kGreen+2)
		H_UNFOLD.SetLineColor  (ROOT.kGreen+2)
		H_UNFOLD.SetFillStyle(3010)

		H_LUM.SetMarkerStyle(0)
		H_LUM.SetFillColor  (ROOT.kOrange)
		H_LUM.SetMarkerColor(ROOT.kOrange)
		H_LUM.SetLineColor  (ROOT.kOrange)
		H_LUM.SetFillStyle(3001)

		H_JER.SetMarkerStyle(0)
		H_JER.SetFillColor  (ROOT.kCyan)
		H_JER.SetMarkerColor(ROOT.kCyan)
		H_JER.SetLineColor  (ROOT.kCyan)
		H_JER.SetFillStyle(3006)

		H_TOT.SetLineColor(ROOT.kRed)
		H_TOT.SetLineStyle(ROOT.kDashed)
		H_TOT.SetLineWidth(2)
		H_TOT.SetFillStyle(0);
		H_TOT.SetFillColor(ROOT.kDashed);

		## AXIS
		H.GetXaxis().SetTitle("p_{T}^{#gamma}");
		H.GetYaxis().SetTitle("L #frac{d#sigma}{dp_{T}}[fb^{-1}/GeV]");
		H.GetXaxis().SetMoreLogLabels()
		H.GetXaxis().SetNoExponent()

		#DRAW
		H.Draw("P")
		H.Draw("AXIS X+ Y+ SAME")
		H_UNFOLD.Draw("P E2 SAME")
		H_BKG.Draw("P E2 SAME")
		H_PU.Draw("P E2 SAME")
		H_JES.Draw("P E2 SAME")
		H_JER.Draw("P E2 SAME")
		H_SIG.Draw("P E2 SAME")
		H_BIAS.Draw("P E2 SAME")
		H_LUM.Draw("P E2 SAME")

		if doMC:
			H_MC.Draw("HIST SAME");

		H_TOT.Draw("E3 SAME");

		H.Draw("P SAME") # redraw on top

		## TEXT
		l=ROOT.TLatex()
		l.SetNDC()
		l.SetTextFont(63)
		l.SetTextSize(30)
		l.SetTextAlign(22);
		l.DrawLatex(0.28,.85,"CMS Preliminary")
		l.SetTextFont(43)
		l.SetTextSize(24)
		l.DrawLatex(.28,.80,"#sqrt{s} = 8TeV, #it{L} = 19.7fb^{-1}")
		## LEGEND
	
		if HtCuts[h] == 0:
			Header="N_{jets} #geq %.0f"%(nJetsCuts[nj])
		else:
			Header="H_{T} > %.0f GeV, N_{jets} #geq %.0f"%(HtCuts[h],nJetsCuts[nj])
			
		
		L=ROOT.TLegend(0.65,0.60,.89,.89,Header)
		L.SetFillStyle(0)
		L.SetBorderSize(0)
		L.AddEntry(H,"Data")
		L.AddEntry(H_PU,"PU Syst")
		L.AddEntry(H_JES,"JES Syst")
		L.AddEntry(H_JER,"JER Syst")
		L.AddEntry(H_SIG,"SIG shape Syst")
		L.AddEntry(H_BKG,"BKG shape Syst")
		L.AddEntry(H_BIAS,"BIAS shape Syst")
		L.AddEntry(H_LUM,"LUM shape Syst")
		L.AddEntry(H_UNFOLD,"UNFOLD shape Syst")
		if doMC:
			L.AddEntry(H_MC,"MC")

		L.Draw()
		#SAVE
		C.SaveAs(WorkDir+"plots/unfoldedPlots_Ht%.0f_nJets%.0f_JPt%.0f.pdf"%(HtCuts[h],nJetsCuts[nj],jpt))		
		C.SaveAs(WorkDir+"plots/unfoldedPlots_Ht%.0f_nJets%.0f_JPt%.0f.root"%(HtCuts[h],nJetsCuts[nj],jpt))		

		C2=ROOT.TCanvas("C2","C2")
		C2.SetLogx()

		R_H=Ratio(H,H,NoErrorH=True); R_H.SetMarkerStyle(0)
		R_H.GetYaxis().SetRangeUser(0.5,1.5)
		R_SIG=Ratio(H,H_SIG,NoErrorH=True);
		R_BKG=Ratio(H,H_BKG,True);
		R_BIAS=Ratio(H,H_BIAS,NoErrorH=True);
		R_LUM=Ratio(H,H_LUM,True);
		R_PU=Ratio(H,H_PU,True);
		R_JES=Ratio(H,H_JES,True);
		R_JER=Ratio(H,H_JER,True);
		R_TOT=Ratio(H,H_TOT,True);

		R_H.Draw("P")
		R_H.Draw("AXIS X+ Y+ SAME")
		R_BIAS.Draw("P E2 SAME")
		R_LUM.Draw("P E2 SAME")
		R_BKG.Draw("P E2 SAME")
		R_PU.Draw("P E2 SAME")
		R_JES.Draw("P E2 SAME")
		R_JER.Draw("P E2 SAME")
		R_SIG.Draw("P E2 SAME")
		R_TOT.Draw("E3 SAME")
		
		L.Draw("SAME")

		if doMC:
			R_MC=Ratio(H,H_MC);
			R_MC.Draw("HIST SAME");

		R_H.Draw("P SAME") # redraw on top
		C2.SaveAs(WorkDir+"plots/unfoldedPlotsRatio_Ht%.0f_nJets%.0f_JPt%.0f.pdf"%(HtCuts[h],nJetsCuts[nj],jpt))		

		#------------ NICE CANVAS ----------------------
		C3=ROOT.TCanvas("C3","C3")
		C3.SetLogx()
		C3.SetLogy()


		BinsToMerge=[(750,1000)]
		H=MergeBins(BinsToMerge,H)
		H_TOT=MergeBins(BinsToMerge,H_TOT)

		H.SetMarkerStyle(20)
		H.SetMarkerColor(ROOT.kBlack)
		H.SetLineColor(ROOT.kBlack)

		H_TOT.SetLineColor(ROOT.kOrange)
		H_TOT.SetLineStyle(1)
		H_TOT.SetLineWidth(2)
		#H_TOT.SetFillStyle(0);
		H_TOT.SetFillColor(ROOT.kOrange-4);
		H_TOT.SetFillStyle(3001);


		H.Draw("P")
		H.GetXaxis().SetRangeUser(100,1000)
		H_TOT.GetXaxis().SetRangeUser(100,1000)
		H.GetXaxis().SetNoExponent()
		H.GetXaxis().SetMoreLogLabels()
		#H.GetYaxis().SetNoExponent()
		#H.GetYaxis().SetMoreLogLabels()
		H.GetYaxis().SetTitle("L d#sigma/dp_{T}")
		H.GetXaxis().SetTitle("dp_{T}^{#gamma}")
		H_TOT.Draw("E2 SAME");
		H.Draw("AXIS X+ Y+ SAME")

		if doMC:
			H_MC=MergeBins(BinsToMerge,H_MC)
			H_MC.GetXaxis().SetRangeUser(100,1000)
			H_MC.SetLineColor(ROOT.kBlue+2)
			H_MC.SetLineWidth(2)
			H_MC.SetLineStyle(ROOT.kDashed)
			H_MC.Draw("HIST SAME");


		H.Draw("P SAME") # redraw on top
		## TEXT
		l.SetNDC()
		l.SetTextFont(63)
		l.SetTextSize(30)
		l.SetTextAlign(22);
		l.DrawLatex(0.28,.20,"CMS Preliminary")
		l.SetTextFont(43)
		l.SetTextSize(24)
		l.DrawLatex(.28,.15,"#sqrt{s} = 8TeV, #it{L} = 19.7fb^{-1}")
		## LEGEND
	
		if HtCuts[h] == 0:
			Header="N_{jets} #geq %.0f"%(nJetsCuts[nj])
		else:
			Header="H_{T} > %.0f GeV, N_{jets} #geq %.0f"%(HtCuts[h],nJetsCuts[nj])
			
		
		L=ROOT.TLegend(0.70,0.70,.89,.89,Header)
		L.SetFillStyle(0)
		L.SetBorderSize(0)
		L.AddEntry(H,"Data","PL")
		L.AddEntry(H_TOT,"Stat+Syst","F")
		if doMC:
			L.AddEntry(H_MC,"MC")

		L.Draw()
		C3.RedrawAxis()
		C3.SaveAs(WorkDir+"plots/C3_Ht%.0f_nJets%.0f_JPt%.0f.pdf"%(HtCuts[h],nJetsCuts[nj],jpt))		
		C4=ROOT.TCanvas("C4","C4")
		C4.SetLogx()

		R_H=Ratio(H,H,NoErrorH=True); R_H.SetMarkerStyle(0)
		R_TOT=Ratio(H,H_TOT,True);

		R_H.Draw("P")
		R_H.GetYaxis().SetRangeUser(.5,1.5)
		R_TOT.Draw("E2 SAME")
		R_H.Draw("AXIS X+ Y+ SAME")
		
		L.Draw("SAME")

		if doMC:
			R_MC=Ratio(H,H_MC);
			R_MC.Draw("HIST SAME");

		R_H.Draw("P SAME") # redraw on top
		C4.RedrawAxis()
		C4.SaveAs(WorkDir+"plots/C4_Ht%.0f_nJets%.0f_JPt%.0f.pdf"%(HtCuts[h],nJetsCuts[nj],jpt))

