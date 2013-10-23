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

def Loop(t,nBins=100,xMin=40,xMax=120,PtBins=[0,100,150,200,250,300,400,500,1000],EtaBins=[0,0.5,1.0,1.5],maxentries=-1):
	entry=Entry()
	photonIsoFPRRandomConePhoton=ROOT.std.vector(float)()
	photonPt=ROOT.std.vector(float)()
	photonEta=ROOT.std.vector(float)()
	photonid_sieie=ROOT.std.vector(float)()
	photonPassConversionVeto=ROOT.std.vector(float)()

	t.SetBranchAddress("isRealData",ROOT.AddressOf(entry,'isRealData'))
	t.GetEntry(0);#update isRealData
	t.SetBranchAddress("photonIsoFPRRandomConePhoton"	,ROOT.AddressOf(photonIsoFPRRandomConePhoton) )
	t.SetBranchAddress("photonPt"	,ROOT.AddressOf(photonPt) )
	t.SetBranchAddress("photonEta"	,ROOT.AddressOf(photonEta) )
	t.SetBranchAddress("rho",ROOT.AddressOf(entry,'rho'))
	t.SetBranchAddress("nVtx",ROOT.AddressOf(entry,'nVtx'))
	t.SetBranchAddress("photonid_sieie",ROOT.AddressOf(photonid_sieie));
	t.SetBranchAddress("photonPassConversionVeto",ROOT.AddressOf(photonPassConversionVeto));

	#H=ROOT.std.map(ROOT.std.pair(string,ROOT.TH2D))()
	H={}
	for iPt in range(0,len(PtBins)-1):
		for iEta in range(0,len(EtaBins)-1):
			name="rho_vs_nvtx"+UniqName(PtBins,iPt,EtaBins,iEta)
			if(DEBUG>1): print "Going to create:" + name
			H[name]=ROOT.TH2D(name,name,nBins,xMin,xMax,1000,0,50)   
			name="iso_vs_nvtx"+UniqName(PtBins,iPt,EtaBins,iEta)
			if(DEBUG>1): print "Going to create:" + name
			H[name]=ROOT.TH2D(name,name,nBins,xMin,xMax,1000,0,50)  
	#loop
	if(DEBUG>1):
		for name in H:
			print "HISTO "+name+" is present in the database"

	if(maxentries<0):
		maxentries=t.GetEntries();
	else:
		print "Running on partial tree: MaxEntry="+str(maxentries)+"/"+str(t.GetEntries())
	for iEntry in range(0,maxentries):
		#if(iEntry>10000): 
		#	print "Exiting, too many entries"
		#	break
		t.GetEntry(iEntry)
		iPt=-1;iEta=-1;
		if( photonPt.size() <1): continue;
		GammaIdx=-1
		for iGamma in range(0,photonPt.size()):
			for i in range(0,len(PtBins)-1): 
				if( photonPt[iGamma]>= PtBins[i] and photonPt[iGamma] <=PtBins[i+1]): iPt=i;
			for i in range(0,len(EtaBins)-1): 
					if( abs(photonEta[iGamma])>= EtaBins[i] and abs(photonEta[iGamma]) <=EtaBins[i+1]): iEta=i;
			if iPt<0 or iEta<0 : continue;
			if photonid_sieie[iGamma]>0.011: continue;
			if photonPassConversionVeto[iGamma]<0.001: continue;
			GammaIdx=iGamma
			break;
		if GammaIdx<0 : continue;
		name="rho_vs_nvtx"+UniqName(PtBins,iPt,EtaBins,iEta)
		if(DEBUG>1): print "Going to Fill:" + name
		H[name].Fill(entry.nVtx,entry.rho);
		name="iso_vs_nvtx"+UniqName(PtBins,iPt,EtaBins,iEta)
		if(DEBUG>1): print "Going to Fill:" + name
		H[name].Fill(entry.nVtx,photonIsoFPRRandomConePhoton[GammaIdx]);
	return H;


print "PARSING"
#####################
usage = "usage: %prog [options] arg1 arg2"
parser = OptionParser(usage=usage)
parser.add_option("-d","--dirName"  ,dest='dirName' ,type='string',help="directory on eos root://eoscms///store/...",default="root://eoscms///store/user/amarini/zjets_V00-12")
parser.add_option("-x","--dataName" ,dest='dataName',type='string',help="data files comma separated",default="Photon_Run2012A-22Jan2013-v1_AOD_v2.root")
parser.add_option("-i","--inputDat" ,dest='inputDat',type='string',help="Configuration file",default="data/config.dat")
parser.add_option("-f","--fast" ,dest='fast',help="Run only on 50.000 entries",default=False,action='store_true')

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
	PrintDat(config)

try:	
	for tree in config["DataTree"]: 
		print "Added Tree "+tree
		data.Add(tree) 
except KeyError: 
	print "Going To Exit"
	exit

PtBins=ReadFromDat(config,"PtBins",[0,100,150,200,250,300,400,500,1000,2000],"--> Default PtBins")

EtaBins=ReadFromDat(config,"EtaBins",[0,.5,1,1.5],"--> Default EtaBins")

WorkDir=ReadFromDat(config,"WorkDir","./","-->Set Default WDIR")

print "Begin LOOP"

if(options.fast): maxentries=50000
else: maxentries=-1

H=Loop(data,40,0,40,PtBins,EtaBins,maxentries)

#LOAD ANALYSIS stat - inside there is the regression method
#ROOT.gSystem.Load("stat.so");

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
	
	x=ROOT.std.vector(float)();
	y=ROOT.std.vector(float)();
	e_y=ROOT.std.vector(float)();
	e2=ROOT.std.vector(float)();

	for iBin in range(1,h.GetNbinsX()+1):
		if(h.GetBinContent(iBin) >0 and rMin>h.GetBinLowEdge(iBin)): rMin=h.GetBinLowEdge(iBin);
		if(h.GetBinContent(iBin) >0 and rMax<h.GetBinLowEdge(iBin+1)): rMax=h.GetBinLowEdge(iBin+1);
		if(h.GetBinContent(iBin)> 0 ): 
			x.push_back  (h.GetBinCenter(iBin)  )
			y.push_back  (h.GetBinContent(iBin) )
			e_y.push_back(h.GetBinError(iBin)   )

	
	l=ROOT.TF1("lin","[0]+[1]*x",0,100)
	#R=ROOT.STAT.regression(x,y,e_y,e2)
	#l.SetParameter(0,R.first)
	#l.SetParameter(1,R.second)
	h.Fit("lin","N"); # does not implement correctly the chisquare with the sumw2

	outputStr=name;	
	outputStr=outputStr.replace("vs_nvtx_","");
	outputStr=outputStr.replace("pt","");
	outputStr=outputStr.replace("eta","");
	outputStr=outputStr.replace("_"," ");
	f.write( outputStr + " " + str(l.GetParameter(1)) +"\n" )
	#Save the histograms fitted in tf
	tf.cd()
	C=ROOT.TCanvas(name+"_C",name)
	H[name].Draw()
	h.SetLineColor(ROOT.kRed)	
	h.SetMarkerColor(ROOT.kRed)	
	h.Draw("P SAME")
	l.SetLineColor(ROOT.kBlue)
	l.SetLineWidth(2)
	l.Draw("L SAME");
	
	C.Write()

	x.clear()
	y.clear()
	e_y.clear()
	e2.clear()
	print "END STAGE "+name
	
print 
print 
print "******************************"
print "*            DONE            *"
print "******************************"
print 
print

