#!/usr/bin/python
import sys,os
import array
import ROOT
import time
from optparse import OptionParser

print "BEGIN"

ROOT.gROOT.ProcessLine (\
"struct Entry{ \
float llM; \
float llPt; \
float weight;\
float rho;\
float nVtx;\
bool isRealData;\
};" )

from ROOT import Entry

def Loop(t,sys=0,RD=False,var='llM',nBins=100,xMin=40,xMax=120):
	entry=Entry()
	jetPt=ROOT.std.vector(float)()
        jetEta=ROOT.std.vector(float)()
        jetPhi=ROOT.std.vector(float)()
        jetE=ROOT.std.vector(float)()
        jetRMS=ROOT.std.vector(float)()
        jetBeta = ROOT.std.vector(float)()
        lepPt=ROOT.std.vector(float)()
        lepEta=ROOT.std.vector(float)()
        lepPhi=ROOT.std.vector(float)()
        lepE=ROOT.std.vector(float)()
	lepChId=ROOT.std.vector(int)()

	t.SetBranchAddress("isRealData",ROOT.AddressOf(entry,'isRealData'))
	t.GetEntry(0);#update isRealData
	t.SetBranchAddress("jetPt"	,ROOT.AddressOf(jetPt) )
	t.SetBranchAddress("jetEta"	,ROOT.AddressOf(jetEta) )
	t.SetBranchAddress("jetPhi"	,ROOT.AddressOf(jetPhi) )
	t.SetBranchAddress("jetE"	,ROOT.AddressOf(jetE) )
	t.SetBranchAddress("jetRMS"	,ROOT.AddressOf(jetRMS) )
	t.SetBranchAddress("jetBeta"	,ROOT.AddressOf(jetBeta) )
	t.SetBranchAddress("lepPt"	,ROOT.AddressOf(lepPt) )
	t.SetBranchAddress("lepEta"	,ROOT.AddressOf(lepEta) )
	t.SetBranchAddress("lepPhi"	,ROOT.AddressOf(lepPhi) )
	t.SetBranchAddress("lepE"	,ROOT.AddressOf(lepE) )
	t.SetBranchAddress("lepChId"	,ROOT.AddressOf(lepChId) )
	lumi=1.0
	if RD and not entry.isRealData:
		lumi=1.0;
		if sys==0:
			t.SetBranchAddress("RDWeight",ROOT.AddressOf(entry,'weight'))
		elif sys>0:
			t.SetBranchAddress("RDWeightSysUp",ROOT.AddressOf(entry,'weight'))
		else:
			t.SetBranchAddress("RDWeightSysDown",ROOT.AddressOf(entry,'weight'))
			
	elif not RD and not entry.isRealData:
		lumi=19.7
		if sys==0:
			t.SetBranchAddress("PUWeight",ROOT.AddressOf(entry,'weight'))
		elif sys>0:
			t.SetBranchAddress("PUWeightSysUp",ROOT.AddressOf(entry,'weight'))
		else :
			t.SetBranchAddress("PUWeightSysDown",ROOT.AddressOf(entry,'weight'))
	t.SetBranchAddress("rho",ROOT.AddressOf(entry,'rho'))
	t.SetBranchAddress("nVtx",ROOT.AddressOf(entry,'nVtx'))
	
	v=ROOT.AddressOf(entry,var)
	h=ROOT.TH1F("h","h",nBins,xMin,xMax)
	#loop
	for iEntry in range(0,t.GetEntries()):
		t.GetEntry(iEntry)	
		if len(lepPt) <2: continue;
		#select jet
		l1=ROOT.TLorentzVector()
		l2=ROOT.TLorentzVector()
		l1.SetPtEtaPhiE(lepPt.at(0),lepEta.at(0),lepPhi.at(0),lepE.at(0))
		l2.SetPtEtaPhiE(lepPt.at(1),lepEta.at(1),lepPhi.at(1),lepE.at(1))
		jetList=[]
		for iJet in range(0,jetPt.size()):
			j=ROOT.TLorentzVector()
			j.SetPtEtaPhiE(jetPt[iJet],jetEta[iJet],jetPhi[iJet],jetE[iJet])
			#jetPt
			if j.Pt()<30: continue;
			#lepton rejection
			if j.DeltaR(l1) < 0.5 or j.DeltaR(l2)<0.5: continue;
			#PU ID
			#if( ( 1. - jetBeta[k] >= 0.2 * TMath.Log( nVtx - 0.67)))
			if 1.-jetBeta[iJet] >= 0.2* ROOT.TMath.Log(entry.nVtx-0.67) : continue
			if jetRMS[iJet] > ROOT.TMath.Sqrt(0.06): continue;
			jetList.append(iJet)
		#selection
		#llM
		if abs(entry.llM - 91) >20 : continue;
		#chid
		if lepChId[0]*lepChId[1] !=-1 and lepChId[0]*lepChId[1] !=-4 : continue;
		# jet
		if len(jetList)<=0 : continue;
		h.Fill(v,entry.weight);
	return h;


