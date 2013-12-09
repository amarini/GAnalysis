#!/usr/bin/python
import sys,os
import array
import time
import math
from optparse import OptionParser

print "PARSING"
#####################
usage = "usage: %prog [options] arg1 arg2"
parser = OptionParser(usage=usage)
parser.add_option("-i","--inputDat" ,dest='inputDat',type='string',help="Configuration file",default="data/config.dat")
parser.add_option("-j","--inputDatMC" ,dest='inputDatMC',type='string',help="Configuration file for MC",default="data/configMC.dat")
parser.add_option("-f","--fast",dest='fast',action='store_true',help="Run on limited n. of entries",default=False)

(options,args)=parser.parse_args()


import ROOT

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

PtTriggers=[]
TriggerMenus=[]

def Loop(t,PtCuts=[0,100,200,2000],EtaCuts=[0,1.5],nBins=30,mass=91,mw=30,maxentries=-1):
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
	TriMatchF4Path_photon = ROOT.std.vector(int)()
	

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
        t.SetBranchAddress("TriMatchF4Path_photon",ROOT.AddressOf( TriMatchF4Path_photon)); 
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
	if maxentries < 0:
		maxentries=t.GetEntries()
	for iEntry in range(0,maxentries):
		t.GetEntry(iEntry)
		if lepPt.size() <=0 : continue; #No Electron
	
		electron=ROOT.TLorentzVector()
		electron.SetPtEtaPhiE( lepPt[0],lepEta[0],lepPhi[0],lepE[0]  )
		
		#G PreSelection
		#ETA
		#G
		GammaIdx=-1
		gamma=ROOT.TLorentzVector()
		for iGamma in range(0,photonPt.size() ):
			gamma.SetPtEtaPhiE( photonPt[iGamma],photonEta[iGamma],photonPhi[iGamma],photonE[iGamma])
			if math.fabs( gamma.Eta() ) >= 1.4 : continue;
		##
			if photonid_sieie[iGamma] >0.014: continue;
			if photonid_r9[iGamma]>=0.9:
				if photonid_hadronicOverEm[iGamma] >0.082: continue; 
				if photonhcalTowerSumEtConeDR03[iGamma] > 50 + 0.005*photonPt[iGamma] : continue;
				if photontrkSumPtHollowConeDR03[iGamma] > 50 + 0.002*photonPt[iGamma] :continue;
			else:
				if photonid_hadronicOverEm[iGamma] >0.075:  continue; 
				if photonhcalTowerSumEtConeDR03[iGamma] > 4 + 0.005*photonPt[iGamma] : continue;
				if photontrkSumPtHollowConeDR03[iGamma] > 4 + 0.002*photonPt[iGamma] : continue;
			
			if photonPfIsoCharged02ForCicVtx0[iGamma] > 4 : continue;
			if photonIsoFPRPhoton[iGamma]> 10: continue;  
			trigger=TriMatchF4Path_photon[iGamma]
			## Select the right trigger
			if entry.isRealData and len(PtTriggers)>0:
				####
				j=-1
				for i in range(0,len(PtTriggers)):
					if gamma.Pt() >= PtTriggers[i][0] and gamma.Pt()< PtTriggers[i][1]: j=1
				if j<0: continue; #no trigger
				if   TriggerMenus[j] == "HLT_Photon20_CaloIdVL_v*"      and not (trigger&1): continue;
				elif TriggerMenus[j] == "HLT_Photon20_CaloIdVL_IsoL_v*"  and not (trigger &  2     ) : continue;
				elif TriggerMenus[j] == "HLT_Photon30_v*"                and not (trigger &  4     ) : continue;
				elif TriggerMenus[j] == "HLT_Photon30_CaloIdVL_v*"       and not (trigger &  8     ) : continue;
				elif TriggerMenus[j] == "HLT_Photon30_CaloIdVL_IsoL_v*"  and not (trigger &  16    ) : continue;
				elif TriggerMenus[j] == "HLT_Photon50_CaloIdVL_v*"       and not (trigger &  32    ) : continue;
				elif TriggerMenus[j] == "HLT_Photon50_CaloIdVL_IsoL_v*"  and not (trigger &  64    ) : continue;
				elif TriggerMenus[j] == "HLT_Photon75_CaloIdVL_v*"       and not (trigger &  128   ) : continue;
				elif TriggerMenus[j] == "HLT_Photon75_CaloIdVL_IsoL_v*"  and not (trigger &  256   ) : continue;
				elif TriggerMenus[j] == "HLT_Photon90_CaloIdVL_v*"       and not (trigger &  512   ) : continue;
				elif TriggerMenus[j] == "HLT_Photon90_CaloIdVL_IsoL_v*"  and not (trigger &  1024  ) : continue;
				elif TriggerMenus[j] == "HLT_Photon135_v*"               and not (trigger &  2048  ) : continue;
				elif TriggerMenus[j] == "HLT_Photon150_v*"               and not (trigger &  4096  ) : continue;
			GammaIdx=iGamma
			break;
		if GammaIdx <0 : 
			isEG=True; #NO GAMMA
		else: isEG=False

		# ELECTRON - GAMMA
		if isEG:
			eg=electron+gamma
			print "EG Mass="+str(eg.M())
			if eg.M() < mass-mw or eg.M()>mass+mw: continue
			print "Mass Pass"
			p=-1
			e=-1
			for pp in range(0,len(PtCuts)):
				if gamma.Pt() >= PtCuts[pp] and gamma.Pt() < PtCuts[pp]: 
					p=pp
			for ee in range(0,len(EtaCuts)):
				if math.fabs(gamma.Eta()) >= EtaCuts[ee] and math.fabs(gamma.Eta()) < EtaCuts[ee]: 
					e=ee
			print "Pt="+str(gamma.Pt())
			if p<0: continue;
			print "Eta="+str(gamma.Eta())
			print "PT Pass"
			if e<0: continue;
			print "Eta Pass"
			Name="Mass_EG_"+"Pt_"+str(PtCuts[p])+"_"+str(PtCuts[p+1])+"_Eta_"+str(EtaCuts[e])+"_"+str(EtaCuts[e+1])
			try:
				H[Name].Integral()
			except KeyError,TypeError:
				print "Creating histo with Name " + Name
				H[Name]=ROOT.TH1F(Name,Name,nBins,mass-mw,mass+mw)	
				
			
			H[Name].Fill(eg.M())	
		#END OF FOR iEntries LOOP
	return H



