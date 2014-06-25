#!/usr/bin/python
import sys,os
import array
import time
import math
from optparse import OptionParser

DEBUG=1

if(DEBUG>0):print "-PARSING OPTIONS-"
usage = "usage: %prog [options] arg1 arg2"
parser=OptionParser(usage=usage)
parser.add_option("","--inputDat" ,dest='inputDat',type='string',help="Input Configuration file",default="")
parser.add_option("","--inputDatMC" ,dest='inputDatMC',type='string',help="MC Input Configuration file",default="")

(options,args)=parser.parse_args()

import ROOT

ROOT.gROOT.SetBatch()
ROOT.gStyle.SetOptStat(0)
ROOT.gStyle.SetOptTitle(0)

if(DEBUG>0):print "----- BEGIN -----"


print "inserting in path cwd"
sys.path.insert(0,os.getcwd())
print "inserting in path cwd/python"
sys.path.insert(0,os.getcwd()+'/python')
from common import *

if(DEBUG>0): print "----- Analyzer ------" #for syst name & type
ROOT.gSystem.Load("libGAnalysis.so")

if(DEBUG>0): print "--> load dat file: "+options.inputDat

config=read_dat(options.inputDat)

if(DEBUG>0):
	print "--------- DATA CONFIG -----------"
	PrintDat(config)

WorkDir=ReadFromDat(config,"WorkDir","./","-->Set Default WDIR")

PtCuts=ReadFromDat(config,"PtCuts",[0,100,200,300],"--> Default PtCuts")

HtCuts=ReadFromDat(config,"HtCuts",[0,100,200,300],"--> Default HtCuts")

nJetsCuts=ReadFromDat(config,"nJetsCuts",[1,3],"--> Default nJetsCuts")

SigPhId=ReadFromDat(config,"SigPhId",[0,0.011],"--> Default SigPhId")

BkgPhId=ReadFromDat(config,"BkgPhId",[0.011,0.014],"--> Default BkgPhId")

inputFileNameFit=WorkDir + "/fit.txt" 

doMC=False
if not options.inputDatMC == "": 
	doMC=True
	if(DEBUG>0): print "--> load dat file: "+options.inputDatMC
	configMC=read_dat(options.inputDatMC)
	if(DEBUG>0):
        	print "--------- MC CONFIG -----------"
        	PrintDat(configMC)
	WorkDirMC=ReadFromDat(configMC,"WorkDir","./","-->Set Default MC WDIR")
	inputFile=WorkDirMC+ReadFromDat(configMC,"outputFileName","output","-->Set Default Output") + ".root"
	fMC=ROOT.TFile.Open(inputFile)
	

inputFile=WorkDir+ReadFromDat(config,"outputFileName","output","-->Set Default Output") + ".root"
fRoot=ROOT.TFile.Open(inputFile)
#fRoot.ls()

if DEBUG>0 : print "--> Read File"
fFit= open(inputFileNameFit,"r")

if DEBUG>0:print "--> Read Fraction"
#READ FITTED FRACTION IN A DATABASE
#Pt 43.5 48.3 Ht 0.0 nJets 1 Fraction= 0.528608322144 ERROR= 0.000138673000038
Frac={};
FracBias={};
FracErr={};
for line in fFit:
	#exclude not well done lines
	if '#' in line : continue
	if len(line) <5 : continue
	l=line.split(' ')
	for iWord in range(0,len(l)):
		if "Pt" == l[iWord] :
			ptmin= round(float(l[iWord+1]),1)
			ptmax= round(float(l[iWord+2]),1)
		elif "Ht" in l[iWord]:
			ht=float(l[iWord+1])
		elif "nJets" in l[iWord]:
			nj=float(l[iWord+1])
		elif "jetPt" in l[iWord]:
			jpt=float(l[iWord+1])
		elif "Fraction" in l[iWord]:
			fr=float(l[iWord+1])
		elif "TOYS" in l[iWord]: #read error from toys
			er=float(l[iWord+1])
		elif "BIAS" in l[iWord]: #read error from toys
			bias=float(l[iWord+1])
	try:
		Frac[ (ptmin,ptmax,ht,nj,jpt) ] = fr
	except NameError: continue;
	try:
		FracErr[ (ptmin,ptmax,ht,nj,jpt) ] = er
	except NameError: pass;
	try:
		FracBias[ (ptmin,ptmax,ht,nj,jpt) ] = bias
	except NameError: continue;

