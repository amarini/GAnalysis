#!/usr/bin/python
import sys,os
import array
import ROOT
import time
from optparse import OptionParser

DEBUG=1

ROOT.gROOT.SetBatch()

if(DEBUG>0):print "----- BEGIN -----"

if(DEBUG>0):print "-PARSING OPTIONS-"
usage = "usage: %prog [options] arg1 arg2"
parser=OptionParser(usage=usage)
parser.add_option("-f","--fileName" ,dest='fileName',type='string',help="FileName result of step0",default="output.root")
parser.add_option("","--inputDat" ,dest='inputDat',type='string',help="Input Configuration file",default="")

(options,args)=parser.parse_args()

from common import *

if(DEBUG>0): print "--> load dat file: "+options.inputDat;

config=read_dat(options.inputDat)

if(DEBUG>0):
	PrintDat(config)

try:
	WorkDir=config["WorkDir"]
except KeyError:
	WorkDir="./"

try:	
	inputFileName=WorkDir+config["outputFileName"] +".root"
	if(DEBUG>0):print "OutputFile="+config["outputFileName"]+".root"
except KeyError:	
	inputFileName=WorkDir+"output.root"
	if(DEBUG>0):print "InputFile=output"
try:
	PtCuts=config["PtCuts"]
except KeyError: 
	PtCuts=[0,100,200,300]
	if(DEBUG>0):print "Loaded default PtCuts"

try:
	HtCuts=config["HtCuts"]
except KeyError: 
	print "ERROR HtCuts"
	HtCuts=[0,100,200,300]

try:
	nJetsCuts=config["nJetsCuts"]
except KeyError: 
	print "ERROR nJetsCuts"
	nJetsCuts=[1,3]

try:
	SigPhId=config["SigPhId"]
except KeyError: 
	SigPhId=[0,0.11]	
	if(DEBUG>0):print "Loaded default SigPhId"

try:
	BkgPhId=config["BkgPhId"]
except KeyError: 
	BkgPhId=[0,0.11]	
	if(DEBUG>0):print "Loaded default BkgPhId"

#OPEN ROOT FILE - INPUT FILE FROM PREVIOUS RUNS
if(DEBUG>0): print "-> Open File "+ inputFileName
file=ROOT.TFile.Open( inputFileName)

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

