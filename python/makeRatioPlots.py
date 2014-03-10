#!/usr/bin/python
import sys,os
import array
import time
import math
from optparse import OptionParser

DEBUG=1


if(DEBUG>0):print "----- BEGIN -----"

if(DEBUG>0):print "-PARSING OPTIONS-"
usage = "usage: %prog [options] arg1 arg2"
parser=OptionParser(usage=usage)
parser.add_option("","--inputDat" ,dest='inputDat',type='string',help="Input Configuration file for Ratio",default="data/configRatio.dat")
parser.add_option("-b","--batch" ,dest='batch',action='store_true',help="ROOT Batch",default=False)
parser.add_option("-s","--syst" ,dest='syst',action='store_true',help="Syst does not include stat",default=False)
parser.add_option("-c","--cov" ,dest='cov',action='store_true',help="Use Covariance Matrix",default=False)
parser.add_option("-m","--mc" ,dest='mc',action='store_true',help="Add MC:TODO",default=False)

(options,args)=parser.parse_args()
import ROOT
if options.batch:
	ROOT.gROOT.SetBatch()
ROOT.gStyle.SetOptStat(0)
ROOT.gStyle.SetOptTitle(0)

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
			if 'eventList1' not in R: R['eventList1']=''
		elif parts[0] == 'file2': 
			R["file2"]=parts[1]
			if 'eventList2' not in R: R['eventList2']=''
		elif parts[0] == 'lumi1': 
			R["lumi1"]=float(parts[1])
		elif parts[0] == 'lumi2': 
			R["lumi2"]=float(parts[1])
		elif parts[0] == 'eventList1': 
			R['eventList1Compress']=0
			R['eventList1HistoName']=''
			for i in range(1,len(parts)):
				if parts[i].split('=')[0] == 'file':
					R['eventList1']=parts[i].split('=')[1]
				elif parts[i].split('=')[0] == 'compress':
					R['eventList1Compress']=int(parts[i].split('=')[1])
				elif parts[i].split('=')[0] == 'histoName':
					R['eventList1HistoName']=parts[i].split('=')[1]
		elif parts[0] == 'eventList2': 
			R['eventList2Compress']=0
			R['eventList2HistoName']=''
			for i in range(1,len(parts)):
				if parts[i].split('=')[0] == 'file':
					R['eventList2']=parts[i].split('=')[1]
				elif parts[i].split('=')[0] == 'compress':
					R['eventList2Compress']=int(parts[i].split('=')[1])
				elif parts[i].split('=')[0] == 'histoName':
					R['eventList2HistoName']=parts[i].split('=')[1]
		elif parts[0] == 'histoName1': R["histoName1"]=parts[1]
		elif parts[0] == 'histoName2': R["histoName2"]=parts[1]
		elif parts[0] == 'mcName1': R["mcName1"]=parts[1]
		elif parts[0] == 'mcName2': R["mcName2"]=parts[1]
		elif parts[0] == 'cov1': R["cov1"]=parts[1]
		elif parts[0] == 'cov2': R["cov2"]=parts[1]
		elif parts[0] == 'NoCut':
			R['Cut']=[]
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
			K =  parts[1:]
			R['PrePendSyst']=[]
			for s in K:
				s=s.replace("'","")
				s=s.replace('"',"")
				R['PrePendSyst'].append(s)
		elif parts[0] == 'xaxis' or parts[0]=='yaxis':
			R[parts[0]]=[ float(parts[1]), float(parts[2] )]
		elif parts[0] == 'ylog' or parts[0]=='xlog':
			R[parts[0]] = int(parts[1])
		elif parts[0] == 'include':
			tmp = ReadRatioDat( parts[1] )
			for key in tmp:
				R[ key ] = tmp[ key ]
	   except: 
		print "Malformed line (probably ignored):"+l
	#set default if not specified in dat file
	if 'xaxis' not in R:
		R['xaxis']=[0,0]
	if 'yaxis' not in R:
		R['yaxis']=[0,0]
	if 'xlog' not in R:
		R['xlog']=0
	if 'ylog' not in R:
		R['ylog']=0
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

