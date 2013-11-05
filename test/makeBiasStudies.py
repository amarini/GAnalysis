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
ROOT.gSystem.Load("fit.so")
if(DEBUG>0): print "----- Analyzer ------" #for syst name & type
ROOT.gSystem.Load("Analyzer.so")

if not ((SigBin==1 and BkgBin==1) or (SigBin==0 and BkgBin==0)):
	print "Unable to handle Bins"
	exit

try:PtCuts2=PtCuts[PtCuts.index(-1)+1: ]
except ValueError: PtCuts2=PtCuts

rand=ROOT.TRandom()

def TOY(file,nJets,Ht,Pt1,Pt2,nToys=100):
	if DEBUG>0: 
		print "-> nJets=%d Ht=%.1f"%(nJets,Ht)

	BkgTemplate(file.Get("photoniso_VPt_%.0f_%.0f_Ht_%.0f_%.0f_phid_%.3f_%.3f_nJets_%d"%(Pt1,Pt2,Ht,8000,BkgPhId[0],BkgPhId[1],nJets)  ) )
	SigTemplate(file.Get("photonisoRC_VPt_%.0f_%.0f_Ht_%.0f_%.0f_phid_%.3f_%.3f_nJets_%d"%(Pt1,Pt2,Ht,8000,SigPhId[0],SigPhId[1],nJets)  ) )
	try:
		NormSig   = SigTemplate.Integral();
		NormBkg   = BkgTemplate.Integral();
	except (ReferenceError, AttributeError) as e:
		print "--> ERROR NULL HISTOS"
		return {}
		
	if DEBUG>0: 
		print "---> Sig Template:" + SigTemplate.GetName()
		print "---> Bkg Template:" + BkgTemplate.GetName()

	if NormToFit == 0 or NormSig == 0 or NormBkg == 0 :
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
				#SigClone.SetBinContent(iBin,  rand->Gaus(SigClone.GetBinContent(iBin),SigClone.GetBinError(iBin)) ##TODO RANDOM GAUS
				#BkgClone.SetBinContent(iBin,  rand->Gaus(BkgClone.GetBinContent(iBin),BkgClone.GetBinError(iBin)) ##TODO RANDOM GAUS 
				SigClone.SetBinContent(iBin,  rand->Poisson(SigClone.GetBinContent(iBin)) ##TODO RANDOM  POISSON
				BkgClone.SetBinContent(iBin,  rand->Poisson(BkgClone.GetBinContent(iBin)) ##TODO RANDOM  POISSON
				ToFitTemplate.SetBinContent(iBin,ROOT.TMath.Max(rand->Gaus(ToFitTemplate.GetBinContent(iBin),ToFitTemplate.GetBinError(iBin),0))
				
			#variation on Sig Bkg and Template	
			f=ROOT.FIT.fit(ToFitTemplate,SigClone,BkgClone,"","")
			fractions.append(f)
		##
		P1=ROOT.std.pair(float,float)()
		P2=ROOT.std.pair(float,float)()
		ROOT.STAT.ConfidenceInterval(fractions,P1,0.68)
		ROOT.STAT.ConfidenceInterval(fractions,P2,0.95)
		mean=ROOT.STAT.mean(fractions)
		rms=ROOT.STAT.rms(fractions)
		R[ (Pt1,Pt2,purity) ] = (mean,rms,P1.first,P1.second,P2.first,P2.second)
	return R;

C=ROOT.TCanvas("c","c")
C.SetLogx()
AllGraph=[]
for h in HtCuts:
	for n in nJetsCuts:
		if n!=1 and h!=0: continue; ##don't overlap cuts in njets & ht
		ToysResults={}
		for p in range(0,len(PtCuts2)-1):
			R=TOYS(file,int(n),h,PtCuts2[p],PtCuts2[p+1],100) #num of toys
			for key in R: ToysResults[ key ] = R[ key ];
		g1=ROOT.TGraphAsymmetricErrors()
		g1.SetName("biasPurity_Ht"+str(h)+"_nJets"+str(n))
		g2=ROOT.TGraphAsymmetricErrors()
		g2.SetName("biasPurity2_Ht"+str(h)+"_nJets"+str(n))
		n=0
		for (Pt1,Pt2,purity) in R:
			(mean,rms,eyl,eyh,e2yl,e2yh)= R[ (Pt1,Pt2,purity) ]
			g1.SetPoint(n,(Pt1+Pt2)/2.0,mean)
			g2.SetPoint(n,(Pt1+Pt2)/2.0,mean)
			g1.SetPointError(n,Pt1,Pt2,eyl,eyh)
			g2.SetPointError(n,Pt1,Pt2,e2yl,e2yh)
			n+=1
		g1.SetFillColor(kGreen)
		g2.SetFillColor(kYellow)
		g1.SetFillStyle(3001)
		g2.SetFillStyle(3001)
		
		if n==1 and h==0:
			g1.Draw("A");

		g1.GetYaxis().SetRangeUser(0,1);

		g2.Draw("P E2 SAME")
		g1.Draw("P E2 SAME")
			
C.SaveAs(WorkDir+"/plots/Bias.pdf")

if(DEBUG>0): print "----- END ------"
