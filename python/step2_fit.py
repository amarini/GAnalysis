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
parser.add_option("","--inputDat" ,dest='inputDat',type='string',help="Input Configuration file",default="")
parser.add_option("","--inputDatMC" ,dest='inputDatMC',type='string',help="Input Configuration file for MC - must provided only in DoShapeCorrFit is set to true",default="")
parser.add_option("","--checkTime" ,dest='checkTime',action='store_true',help="check Time usage by different Functions.",default=False)

parser.add_option("","--nJobs" ,dest='nJobs',type='int',help="Total number of jobs. Useful to run on batch",default=-1)
parser.add_option("","--jobId" ,dest='jobId',type='int',help="Current job number. Useful to run on batch",default=0)

(options,args)=parser.parse_args()

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
	
DoShapeCorrFit=ReadFromDat(config,"DoShapeCorrFit",0,"--> Set Shape Corr For Fit to 0");

DoBiasStudies=ReadFromDat(config,"DoBiasStudies",0,"--> Set Do Bias Studies to 0");

JetPtThr=ReadFromDat(config,"JetPt",[30],"-->Default JetPT")

isFirstJob=True

configMC={}
WorkDirMC=""
inputFileNameMC=""
if DoShapeCorrFit:
	if options.inputDatMC == "": print "You must provide a MC dat file, or disable Shape Corr for Fit"
	configMC=read_dat(options.inputDatMC)
	print "------ MC DAT --------"
	if(DEBUG>0):PrintDat(configMC)
	WorkDirMC=ReadFromDat(configMC,"WorkDir","./","-->Set Default WDIR MC")
	inputFileNameMC=WorkDirMC+ReadFromDat(configMC,"outputFileName","output","-->Default Output Name for MC")+".root"		

#OPEN ROOT FILE - INPUT FILE FROM PREVIOUS RUNS
if(DEBUG>0): print "-> Open File "+ inputFileName
from subprocess import call
from glob import glob
if not os.path.isfile( inputFileName ):
	print "-- try to hadd ---"
	cmd=["hadd",inputFileName]
	for source in glob(WorkDir+ReadFromDat(config,"outputFileName","output","-->Default Output Name")+"*.root"):
		cmd.append(source)
	call(cmd)
	
file=ROOT.TFile.Open( inputFileName)

if DoShapeCorrFit: 
	if not os.path.isfile( inputFileNameMC ):
		print "-- try to hadd MC---"
		cmd=["hadd",inputFileNameMC]
		for source in glob(WorkDirMC+ReadFromDat(configMC,"outputFileName","output","-->Default Output Name")+"*.root"):
			cmd.append(source)
		call(cmd)
	print "-> Opening MC File:",inputFileNameMC
	fileMC=ROOT.TFile.Open(inputFileNameMC)
else:
	fileMC=ROOT.TFile.Open("/dev/null")

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

if options.checkTime:
    A=ROOT.Analyzer()
    A.doTimeUsage=1