def FIT(file,nJets=1,Ht=0):
	Bin=0
	SigTemplate=[]
	BkgTemplate=[]
	ToFitTemplate=[]
	ToFitTree=[]
	PtSig=[]
	PtBkg=[]
	PtToFit=[]
	for p in range(0,len(PtCuts)-1):
		if( PtCuts[p] <0 ): 
			Bin+=1		
			continue
		if( PtCuts[p+1] <0 ): continue
		if( Bin == ToFitBin):
			ToFitTemplate.append(file.Get("photoniso_VPt_%.0f_%.0f_Ht_%.0f_%.0f_phid_%.3f_%.3f_nJets_%d"%(PtCuts[p],PtCuts[p+1],Ht,8000,SigPhId[0],SigPhId[1] ,nJets ) ) )
			#ToFitTree.append(file.Get("tree_VPt_%.0f_%.0f_Ht_%.0f_%.0f_phid_%.3f_%.3f_nJets_%d"%(PtCuts[p],PtCuts[p+1],Ht,8000,SigPhId[0],SigPhId[1],nJets)  ) )
			if(len(PtToFit)==0): PtToFit.append(PtCuts[p]);
			PtToFit.append(PtCuts[p+1])
		if( Bin == BkgBin ):
			BkgTemplate.append(file.Get("photoniso_VPt_%.0f_%.0f_Ht_%.0f_%.0f_phid_%.3f_%.3f_nJets_%d"%(PtCuts[p],PtCuts[p+1],Ht,8000,BkgPhId[0],BkgPhId[1],nJets)  ) )
			if(len(PtBkg)==0): PtBkg.append(PtCuts[p]);
			PtBkg.append(PtCuts[p+1])
		if( Bin == SigBin ):
			SigTemplate.append(file.Get("photonisoRC_VPt_%.0f_%.0f_Ht_%.0f_%.0f_phid_%.3f_%.3f_nJets_%d"%(PtCuts[p],PtCuts[p+1],Ht,8000,SigPhId[0],SigPhId[1],nJets)  ) )
			if(len(PtSig)==0): PtSig.append(PtCuts[p]);
			PtSig.append(PtCuts[p+1])
	
	if nJets == 1 and Ht ==0:
		o_txt=open(WorkDir+"/fit.txt","w")
		try:
			os.remove(WorkDir+"/fitresults.root")
		except OSError: print "file doesn't exist: not removed"
	else: o_txt=open(WorkDir+"/fit.txt","a")

	
	for p in range(0,len(PtToFit)-1):
		#find pt bin for sig
		Sbin=-1
		Bbin=-1
		for s in range(0,len(PtSig)-1):
			if PtSig[s] <= PtToFit[p]  and PtToFit[p+1]<= PtSig[s+1]:
				Sbin=s
		for b in range(0,len(PtBkg)-1):
			if PtBkg[b] <= PtToFit[p]  and PtToFit[p+1]<= PtBkg[b+1]:
				Bbin=b
		if Sbin<0 or Bbin<0:
			print "ERROR: not found a suitable bin for signal or background"
			continue
		try:
			NormToFit = ToFitTemplate[p].Integral();
			NormSig   = SigTemplate[Sbin].Integral();
			NormBkg   = BkgTemplate[Bbin].Integral();
		except (ReferenceError, AttributeError) as e:
			print "-> Going to fit PtBin %.0f-%.0f with sig %.0f-%.0f and bkg %.0f %.0f"%(PtToFit[p],PtToFit[p+1],PtSig[Sbin],PtSig[Sbin+1],PtBkg[Bbin],PtBkg[Bbin+1])
			print "--> ERROR NULL HISTOS"
			continue;
		
		if DEBUG>0: 
			print "-> Going to fit PtBin %.0f-%.0f with sig %.0f-%.0f and bkg %.0f %.0f"%(PtToFit[p],PtToFit[p+1],PtSig[Sbin],PtSig[Sbin+1],PtBkg[Bbin],PtBkg[Bbin+1])
			print "-> nJets=%d Ht=%.1f"%(nJets,Ht)
			print "---> Fit Template:" + ToFitTemplate[p].GetName()
			print "---> Sig Template:" + SigTemplate[Sbin].GetName()
			print "---> Bkg Template:" + BkgTemplate[Bbin].GetName()
		if NormToFit == 0 or NormSig == 0 or NormBkg == 0 :
			print "-> NUll INTEGRAL"
			continue
	
		#BINNED
		f=ROOT.FIT.fit(ToFitTemplate[p],SigTemplate[Sbin],BkgTemplate[Bbin],WorkDir+"/fitresults.root","Bin_PT_"+str(PtToFit[p])+"_"+str(PtToFit[p+1])+"_HT_"+str(Ht) +"_nJets_"+str(nJets) )
		#UNBINNED
		#f=ROOT.FIT.fit(ToFitTree[p],SigTemplate[s],BkgTemplate[b],"fitresults.root","Bin_PT_"+str(PtToFit[p])+"_"+str(PtToFit[p+1]))
		
		#Write output
		o_txt.write("Pt "+str(PtToFit[p])+" "+str(PtToFit[p+1])+" Ht " +str(Ht) + " nJets "+ str(nJets)+ " Fraction= "+str(f))
		rms=-1
		#make sure Normalization didn't change ->Poisson
		ToFitTemplate[p].Scale(NormToFit/ToFitTemplate[p].Integral());
		SigTemplate[Sbin].Scale(NormSig/SigTemplate[Sbin].Integral());
		BkgTemplate[Bbin].Scale(NormBkg/BkgTemplate[Bbin].Integral());
		# TODO: the rms function implementation is wrong
		if PtToFit[p] <300 and nJets==1 and Ht==0:
			rms=ROOT.TOYS.toy(ToFitTemplate[p],SigTemplate[Sbin],BkgTemplate[Bbin],20);
		o_txt.write(" ERROR= "+str(rms) +"\n");

for h in HtCuts:
	for n in nJetsCuts:
		if n!=1 and h!=0: continue; ##don't overlap cuts in njets & ht
		FIT(file,int(n),h)

if(DEBUG>0): print "----- END ------"