#Float_t * is needed for TH1D
ROOT.gROOT.ProcessLine("struct Bins{ \
		Double_t PtBins[1023];\
		};")

from ROOT import Bins
PtBins=ROOT.Bins()

#LOOP OVER THE BINs
AllH={}
AllHBias={}
AllHMC={}
AllHCorrected={}
C=ROOT.TCanvas("C","C")
C2=ROOT.TCanvas("C2","C2")
L=ROOT.TLegend(0.65,0.15,.89,.45)
L.SetFillStyle(0)
L.SetBorderSize(0)
C.SetLogx()
jpt=30.
for h in range(0,len(HtCuts)):
	for nj in range(0,len(nJetsCuts)):
		if nJetsCuts[nj] != 1 and HtCuts[h] !=0:continue;	
		if nJetsCuts[nj] != 1 or HtCuts[h] !=0 : continue; # ONLY for inclusive
		#CREATE TARGET HISTO
		try:
			PtCuts2_tmp=PtCuts[0:PtCuts.index(-1) ]
		except ValueError: PtCuts2_tmp=PtCuts

		PtCuts2=[]
		for pt in PtCuts2_tmp:
			PtCuts2.append(round(pt,1));

		for c in range(0,len(PtCuts2)):
			PtBins.PtBins[c]=PtCuts2_tmp[c] ## bin for histo with high precision
		Bin="Ht_"+str(HtCuts[h])+"_nJets_"+str(nJetsCuts[nj])
		#Will it work?
		H=ROOT.TH1D("f_"+Bin,"Fraction_"+Bin , len(PtCuts2)-1 , PtBins.PtBins )
		HCorrected=ROOT.TH1D("fCorr_"+Bin,"Fraction_"+Bin , len(PtCuts2)-1 , PtBins.PtBins )
		HBias=ROOT.TH1D("bias_"+Bin,"Bias_"+Bin , len(PtCuts2)-1 , PtBins.PtBins )
		HCorrectedBias=ROOT.TH1D("biasiCorr_"+Bin,"Bias_"+Bin , len(PtCuts2)-1 , PtBins.PtBins )

		if doMC:
			HMC=ROOT.TH1D("mc_"+Bin,"Fraction_"+Bin , len(PtCuts2)-1 , PtBins.PtBins )

		for p in range(0,len(PtCuts2)-1):
			## TAKE FITTED FRACTION
			try:
				fr=Frac[ (PtCuts2[p],PtCuts2[p+1],HtCuts[h],nJetsCuts[nj],jpt) ]
			except (IndexError,KeyError): 
				print "ERROR IN FRACTION: Pt %.1f %.1f Ht %.0f nJ %.0f JetPt %.0f"%(PtCuts2[p],PtCuts2[p+1],HtCuts[h],nJetsCuts[nj],jpt)
				fr=1	
			try:
				er=FracErr[ (PtCuts2[p],PtCuts2[p+1],HtCuts[h],nJetsCuts[nj],jpt) ]
			except (IndexError,KeyError): 
				print "ERROR IN ERR: Pt %.1f %.1f Ht %.0f nJ %.0f JetPt %.0f"%(PtCuts2[p],PtCuts2[p+1],HtCuts[h],nJetsCuts[nj],jpt)
				er=1	
			try:
				bias=FracBias[ (PtCuts2[p],PtCuts2[p+1],HtCuts[h],nJetsCuts[nj],jpt) ]
			except (IndexError,KeyError): 
				print "ERROR IN BIAS: Pt %.1f %.1f Ht %.0f nJ %.0f JetPt %.0f"%(PtCuts2[p],PtCuts2[p+1],HtCuts[h],nJetsCuts[nj],jpt)
				bias=1	

			H.SetBinContent( H.FindBin( (PtCuts2[p]+PtCuts2[p+1])/2.), fr )
			H.SetBinError( H.FindBin( (PtCuts2[p]+PtCuts2[p+1])/2.), er )

			HBias.SetBinContent( H.FindBin( (PtCuts2[p]+PtCuts2[p+1])/2.), bias )

			if doMC:
				RU= fMC.Get("gammaPt_RECO_UNFOLD_VPt_0_8000_Ht_%.0f_8000_phid_%.3f_%.3f_nJets_%d"%(HtCuts[h],SigPhId[0],SigPhId[1],nJetsCuts[nj]))
				RE= fMC.Get("gammaPt_VPt_%.0f_%.0f_Ht_%.0f_8000_phid_%.3f_%.3f_nJets_%d"%(PtCuts2[p],PtCuts2[p+1],HtCuts[h],SigPhId[0],SigPhId[1],nJetsCuts[nj]))
				try:
					frmc= RU.GetBinContent( RU.FindBin((PtCuts2[p]+PtCuts2[p+1])/2.) ) / RE.Integral()
				except AttributeError: 
					print "--ERROR in MC Fraction: Pt %.0f Ht %.0f nJets %d"%(PtCuts2[p],HtCuts[h],nJetsCuts[nj])
					frmc=0
				HMC.SetBinContent( HMC.FindBin((PtCuts2[p]+PtCuts2[p+1])/2.) , frmc)

				# compute correction
			doEffCorr=True
			if doEffCorr:
				Ht=HtCuts[h]
				nJets=int(nJetsCuts[nj])
				cutSig=ROOT.Analyzer.CUTS(PtCuts[p],PtCuts[p+1],Ht,8000,SigPhId[0],SigPhId[1],nJets);
				IsoSig=fRoot.Get("photonisoRC_"+cutSig.name())
				cutBkg=ROOT.Analyzer.CUTS(PtCuts[p],PtCuts[p+1],Ht,8000,BkgPhId[0],BkgPhId[1],nJets);
				IsoBkg=fRoot.Get("photoniso_"+cutBkg.name())
			
				sigeff=0
				bkgeff=1
				bincut=-1
				if IsoSig!=None:
					bincut=IsoSig.FindBin(0.7+0.005*PtCuts2[p])
					sigeff=IsoSig.Integral(1,bincut)/IsoSig.Integral()
					sigefferr=math.sqrt(sigeff*(1-sigeff)/IsoSig.Integral() )
				else:
					print "ERROR NO SIGEFF"
				if IsoBkg!=None:
					bincut=IsoBkg.FindBin(0.7+0.005*PtCuts2[p])
					bkgeff=IsoBkg.Integral(1,bincut)/IsoBkg.Integral()
					bkgefferr=math.sqrt(bkgeff*(1-bkgeff)/IsoBkg.Integral() )
				else:
					print "ERROR NO BKGEFF"
				if fr<1 and bkgeff>0 and IsoBkg and IsoSig:
					newpurity=fr * sigeff / (  (1.-fr)*bkgeff + fr*sigeff) 
					den= (1.-fr)*bkgeff + fr*sigeff
					newerror=math.sqrt( (er/fr*newpurity)**2 + (sigefferr * (fr*den - fr*fr*sigeff)/(den**2) )**2 + (bkgefferr * ((1.-fr)*fr*sigeff)/(den**2))**2 )
					#newerror=(er/fr)*newpurity
				else:
					print "PURITY ERROR"
					newpurity=0
				if nj==0 and h==0:
					print  "Bin",PtCuts2[p],PtCuts2[p+1],"=",PtCuts[p],PtCuts[p+1]
					if IsoSig!=None : print "Cut is", bincut,IsoSig.GetBinLowEdge(bincut+1)
					print "Template Sig is","photonisoRC_"+cutSig.name()
					print "Template Bkg is","photoniso_"+cutBkg.name()
					print "SigEff is", sigeff
					print "BkgEff is", bkgeff
					if fr<1 and bkgeff>0:
						print "Purity was",fr,"and now is",newpurity 
				if fr<1 and bkgeff>0:
					HCorrected.SetBinContent( H.FindBin( (PtCuts2[p]+PtCuts2[p+1])/2.), newpurity)
					HCorrected.SetBinError( H.FindBin( (PtCuts2[p]+PtCuts2[p+1])/2.), newerror)
				else:
					HCorrected.SetBinContent( H.FindBin( (PtCuts2[p]+PtCuts2[p+1])/2.), 0)
					HCorrected.SetBinError( H.FindBin( (PtCuts2[p]+PtCuts2[p+1])/2.), 1)

		## PLOT HISTOS
		if   HtCuts[h] == 0 and nJetsCuts[nj]==1:
			H.SetMarkerColor(ROOT.kBlack)
			H.SetMarkerStyle(20)
			HCorrected.SetMarkerColor(ROOT.kBlack)
			HCorrected.SetMarkerStyle(20)
			if doMC: 
				HMC.SetLineColor(ROOT.kBlack)
				HMC.SetLineWidth(2)
				HMC.SetLineStyle(ROOT.kDashed)
			HBias.SetLineColor(ROOT.kBlack)
			HBias.SetLineWidth(2)
			HBias.SetLineStyle(3)
		elif HtCuts[h] == 100 and nJetsCuts[nj]==1:
			H.SetMarkerColor(ROOT.kRed+1)
			H.SetLineColor(ROOT.kRed+1)
			H.SetMarkerStyle(33)
			HCorrected.SetMarkerColor(ROOT.kRed+1)
			HCorrected.SetLineColor(ROOT.kRed+1)
			HCorrected.SetMarkerStyle(33)
			if doMC: 
				HMC.SetLineColor(ROOT.kRed)
				HMC.SetLineWidth(2)
				HMC.SetLineStyle(ROOT.kDashed)
			HBias.SetLineColor(ROOT.kRed+1)
			HBias.SetLineWidth(2)
			HBias.SetLineStyle(3)
		elif HtCuts[h] == 300 and nJetsCuts[nj]==1:
			H.SetMarkerColor(ROOT.kBlue-3)
			H.SetLineColor(ROOT.kBlue-3)
			H.SetMarkerStyle(29)
			HCorrected.SetMarkerColor(ROOT.kBlue-3)
			HCorrected.SetLineColor(ROOT.kBlue-3)
			HCorrected.SetMarkerStyle(29)
			if doMC: 
				HMC.SetLineColor(ROOT.kBlue-3)
				HMC.SetLineWidth(2)
				HMC.SetLineStyle(ROOT.kDashed)
			HBias.SetLineColor(ROOT.kBlue-3)
			HBias.SetLineWidth(2)
			HBias.SetLineStyle(3)
		elif HtCuts[h] == 0 and nJetsCuts[nj]==3:
			H.SetMarkerColor(ROOT.kGreen+2)
			H.SetLineColor(ROOT.kGreen+2)
			H.SetMarkerStyle(21)
			H.SetMarkerSize(0.8)
			HCorrected.SetMarkerColor(ROOT.kGreen+2)
			HCorrected.SetLineColor(ROOT.kGreen+2)
			HCorrected.SetMarkerStyle(21)
			HCorrected.SetMarkerSize(0.8)
			if doMC: 
				HMC.SetLineColor(ROOT.kGreen+2)
				HMC.SetLineWidth(2)
				HMC.SetLineStyle(ROOT.kDashed)
			HBias.SetLineColor(ROOT.kGreen+2)
			HBias.SetLineWidth(2)
			HBias.SetLineStyle(3)
		else:
			H.SetMarkerStyle(25)
		#DRAW
		H.SetFillStyle(0);
		H.SetFillColor(H.GetLineColor());
		HCorrected.SetFillStyle(0);
		HCorrected.SetFillColor(H.GetLineColor());
		C.cd()
		if   h== 0 and nj==0:
			print "Draw"
			H.GetXaxis().SetTitle("p_{T}^{#gamma}");
			H.GetYaxis().SetTitle("Purity");
			H.GetXaxis().SetMoreLogLabels()
			H.GetXaxis().SetNoExponent()
			H.GetYaxis().SetRangeUser(0,1);
			H.GetXaxis().SetRangeUser(100,1000);
			H.Draw("P E4")
		else:
			print "Draw h"+str(h)+" nj"+str(nj)
			H.Draw("P E4 SAME")
		#HBias.Draw("HIST SAME")

		if doMC:
			HMC.Draw("HIST SAME")
			AllHMC[ (h,nj) ] = HMC

		L.AddEntry(H,"H_{T}>"+str(HtCuts[h])+" N_{jets}#geq"+str(nJetsCuts[nj]))

		C2.cd()
		if   h== 0 and nj==0:
			H.GetYaxis().SetRangeUser(0,1);
			H.GetXaxis().SetRangeUser(40,1000);
			H.Draw("AXIS")
		HCorrected.Draw("P E4 SAME")
		
		AllHBias[ (h,nj) ] = HBias
		AllH[ (h,nj) ] = H
		AllHCorrected[ (h,nj) ] = HCorrected
