#!/usr/bin/python
import sys,os
import array
import ROOT
import time
import math
from optparse import OptionParser

DEBUG=1

ROOT.gROOT.SetBatch()
ROOT.gStyle.SetOptStat(0)
ROOT.gStyle.SetOptTitle(0)

if(DEBUG>0):print "----- BEGIN -----"

if(DEBUG>0):print "-PARSING OPTIONS-"
usage = "usage: %prog [options] arg1 arg2"
parser=OptionParser(usage=usage)
parser.add_option("","--inputDat" ,dest='inputDat',type='string',help="Input Configuration file for Ratio",default="data/configRatio.dat")

(options,args)=parser.parse_args()

###
print "inserting in path cwd"
sys.path.insert(0,os.getcwd())
print "inserting in path cwd/python"
sys.path.insert(0,os.getcwd()+'/python')
from common import *
### READ DAT#########
def ReadRatioDat( inputDat ):
	f=open( inputDat,"r" )
	R={}
	R['Cut']=[]
	R['Syst']=[]
	for l in f:
	   try:
		l0=l.split('#')[0]
		if l0 == "" : continue;
		l0=l0.replace('\n','')
		l0=l0.replace('\r','')
		parts=l0.split(' ')
		if len(parts) == 0 : continue;
		if   parts[0] == 'file1': 
			R["file1"]=parts[1]
		elif parts[0] == 'file2': 
			R["file2"]=parts[1]
		elif parts[0] == 'histoName1': R["histoName1"]=parts[1]
		elif parts[0] == 'histoName2': R["histoName2"]=parts[1]
		elif parts[0] == 'Cut':
			#default
			ht=0
			nj=1
			ptj=30
			for j in range(1,len(parts)):
				if 'Ht' == parts[j].split('=')[0]:ht=parts[j].split('=')[1]
				if 'nJets' == parts[j].split('=')[0]:nj=parts[j].split('=')[1]
				if 'ptJet' == parts[j].split('=')[0]:ptj=parts[j].split('=')[1]
			R['Cut'].append( (ht,nj,ptj) );
		elif parts[0] == 'Syst':
			name=parts[1]
			typ=parts[2]
			hn1=parts[3]
			hn2=parts[4]
			R['Syst'].append( (name,typ,hn1,hn2) )
		elif parts[0] == 'Up':
			R['Up']=[]
			R['Up'].append(parts[1])
			R['Up'].append(parts[2])
		elif parts[0] == 'Down':
			R['Down']=[]
			R['Down'].append(parts[1])
			R['Down'].append(parts[2])
		elif parts[0] == 'Out':
			R['Out']=parts[1]
		elif parts[0] == 'PrePendSyst':
			R['PrePendSyst']=parts[1]
	   except: 
		print "Malformed line (probably ignored):"+l
			
	return R;
		
config = ReadRatioDat(options.inputDat)
##########################

def makeBands(h1,h2,type="Mean"):
	H=h1.Clone(h1.GetName()+"_band")
	for i in range(1,h1.GetNbinsX()+1):
		if type=="First":
			H.SetBinContent(i, h1.GetBinContent(i))
			H.SetBinError  (i, math.fabs(h1.GetBinContent(i)-h2.GetBinContent(i) ))
		else: #type = "Mean"
			H.SetBinContent(i, (h1.GetBinContent(i)+h2.GetBinContent(i) )/2.0)
			H.SetBinError  (i, math.fabs(h1.GetBinContent(i)-h2.GetBinContent(i) )/2.0)
	return H

epsilon=0.0001
def sqrtSum(h1,h2):
	for i in range (1,h2.GetNbinsX()+1):
		if h1.GetBinError(i)  > epsilon and h2.GetBinError(i)  > epsilon:
			e=math.sqrt( h1.GetBinError(i)**2 + h2.GetBinError(i)**2 )
		elif h1.GetBinError(i) <= epsilon and h2.GetBinError(i) <= epsilon:
			e=epsilon
		elif h1.GetBinError(i) > epsilon:
			e=h1.GetBinError(i)
		elif h2.GetBinError(i) > epsilon:
			e=h2.GetBinError(i)
		elif ROOT.TMath.IsNaN( h1.GetBinError(i) ) or ROOT.TMath.IsNaN( h2.GetBinError(i) ):
			e=epsilon
		else:
			print "-- assertion error -- %f -- %f -- %f"%(h1.GetBinError(i),h2.GetBinError(i),epsilon)
			e=epsilon
		h1.SetBinError(i, e)

def Ratio(H,H1,NoErrorH=False):
	R=H1.Clone(H1.GetName()+"_ratio")
	hTmp=H.Clone("tmp")
	#in order to account error properly in ratios
	if NoErrorH:
		for i in range(1,hTmp.GetNbinsX()+1):
			hTmp.SetBinError(i,0)
	R.Divide(hTmp)
	return R