def sqrtSum(h1,h2,epsilon=0.0001):
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

import gzip
def computeOverlap(eventList1,compress1,name1,pt1,eventList2,compress2,name2,pt2):
	if eventList1=='' or eventList2=='': return (0,1,1);
	l1=glob(eventList1);
	l2=glob(eventList2);
	EventList1={}
	EventList2={}
	for fileName in l1:
		if compress1:file1 = gzip.open(fileName,"r")
		else:        file1 =      open(fileName,"r")
		
		for l in file1:
			parts=l.split();
			run = -1 
			lumi= -1
			event= -1
			name=''
			high=-1
			low=-1
			for p in parts:
				if p.split(':')[0]=='run':run = int (p.split(':')[1] )
				elif p.split(':')[0]=='lumi':lumi = int (p.split(':')[1] )
				elif p.split(':')[0]=='event':event = int (p.split(':')[1] )
				elif p.split(':')[0]=='name':name = str (p.split(':')[1] )
				elif p.split(':')[0]=='high':high = float (p.split(':')[1] )
				elif p.split(':')[0]=='low':low = float (p.split(':')[1] )
			if (not (pt1>=low and pt1<high)) and pt1>=0:continue;
			if name1 != "" and name != name1:continue;
			EventList1[ (run,lumi,event) ] = 1
		file1.close();
	for fileName in l2:
		if compress2:file2 = gzip.open(fileName,"r")
		else:        file2 =      open(fileName,"r")
		
		for l in file2:
			parts=l.split();
			run = -1 
			lumi= -1
			event= -1
			name=''
			high=-1
			low=-1
			for p in parts:
				if p.split(':')[0]=='run':run = int (p.split(':')[1] )
				elif p.split(':')[0]=='lumi':lumi = int (p.split(':')[1] )
				elif p.split(':')[0]=='event':event = int (p.split(':')[1] )
				elif p.split(':')[0]=='name':name = str (p.split(':')[1] )
				elif p.split(':')[0]=='high':high = float (p.split(':')[1] )
				elif p.split(':')[0]=='low':low = float (p.split(':')[1] )
			if (not (pt2>=low and pt2<high)) and pt2>=0:continue;
			if name2 != "" and name != name2:continue;
			EventList2[ (run,lumi,event) ] = 1
		file2.close();
	common=0;
	only1=0;
	only2=0
	for (run,lumi,event) in EventList1:
		if (run,lumi,event) in EventList2:
			common+=1	
			EventList2[(run,lumi,event)]=0
		else: only1+=1
	for (run,lumi,event) in EventList2:
		if EventList2[(run,lumi,event)] == 0: only2+=1
	return (common,only1,only2)				

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

def ConvertToTargetTH1( h1, h2):
	h2.SetName("old_"+h2.GetName())
	h=h1.Clone(h2.GetName());
	for iBin in range(1,h.GetNbinsX()+1):
		h.SetBinContent(iBin,  h2.GetBinContent(h2.FindBin(h.GetBinCenter(iBin)) ))
		h.SetBinError(iBin,    h2.GetBinError  (h2.FindBin(h.GetBinCenter(iBin)) ))
	return h
	
	
#open files
file1 = ROOT.TFile.Open(config['file1'])
file2 = ROOT.TFile.Open(config['file2'])

AllCanvas=[]

ROOT.gROOT.ProcessLine("struct Bins{ \
		Double_t PtBins[1023];\
		int nBins;\
		};")

from ROOT import Bins

