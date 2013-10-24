#!/usr/bin/python
import sys,os
import array
import ROOT
import time
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

(options,args)=parser.parse_args()

print "inserting in path cwd"
sys.path.insert(0,os.getcwd())
print "inserting in path cwd/python"
sys.path.insert(0,os.getcwd()+'/python')
from common import *

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


if DEBUG>0 : print "--> Read File"
fFit= open(inputFileNameFit,"r")

if DEBUG>0:print "--> Read Fraction"
#READ FITTED FRACTION IN A DATABASE
#Pt 43.5 48.3 Ht 0.0 nJets 1 Fraction= 0.528608322144 ERROR= 0.000138673000038
Frac={};
for line in fFit:
	#exclude not well done lines
	if '#' in line : continue
	if len(line) <5 : continue
	l=line.split(' ')
	for iWord in range(0,len(l)):
		if "Pt" in l[iWord] :
			ptmin=float(l[iWord+1])
			ptmax=float(l[iWord+2])
		elif "Ht" in l[iWord]:
			ht=float(l[iWord+1])
		elif "nJets" in l[iWord]:
			nj=float(l[iWord+1])
		elif "Fraction" in l[iWord]:
			fr=float(l[iWord+1])
		elif "ERROR" in l[iWord]:
			er=float(l[iWord+1])
	try:
		Frac[ (ptmin,ptmax,ht,nj) ] = fr
	except NameError: continue;

#Float_t * is needed for TH1F
ROOT.gROOT.ProcessLine("struct Bins{ \
		Float_t PtBins[1023];\
		};")

from ROOT import Bins
PtBins=ROOT.Bins()

#LOOP OVER THE BINs
AllH={}
C=ROOT.TCanvas("C","C")
L=ROOT.TLegend(0.65,0.15,.89,.45)
L.SetFillStyle(0)
L.SetBorderSize(0)
for h in range(0,len(HtCuts)):
	for nj in range(0,len(nJetsCuts)):
		if nJetsCuts[nj] != 1 and HtCuts[h] !=0:continue;	
		#CREATE TARGET HISTO
		try:
			PtCuts2=PtCuts[0:PtCuts.index(-1) ]
		except ValueError: PtCuts2=PtCuts

		for c in range(0,len(PtCuts2)):
			PtBins.PtBins[c]=PtCuts2[c]
		Bin="Ht_"+str(HtCuts[h])+"_nJets_"+str(nJetsCuts[nj])
		#Will it work?
		H=ROOT.TH1F("f_"+Bin,"Fraction_"+Bin , len(PtCuts2)-1 , PtBins.PtBins )

		for p in range(0,len(PtCuts2)-1):
			## TAKE FITTED FRACTION
			try:
				fr=Frac[ (PtCuts[p],PtCuts[p+1],HtCuts[h],nJetsCuts[nj]) ]
			except (IndexError,KeyError): 
				print "ERROR IN FRACTION: Pt %.1f %.1f Ht %.0f nJ %.0f"%(PtCuts[p],PtCuts[p+1],HtCuts[h],nJetsCuts[nj])
				fr=1	
			H.SetBinContent( H.FindBin( (PtCuts[p]+PtCuts[p+1])/2.), fr )
		## PLOT HISTOS
		if   HtCuts[h] == 0 and nJetsCuts[nj]==1:
			H.SetMarkerColor(ROOT.kBlack)
			H.SetMarkerStyle(20)
		elif HtCuts[h] == 100 and nJetsCuts[nj]==1:
			H.SetMarkerColor(ROOT.kRed+1)
			H.SetMarkerStyle(33)
		elif HtCuts[h] == 300 and nJetsCuts[nj]==1:
			H.SetMarkerColor(ROOT.kBlue-3)
			H.SetMarkerStyle(29)
		elif HtCuts[h] == 0 and nJetsCuts[nj]==3:
			H.SetMarkerColor(ROOT.kGreen+2)
			H.SetMarkerStyle(21)
			H.SetMarkerSize(0.8)
		else:
			H.SetMarkerStyle(25)
		#DRAW
		if   h== 0 and nj==0:
			print "Draw"
			H.GetXaxis().SetTitle("p_{T}^{#gamma}");
			H.GetYaxis().SetTitle("Purity");
			H.Draw("P")
		else:
			print "Draw h"+str(h)+" nj"+str(nj)
			H.Draw("P SAME")

		L.AddEntry(H,"H_{T}>"+str(HtCuts[h])+" N_{jets}#geq"+str(nJetsCuts[nj]))

		AllH[ (h,nj) ] = H
L.Draw()
wait = raw_input("PRESS ENTER TO CONTINUE.")
C.SaveAs(WorkDir+"/fraction.pdf")		
C.SaveAs(WorkDir+"/fraction.root")		
