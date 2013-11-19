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

def Loop(t,PtCuts=[0,100,200,2000],nBins=30,mass=91,mw=30,maxentries=-1):
	entry=Entry()
	photonIsoFPRRandomConePhoton=ROOT.std.vector(float)()
	photonPt=ROOT.std.vector(float)()
	photonEta=ROOT.std.vector(float)()
	photonPhi=ROOT.std.vector(float)()
	photonE=ROOT.std.vector(float)()
	photonid_sieie=ROOT.std.vector(float)()
	photonid_r9=ROOT.std.vector(float)()
	photonid_hadronicOverEm=ROOT.std.vector(float)()
	photonhcalTowerSumEtConeDR03=ROOT.std.vector(float)()
	photontrkSumPtHollowConeDR03=ROOT.std.vector(float)()
	photonIsoFPRPhoton=ROOT.std.vector(float)()
	photonPfIsoCharged02ForCicVtx0=ROOT.std.vector(float)()
	photonPassConversionVeto=ROOT.std.vector(float)()

	t.SetBranchAddress("isRealData",ROOT.AddressOf(entry,'isRealData'))
	t.GetEntry(0);#update isRealData
	t.SetBranchAddress("photonIsoFPRRandomConePhoton"	,ROOT.AddressOf(photonIsoFPRRandomConePhoton) )
	t.SetBranchAddress("photonPt"	,ROOT.AddressOf(photonPt) )
	t.SetBranchAddress("photonEta"	,ROOT.AddressOf(photonEta) )
	t.SetBranchAddress("photonPhi"	,ROOT.AddressOf(photonPhi) )
	t.SetBranchAddress("photonE"	,ROOT.AddressOf(photonE) )
	t.SetBranchAddress("photonhcalTowerSumEtConeDR03"	,ROOT.AddressOf(photonhcalTowerSumEtConeDR03) )
	t.SetBranchAddress("photontrkSumPtHollowConeDR03"	,ROOT.AddressOf(photontrkSumPtHollowConeDR03) )
	t.SetBranchAddress("photonPfIsoCharged02ForCicVtx0"	,ROOT.AddressOf(photonPfIsoCharged02ForCicVtx0) )
	t.SetBranchAddress("photonIsoFPRPhoton"	,ROOT.AddressOf(photonIsoFPRPhoton) )
	t.SetBranchAddress("rho",ROOT.AddressOf(entry,'rho'))
	t.SetBranchAddress("nVtx",ROOT.AddressOf(entry,'nVtx'))
	t.SetBranchAddress("photonid_sieie",ROOT.AddressOf(photonid_sieie));
	t.SetBranchAddress("photonid_r9",ROOT.AddressOf(photonid_r9));
	t.SetBranchAddress("photonid_hadronicOverEm",ROOT.AddressOf(photonid_hadronicOverEm));
	t.SetBranchAddress("photonPassConversionVeto",ROOT.AddressOf(photonPassConversionVeto));
	#electrons
	lepPt=ROOT.std.vector(float)()
	lepEta=ROOT.std.vector(float)()
	lepPhi=ROOT.std.vector(float)()
	lepE=ROOT.std.vector(float)()
	t.SetBranchAddress("lepPt"	,ROOT.AddressOf(lepPt) )
	t.SetBranchAddress("lepEta"	,ROOT.AddressOf(lepEta) )
	t.SetBranchAddress("lepPhi"	,ROOT.AddressOf(lepPhi) )
	t.SetBranchAddress("lepE"	,ROOT.AddressOf(lepE) )

	H={}

	#H=ROOT.std.map(ROOT.std.pair(string,ROOT.TH2D))()
	for iEntry in range(0,maxentries):
		t.GetEntry(iEntry)
		if lepPt.size() <=0 : continue; #No Electron
	
		if lepPt.size() >1 : isEE=True
		else: isEE=False

		#G PreSelection
		electron=ROOT.TLorentzVector()
		electron.SetPtEtaPhiE( lepPt[0],lepEta[0],lepPhi[0],lepE[0]  )
		electron2=ROOT.TLorentzVector()
		if isEE: electron2.SetPtEtaPhiE( lepPt[1],lepEta[1],lepPhi[1],lepE[1]  )
		
		#ETA
		#G
		GammaIdx=-1
		gamma=ROOT.TLorentzVector()
		for iGamma in range(0,photonPt.size() ):
			gamma.SetPtEtaPhiE( photonPt[iGamma],photonEta[iGamma],photonPhi[iGamma],photonE[iGamma])
			if math.abs( gamma.Eta() ) >= 1.4 : continue;
		##
			if photonid_sieie[iGamma] >0.014: continue;
			if photonid_r9[iGamma]>=0.9:
				if photonid_hadronicOverEm[iGamma] >0.082: continue; 
				if photonhcalTowerSumEtConeDR03[iGamma] > 50 + 0.005*(*photonPt)[iGamma] : continue;
				if photontrkSumPtHollowConeDR03[iGamma] > 50 + 0.002*(*photonPt)[iGamma] :continue;
			else:
				if photonid_hadronicOverEm[iGamma] >0.075:  continue; 
				if photonhcalTowerSumEtConeDR03[iGamma] > 4 + 0.005*(*photonPt)[iGamma] : continue;
				if photontrkSumPtHollowConeDR03[iGamma] > 4 + 0.002*(*photonPt)[iGamma] : continue;
			
			if photonPfIsoCharged02ForCicVtx0[iGamma] > 4 : continue;
			if photonIsoFPRPhoton[iGamma]> 10: continue;  /
			GammaIdx=iGamma
			break;
		if GammaIdx <0 : isEG=True; #NO GAMMA
		else: isEG=False

		# ELECTRON - GAMMA
		if isEG:
			eg=electron+gamma
			if eg.M() < mass-mw or eg.M()>mass+mv: continue
			p=-1
			for pp in range(0,len(PtCuts)):
				if gamma.Pt() >= PtCuts[pp] and gamma.Pt() < PtCuts[pp]: 
					p=pp
			if p<0: continue;
			Name="Mass_EG_"+"Pt_"+str(PtCuts[p])+"_"+str(PtCuts[p+1])
			try:
				H[Name]	
			except KeyError:
				H[Name]=ROOT.TH1F(Name,Name,nBins,mass-mw,mass+mw)	
			
			H[Name].Fill(eg.M())	
		if isEE:
			ee=electron+electron2
			if ee.M() < mass-mw or ee.M()>mass+mv: continue
			p1=-1
			p2=-1
			for pp in range(0,len(PtCuts)):
				if electron.Pt() >= PtCuts[pp] and electron.Pt() < PtCuts[pp]: 
					p1=pp
				if electron2.Pt() >= PtCuts[pp] and electron2.Pt() < PtCuts[pp]: 
					p2=pp
			if p1>= 0 :
				Name="Mass_EE_"+"Pt_"+str(PtCuts[p1])+"_"+str(PtCuts[p1+1])
				try:
					H[Name]	
				except KeyError:
					H[Name]=ROOT.TH1F(Name,Name,nBins,mass-mw,mass+mw)	
				
				H[Name].Fill(ee.M())	

			if p2>=0 :
				Name="Mass_EE_"+"Pt_"+str(PtCuts[p2])+"_"+str(PtCuts[p2+1])
				try:
					H[Name]	
				except KeyError:
					H[Name]=ROOT.TH1F(Name,Name,nBins,mass-mw,mass+mw)	
				
				H[Name].Fill(ee.M())	
		#END OF FOR iEntries LOOP
	return H

print "PARSING"
#####################
usage = "usage: %prog [options] arg1 arg2"
parser = OptionParser(usage=usage)
parser.add_option("-i","--inputDat" ,dest='inputDat',type='string',help="Configuration file",default="data/config.dat")

(options,args)=parser.parse_args()

dataNames=options.dataName.split(',')


print "Adding Files"

data=ROOT.TChain("accepted/events")

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

PtCuts=ReadFromDat(config,"PtCuts",[0,100,150,200,250,300,400,500,1000,2000],"--> Default PtBins")

WorkDir=ReadFromDat(config,"WorkDir","./","-->Set Default WDIR")

print "Begin LOOP"

if(options.fast): maxentries=50000
else: maxentries=-1

H=Loop(data,PtCuts,maxentries)

print "Begin Analysis"
#DO PROFILE
f=open(WorkDir+"effarea.txt","w")
tf=ROOT.TFile.Open(WorkDir+"effarea.root","RECREATE")
tf.cd()
f.write( "#what ptmin ptmax etamin etamax value\n" )

	
print 
print 
print "******************************"
print "*            DONE            *"
print "******************************"
print 
print

