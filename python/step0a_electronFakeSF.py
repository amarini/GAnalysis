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
parser.add_option("-d","--debug" ,dest='debug',type='int',help="Debug Level 0 - 3. Default=%default",default=1)
parser.add_option("-r","--refit" ,dest='refit',type='string',help="Refit fileName",default="")

(options,args)=parser.parse_args()


import ROOT

DEBUG=options.debug
Refit=options.refit!=""
RefitFile=options.refit

if DEBUG>0:print "BEGIN"

WorkDir="./"

ROOT.gROOT.SetBatch()

ROOT.gROOT.ProcessLine (\
"struct Entry{ \
float rho;\
double PUWeight;\
int nVtx;\
bool isRealData;\
};" )

from ROOT import Entry
def UniqName(PtBins,iPt,EtaBins,iEta):
	return "_pt"+str(PtBins[iPt])+"_"+str(PtBins[iPt+1])+"_eta"+str(EtaBins[iEta])+"_"+str(EtaBins[iEta+1])

PtTriggers=[]
TriggerMenus=[]

def Loop(t,PtCuts=[0,100,200,2000],EtaCuts=[0,1.5],nBins=30,mass=91,mw=30,maxentries=-1,Extra=""):
	if DEBUG>0:
		print "PtCuts"
		print PtCuts
		print "EtaCuts"
		print EtaCuts
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
	if not entry.isRealData:
		t.SetBranchAddress("PUWeight",ROOT.AddressOf(entry,'PUWeight'))

	H={}

	#H=ROOT.std.map(ROOT.std.pair(string,ROOT.TH2D))()
	if maxentries < 0:
		ment=t.GetEntries()
	else:
		print "Max Entries Set to " + str(maxentries)
		ment=maxentries
	for iEntry in range(0,ment):
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
			if DEBUG >1:print "EG Mass="+str(eg.M())
			if eg.M() < mass-mw or eg.M()>mass+mw: continue
			if DEBUG >1:print "Mass Pass"
			p=-1
			e=-1
			for pp in range(0,len(PtCuts)-1):
				if gamma.Pt() >= PtCuts[pp] and gamma.Pt() < PtCuts[pp+1]: 
					p=pp
					break
			for ee in range(0,len(EtaCuts)-1):
				if math.fabs(gamma.Eta()) >= EtaCuts[ee] and math.fabs(gamma.Eta()) < EtaCuts[ee+1]: 
					e=ee
					break;
			if DEBUG >1:print "Pt="+str(gamma.Pt()) + " bin = " + str(p)
			if p<0: continue;
			if DEBUG >1:print "Eta="+str(gamma.Eta()) + " bin = " + str(e)
			if DEBUG >1:print "PT Pass"
			if e<0: continue;
			if DEBUG >1:print "Eta Pass"
			Name=Extra+"Mass_EG_"+"Pt_"+str(PtCuts[p])+"_"+str(PtCuts[p+1])+"_Eta_"+str(EtaCuts[e])+"_"+str(EtaCuts[e+1])
			try:
				H[Name].Integral()
			except KeyError,TypeError:
				if DEBUG >0:print "Creating histo with Name " + Name
				H[Name]=ROOT.TH1F(Name,Name,nBins,mass-mw,mass+mw)	
				
			if entry.isRealData:
				weight=1
			else: weight=PUWeight
			H[Name].Fill(eg.M(),weight)	
		#END OF FOR iEntries LOOP
	return H



data=ROOT.TChain("accepted/events")
mc=ROOT.TChain("accepted/events")

if DEBUG>0:print "Load Configuration"
from common import *
config=read_dat(options.inputDat);
configMC=read_dat(options.inputDatMC);
#SET BRANCH ADDRESSES -- LOOP
if(DEBUG>0):
	PrintDat(config)
if DEBUG>0:
	PrintDat(configMC)

if not Refit:
	try:	
		for tree in config["DataTree"]: 
			if DEBUG>0:print "Added Tree "+tree
			data.Add(tree) 
		for tree in configMC["DataTree"]: 
			if DEBUG>0:print "Added Tree to MC "+tree
			mc.Add(tree) 
	except KeyError: 
		print "Going To Exit"
		exit

#PtCuts=ReadFromDat(config,"PtCuts",[0,100,150,200,250,300,400,500,1000,2000],"--> Default PtBins")

WorkDir=ReadFromDat(config,"WorkDir","./","-->Set Default WDIR")
WorkDirMC=ReadFromDat(configMC,"WorkDir","./","-->Set Default WDIR")

PtTriggers=ReadFromDat(config,"PtTriggers",[],"-->No Triggers Pt")
TriggerMenus=ReadFromDat(config,"TriggerMenus",[],"--> No Trigger Menus")

if Refit:
	if os.path.abspath(RefitFile) == os.path.abspath(WorkDirMC+"electrongamma.root"):
		print "-- ERROR input file and output file should be different"	
		print "-- " + os.path.abspath(RefitFile) 
		sys.exit(1)
