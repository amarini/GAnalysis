#!/usr/bin/python
import sys,os
import array
import ROOT
import time
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
parser.add_option("","--inputDat" ,dest='inputDat',type='string',help="Input Configuration file MC",default="")

(options,args)=parser.parse_args()

print "inserting in path cwd"
sys.path.insert(0,os.getcwd())
print "inserting in path cwd/python"
sys.path.insert(0,os.getcwd()+'/python')

from common import *

if(DEBUG>0): print "--> load dat file: "+options.inputDat;

config=read_dat(options.inputDat)

if(DEBUG>0):
	PrintDat(config)

WorkDir=ReadFromDat(config,"WorkDir","./","-->Set Default WDIR")

inputFileName=WorkDir+ReadFromDat(config,"outputFileName","output","-->Default Output Name")+".root"

PtCuts=ReadFromDat(config,"PtCuts",[0,100,200,300],"--> Default PtCuts")

HtCuts=ReadFromDat(config,"HtCuts",[0,100,200,300],"--> Default HtCuts")

nJetsCuts=ReadFromDat(config,"nJetsCuts",[1,3],"--> Default nJetsCuts")

SigPhId=ReadFromDat(config,"SigPhId",[0,0.011],"--> Default SigPhId")

BkgPhId=ReadFromDat(config,"BkgPhId",[0.011,0.014],"--> Default BkgPhId")

#OPEN ROOT FILE - INPUT FILE FROM PREVIOUS RUNS
if(DEBUG>0): print "-> Open File "+ inputFileName
	
file=ROOT.TFile.Open( inputFileName )

#signal template binning
###############Configuration ##############
ToFitBin=0
BkgBin=1
SigBin=1
###########################################
#nJets=1
#Ht=0

if(DEBUG>0): print "----- FIT ------"
#ROOT.gSystem.Load("fit.so")
if(DEBUG>0): print "----- Analyzer ------" #for syst name & type
#ROOT.gSystem.Load("Analyzer.so")
ROOT.gSystem.Load("libGAnalysis.so")

if not ((SigBin==1 and BkgBin==1) or (SigBin==0 and BkgBin==0)):
	print "Unable to handle Bins"
	exit

try:PtCuts2=PtCuts[PtCuts.index(-1)+1: ]
except ValueError: PtCuts2=PtCuts

print >>sys.stderr, "PtCuts1=" +str(PtCuts2)

rand=ROOT.TRandom()

def TOY(file,nJets,Ht,Pt1,Pt2,nToys=100):
	if DEBUG>0: 
		print "-> nJets=%d Ht=%.1f"%(nJets,Ht)
		print >>sys.stderr, "STARTING TOYS for: nJets=%d Ht=%.0f Pt1=%.0f Pt2=%.0f"%(nJets,Ht,Pt1,Pt2)

	BkgTemplate=file.Get("photoniso_VPt_%.0f_%.0f_Ht_%.0f_%.0f_phid_%.3f_%.3f_nJets_%d"%(Pt1,Pt2,Ht,8000,BkgPhId[0],BkgPhId[1],nJets)  ) 
	SigTemplate=file.Get("photonisoRC_VPt_%.0f_%.0f_Ht_%.0f_%.0f_phid_%.3f_%.3f_nJets_%d"%(Pt1,Pt2,Ht,8000,SigPhId[0],SigPhId[1],nJets)  ) 
	try:
		NormSig   = SigTemplate.Integral();
		NormBkg   = BkgTemplate.Integral();
	except (ReferenceError, AttributeError) as e:
		print "--> ERROR NULL HISTOS"
		return {}
		
	if DEBUG>0: 
		print "---> Sig Template:" + SigTemplate.GetName()
		print "---> Bkg Template:" + BkgTemplate.GetName()

	if NormSig == 0 or NormBkg == 0 :
		print "-> NUll INTEGRAL"
		return {}	

	R={}

	for purity in [ x/10. for x in range(1,10) ] :
		fractions=[]
		for iToy in range(0,nToys):
			#Build histogram
			SigClone=SigTemplate.Clone("tmp_Sig")
			BkgClone=BkgTemplate.Clone("tmp_Bkg")
			
			SigClone.Sumw2()
			BkgClone.Sumw2()

			SigClone.Scale(1./SigClone.Integral() * purity)
			BkgClone.Scale(1./BkgClone.Integral() * (1.-purity))

			ToFitTemplate=SigClone.Clone("toFit")
			ToFitTemplate.Add(BkgClone)
	
			for iBin in range(1,SigClone.GetNbinsX()+1):
				SigClone.SetBinContent(iBin,  ROOT.TMath.Max(rand.Gaus(SigClone.GetBinContent(iBin),SigClone.GetBinError(iBin)),0) ) ##TODO RANDOM GAUS
				BkgClone.SetBinContent(iBin,  ROOT.TMath.Max(rand.Gaus(BkgClone.GetBinContent(iBin),BkgClone.GetBinError(iBin)),0)) ##TODO RANDOM GAUS 
				#SigClone.SetBinContent(iBin,  rand.Poisson(SigClone.GetBinContent(iBin))) ##TODO RANDOM  POISSON
				#BkgClone.SetBinContent(iBin,  rand.Poisson(BkgClone.GetBinContent(iBin))) ##TODO RANDOM  POISSON
				ToFitTemplate.SetBinContent(iBin,ROOT.TMath.Max(rand.Gaus(ToFitTemplate.GetBinContent(iBin),ToFitTemplate.GetBinError(iBin)),0) )
				
			#variation on Sig Bkg and Template	
			f=ROOT.FIT.fit(ToFitTemplate,SigClone,BkgClone,"","")
			fractions.append(f)
		##
		P1=ROOT.std.pair(float,float)()
		P2=ROOT.std.pair(float,float)()
		vFractions=ROOT.std.vector(float)()
		for f in fractions: vFractions.push_back(f)	
		ROOT.STAT.ConfidenceInterval(vFractions,P1,0.68)
		ROOT.STAT.ConfidenceInterval(vFractions,P2,0.95)
		mean=ROOT.STAT.mean(vFractions)
		rms=ROOT.STAT.rms(vFractions)
		R[ (Pt1,Pt2,purity) ] = (mean,rms,P1.first,P1.second,P2.first,P2.second)
	return R;