def FIT(file,nJets=1,Ht=0,jetPt=30.,doShapeCorrFit=0,fileMC=ROOT.TFile.Open("/dev/null")):
	print "->Going to Fit: nJets",nJets,"Ht",Ht,"jetPt",jetPt,"doShape",doShapeCorrFit
	Bin=0
	SigTemplate=[]
	BkgTemplate=[]
	ToFitTemplate=[]
	ToFitTree=[]
	PtSig=[]
	PtBkg=[]
	PtToFit=[]
	TruthSig=[]
	TruthBkg=[]
	BiasStudySig=[]
	BiasStudyBkg=[]
	BiasStudySigRC=[]
	BiasStudyBkgInv=[]
	SigCorr=[]
	BkgCorr=[]
        if options.checkTime: A.checkTimeUsage(0,"Begin");
	for p in range(0,len(PtCuts)-1):
	   try:
		cutSig=ROOT.Analyzer.CUTS(PtCuts[p],PtCuts[p+1],Ht,8000,SigPhId[0],SigPhId[1],nJets);
		cutSig.JetPtThreshold=jetPt;
		cutBkg=ROOT.Analyzer.CUTS(PtCuts[p],PtCuts[p+1],Ht,8000,BkgPhId[0],BkgPhId[1],nJets);
		cutBkg.JetPtThreshold=jetPt;

		cutSigTemplates=ROOT.Analyzer.CUTS(PtCuts[p],PtCuts[p+1],0,8000,SigPhId[0],SigPhId[1],1);
		cutBkgTemplates=ROOT.Analyzer.CUTS(PtCuts[p],PtCuts[p+1],0,8000,BkgPhId[0],BkgPhId[1],1);

		if( PtCuts[p] <0 ): 
			Bin+=1		
			continue
		if jpt > 250 and PtCuts[p]<200:continue; ##avoid trying to fit: no bkg
		if( PtCuts[p+1] <0 ): continue
		if( Bin == ToFitBin):
			ToFitTemplate.append(file.Get("photoniso_"+cutSig.name() ) )
			if(len(PtToFit)==0): PtToFit.append(PtCuts[p]);
			PtToFit.append(PtCuts[p+1])
		if( Bin == BkgBin ):
			BkgTemplate.append(file.Get("photoniso_"+cutBkgTemplates.name()  ) )
			if(len(PtBkg)==0): PtBkg.append(PtCuts[p]);
			PtBkg.append(PtCuts[p+1])
		if( Bin == SigBin ):
			SigTemplate.append(file.Get("photonisoRC_"+cutSigTemplates.name() ) )
			if(len(PtSig)==0): PtSig.append(PtCuts[p]);
			PtSig.append(PtCuts[p+1])
		if doShapeCorrFit:
			#SIG
			if Bin == SigBin:
				try:
					SigMC=fileMC.Get("photonisoRC_"+ cutSig.name() )
					print "Going to Get:","photoniso_MATCHED_"+cutSig.name()
					TruthSig.append(fileMC.Get("photoniso_MATCHED_"+cutSig.name() ) )
					BiasStudySig.append(fileMC.Get("photoniso_MATCHED_"+cutSig.name() ).Clone("BiasStudySig") )
					BiasStudySigRC.append(fileMC.Get("photonisoRC_"+cutSig.name() ).Clone("BiasStudySigRC") )
					TruthSig[-1].Divide(SigMC)
					for iHbin in range(1,TruthSig[-1].GetNbinsX()+1):
						if( TruthSig[-1].GetBinContent(iHbin) >100 and TruthSig[-1].GetBinError(iHbin)> TruthSig[-1].GetBinContent(iHbin)*.5 ):
							TruthSig[-1].SetBinContent(iHbin,1) #small numbers correction
					TruthSig[-1].SetName("SigShapeCorrFit_"+cutSig.name() ) 
					SigCorr.append( SigTemplate[-1].Clone("photonisoRC_MCCOR_"+cutSig.name()) ) 
					SigCorr[-1].Multiply(TruthSig[-1])
				except (AttributeError,TypeError):
					print "SHAPECORR SIG: no Histo"
					doShapeCorrFit=0 # Turn Off Local var
			#BKG
			if Bin == BkgBin:
				try:
					BkgMC=fileMC.Get("photoniso_"+cutBkg.name() )
					print "Going to Get", "photoniso_NOTMATCHED_"+cutSig.name() 
					TruthBkg.append( fileMC.Get("photoniso_NOTMATCHED_"+cutSig.name() ) )#Truth has Sig Id
					print "Goint to Get", "photoniso_NOTMATCHED_"+cutSig.name()
					BiasStudyBkg.append( fileMC.Get("photoniso_NOTMATCHED_"+cutSig.name()).Clone("BiasStudyBkg") )#Truth has Sig Id
					print "Going to Get", "photoniso_"+cutBkg.name() 
					BiasStudyBkgInv.append(fileMC.Get("photoniso_"+cutBkg.name()  ).Clone("BiasStudyBkgInv") )
					TruthBkg[-1].Divide(BkgMC)
					for iHbin in range(1,TruthBkg[-1].GetNbinsX()+1):
						if( TruthBkg[-1].GetBinContent(iHbin) >100 and TruthBkg[-1].GetBinError(iHbin)> TruthBkg[-1].GetBinContent(iHbin)*.5 ):
							TruthBkg[-1].SetBinContent(iHbin,1) #small numbers correction
					BkgCorr.append( BkgTemplate[-1].Clone("photoniso_MCCOR_"+cutBkg.name()))
					BkgCorr[-1].Multiply(TruthBkg[-1])
				except (AttributeError,TypeError):
					print "SHAPECORR BKG: no Histo"
					print "-- histos: "+"photoniso_"+cutBkg.name()
					print "-- histos: "+"photoniso_NOTMATCHED_"+cutSig.name()
					doShapeCorrFit=0 # Turn Off Local var
	   ###
	   except ReferenceError: pass

        if options.checkTime: A.checkTimeUsage(1,"GetHisto");

	#if options.nJobs >0 :
	if isFirstJob:
		if options.nJobs> 0:
			o_txt=open(WorkDir+"/fit_%d_%d.txt"%(options.jobId,options.nJobs),"w")
			o_pars=open(WorkDir+"/fitPars_%d_%d.txt"%(options.jobId,options.nJobs),"w")
		else:
			o_txt=open(WorkDir+"/fit.txt","w")
			o_pars=open(WorkDir+"/fitPars.txt","w")

		try:
			if options.nJobs<0:
				os.remove(WorkDir+"/fitresults.root")
			else:
				os.remove(WorkDir+"/fitresults_%d_%d.root"%(options.jobId,options.nJobs))
		except OSError: print "file doesn't exist: not removed"
	else:	
		if options.nJobs >0:
			o_txt=open(WorkDir+"/fit_%d_%d.txt"%(options.jobId,options.nJobs),"a")
			o_pars=open(WorkDir+"/fitPars_%d_%d.txt"%(options.jobId,options.nJobs),"a")
		else:
			o_txt=open(WorkDir+"/fit.txt","a")
			o_pars=open(WorkDir+"/fitPars.txt","a")

	for p in range(0,len(PtToFit)-1):
	   try:
		if jpt > 250 and PtToFit[p]<200:continue; ##avoid trying to fit: no bkg
		#find pt bin for sig
        	if options.checkTime: A.checkTimeUsage(0,"Begin");
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
			if doShapeCorrFit:
				NormSigCorr = SigCorr[Sbin].Integral();
				NormBkgCorr = BkgCorr[Bbin].Integral();
		except (ReferenceError, AttributeError):
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

		if doShapeCorrFit and (NormSigCorr == 0 or NormBkgCorr==0):
			print "-> NULL INTEGRAL SIG CORRECTED"
			doShapeCorrFit=0;

		if doShapeCorrFit:
			for x in range(1,SigCorr[Sbin].GetNbinsX()+1):
				if SigTemplate[Sbin].GetBinContent(x) == 0:
					SigCorr[Sbin].SetBinContent(x,0.0000000001)
			for x in range(1,BkgCorr[Bbin].GetNbinsX()+1):
				if BkgTemplate[Bbin].GetBinContent(x) == 0:
					BkgCorr[Bbin].SetBinContent(x,0.0000000001)
	
		#BINNED
		#v=ROOT.std.vector(float)()
		if jetPt == 30: extra=""
		else: extra = "_JPT_%.1f"%jetPt
		fitResultName="fitresults.root"
		if options.nJobs>0: fitResultName="fitresults_%d_%d.root"%(options.jobId,options.nJobs)
		fitR=ROOT.std.map(ROOT.std.string,float)()
		f=ROOT.FIT.fit(ToFitTemplate[p],SigTemplate[Sbin],BkgTemplate[Bbin],
				WorkDir+"/"+fitResultName,
				"Bin_PT_"+str(round(PtToFit[p],1))+"_"+str(round(PtToFit[p+1],1))+"_HT_"+str(Ht) +"_nJets_"+str(nJets) +extra,
				fitR
				)
        	if options.checkTime: A.checkTimeUsage(2,"Fit");

		if doShapeCorrFit:
			print "-> FIT SIGSHAPE CORR"
			BinName="Bin_PT_"+str(round(PtToFit[p],1))+"_"+str(round(PtToFit[p+1],1))+"_HT_"+str(Ht) +"_nJets_"+str(nJets);
			if jpt > 35: BinName += "_JetPt_"+str(jpt) 
			#BinName += ROOT.Analyzer.SystName(ROOT.Analyzer.SIGSHAPE)
			fSigCorr=ROOT.FIT.fit(ToFitTemplate[p],SigCorr[Sbin],BkgTemplate[Bbin],WorkDir+"/"+fitResultName,BinName + ROOT.Analyzer.SystName(ROOT.Analyzer.SIGSHAPE))
			fBkgCorr=ROOT.FIT.fit(ToFitTemplate[p],SigTemplate[Sbin],BkgCorr[Bbin],WorkDir+"/"+fitResultName,BinName + ROOT.Analyzer.SystName(ROOT.Analyzer.BKGSHAPE))

        	if options.checkTime: A.checkTimeUsage(3,"Shape Corr Fit");
		#UNBINNED
		#f=ROOT.FIT.fit(ToFitTree[p],SigTemplate[s],BkgTemplate[b],"fitresults.root","Bin_PT_"+str(PtToFit[p])+"_"+str(PtToFit[p+1]))
		
		#Write output
		if doShapeCorrFit:
			o_txt.write("Pt "+str(PtToFit[p])+" "+str(PtToFit[p+1])+" Ht " +str(Ht) + " nJets "+ str(nJets)+ " jetPt "+ str(jetPt)+" Fraction= "+str(f) + " "+ROOT.Analyzer.SystName(ROOT.Analyzer.SIGSHAPE)+" "+str(fSigCorr)+ " "+ ROOT.Analyzer.SystName(ROOT.Analyzer.BKGSHAPE)+" "+str(fBkgCorr))
		else:
			o_txt.write("Pt "+str(PtToFit[p])+" "+str(PtToFit[p+1])+" Ht " +str(Ht) + " nJets "+ str(nJets)+ " jetPt "+ str(jetPt)+" Fraction= "+str(f))
	
		o_pars.write("Pt "+str(PtToFit[p])+" "+str(PtToFit[p+1])+" Ht " +str(Ht) + " nJets "+ str(nJets)+ " jetPt "+ str(jetPt)+" Par0 "+str(fitR["bkg0"])+" Par1 "+str(fitR["bkg1"]) + " Par2 "+str(fitR["bkg2"])+"\n")

		rms=-1
		#make sure Normalization didn't change ->Poisson
		ToFitTemplate[p].Scale(NormToFit/ToFitTemplate[p].Integral());
		SigTemplate[Sbin].Scale(NormSig/SigTemplate[Sbin].Integral());
		BkgTemplate[Bbin].Scale(NormBkg/BkgTemplate[Bbin].Integral());
		if doShapeCorrFit:
			SigCorr[Sbin].Scale(NormSigCorr/SigCorr[Sbin].Integral());
			BkgCorr[Bbin].Scale(NormBkgCorr/BkgCorr[Bbin].Integral());
		 
		if PtToFit[p] == 100 and nJets==1 and Ht==0:
			try:
				os.remove(WorkDir+"/toysresults.root")
			except OSError: print "toy file doesn't exist: not removed"
			t=ROOT.TOYS.toy(ToFitTemplate[p],SigTemplate[Sbin],BkgTemplate[Bbin],20,0,WorkDir+"/toysresults.root");
		else:
			t=ROOT.TOYS.toy(ToFitTemplate[p],SigTemplate[Sbin],BkgTemplate[Bbin],20);
        	if options.checkTime: A.checkTimeUsage(4,"Toys");

		o_txt.write(" TOYS= "+str( t["rms"] )+ " TMEAN= "+str(t["mean"]) );

		if DoBiasStudies:
			try:
				 Bin="Bin_PT_"+str(PtToFit[p])+"_"+str(PtToFit[p+1])+"_HT_"+str(Ht) +"_nJets_"+str(nJets) 
				 os.remove(WorkDir+"/biasresults"+Bin+".root")
			except OSError: print "bias file doesn't exist: not removed"
			#The fit model is build with thruth
			BiasStudySig[Sbin].Scale( 1./BiasStudySig[Sbin].Integral() )
			BiasStudyBkg[Bbin].Scale( 1./BiasStudyBkg[Bbin].Integral() )
			#The template to fit is build with mc thruth
			ToFitBias=BiasStudySig[Sbin].Clone("ToFitBias"+Bin)
			ToFitBias.Scale(f)
			ToFitBias.Add(BiasStudyBkg[Bbin],(1-f))
			#The template are build with RC & Inv from MC (BiasStudies)
			b=ROOT.TOYS.toy(ToFitBias,BiasStudySigRC[Sbin],BiasStudyBkgInv[Bbin],100,0,WorkDir+"/biasresults"+Bin+".root");
			o_txt.write(" BIAS= "+str(b["mean"]) + " BRMS= " + str(b["rms"]))
			bf=ROOT.TFile.Open(WorkDir+"/biasresults"+Bin+".root","UPDATE")
			bf.cd()
			BiasStudyBkg[Bbin].Write()
			BiasStudySig[Sbin].Write()
			BiasStudyBkgInv[Bbin].Write()
			BiasStudySigRC[Sbin].Write()
			bf.Close()
			

        	if options.checkTime: A.checkTimeUsage(5,"Bias Studies");

		o_txt.write(" ERROR= "+str( fitR["error"]) +"\n"); ## ROOFIT ERROR
		
		if doShapeCorrFit:
			fOut=ROOT.TFile.Open(WorkDir+"/fitresults.root","UPDATE")
			TruthSig[Sbin].Write("",ROOT.TObject.kOverwrite)	
			SigCorr[Sbin].Write("",ROOT.TObject.kOverwrite)	
			TruthBkg[Bbin].Write("",ROOT.TObject.kOverwrite)	
			BkgCorr[Bbin].Write("",ROOT.TObject.kOverwrite)	
			fOut.Close();
	   except ReferenceError: pass
	if(options.checkTime):A.checkTimeUsage(-1,"Print");

#MAIN LOOP
ListOfJobs=[]

for jpt in JetPtThr:
     for h in HtCuts:
	for n in nJetsCuts:
		if jpt !=30 and (n!=1 and h!=0): continue #only inclusive for different jpt
		if n!=1 and h!=0: continue; ##don't overlap cuts in njets & ht
		ListOfJobs.append((int(n),h,jpt))

JobBegin=(len(ListOfJobs)/options.nJobs+1)*options.jobId;
JobEnd  =(len(ListOfJobs)/options.nJobs+1)*(options.jobId+1);
if JobEnd > len(ListOfJobs): JobEnd=len(ListOfJobs)
if options.nJobs<0: 
	JobBegin=0
	JobEnd=len(ListOfJobs)

if DEBUG>0: 
	print "JobBegin=",JobBegin
	print "JobEnd=",JobEnd
	print "ListOfJobs:",ListOfJobs
for iJob in range(JobBegin,JobEnd):
		if iJob != JobBegin: isFirstJob=False
		(n,h,jpt)=ListOfJobs[iJob]
		FIT(file,int(n),h,jpt,DoShapeCorrFit,fileMC)
if(DEBUG>0): print "----- END ------"
