#!/usr/bin/python
import sys,os
import array
import ROOT
import time
from optparse import OptionParser

DEBUG=1

if(DEBUG>0):print "----- BEGIN -----"

if(DEBUG>0):print "-PARSING OPTIONS-"
usage = "usage: %prog [options] arg1 arg2"
parser=OptionParser(usage=usage)
parser.add_option("-f","--fileName" ,dest='fileName',type='string',help="FileName result of step0",default="output.root")
#parser.add_option("","--jobId" ,dest='jobId',type='int',help="Current job number. Useful to run on batch",default=0)
(options,args)=parser.parse_args()

#import cuts
#from step1_makeHisto import PtCuts
#from step1_makeHisto import SigPhId
#from step1_makeHisto import BkgPhId
PtCuts=[100,150,200,250,300,350,450,550,650,750,-1,100,300,750]
SigPhId=[-10.,-.1]
BkgPhId=[0.1,10.]

#OPEN ROOT FILE
if(DEBUG>0): print "-> Open File" + options.fileName
f=ROOT.TFile.Open(options.fileName)

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
for p in range(0,len(PtCuts)-1):
	if( PtCuts[p] <0 ): 
		Bin+=1		
		continue
	if( PtCuts[p+1] <0 ): continue
	if( Bin == ToFitBin):
		ToFitTemplate.append(f.Get("photoniso_VPt_%.0f_%.0f_Ht_%.0f_%.0f_phid_%.2f_%.2f"%(PtCuts[p],PtCuts[p+1],0,8000,SigPhId[0],SigPhId[1])  ) )
		ToFitTree.append(f.Get("tree_VPt_%.0f_%.0f_Ht_%.0f_%.0f_phid_%.2f_%.2f"%(PtCuts[p],PtCuts[p+1],0,8000,SigPhId[0],SigPhId[1])  ) )
		if(len(PtToFit)==0): PtToFit.append(PtCuts[p]);
		PtToFit.append(PtCuts[p+1])
	if( Bin == BkgBin ):
		BkgTemplate.append(f.Get("photoniso_VPt_%.0f_%.0f_Ht_%.0f_%.0f_phid_%.2f_%.2f"%(PtCuts[p],PtCuts[p+1],0,8000,BkgPhId[0],BkgPhId[1])  ) )
		if(len(PtBkg)==0): PtBkg.append(PtCuts[p]);
		PtBkg.append(PtCuts[p+1])
	if( Bin == SigBin ):
		SigTemplate.append(f.Get("photonisoRC_VPt_%.0f_%.0f_Ht_%.0f_%.0f_phid_%.2f_%.2f"%(PtCuts[p],PtCuts[p+1],0,8000,SigPhId[0],SigPhId[1])  ) )
		if(len(PtSig)==0): PtSig.append(PtCuts[p]);
		PtSig.append(PtCuts[p+1])

if(DEBUG>0): print "----- FIT ------"
ROOT.gSystem.Load("fit_C.so")
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
	#BINNED
	if DEBUG>0: print "-> Going to fit PtBin %.0f-%.0f with sig %.0f-%.0f and bkg %.0f %.0f"%(PtToFit[p],PtToFit[p+1],PtSig[Sbin],PtSig[Sbin+1],PtBkg[Bbin],PtBkg[Bbin+1])
	f=ROOT.fit(ToFitTemplate[p],SigTemplate[Sbin],BkgTemplate[Bbin],"fitresults.root","Bin_PT_"+str(PtToFit[p])+"_"+str(PtToFit[p+1]))
	#UNBINNED
	#f=ROOT.fit(ToFitTree[p],SigTemplate[s],BkgTemplate[b],"fitresults.root","Bin_PT_"+str(PtToFit[p])+"_"+str(PtToFit[p+1]))
	print "Fraction="+str(f);
	rms=ROOT.TOYS.toy(ToFitTemplate[p],SigTemplate[Sbin],BkgTemplate[Bbin],1000);
	print "ERROR="+str(rms);	

if(DEBUG>0): print "----- END ------"
