#!/usr/bin/python
import sys,os
import array
import ROOT
import time
from optparse import OptionParser


DEBUG=1

print "BEGIN"

WorkDir="./"

ROOT.gROOT.SetBatch()

ROOT.gROOT.ProcessLine (\
"struct Entry{ \
float rho;\
int nVtx;\
bool isRealData;\
};" )

from ROOT import Entry
def UniqName(PtBins,iPt,EtaBins,iEta):
	return "_pt"+str(PtBins[iPt])+"_"+str(PtBins[iPt+1])+"_eta"+str(EtaBins[iEta])+"_"+str(EtaBins[iEta+1])

def Loop(t,nBins=100,xMin=40,xMax=120,PtBins=[0,100,150,200,250,300,400,500,1000],EtaBins=[0,0.5,1.0,1.5]):
	entry=Entry()
	photonIsoFPRRandomConePhoton=ROOT.std.vector(float)()
	photonPt=ROOT.std.vector(float)()
	photonEta=ROOT.std.vector(float)()

	t.SetBranchAddress("isRealData",ROOT.AddressOf(entry,'isRealData'))
	t.GetEntry(0);#update isRealData
	t.SetBranchAddress("photonIsoFPRRandomConePhoton"	,ROOT.AddressOf(photonIsoFPRRandomConePhoton) )
	t.SetBranchAddress("photonPt"	,ROOT.AddressOf(photonPt) )
	t.SetBranchAddress("photonEta"	,ROOT.AddressOf(photonEta) )
	t.SetBranchAddress("rho",ROOT.AddressOf(entry,'rho'))
	t.SetBranchAddress("nVtx",ROOT.AddressOf(entry,'nVtx'))

	#H=ROOT.std.map(ROOT.std.pair(string,ROOT.TH2D))()
	H={}
	for iPt in range(0,len(PtBins)-1):
		for iEta in range(0,len(EtaBins)-1):
			name="rho_vs_nvtx"+UniqName(PtBins,iPt,EtaBins,iEta)
			if(DEBUG>1): print "Going to create:" + name
			H[name]=ROOT.TH2D(name,name,nBins,xMin,xMax,1000,0,100)   
			name="iso_vs_nvtx"+UniqName(PtBins,iPt,EtaBins,iEta)
			if(DEBUG>1): print "Going to create:" + name
			H[name]=ROOT.TH2D(name,name,nBins,xMin,xMax,1000,0,1000)  
	#loop
	if(DEBUG>1):
		for name in H:
			print "HISTO "+name+" is present in the database"
	
	for iEntry in range(0,t.GetEntries()):
		#if(iEntry>10000): 
		#	print "Exiting, too many entries"
		#	break
		t.GetEntry(iEntry)
		iPt=0;iEta=0;
		if( photonPt.size() <1): continue;
		for i in range(0,len(PtBins)-1): 
			if( photonPt[0]>= PtBins[i] and photonPt[0] <=PtBins[i+1]): iPt=i;
		for i in range(0,len(EtaBins)-1): 
				if( abs(photonEta[0])>= EtaBins[i] and abs(photonEta[0]) <=EtaBins[i+1]): iEta=i;
		name="rho_vs_nvtx"+UniqName(PtBins,iPt,EtaBins,iEta)
		if(DEBUG>1): print "Going to Fill:" + name
		H[name].Fill(entry.nVtx,entry.rho);
		name="iso_vs_nvtx"+UniqName(PtBins,iPt,EtaBins,iEta)
		if(DEBUG>1): print "Going to Fill:" + name
		H[name].Fill(entry.nVtx,photonIsoFPRRandomConePhoton[0]);
	return H;