def FixNames(histoName,cut,syst=''):
	n=histoName.find('$')
	if n<0: return histoName;
	if histoName[n+1] != '{': print 'PUT ${} things that must be sub'
	#look for first }
	r=histoName.find('}')
	if (r<n):print "error } $"
	
	#copy from n to r
	substring=histoName[n+2:r] ## keep out ${}
	#cut[0]=ht cut[1]=njets cut[2]=pt
	if 'HT' in substring:
		var =float(cut[0])
		substring=substring.replace('HT','')
		if substring=='': substring='%d'
		else: substring='%'+substring
	elif 'NJETS' in substring:
		var=float(cut[1])
		substring=substring.replace('NJETS','')
		if substring=='': substring='%d'
		else: substring='%'+substring
	elif 'PTJ' in substring:
		var=float(cut[2])
		substring=substring.replace('PTJ','')
		if substring=='': substring='%d'
		else: substring='%'+substring
	elif 'SYST' in substring:
		var=syst
		substring=substring.replace('SYST','')
		if substring=='': substring='%s'
		else: substring='%'+substring
	else: 
		print "error: unknown substitution"
		var=''
	#print "histoname=" + histoName[:n] + "   substri="+ substring + "    histoname="+histoName[r+1:] 
	name=(histoName[:n] + substring + histoName[r+1:] )%(var)
	return FixNames(name,cut,syst)
	
#open files
file1 = ROOT.TFile.Open(config['file1'])
file2 = ROOT.TFile.Open(config['file2'])

AllCanvas=[]

for cut in config['Cut']:
	#take histo from file 1
	
	#for the histoname:
	hn1=config['histoName1']
	hn2=config['histoName2']
	
	hn1=FixNames( hn1,cut)
	hn2=FixNames( hn2,cut)
	
	print "Going to Get Histo :"+hn1 + ": from file " + config["file1"]
	h1=file1.Get(hn1) 
	print "Going to Get Histo :"+hn2 + ": from file " + config["file2"]
	h2=file2.Get(hn2)

	#get syst	
	print "Taken Histo "+ h1.GetName()
	h1.SetName("Histo_Ht_%s_nJets_%s_ptJet_%s"%cut )
	R=Ratio(h1,h2,True)
	S=R.Clone("Syst_Ht_%s_nJets_%s_ptJet_%s"%cut )
	for s in config['Syst']:
		hns1=s[2]	
		hns2=s[3]
		hns1=hns1.replace('-',hn1)
		hns2=hns2.replace('-',hn2)
		typ=s[1]
		syst=s[0]
		if hns1=='None': typ='.'+typ[1]
		if hns2=='None': typ=typ[0]+'.'
		if typ[0]=='+': #h1 double band
			h1nup=FixNames(hns1,cut,config["PrePendSyst"][0]+syst+config['Up'][0])
			h1ndn=FixNames(hns1,cut,config["PrePendSyst"][0]+syst+config['Down'][0])
			print "Going to get Histo " +h1nup + " - " + h1ndn
			h1up=file1.Get(h1nup)
			h1dn=file1.Get(h1ndn)
			s1=makeBands(h1up,h1dn,"Mean")
		elif typ[0]==':':
			h1nfirst=FixNames(hns1,cut,config["PrePendSyst"][0]+syst)
			print "Going to get Histo " +h1nfirst
			h1first=file1.Get(h1nfirst)
			s1=makeBands(h1,h1first,"First")
		elif typ[0]=='.':
			s1=h1.Clone("syst1"+syst)
			for i in range(1,s1.GetNbinsX()+1): s1.SetBinError(i,0);
		else: print "error on type 0 of "+typ	
			
		if typ[1]=='+': #h1 double band
			h2nup=FixNames(hns2,cut,config["PrePendSyst"][1]+syst+config['Up'][1])
			h2ndn=FixNames(hns2,cut,config["PrePendSyst"][1]+syst+config['Down'][1])
			print "Going to get Histo " +h2nup + " - " + h2ndn
			h2up=file2.Get(h2nup)
			h2dn=file2.Get(h2ndn)
			s2=makeBands(h2up,h2dn,"Mean")
		elif typ[1]==':':
			h2nfirst=FixNames(hns2,cut,config["PrePendSyst"][1]+syst)
			print "Going to get Histo " +h2nfirst
			h2first=file2.Get(h2nfirst)
			s2=makeBands(h2,h2first,"First")
		elif typ[1]=='.':
			s2=h2.Clone("syst2"+syst)
			for i in range(1,s2.GetNbinsX()+1): s2.SetBinError(i,0);
		else: print "error on type 1 of "+typ	
		s=Ratio(s1,s2,True)
		sqrtSum(S,s)
	C=ROOT.TCanvas("C_Ht_%s_nJets_%s_ptJet_%s"%cut)
	R.SetMarkerStyle(20)
	S.SetLineColor(ROOT.kRed)
	S.SetFillStyle(0)
	
	R.GetXaxis().SetTitle("P_{T}^{Z/#gamma}[GeV]")
	R.GetYaxis().SetTitle("d#sigma/dP_{T}^{Z} / d#sigma/dP_{T}^{#gamma}")
	R.GetYaxis().SetRangeUser(0,2)
	R.Draw("AXIS P")
	S.Draw("P E4 SAME")
	R.Draw("P SAME")
	R.Draw("AXIS X+ Y+ SAME")
	R.Draw("AXIS SAME")
	name= config["Out"]+("/C_Ht_%s_nJets_%s_ptJet_%s.pdf"%cut)
	print "Going to save "+ name
	C.SaveAs( name )	
	name= config["Out"]+("/C_Ht_%s_nJets_%s_ptJet_%s.root"%cut)
	print "Going to save "+ name
	C.SaveAs( name)	
	AllCanvas.append(C)


