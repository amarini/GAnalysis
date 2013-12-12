#!/usr/bin/python
import sys,os
import array
import ROOT
import time
import math
from optparse import OptionParser

DEBUG=1

ROOT.gROOT.SetBatch()

if(DEBUG>0):print "----- BEGIN -----"

if(DEBUG>0):print "-PARSING OPTIONS-"
usage = "usage: %prog [options] arg1 arg2"
parser=OptionParser(usage=usage)
parser.add_option("","--inputDat" ,dest='inputDat',type='string',help="Input Configuration file",default="")
parser.add_option("","--inputDatMC" ,dest='inputDatMC',type='string',help="Input Configuration file",default="")
parser.add_option("-l","--libRooUnfold" ,dest='libRooUnfold',type='string',help="Shared RooUnfoldLibrary",default="/afs/cern.ch/user/a/amarini/work/RooUnfold-1.1.1/libRooUnfold.so")
parser.add_option("","--doUnfoldStudies",dest='doUnfoldStudies',action='store_true',default=False)

(options,args)=parser.parse_args()

from common import *

doUnfoldStudies=options.doUnfoldStudies

if(DEBUG>0): print "--> load dat file: "+options.inputDat;

config=read_dat(options.inputDat)

if(DEBUG>0):
	print "--------- DATA CONFIG -----------"
	PrintDat(config)

configMC=read_dat(options.inputDatMC)

if(DEBUG>0):
	print "--------- MC CONFIG -----------"
	PrintDat(configMC)

WorkDir=ReadFromDat(config,"WorkDir","./","-->Set Default WDIR")
WorkDirMC=ReadFromDat(configMC,"WorkDir","./","-->Set Default WDIR")

PtCuts=ReadFromDat(config,"PtCuts",[0,100,200,300],"--> Default PtCuts")

HtCuts=ReadFromDat(config,"HtCuts",[0,100,200,300],"--> Default HtCuts")

nJetsCuts=ReadFromDat(config,"nJetsCuts",[1,3],"--> Default nJetsCuts")

SigPhId=ReadFromDat(config,"SigPhId",[0,0.011],"--> Default SigPhId")

BkgPhId=ReadFromDat(config,"BkgPhId",[0.011,0.014],"--> Default BkgPhId")

inputFileNameFit=WorkDir + "/fit.txt"  
inputFileNameRoot= WorkDir + ReadFromDat(config,"outputFileName","output","--> Default outputFileName")
inputFileNameRootMC= WorkDirMC + ReadFromDat(configMC,"outputFileName","output","--> Default outputFileName")

if(DEBUG>0): print "--> Load RooUnfold Library"
ROOT.gSystem.Load(options.libRooUnfold)

#Analyzer is required just for SYSTNAMES AND TYPE
if(DEBUG>0): print "-->Load Analyzer"
#ROOT.gSystem.Load("Analyzer.so")
ROOT.gSystem.Load("libGAnalysis.so")

if(DEBUG>0): print "--> Opening files"
fFit= open(inputFileNameFit,"r")
fRoot= ROOT.TFile.Open(inputFileNameRoot+".root");
fRootMC= ROOT.TFile.Open(inputFileNameRootMC+".root");
fUnfOut = ROOT.TFile.Open(WorkDir+"UnfoldedDistributions.root","RECREATE")
fUnfStudiesOut = ROOT.TFile.Open(WorkDir+"UnfoldStudies.root","RECREATE")
fUnfOut.cd()

if DEBUG>0:print "--> Read Fraction"
#READ FITTED FRACTION IN A DATABASE
#Pt 43.5 48.3 Ht 0.0 nJets 1 Fraction= 0.528608322144 ERROR= 0.000138673000038
Frac={};
FracSigCorr={};
FracBkgCorr={};
FracBias={};
FracErr={};
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
		elif "TOYS" in l[iWord]: #read error from toys
			er=float(l[iWord+1])
		elif "BIAS" in l[iWord]: #read error from toys
			bias=float(l[iWord+1])
		elif ROOT.Analyzer.SystName(ROOT.Analyzer.SIGSHAPE) in l[iWord]:
			fr_sigcorr=float(l[iWord+1])
		elif ROOT.Analyzer.SystName(ROOT.Analyzer.BKGSHAPE) in l[iWord]:
			fr_bkgcorr=float(l[iWord+1])
	try:
		Frac[ (ptmin,ptmax,ht,nj) ] = fr
	except NameError: pass;
	try:
		FracSigCorr[ (ptmin,ptmax,ht,nj) ] = fr_sigcorr
	except NameError: pass;
	try:
		FracBkgCorr[ (ptmin,ptmax,ht,nj) ] = fr_bkgcorr
	except NameError: pass;
	try:
		FracErr[ (ptmin,ptmax,ht,nj) ] = er;
	except NameError: pass
	try:
		FracBias[ (ptmin,ptmax,ht,nj) ] = bias;
	except NameError: pass