C.cd()
L.Draw()
C.SaveAs(WorkDir+"plots/fraction.pdf")		
C.SaveAs(WorkDir+"plots/fraction.root")		
C2.cd()
L.Draw()
C2.SaveAs(WorkDir+"plots/fraction_corrected.pdf")		
C2.SaveAs(WorkDir+"plots/fraction_corrected.root")		

#### NICE  ###

C3=ROOT.TCanvas("C3","C3",800,800)
C3.SetRightMargin(0.10)
C3.SetTopMargin(0.10)
C3.SetLeftMargin(0.13)
C3.SetBottomMargin(0.13)
#bin, not value
b=(0,0)
AllHCorrected[ b ].GetXaxis().SetRangeUser(50,500)
AllHCorrected[ b ].GetYaxis().SetRangeUser(0.6,1.0)
AllHCorrected[ b ].GetXaxis().SetTitle("p_{T}^{#gamma}")
AllHCorrected[ b ].GetYaxis().SetTitle("purity")
AllHCorrected[ b ].GetYaxis().SetTitleOffset(1.8)
AllHCorrected[ b ].GetXaxis().SetTitleOffset(1.5)
AllHCorrected[ b ].GetYaxis().SetLabelOffset(0.015)
AllHCorrected[ b ].GetXaxis().SetLabelOffset(0.015)
AllHCorrected[ b ].GetYaxis().SetDecimals()
AllHCorrected[ b ].SetMarkerSize(1.5)
AllHCorrected[ b ].SetLineColor(ROOT.kBlack)
AllHCorrected[ b ].Draw("P")
#AllHBias[ b ].SetLineWidth(2)
#AllHBias[ b ].SetLineColor(ROOT.kBlack)
#AllHBias[ b ].SetLineStyle(ROOT.kDashed)
#AllHBias[ b ].GetXaxis().SetRangeUser(100,1000)
#AllHBias[ b ].GetYaxis().SetRangeUser(0.6,1.0)
#for i in range(1,AllHBias[ b ].GetNbinsX()+1):
#	print AllHBias[ b ].GetBinCenter(i)," -> ",AllHBias[ b ].GetBinContent(i)

#f2=ROOT.TF1("func","[0] * TMath::TanH(  TMath::Sqrt( (x-[1])/[2]) ) ",0,1000)
#f2.SetParameter(0,1)
#f2.SetParameter(1,100)
#f2.SetParameter(2,100)
#f2.SetParLimits(1,30,200)
#f2.SetParLimits(2,30,200)
#AllH[ b ].Fit("func");
#f2.Draw("SAME")
#AllHBias[ b ].Draw("HIST ][ SAME")

l=ROOT.TLatex()
l.SetNDC()
l.SetTextAlign(11)
l.SetTextFont(63)
l.SetTextSize(28)
l.DrawLatex(0.15,0.86,"CMS")
l.SetTextFont(53)
l.SetTextSize(20)
l.DrawLatex(0.23,0.86,"Preliminary")
l.SetTextFont(43)
l.SetTextSize(20)
l.SetTextAlign(31)
l.DrawLatex(0.89,0.91,"19.7 fb^{-1}(8TeV)")

C3.SaveAs(WorkDir+"plots/fraction2_Corrected.pdf")
C3.SaveAs(WorkDir+"plots/fraction2_Corrected.root")
C3.SaveAs(WorkDir+"plots/fraction2_Corrected.png")