AllGraph={}
tmp=ROOT.TCanvas("tmp","tmp")
for h in HtCuts:
	for nj in nJetsCuts:
		if nj!=1 and h!=0: continue; ##don't overlap cuts in njets & ht
		ToysResults={}
		tmp.cd()
		for p in range(0,len(PtCuts2)-1):
			R=TOY(file,int(nj),h,PtCuts2[p],PtCuts2[p+1],100) #num of toys
			for key in R: ToysResults[ key ] = R[ key ];

		for (Pt1,Pt2,purity) in ToysResults:
			name="biasPurity1s_Ht"+str(h)+"_nJets"+str(nj)+"_Purity"+str(purity)
			name2="biasPurity2s_Ht"+str(h)+"_nJets"+str(nj)+"_Purity"+str(purity)
			try:
				g1=AllGraph[name]
				g2=AllGraph[name2]
			except KeyError:
				g1=ROOT.TGraphAsymmErrors()
				g1.SetName(name)
				g2=ROOT.TGraphAsymmErrors()
				g2.SetName(name2)
				AllGraph[g1.GetName()]=g1 ## Preserve histograms from delete
				AllGraph[g2.GetName()]=g2
			n=g1.GetN()
			(mean,rms,eyl,eyh,e2yl,e2yh)= ToysResults[ (Pt1,Pt2,purity) ]
			g1.SetPoint(n,(Pt1+Pt2)/2.0,mean)
			g2.SetPoint(n,(Pt1+Pt2)/2.0,mean)
			g1.SetPointError(n,(Pt2-Pt1)/2,(Pt2-Pt1)/2.,eyl,eyh)
			g2.SetPointError(n,(Pt2-Pt1)/2.,(Pt2-Pt1)/2,e2yl,e2yh)
			n+=1
			print >>sys.stderr, "--- Pt=[%.0f,%.0f] Purity=%.1f%% values=[%.2f,%.2f,%.2f]%%"%(Pt1,Pt2,purity,mean,eyl,eyh)
		
			print >> sys.stderr, "Graph "+g1.GetName()+" Has " + str(n) + " points"

			
C=ROOT.TCanvas("c","c")
C.SetLogx()
for h in HtCuts:
	for nj in nJetsCuts:
		if nj!=1 and h!=0: continue; ##don't overlap cuts in njets & ht
		for purity in [ x/10. for x in range(1,10) ] :
			g1=AllGraph["biasPurity1s_Ht"+str(h)+"_nJets"+str(nj)+"_Purity"+str(purity)]
			g2=AllGraph["biasPurity2s_Ht"+str(h)+"_nJets"+str(nj)+"_Purity"+str(purity)]
			if nj==1 and h==0 and purity==0.1:
				g1.Draw("A P");
	
			g1.GetYaxis().SetRangeUser(0,1);
			g1.GetYaxis().SetTitle("Purity");
			g1.GetXaxis().SetTitle("p_{T}^{#gamma}");
			g1.GetXaxis().SetNoExponent()
			g1.GetXaxis().SetMoreLogLabels()
	
			g1.SetFillColor(ROOT.kGreen)
			g2.SetFillColor(ROOT.kYellow)
	
			g1.SetFillStyle(3001)
			g2.SetFillStyle(3001)
	
			g1.SetMarkerStyle(20)
			
			C.cd()
	
			g2.Draw("P 2 SAME")
			g1.Draw("P 2 SAME")

C.SaveAs(WorkDir+"/plots/Bias.pdf")
f=ROOT.TFile.Open(WorkDir+"/plots/Bias.root","RECREATE")
f.cd()
C.Write()
for key in AllGraph: AllGraph[key].Write()

if(DEBUG>0): print "----- END ------"