def Unfold(Response,H,par,type="SVD"):
	#U=ROOT.RooUnfold.RooUnfoldSvd(Response,H,par,1000)
	if type.lower() == "svd":
		U=ROOT.RooUnfoldSvd(Response,H,par,1000)
	elif type.lower() == "invert" or type.lower() == "inversion":
		U=ROOT.RooUnfoldInvert(Response,H)
	elif type.lower() == "bayes":
		U=ROOT.RooUnfoldBayes(Response,H,par,False) # last= smooth
		
	U.SetNToys(1000)
	u=U.Hreco(ROOT.RooUnfold.kCovToy)
	c=U.Ereco(ROOT.RooUnfold.kCovToy)
	return (u,c)


if DEBUG>0:print "--> Loop"
#Float_t * is needed for TH1D
ROOT.gROOT.ProcessLine("struct Bins{ \
		Double_t PtBins[1023];\
		};")

from ROOT import Bins
PtBins=ROOT.Bins()

#LOOP OVER THE BINs
def Loop(systName=""):
   for h in range(0,len(HtCuts)):
	for nj in range(0,len(nJetsCuts)):
		if nJetsCuts[nj] != 1 and HtCuts[h] !=0:continue;	
		#CREATE TARGET HISTO
		try:
			PtCuts2=PtCuts[0:PtCuts.index(-1) ]
		except ValueError: PtCuts2=PtCuts
		for c in range(0,len(PtCuts2)):
			PtBins.PtBins[c]=PtCuts2[c]
		Bin="Ht_"+str(HtCuts[h])+"_nJets_"+str(nJetsCuts[nj])+systName
		#Will it work?
		H=ROOT.TH1D("m_"+Bin,"Measured_"+Bin , len(PtCuts2)-1 , PtBins.PtBins )

		for p in range(0,len(PtCuts2)-1):
			## TAKE FITTED FRACTION
			try:
				if   systName == ROOT.Analyzer.SystName(ROOT.Analyzer.SIGSHAPE) :
					fr=FracSigCorr[ (PtCuts[p],PtCuts[p+1],HtCuts[h],nJetsCuts[nj]) ]
				elif systName == ROOT.Analyzer.SystName(ROOT.Analyzer.BKGSHAPE):
					fr=FracBkgCorr[ (PtCuts[p],PtCuts[p+1],HtCuts[h],nJetsCuts[nj]) ]
				elif  systName == "_BIAS" :
					fr=FracBias[  (PtCuts[p],PtCuts[p+1],HtCuts[h],nJetsCuts[nj]) ]
				else: ##DEFAULT
					fr=Frac[ (PtCuts[p],PtCuts[p+1],HtCuts[h],nJetsCuts[nj]) ]

			except (IndexError,KeyError): 
				print "ERROR IN FRACTION: Pt %.1f %.1f Ht %.0f nJ %.0f"%(PtCuts[p],PtCuts[p+1],HtCuts[h],nJetsCuts[nj])+" SYST="+systName
				fr=1	
				
			if systName == ROOT.Analyzer.SystName(ROOT.Analyzer.NONE) :
				try:
					er= FracErr[  (PtCuts[p],PtCuts[p+1],HtCuts[h],nJetsCuts[nj]) ]
				except (IndexError,KeyError):
					er=1
			else : er=0
			## TAKE HISTO WITH YIELDS
			systNameForHisto=systName
			if systName == ROOT.Analyzer.SystName(ROOT.Analyzer.SIGSHAPE)  or systName == ROOT.Analyzer.SystName(ROOT.Analyzer.BKGSHAPE) or  systName == ROOT.Analyzer.SystName(ROOT.Analyzer.UNFOLD):
				systNameForHisto=ROOT.Analyzer.SystName(ROOT.Analyzer.NONE)

			print "Getting histo gammaPt_VPt_%.0f_%.0f_Ht_%.0f_8000_phid_%.3f_%.3f_nJets_%.0f"%(PtCuts[p],PtCuts[p+1],HtCuts[h],SigPhId[0],SigPhId[1],nJetsCuts[nj]) + systNameForHisto
			try:
				hBin=fRoot.Get("gammaPt_VPt_%.0f_%.0f_Ht_%.0f_8000_phid_%.3f_%.3f_nJets_%.0f"%(PtCuts[p],PtCuts[p+1],HtCuts[h],SigPhId[0],SigPhId[1],nJetsCuts[nj]) + systNameForHisto )
				rawError= ROOT.Double(0)
				rawYield=hBin.IntegralAndError(1,hBin.GetNbinsX(),rawError)
			except AttributeError:
				print "ERROR HISTO NOT FOUND: Setting yield to 0"
				rawYield=0
				rawError=1
			## FILL HISTO CORRECTED
			corYield=rawYield*fr
			if rawYield !=0 and fr !=0:
				corErr= corYield*math.sqrt( (rawError/rawYield)**2 + (er/fr)**2)
			else:
				corErr=1
			H.SetBinContent( H.FindBin( (PtCuts[p]+PtCuts[p+1])/2.), corYield )
			H.SetBinError(   H.FindBin( (PtCuts[p]+PtCuts[p+1])/2.), corErr )
		## TAKE MATRIX & HISTO FOR REPSONSE MATRIX
		M=fRootMC.Get("gammaPt_MATRIX_VPt_0_8000_Ht_%.0f_8000_phid_%.3f_%.3f_nJets_%.0f"%(HtCuts[h],SigPhId[0],SigPhId[1],nJetsCuts[nj]) + systNameForHisto)
		G=fRootMC.Get("gammaPtGEN_VPt_0_8000_Ht_%.0f_8000_phid_%.3f_%.3f_nJets_%.0f"%(HtCuts[h],SigPhId[0],SigPhId[1],nJetsCuts[nj]) + systNameForHisto)
		R=fRootMC.Get("gammaPt_RECO_UNFOLD_VPt_0_8000_Ht_%.0f_8000_phid_%.3f_%.3f_nJets_%.0f"%(HtCuts[h],SigPhId[0],SigPhId[1],nJetsCuts[nj]) + systNameForHisto)
		try:
			Response= ROOT.RooUnfoldResponse(R,G,M,"Response"+Bin,"Response"+Bin)
			#Response= ROOT.RooUnfoldResponse(0,0,M,"Response"+Bin,"Response"+Bin)
		except TypeError:
			print "ERROR Unable to construct Matrix"
			continue;
		if doUnfoldStudies and systName=="":
			## UNFOLDSTUDIES
			fUnfStudiesOut.mkdir(Bin)
			fUnfStudiesOut.cd(Bin)
			for UnfPar in range(5,H.GetNbinsX(),3):
				H_us=Unfold(Response,H,UnfPar,"SVD")[0]
				H_us.SetName("u_svd_par"+str(UnfPar)+Bin)
				H_us.Write()
			for UnfPar in range(1,8,2):
				H_us=Unfold(Response,H,UnfPar,"Bayes")[0]
				H_us.SetName("u_bayes_par"+str(UnfPar)+Bin)
				H_us.Write()
			if True:
				H_us=Unfold(Response,H,UnfPar,"Invert")[0]
				H_us.SetName("u_invert_par"+str(UnfPar)+Bin)
				H_us.Write()
			H.Clone("r_"+Bin).Write()	
			G.Clone("g_"+Bin).Write()
			fUnfOut.cd()
		## UNFOLD -- ONE USED IN THE ANALYSIS
		(u,c)=Unfold(Response,H,3,"Bayes");

		u.SetName("u_"+Bin)
		u.SetTitle("Unfolded "+Bin.replace("_"," ")  )
		hcov= ROOT.TH2D(c) # must be D because cov is a TMatrixD
		hcov.SetName("cov_"+Bin)
		hcov.SetTitle("Covariance "+Bin.replace("_"," ") )
		b=u.Clone("b_"+Bin)
		b.SetTitle( "Unfolded And Bin Width Scaled" +Bin.replace("_"," "))
		for i in range(1,b.GetNbinsX()+1 ):
			b.SetBinContent(i, b.GetBinContent(i)/b.GetBinWidth(i) )
			b.SetBinError  (i, b.GetBinError(i)/b.GetBinWidth(i) ) 
		## SAVE OUTPUT
		fUnfOut.cd()
		u.Write()
		hcov.Write()
		b.Write()

### SYST ####
#NONE
#Loop("")
Loop(ROOT.Analyzer.SystName(ROOT.Analyzer.NONE))
#PU
Loop(ROOT.Analyzer.SystName(ROOT.Analyzer.PUUP))
Loop(ROOT.Analyzer.SystName(ROOT.Analyzer.PUDN))
#JEC
Loop(ROOT.Analyzer.SystName(ROOT.Analyzer.JESUP))
Loop(ROOT.Analyzer.SystName(ROOT.Analyzer.JESDN))
#JER
Loop(ROOT.Analyzer.SystName(ROOT.Analyzer.JERUP))
Loop(ROOT.Analyzer.SystName(ROOT.Analyzer.JERDN))
#SIGSHAPE
Loop(ROOT.Analyzer.SystName(ROOT.Analyzer.SIGSHAPE))
#BKGSHAPE
Loop(ROOT.Analyzer.SystName(ROOT.Analyzer.BKGSHAPE))
#
Loop(ROOT.Analyzer.SystName("_BIAS"))
		