print "PARSING"
#####################
usage = "usage: %prog [options] arg1 arg2"
parser = OptionParser(usage=usage)
parser.add_option("-d","--dirName"  ,dest='dirName' ,type='string',help="directory on eos root://eoscms///store/...",default="root://eoscms///store/user/amarini/zjets_V00-12")
parser.add_option("-x","--dataName" ,dest='dataName',type='string',help="data files comma separated",default="Photon_Run2012A-22Jan2013-v1_AOD_v2.root")
parser.add_option("-i","--inputDat" ,dest='inputDat',type='string',help="Configuration file",default="data/config.dat")

(options,args)=parser.parse_args()

dataNames=options.dataName.split(',')


print "Adding Files"

data=ROOT.TChain("accepted/events")

if options.inputDat=="" :
	for name in dataNames:
		data.Add(options.dirName+"/"+name)

print "Load Configuration"
from common import *
config=read_dat(options.inputDat);
#SET BRANCH ADDRESSES -- LOOP
if(DEBUG>0):
	for name in config:
		print "Dat contains key " +str(name) + "with value" + str(config[name])

try:	
	for tree in config["DataTree"]: 
		print "Added Tree "+tree
		data.Add(tree) 
except KeyError: 
	print "Going To Exit"
	exit


try: 
	PtBins=config["PtBins"]
	print "PtBins="+str(PtBins)
except KeyError: 
	print "-> Load std PtBins" 
	PtBins=[0,100,150,200,250,300,400,500,1000,2000]

try: 
	EtaBins=config["EtaBins"]
	print "EtaBins="+str(EtaBins)
except KeyError: 
	print "-> Load std EtaBins"
	EtaBins=[0,.5,1,1.5]

try: 
	WorkDir=config["WorkDir"]
	print "WorkDir is "+str(WorkDir)
except KeyError: 
	print "-> Working Directory set as ./"
	WorkDir="./"

print "Begin LOOP"
H=Loop(data,40,0,40,PtBins,EtaBins)

#LOAD ROOFIT
print "LOAD ROOFIT"
ROOT.gSystem.Load("libRooFit") ;

print "Begin Analysis"
#DO PROFILE
f=open(WorkDir+"effarea.txt","w")
tf=ROOT.TFile.Open(WorkDir+"effarea.root","RECREATE")
tf.cd()
f.write( "#what ptmin ptmax etamin etamax value\n" )
for name in H:
	h=H[name].ProfileX();
	
	#find range
	rMin=10000;
	rMax=-10000;
	for iBin in range(1,h.GetNbinsX()+1):
		if(h.GetBinContent(iBin) >0 and rMin>h.GetBinLowEdge(iBin)): rMin=h.GetBinLowEdge(iBin);
		if(h.GetBinContent(iBin) >0 and rMax<h.GetBinLowEdge(iBin+1)): rMax=h.GetBinLowEdge(iBin+1);

	Rnvtx=ROOT.RooRealVar("nvtx","nvtx",0,40);
	Rh=ROOT.RooDataHist(name+"_R",name+"_R",ROOT.RooArgList(Rnvtx),h);
	Ra=ROOT.RooRealVar("a","a",0,40);

	Rp=ROOT.RooPolynomial("lin","linear",Rnvtx,ROOT.RooArgList(Ra));
	RR=Rp.fitTo(Rh,ROOT.RooFit.Extended(ROOT.kFALSE), ROOT.RooFit.Save(ROOT.kTRUE),ROOT.RooFit.SumW2Error(ROOT.kTRUE),ROOT.RooFit.Range(rMin,rMax));

	outputStr=name;	
	outputStr.replace("vs_nvtx_","");
	outputStr.replace("pt"," ");
	outputStr.replace("eta"," ");
	outputStr.replace("_"," ");
	f.write( name + " " + str(Ra.getVal()) +"\n" )
	#Save the histograms fitted in tf
	tf.cd()
	C=ROOT.TCanvas(name+"_C",name)
	frame = Rnvtx.frame()
	Rh.plotOn(frame) ;
	Rp.plotOn(frame) ;	
	frame.Write(name+"_F")
	frame.Draw()
	C.Write()	
	
print 
print 
print "******************************"
print "*            DONE            *"
print "******************************"
print 
print