print "PARSING"
#####################
usage = "usage: %prog [options] arg1 arg2"
parser = OptionParser(usage=usage)
parser.add_option("-d","--dirName"  ,dest='dirName' ,type='string',help="directory on eos root://eoscms///store/...",default="root://eoscms///store/user/amarini/zjets_V00-12")
parser.add_option("-m","--mcName"   ,dest='mcName'  ,type='string',help="mc files comma separated, with *",default="DYJetsToLL_M-50_TuneZ2Star_8TeV-madgraph-tarball_Summer12_DR53X-PU_S10_START53_V7A-v1.root,TTJets_MassiveBinDECAY_TuneZ2star_8TeV-madgraph-tauola_Summer12_DR53X-PU_S10_START53_V7C-v1.root")
parser.add_option("-x","--dataName" ,dest='dataName',type='string',help="data files comma separated",default="DYJetsToLL_M-50_TuneZ2Star_8TeV-madgraph-tarball_Summer12_DR53X-PU_S10_START53_V7A-v1.root,")
parser.add_option("-l","--legendName" ,dest='legendName',type='string',help="legend names comma separated",default="DY,TT")
parser.add_option("-r","--runDep" ,action='store_true',dest='RD',help="is RD? defalut =false",default=False)
#parser.add_option("-h","--help" , action='store_true', dest='help',help="Print Help",default=False)

(options,args)=parser.parse_args()

#if options.help:
#parser.print_help()
#exit(0)

fileNames=options.mcName.split(',')
dataNames=options.mcName.split(',')

print "Adding Files"
iName=0
mc=[]
for name in fileNames:
	mc.append( ROOT.TChain("accepted/events") )
	mc[iName].Add(options.dirName+"/"+name)
	iName+=1

data=ROOT.TChain("accepted/events")
for name in dataNames:
	data.Add(options.dirName+"/"+name)
#SET BRANCH ADDRESSES -- LOOP

print "Begin LOOP"
Hdata=Loop(data,0,options.RD,'llM',100,40,120)

Hdata.SetMarkerStyle(20)
Hdata.SetLineColor(ROOT.kBlack)
Hdata.SetMarkerColor(ROOT.kBlack)

Hmc=[]
for iMc in range(0,len(mc)):
	Hmc.append( Loop(mc[iMc],0,options.RD,'llM',100,40,120) )

L = ROOT.TLegend(0.75,0.75,.89,.89)
L.SetFillStyle(0)
L.SetBorderSize(0)
L.AddEntry(Hdata,"data","P");

S=ROOT.THStack("s","s");	
H=ROOT.TH1F("mc","mc",100,40,120)
l=options.legendName.split(',')
for iMc in range(0,len(mc)):
	Hmc[iMc].SetFillColor(
		{0:ROOT.kYellow,
		 1:ROOT.kMagenta+2,
		 2:ROOT.kGreen+2}.get(iMc,ROOT.kWhite)
		)
	Hmc[iMc].SetLineColor(ROOT.kBlack)
	Hmc[iMc].SetLineWidth(2)
	S.Add(Hmc[iMc])
	H.Add(Hmc[iMc])
	if iMc< len(l) and len(l[iMc])>0:
		L.AddEntry(Hmc[iMc],l[iMc],"F");

C=ROOT.TCanvas("c","c",800,800);
Pup = ROOT.TPad("up","up",0,0.3,1.0,1.0)
Pdn = ROOT.TPad("dn","dn",0,0.0,1.0,0.3)
Pup.Draw()
Pdn.Draw()

#draw up plot
Pup.cd()
S.Draw("HIST ")
Hdata.Draw("P SAME")
L.Draw("SAME")

Pdn.cd()
Pdn.SetGridy()
r = Hdata.Clone("ratio")
r.Divide(H)
r.Draw("P")

C.SaveAs("canvas.pdf")

time.sleep(10)	