for cut in config['Cut']:
	#take histo from file 1
	
	#for the histoname:
	hn1=FixNames(config['histoName1'],cut,'')
	hn2=FixNames(config['histoName2'],cut,'')
	
	hn1=FixNames( hn1,cut)
	hn2=FixNames( hn2,cut)
	
	##compute overlap
	El1Files=config['eventList1']
	El2Files=config['eventList2']
	## PER PT
	if El1Files != '' and El2Files !='':
		El1Compress=config['eventList1Compress']
		El1HistoName=config['eventList1HistoName']
		El2Compress=config['eventList2Compress']
		El2HistoName=config['eventList2HistoName']
	
	print "Going to Get Histo :"+hn1 + ": from file " + config["file1"]
	h1Raw=file1.Get(hn1) 
	print "Going to Get Histo :"+hn2 + ": from file " + config["file2"]
	h2Raw=file2.Get(hn2)
	print "Taken Histo "+ h1Raw.GetName()
	print "Taken Histo "+ h2Raw.GetName()
	h1Raw.Scale(1./config['lumi1'])
	h2Raw.Scale(1./config['lumi2'])

	print "Histo1 Available Bins:"
	h1Bin=[]
	for iBin in range(1,h1Raw.GetNbinsX()+1):
		h1Bin.append( int(round(h1Raw.GetBinLowEdge(iBin))) )
		print str(h1Raw.GetBinLowEdge(iBin))+"->"+str(h1Bin[-1]),
	print
	print "Histo2 Available Bins:"
	h2Bin=[]
	for iBin in range(1,h2Raw.GetNbinsX()+1):
		h2Bin.append( int(round(h2Raw.GetBinLowEdge(iBin))) )
		print str(h2Raw.GetBinLowEdge(iBin))+"->"+str(h2Bin[-1]),
	print
	hBinCommon=ROOT.Bins()
	hBinCommon.nBins=0;
	for ptBin in h1Bin:
			if ptBin in h2Bin: 
				hBinCommon.PtBins[hBinCommon.nBins]=ptBin
				hBinCommon.nBins+=1
	h1=ROOT.TH1D("Histo1_Ht_%s_nJets_%s_ptJet_%s"%cut ,"h1",hBinCommon.nBins-1,hBinCommon.PtBins)
	h2=ROOT.TH1D("Histo2_Ht_%s_nJets_%s_ptJet_%s"%cut ,"h2",hBinCommon.nBins-1,hBinCommon.PtBins)

	## Convert to Target TH1
	h1=ConvertToTargetTH1(h1,h1Raw)
	h2=ConvertToTargetTH1(h2,h2Raw)
	print "Values"
	for iBin in range(1,h2.GetNbinsX()+1):
		print " ["+str(h1.GetBinCenter(iBin))+"->"+str(h1.GetBinContent(iBin)) + ","+str(h2.GetBinContent(iBin))+"]",
	print
	#get syst	
	h1.SetName("Histo_Ht_%s_nJets_%s_ptJet_%s"%cut )
	#R=Ratio(h1,h2,True)
	R=Ratio(h2,h1,True)
	print "Ratio"
	for iBin in range(1,h2.GetNbinsX()+1):
		print str(R.GetBinContent(iBin)),
	print
	if options.cov:
		print "Computing covariance matrix assuming gaussian error propagation and (``mu_i/sigma_i >>1'' ) "
		cov1name=FixNames(config['cov1'],cut)
		cov2name=FixNames(config['cov2'],cut)
		cov1Raw=file1.Get(cov1name);
		cov2Raw=file2.Get(cov2name);
		#find common bins -- covariance matrix is in iBin
		cov1=TH2D("Cov1_Ht_%s_nJets_%s_ptJet_%s"%cut ,"h1",hBinCommon.nBins-1,0,hBinCommon.nBins-1);
		
		cov2=TH2D("Cov2_Ht_%s_nJets_%s_ptJet_%s"%cut ,"h2",hBinCommon.nBins-1,0,hBinCommon.nBins-1);
		for iBin in range(1,hBinCommon.nBins):
		 for jBin in range(1,hBinCommon.nBins):
		      cov1.SetBinContent(iBin,jBin, cov1.GetBinContent( h1.FindBin((hBinCommon.PtBins[iBin-1]+ hBinCommon.PtBins[iBin])/2.,(hBinCommon.PtBins[jBin-1]+ hBinCommon.PtBins[jBin])/2.) ) );
		      cov2.SetBinContent(iBin,jBin, cov2.GetBinContent( h2.FindBin((hBinCommon.PtBins[iBin-1]+ hBinCommon.PtBins[iBin])/2.,(hBinCommon.PtBins[jBin-1]+ hBinCommon.PtBins[jBin])/2.) ) );


	if El1Files != '' and El2Files !='':
	   for i in range(1,h1.GetNbinsX()+1):
		e1=h1.GetBinError(i)
		c1=h1.GetBinContent(i)
		e2=h2.GetBinError(i)
		c2=h2.GetBinContent(i)
		pt1=h1.GetBinCenter(i);
		pt2=h2.GetBinCenter(i);
		(common,only1,only2)=computeOverlap(El1Files,El1Compress,El1HistoName,pt1,El2Files,El2Compress,El2HistoName,pt2);
		# r = N1* (a+b) / N2* (a+c)
		(a,b,c) = (common,only1,only2)
		N1=c1/(common+only1)
		N2=c2/(common+only2)
		# Dr= N1/N2 * sqrt ( D(a+b/a+c) )
		da2= float(common)
		db2= float(only1)
		dc2= float(only2)
		if math.abs( da2+db2 - e1**2/N1**2 )> 0.01:print "Error don't match 1"
		if math.abs( da2+dc2 - e2**2/N2**2 )> 0.01:print "Error don't match 1"
		dr= N1/N2 * math.sqrt( ((a+b)/(a+c)) * ( (a/(a+b))**2 * db2 + (a/(a+c))**2 * dc2 + ( a*(b-c)/((a+c)*(a+b)) )**2 * da2  ))
		R.SetBinError(i,dr)
	if options.mc:
		mc1name=FixNames(config['mcName1'],cut)
		mc2name=FixNames(config['mcName2'],cut)
		print "Going to Get",mc1name,"from ",config['file1'],"and",mc2name,"from",config['file2']
		mc1Raw=file1.Get(mc1name)
		mc2Raw=file2.Get(mc2name)

		mc1=ROOT.TH1D("mc1_Ht_%s_nJets_%s_ptJet_%s"%cut ,"h1",hBinCommon.nBins-1,hBinCommon.PtBins)
		mc2=ROOT.TH1D("mc2_Ht_%s_nJets_%s_ptJet_%s"%cut ,"h2",hBinCommon.nBins-1,hBinCommon.PtBins)
		mc1=ConvertToTargetTH1(mc1,mc1Raw)
		mc2=ConvertToTargetTH1(mc2,mc2Raw)

		mc1.Scale(1./config['lumi1'])
		mc2.Scale(1./config['lumi2'])

		mc1.SetName("MC_Ht_%s_nJets_%s_ptJet_%s"%cut )
		mcR=Ratio(mc2,mc1,True)
		mcR.SetLineColor(ROOT.kBlue)

	S=R.Clone("Syst_Ht_%s_nJets_%s_ptJet_%s"%cut )	
	if options.syst:
		for iBin in range(1,S.GetNbinsX()+1):S.SetBinError(iBin,0)
	for s in config['Syst']:
		hns1=s[2]	
		hns2=s[3]
		hns1=hns1.replace('-',config["histoName1"])
		hns2=hns2.replace('-',config["histoName2"])
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
			h1up=ConvertToTargetTH1(h1,h1up)
			h1dn=ConvertToTargetTH1(h1,h1dn)
			h1up.Scale(1./config["lumi1"])
			h1dn.Scale(1./config["lumi1"])
			s1=makeBands(h1up,h1dn,"Mean")
		elif typ[0]==':':
			h1nfirst=FixNames(hns1,cut,config["PrePendSyst"][0]+syst)
			print "Going to get Histo " + h1nfirst
			h1first=file1.Get(h1nfirst)
			h1first=ConvertToTargetTH1(h1,h1first)
			h1first.Scale(1./config["lumi1"])
			s1=makeBands(h1,h1first,"First")
		elif typ[0]=='.':
			s1=h1.Clone("syst1"+syst) #h1 is already scaled
			for i in range(1,s1.GetNbinsX()+1): s1.SetBinError(i,0);
		elif typ[0]=='&': #content of the histo is the error itsef
			h1nerr=FixNames(hns1,cut,config["PrePendSyst"][0]+syst)
			print "Going to get Histo "+ h1nerr 
			h1err=file1.Get(h1nerr)
			s1=h1.Clone("syst1"+syst) #h1 is already scaled
			for i in range(1,s1.GetNbinsX()+1): s1.SetBinError(i,h1err.GetBinContent(i) );
		else: print "error on type 0 of "+typ	
			
		if typ[1]=='+': #h1 double band
			print config["PrePendSyst"]
			print config['Up']
			h2nup=FixNames(hns2,cut,config["PrePendSyst"][1]+syst+config['Up'][1])
			h2ndn=FixNames(hns2,cut,config["PrePendSyst"][1]+syst+config['Down'][1])
			print "Going to get Histo " +h2nup + " - " + h2ndn 
			h2up=file2.Get(h2nup)
			h2dn=file2.Get(h2ndn)
			h2up=ConvertToTargetTH1(h2,h2up)
			h2dn=ConvertToTargetTH1(h2,h2up)
			h2up.Scale(1./config["lumi2"])
			h2dn.Scale(1./config["lumi2"])
			s2=makeBands(h2up,h2dn,"Mean")
		elif typ[1]==':':
			h2nfirst=FixNames(hns2,cut,config["PrePendSyst"][1]+syst)
			print "Going to get Histo " +h2nfirst
			h2first=file2.Get(h2nfirst)
			h2first=ConvertToTargetTH1(h2,h2first)
			h2first.Scale(1./config["lumi2"])
			s2=makeBands(h2,h2first,"First")
		elif typ[1]=='.':
			s2=h2.Clone("syst2"+syst) #h2 is already scale for lumi
			for i in range(1,s2.GetNbinsX()+1): s2.SetBinError(i,0);
		elif typ[1]=='&': #content of the histo is the error itsef
			h2nerr=FixNames(hns2,cut,config["PrePendSyst"][1]+syst)
			print "Going to get Histo "+ h2nerr 
			h2err=file2.Get(h2nerr)
			s2=h2.Clone("syst2"+syst) #h1 is already scaled
			for i in range(1,s2.GetNbinsX()+1): s2.SetBinError(i,h2err.GetBinContent(i) );
		else: print "error on type 1 of "+typ	
		s=Ratio(s2,s1,False)
		print "Syst %s:"%syst
		for i in range(1,s.GetNbinsX()):print s.GetBinError(i),
		print
		sqrtSum(S,s)
		#DEBUG
		print
		print "Relative Errors [tot s1 s2 TOT]%% %s:"%syst
		for i in range(1,s.GetNbinsX()):print "[%.1f %.1f %.1f -> %.1f]"%(s.GetBinError(i)/s.GetBinContent(i)*100, s1.GetBinError(i)/s1.GetBinContent(i)*100,s2.GetBinError(i)/s2.GetBinContent(i) *100, S.GetBinError(i)/S.GetBinContent(i) *100),
		print
		print "Absolute Vales"
		for i in range(1,s.GetNbinsX()):print "[%.1f %.1f %.1f -> %f]"%(s.GetBinContent(i), s1.GetBinContent(i),s2.GetBinContent(i) , S.GetBinContent(i)),
		print
		print
		#ENDDEBUG
	C=ROOT.TCanvas("C_Ht_%s_nJets_%s_ptJet_%s"%cut)
	ROOT.gPad.SetBottomMargin(0.15)
	ROOT.gPad.SetTopMargin(0.05)
	ROOT.gPad.SetLeftMargin(0.15)
	ROOT.gPad.SetRightMargin(0.05)
	xshift= ( ROOT.gPad.GetLeftMargin() - ROOT.gPad.GetRightMargin() )/2.0
	yshift= ( ROOT.gPad.GetBottomMargin() - ROOT.gPad.GetTopMargin() )/2.0

	R.SetMarkerStyle(20)
	R.SetMarkerColor(ROOT.kBlack)
	R.SetLineColor(ROOT.kBlack)
	S.SetLineColor(ROOT.kRed)
	#S.SetFillColor(ROOT.kRed)
	#S.SetFillColor(50)##blue=38
	S.SetFillColor(ROOT.kOrange-4);
	#S.SetFillStyle(0)

	L=ROOT.TLegend(0.75+xshift,0.75+yshift,.89+xshift,.89+yshift)
	L.SetFillStyle(0);
	L.SetBorderSize(0);
	
	R.GetXaxis().SetTitle("P_{T}^{Z/#gamma}[GeV]")
	R.GetYaxis().SetTitle("d#sigma/dP_{T}^{Z} / d#sigma/dP_{T}^{#gamma}")
	R.GetYaxis().SetTitleOffset(1.5)
	R.GetXaxis().SetTitleOffset(1.5)
	R.GetYaxis().SetDecimals()
	#R.GetYaxis().SetRangeUser(0,2)
	R.GetYaxis().SetRangeUser(0,R.GetMaximum()*1.2)
	if not (config['xaxis'][0]==0 and config['xaxis'][1]==0):
		R.GetXaxis().SetRangeUser(config['xaxis'][0],config['xaxis'][1]);
	if not (config['yaxis'][0]==0 and config['yaxis'][1]==0):
		R.GetYaxis().SetRangeUser(config['yaxis'][0],config['yaxis'][1]);
	if config['xlog']: C.SetLogx()
	if config['ylog']: C.SetLogy()

	R.Draw("AXIS P")
	S.Draw("P E2 SAME")
	R.Draw("P SAME")
	R.Draw("AXIS X+ Y+ SAME")
	R.Draw("AXIS SAME")
	L.AddEntry(R,"Data","P");
	L.AddEntry(S,"Stat+Syst","F");
	if options.mc:
		mcR.Draw("HIST SAME")
		mcN=mcR.Clone("Normalize")
		mcN.SetLineStyle(ROOT.kDashed)
		print "Z Scale: %.3f"%(h1.Integral()/ mc1.Integral())
		print "G Scale: %.3f"%(h2.Integral()/ mc2.Integral())
		mcN.Scale(h1.Integral() * mc2.Integral() / (h2.Integral() * mc1.Integral() ))
		mcN.Draw("HIST SAME")
		L.AddEntry(mcR,"MG","F");
		L.AddEntry(mcN,"MG Norm.","F");
	L.Draw();
	lat=ROOT.TLatex()
	lat.SetNDC()
	#lat.SetTextFont(62)
	lat.SetTextSize(0.04)
	lat.SetTextAlign(11)
	text="Ht > %.0f N_{jets} #geq %.0f "%(float(cut[0]),float(cut[1]))
	if ( float(cut[2])> 30 ) : text += " p_{T}^{jet} #geq %.0f"%(float(cut[2]))
	lat.DrawLatex(.15+xshift,.85+yshift,"CMS Preliminary,")
	lat.SetTextFont(42)
	lat.DrawLatex(.15+xshift,.80+yshift,"#sqrt{s} = 8TeV, L=19.7fb^{-1}")
	lat.DrawLatex(.15+xshift,.75+yshift,text)
	if not options.batch:
		a=raw_input("Press Enter");
	name= config["Out"]+("/C_Ht_%s_nJets_%s_ptJet_%s.pdf"%cut)
	print "Going to save "+ name
	C.SaveAs( name )	
	name= config["Out"]+("/C_Ht_%s_nJets_%s_ptJet_%s.root"%cut)
	print "Going to save "+ name
	C.SaveAs( name)	
	AllCanvas.append(C)


