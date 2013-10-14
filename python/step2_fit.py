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
#parser.add_option("","--jobId" ,dest='jobId',type='int',help="Current job number. Useful to run on batch",default=0)
(options,args)=parser.parse_args()

#import cuts
#PtCuts=[100,150,200,250,300,350,450,550,650,750,-1,100,300,750]
#SigPhId=[-10.,-.1]
#BkgPhId=[0.1,10.]

from common import *
if(DEBUG>0): print "--> load dat file: "+options.inputDat;
config=read_dat(options.inputDat)
if(DEBUG>0):
	print "--------------------------------------"
	for name in config:
		print "Dat contains key " +str(name) + "with value" + str(config[name])
	print "--------------------------------------"
	print 
	print 


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
f=ROOT.TFile.Open( inputFileName)

#signal template binning
###############Configuration ##############
ToFitBin=0
BkgBin=1
SigBin=1
###########################################
Bin=0
SigTemplate=[]
BkgTemplate=[]
ToFitTemplate=[]
ToFitTree=[]
PtSig=[]
PtBkg=[]
PtToFit=[]
nJets=1
for p in range(0,len(PtCuts)-1):
	if( PtCuts[p] <0 ): 
		Bin+=1		
		continue
	if( PtCuts[p+1] <0 ): continue
	if( Bin == ToFitBin):
		ToFitTemplate.append(f.Get("photoniso_VPt_%.0f_%.0f_Ht_%.0f_%.0f_phid_%.3f_%.3f_nJets_%d"%(PtCuts[p],PtCuts[p+1],0,8000,SigPhId[0],SigPhId[1] ,nJets ) ) )
		ToFitTree.append(f.Get("tree_VPt_%.0f_%.0f_Ht_%.0f_%.0f_phid_%.3f_%.3f_nJets_%d"%(PtCuts[p],PtCuts[p+1],0,8000,SigPhId[0],SigPhId[1],nJets)  ) )
		if(len(PtToFit)==0): PtToFit.append(PtCuts[p]);
		PtToFit.append(PtCuts[p+1])
	if( Bin == BkgBin ):
		BkgTemplate.append(f.Get("photoniso_VPt_%.0f_%.0f_Ht_%.0f_%.0f_phid_%.3f_%.3f_nJets_%d"%(PtCuts[p],PtCuts[p+1],0,8000,BkgPhId[0],BkgPhId[1],nJets)  ) )
		if(len(PtBkg)==0): PtBkg.append(PtCuts[p]);
		PtBkg.append(PtCuts[p+1])
	if( Bin == SigBin ):
		SigTemplate.append(f.Get("photonisoRC_VPt_%.0f_%.0f_Ht_%.0f_%.0f_phid_%.3f_%.3f_nJets_%d"%(PtCuts[p],PtCuts[p+1],0,8000,SigPhId[0],SigPhId[1],nJets)  ) )
		if(len(PtSig)==0): PtSig.append(PtCuts[p]);
		PtSig.append(PtCuts[p+1])

if(DEBUG>0): print "----- FIT ------"
ROOT.gSystem.Load("fit.so")

o_txt=open(WorkDir+"/fit.txt","w")
#os.popen("rm "+WorkDir+"/fitresults.root")
try:
	os.remove(WorkDir+"/fitresults.root")
except OSError: print "file doesn't exist: not removed"

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
	if DEBUG>0: 
		print "-> Going to fit PtBin %.0f-%.0f with sig %.0f-%.0f and bkg %.0f %.0f"%(PtToFit[p],PtToFit[p+1],PtSig[Sbin],PtSig[Sbin+1],PtBkg[Bbin],PtBkg[Bbin+1])
		print "---> Fit Template:" + ToFitTree[p].GetName()
		print "---> Sig Template:" + SigTemplate[Sbin].GetName()
		print "---> Bkg Template:" + BkgTemplate[Bbin].GetName()

	#BINNED
	f=ROOT.FIT.fit(ToFitTemplate[p],SigTemplate[Sbin],BkgTemplate[Bbin],WorkDir+"/fitresults.root","Bin_PT_"+str(PtToFit[p])+"_"+str(PtToFit[p+1]))
	#UNBINNED
	#f=ROOT.FIT.fit(ToFitTree[p],SigTemplate[s],BkgTemplate[b],"fitresults.root","Bin_PT_"+str(PtToFit[p])+"_"+str(PtToFit[p+1]))
	
	#Write output
	o_txt.write("Fraction= "+str(f))
	rms=ROOT.TOYS.toy(ToFitTemplate[p],SigTemplate[Sbin],BkgTemplate[Bbin],10);
	o_txt.write(" ERROR= "+str(rms) +"\n");

if(DEBUG>0): print "----- END ------"