print "Adding Files"

data=ROOT.TChain("accepted/events")
mc=ROOT.TChain("accepted/events")

print "Load Configuration"
from common import *
config=read_dat(options.inputDat);
configMC=read_dat(options.inputDatMC);
#SET BRANCH ADDRESSES -- LOOP
if(DEBUG>0):
	PrintDat(config)
if DEBUG>0:
	PrintDat(configMC)

try:	
	for tree in config["DataTree"]: 
		print "Added Tree "+tree
		data.Add(tree) 
	for tree in configMC["DataTree"]: 
		print "Added Tree to MC "+tree
		mc.Add(tree) 
except KeyError: 
	print "Going To Exit"
	exit

#PtCuts=ReadFromDat(config,"PtCuts",[0,100,150,200,250,300,400,500,1000,2000],"--> Default PtBins")

WorkDir=ReadFromDat(config,"WorkDir","./","-->Set Default WDIR")
WorkDirMC=ReadFromDat(configMC,"WorkDir","./","-->Set Default WDIR")

PtTriggers=ReadFromDat(config,"PtTriggers",[],"-->No Triggers Pt")
TriggerMenus=ReadFromDat(config,"TriggerMenus",[],"--> No Trigger Menus")


tf=ROOT.TFile.Open(WorkDirMC+"electrongamma.root","RECREATE")
tf.cd()

if(options.fast): maxentries=50000
else: maxentries=-1

nBins=30
mZ=91
mw=30 #mass window
EtaCuts=[0,.5,1.,1.5]
PtCuts=[0,30,50,100,200,8000]
print "Begin LOOP"
H=Loop(data,PtCuts,EtaCuts,nBins,mZ,mw,maxentries)
print "Begin LOOP MC"
HMC=Loop(mc,PtCuts,EtaCuts,nBins,mZ,mw,maxentries)

print "Begin Fit"
f=open(WorkDirMC+"electrongamma.txt","w")
f.write( "# ptmin ptmax etamin etamax s.f. (data/mc)\n" )

##FIT
for name in H:
	print "Doing Histos "+name
	H[name].Write();
	HMC[name].Write(name+"_MC")

	llM=ROOT.RooRealVar("llM","llM",mZ-mw,mZ+mw);
	#construct targets to fit
	h_mc  =  ROOT.RooDataHist("mc_"+name,"hist mc",llM,HMC[name])
	h_data=  ROOT.RooDataHist("data_"+name,"hist data",llM,H[name])
	
	#construct signal model
	mass =  ROOT.RooRealVar("mass","mass",mZ,mZ-mw,mZ+mw) ;
        sigma=  ROOT.RooRealVar("sigma","sigma",1,0.1,20) ;
        width=  ROOT.RooRealVar("width","width",1,0.5,20) ;
        
        sig  =  ROOT.RooVoigtian("sig","sig",llM,mass,sigma,width) ; 
	#construct bkg Model
        a    =  ROOT.RooRealVar("a","a",0,100000) ;
        b    =  ROOT.RooRealVar("b","b",-10,10) ;
        bkg  =  ROOT.RooGenericPdf("bkg","a+b*llM",RooArgSet(llM,a,b));

	#construct fit model	
        frac =  ROOT.RooRealVar("frac","fraction",0.01,1.) ;
        model=  ROOT.RooAddPdf("model","model",RooArgList(sig,bkg),frac);

	#fit
        r_data=model.fitTo(h_data);
	fr_data=frac.getVal()
	C=ROOT.TCanvas("C_"+name,"C_"+name)
	frame= llM.frame()
	model.plotOn(frame)
	model.plotOn(frame,ROOT.Components(bkg))
	h_data.plotOn(frame)
	C.Write()
	
        r_mc=model.fitTo(h_mc);
	fr_mc=frac.getVal()
	C=ROOT.TCanvas("C_"+name+"_MC","C_"+name+"_MC")
	frame= llM.frame()
	model.plotOn(frame)
	model.plotOn(frame,ROOT.Components(bkg))
	h_mc.plotOn(frame)
	C.Write()
	
	#name="Mass_EG_"+"Pt_"+str(PtCuts[p])+"_"+str(PtCuts[p+1])+"_Eta_"+str(EtaCuts[e])+"_"+str(EtaCuts[e+1])	
	s=name.replace('Mass_EG_Pt_','')
	s=s.replace('Eta_','') 
	s=s.replace('_',' ') #space
	f.write("%s %.3f\n"%(s,fr_data/fr_mc))

	
print 
print 
print "******************************"
print "*            DONE            *"
print "******************************"
print 
print