tf=ROOT.TFile.Open(WorkDirMC+"electrongamma.root","RECREATE")
tf.cd()

if(options.fast): maxentries=50000
else: maxentries=-1

nBins=30
mZ=91
mw=30 #mass window
EtaCuts=[0,.5,1.,1.5]
PtCuts=[0,30,50,100,200,8000]

if not Refit:
	if DEBUG>0:print "Begin LOOP"
	H=Loop(data,PtCuts,EtaCuts,nBins,mZ,mw,maxentries)
if not Refit:
	if DEBUG>0:print "Begin LOOP MC"
	HMC=Loop(mc,PtCuts,EtaCuts,nBins,mZ,mw,maxentries,"MC_")

if Refit:
	if DEBUG>0:print "Open File To Be Refit"
	iFile=ROOT.TFile.Open(RefitFile)
	H={}
	HMC={}
	for e in range(0,len(EtaCuts)-1):	
		for p in range(0,len(EtaCuts)-1):	
			Name="Mass_EG_"+"Pt_"+str(PtCuts[p])+"_"+str(PtCuts[p+1])+"_Eta_"+str(EtaCuts[e])+"_"+str(EtaCuts[e+1])
			H[Name]=iFile.Get(Name)
			Name="MC_Mass_EG_"+"Pt_"+str(PtCuts[p])+"_"+str(PtCuts[p+1])+"_Eta_"+str(EtaCuts[e])+"_"+str(EtaCuts[e+1])
			HMC[Name]=iFile.Get(Name)

if DEBUG>0:print "Begin Fit"
f=open(WorkDirMC+"electrongamma.txt","w")
f.write( "# ptmin ptmax etamin etamax s.f. (data/mc)\n" )

tf.cd()
############## FIT ###########################
for name in H:
	if DEBUG>0:print "Doing Histos "+name
	try:
		H[name].Write();
	except TypeError:
		print "Data Histo "+name+" does not exist"
		continue

	try:
		isTH1=HMC["MC_"+name].InheritsFrom("TH1")
	except (TypeError,KeyError):
		isTH1=0
	if not isTH1:
		print "MC Histo "+name +" is not TH1"
		continue;
	
	HMC["MC_"+name].Write()

	llM=ROOT.RooRealVar("llM","llM",mZ-mw,mZ+mw);
	#construct targets to fit
	#Normalize
	H[name].Sumw2();
	HMC["MC_"+name].Sumw2();
	H[name].Scale(1./H[name].Integral());
	HMC["MC_"+name].Scale(1./HMC["MC_"+name].Integral());
	h_data=  ROOT.RooDataHist("data_"+name,"hist data",ROOT.RooArgList(llM),H[name])
	h_mc  =  ROOT.RooDataHist("mc_"+name,"hist mc",ROOT.RooArgList(llM),HMC["MC_"+name])
	
	#construct signal model
	mass =  ROOT.RooRealVar("mass","mass",mZ,mZ-mw,mZ+mw) ;
        width=  ROOT.RooRealVar("width","width",5,.1,10) ;
        sigma=  ROOT.RooRealVar("sigma","sigma",5,0.1,8) ;
        
        sig  =  ROOT.RooVoigtian("sig","sig",llM,mass,sigma,width) ; 
	#construct bkg Model
        a    =  ROOT.RooRealVar("a","a",1,0,100000) ;
        b    =  ROOT.RooRealVar("b","b",10,-100,100) ;
        c    =  ROOT.RooRealVar("c","c",10,-100,100) ;
        bkg  =  ROOT.RooGenericPdf("bkg","a+b*llM + c*llM*llM",ROOT.RooArgList(llM,a,b,c));
        #bkg  =  ROOT.RooGenericPdf("bkg","a+b*llM",ROOT.RooArgList(llM,a,b));

	#construct fit model	
        frac =  ROOT.RooRealVar("frac","fraction",0.01,1.) ;
        model=  ROOT.RooAddPdf("model","model",sig,bkg,frac);

	#fit
        r_data=model.fitTo(h_data,ROOT.RooFit.SumW2Error(ROOT.kTRUE));
	fr_data=frac.getVal()
	C=ROOT.TCanvas("C_"+name,"C_"+name)
	frame= llM.frame()
	h_data.plotOn(frame)
	model.plotOn(frame)
	model.plotOn(frame,ROOT.RooFit.Components("bkg"),ROOT.RooFit.LineStyle(ROOT.kDashed))
	frame.Draw();
	C.Write()
	frame.Write("frame_"+name)
	
        r_mc=model.fitTo(h_mc,ROOT.RooFit.SumW2Error(ROOT.kTRUE));
	fr_mc=frac.getVal()
	C=ROOT.TCanvas("C_MC_"+name,"C_"+name+"_MC")
	frame= llM.frame()
	h_mc.plotOn(frame)
	model.plotOn(frame)
	model.plotOn(frame,ROOT.RooFit.Components("bkg"),ROOT.RooFit.LineStyle(ROOT.kDashed))
	frame.Draw();
	C.Write()
	frame.Write("frame_MC_"+name)
	
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

