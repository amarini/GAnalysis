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
parser.add_option("-m","--mc" ,dest='mc',action='store_true',help="Add MC plots",default=False)
parser.add_option("-t","--table" ,dest='table',action='store_true',help="Print Table for syst. TODO",default=False)

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
from commonRatio import *

		
config = ReadRatioDat(options.inputDat)

if 'mc' in config and config['mc']: options.mc=True;
if 'table' in config and config['table']: options.table=True;
##########################


#open files
file1 = ROOT.TFile.Open(config['file1'])
file2 = ROOT.TFile.Open(config['file2'])

AllCanvas=[]

for cut in config['Cut']:
	#take histo from file 1
	Table=[]
	
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

	# MERGE BINS IF NECESSARY
	if 'Merge1' in config:
		#print "Bins not merged"
		h1Raw=MergeBins(config['Merge1'],h1Raw)
	if 'Merge2' in config:
		#print "Bins not merged"
		h2Raw=MergeBins(config['Merge2'],h2Raw)

	#k=ROOT.TCanvas("k","k")
	#h2Raw.Draw("HIST");
	
	print "Histo1 Available Bins:"
	h1Bin=[]
	for iBin in range(1,h1Raw.GetNbinsX()+2):
		h1Bin.append( int(round(h1Raw.GetBinLowEdge(iBin))) )
		print str(h1Raw.GetBinLowEdge(iBin))+"->"+str(h1Bin[-1]),
	print
	print "Histo2 Available Bins:"
	h2Bin=[]
	for iBin in range(1,h2Raw.GetNbinsX()+2):
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
	if DEBUG>1: print "Values"
	for iBin in range(1,h2.GetNbinsX()+1):
		if DEBUG>1:print " ["+str(h1.GetBinCenter(iBin))+"->"+str(h1.GetBinContent(iBin)) + ","+str(h2.GetBinContent(iBin))+"]",
	if DEBUG>1: print
	#get syst	
	h1.SetName("Histo_Ht_%s_nJets_%s_ptJet_%s"%cut )
	#R=Ratio(h1,h2,True)
	R=Ratio(h2,h1,NoErrorH=False)
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
		if 'Merge1' in config:
			mc1Raw=MergeBins(config['Merge1'],mc1Raw)
		if 'Merge2' in config:
			mc2Raw=MergeBins(config['Merge2'],mc2Raw)

		mc1=ROOT.TH1D("mc1_Ht_%s_nJets_%s_ptJet_%s"%cut ,"h1",hBinCommon.nBins-1,hBinCommon.PtBins)
		mc2=ROOT.TH1D("mc2_Ht_%s_nJets_%s_ptJet_%s"%cut ,"h2",hBinCommon.nBins-1,hBinCommon.PtBins)
		mc1=ConvertToTargetTH1(mc1,mc1Raw)
		mc2=ConvertToTargetTH1(mc2,mc2Raw)

		mc1.Scale(1./config['lumi1'])
		mc2.Scale(1./config['lumi2'])

		mc1.SetName("MC_Ht_%s_nJets_%s_ptJet_%s"%cut )
		mcR=Ratio(mc2,mc1,False)
		mcR.SetLineColor(ROOT.kBlue)

	if options.table:
		Table.append(["Bin"])          #  0 
		Table.append(["Bound"])        #  1
		Table.append(["$Z$"])            #  2
		Table.append(["$\\gamma$"])      #  3
		Table.append(["R"])            #  4
		Table.append(["Stat ($\\%$)"])    #  5
		for i in range(1,R.GetNbinsX()+1):
			Table[0].append( "$%d$"%i)
			Table[1].append( "$%.0f$--$%.0f$"%(R.GetBinLowEdge(i),R.GetBinLowEdge(i+1)))
			Table[2].append( "$%.1f$"%h1.GetBinContent(i))
			Table[3].append( "$%.1f$"%h2.GetBinContent(i))
			Table[4].append( "$%f$"%R.GetBinContent(i))
			Table[5].append( "$%.1f$"%(R.GetBinError(i)/R.GetBinContent(i) * 100) )
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
		#if hns1=='None': typ='.'+typ[1]
		#if hns2=='None': typ=typ[0]+'.'
		#if typ[0]=='+': #h1 double band
		#	h1nup=FixNames(hns1,cut,config["PrePendSyst"][0]+syst+config['Up'][0])
		#	h1ndn=FixNames(hns1,cut,config["PrePendSyst"][0]+syst+config['Down'][0])
		#	print "Going to get Histo " +h1nup + " - " + h1ndn
		#	h1up=file1.Get(h1nup)
		#	h1dn=file1.Get(h1ndn)
		#	if 'Merge1' in config:
		#		h1up=MergeBins(config['Merge1'],h1up)
		#		h1dn=MergeBins(config['Merge1'],h1dn)
		#	h1up=ConvertToTargetTH1(h1,h1up)
		#	h1dn=ConvertToTargetTH1(h1,h1dn)
		#	h1up.Scale(1./config["lumi1"])
		#	h1dn.Scale(1./config["lumi1"])
		#	s1=makeBands(h1up,h1dn,"Mean")
		#elif typ[0]==':':
		#	h1nfirst=FixNames(hns1,cut,config["PrePendSyst"][0]+syst)
		#	print "Going to get Histo " + h1nfirst
		#	h1first=file1.Get(h1nfirst)
		#	if 'Merge1' in config:
		#		h1first=MergeBins(config['Merge1'],h1first)
		#	h1first=ConvertToTargetTH1(h1,h1first)
		#	h1first.Scale(1./config["lumi1"])
		#	s1=makeBands(h1,h1first,"First")
		#elif typ[0]=='.':
		#	s1=h1.Clone("syst1"+syst) #h1 is already scaled
		#	for i in range(1,s1.GetNbinsX()+1): s1.SetBinError(i,0);
		#elif typ[0]=='&': #content of the histo is the error itsef
		#	h1nerr=FixNames(hns1,cut,config["PrePendSyst"][0]+syst)
		#	print "Going to get Histo "+ h1nerr 
		#	h1err=file1.Get(h1nerr)
		#	h1err=ConvertToTargetTH1(h1,h1err)
		#	s1=h1.Clone("syst1"+syst) #h1 is already scaled
		#	if 'Merge1' in config:
		#		s1=MergeBins(config['Merge1'],s1)
		#	for i in range(1,s1.GetNbinsX()+1): 
		#		#print "DEBUG Z ",syst,"Bin%d"%i,"%.0f %%"%( h1err.GetBinContent(i)/h1.GetBinContent(i) ), " %.0f-%.0f"%( h1err.GetBinCenter(i),h1.GetBinCenter(i) ),"%f/%f"%(h1err.GetBinContent(i),h1.GetBinContent(i))
		#		s1.SetBinError(i,h1err.GetBinContent(i) );
		#elif typ[0]=='%': #content of the histo is the error itsef
		#	e=float(hns1)/100.
		#	s1=h1.Clone("syst1"+syst) #h1 is already scaled
		#	for i in range(1,s1.GetNbinsX()+1): s1.SetBinError(i,h1.GetBinContent(i) * e );
		#else: print "error on type 0 of "+typ	
		#	
		#if typ[1]=='+': #h1 double band
		#	print config["PrePendSyst"]
		#	print config['Up']
		#	h2nup=FixNames(hns2,cut,config["PrePendSyst"][1]+syst+config['Up'][1])
		#	h2ndn=FixNames(hns2,cut,config["PrePendSyst"][1]+syst+config['Down'][1])
		#	print "Going to get Histo " +h2nup + " - " + h2ndn 
		#	h2up=file2.Get(h2nup)
		#	h2dn=file2.Get(h2ndn)
		#	if 'Merge2' in config:
		#		h2up=MergeBins(config['Merge2'],h2up)
		#		h2dn=MergeBins(config['Merge2'],h2dn)
		#	h2up=ConvertToTargetTH1(h2,h2up)
		#	h2dn=ConvertToTargetTH1(h2,h2up)
		#	h2up.Scale(1./config["lumi2"])
		#	h2dn.Scale(1./config["lumi2"])
		#	s2=makeBands(h2up,h2dn,"Mean")
		#elif typ[1]==':':
		#	h2nfirst=FixNames(hns2,cut,config["PrePendSyst"][1]+syst)
		#	print "Going to get Histo " +h2nfirst
		#	h2first=file2.Get(h2nfirst)
		#	if 'Merge2' in config:
		#		h2first=MergeBins(config['Merge2'],h2first)
		#	h2first=ConvertToTargetTH1(h2,h2first)
		#	h2first.Scale(1./config["lumi2"])
		#	s2=makeBands(h2,h2first,"First")
		#elif typ[1]=='.':
		#	s2=h2.Clone("syst2"+syst) #h2 is already scale for lumi
		#	for i in range(1,s2.GetNbinsX()+1): s2.SetBinError(i,0);
		#elif typ[1]=='&': #content of the histo is the error itsef
		#	h2nerr=FixNames(hns2,cut,config["PrePendSyst"][1]+syst)
		#	print "Going to get Histo "+ h2nerr 
		#	h2err=file2.Get(h2nerr)
		#	h2err=ConvertToTargetTH1(h2,h2err)
		#	s2=h2.Clone("syst2"+syst) #h1 is already scaled
		#	if 'Merge2' in config:
		#		s2=MergeBins(config['Merge2'],s2)
		#	for i in range(1,s2.GetNbinsX()+1): s2.SetBinError(i,h2err.GetBinContent(i) );
		#elif typ[1]=='%': #content of the histo is the error itsef
		#	e=float(hns2)/100.
		#	s2=h2.Clone("syst2"+syst) #h1 is already scaled
		#	for i in range(1,s2.GetNbinsX()+1): s2.SetBinError(i,h2.GetBinContent(i) *e );
		#else: print "error on type 1 of "+typ	
		s1=ReadSyst(config,typ,0,cut,syst,hns1,file1,h1)
		s2=ReadSyst(config,typ,1,cut,syst,hns2,file2,h2)
		s=Ratio(s2,s1,NoErrorH=False,FullCorr=True)
		print "Syst %s:"%syst
		for i in range(1,s.GetNbinsX()):print s.GetBinError(i),
		print
		if options.table:
			curRow=len(Table)
			Table.append(["%s ($\%%$)"%(syst)])
			for i in range(1,R.GetNbinsX()+1):
				Table[curRow].append("$%.1f$" % (s.GetBinError(i)/R.GetBinContent(i) * 100.))
			# Z #
			curRow=len(Table)
			Table.append(["%s:Z ($\%%$)"%(syst)])
			for i in range(1,R.GetNbinsX()+1):
				Table[curRow].append("$%.1f$" % (s1.GetBinError(i)/h1.GetBinContent(i) * 100.))
			curRow=len(Table)
			Table.append(["%s:$\\gamma$ ($\%%$)"%(syst)])
			for i in range(1,R.GetNbinsX()+1):
				Table[curRow].append("$%.1f$" % (s2.GetBinError(i)/h2.GetBinContent(i) * 100.))
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
	## ADD TOT SYST
	if options.table:
		curRow=len(Table)
		Table.append(["Tot Syst ($\\%$)"])
		for i in range(1,R.GetNbinsX()+1):
			Table[curRow].append("$%.0f$" % (S.GetBinError(i)/R.GetBinContent(i) * 100.))

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
	S.SetLineColor(ROOT.kOrange)
	#S.SetFillColor(ROOT.kRed)
	#S.SetFillColor(50)##blue=38
	S.SetFillColor(ROOT.kOrange-4);
	S.SetFillStyle(3001);
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
	if config['xlog']: C.SetLogx()
	if config['ylog']: C.SetLogy()
	if not (config['xaxis'][0]==0 and config['xaxis'][1]==0):
		R.GetXaxis().SetRangeUser(config['xaxis'][0],config['xaxis'][1]);
		print "x range set to ",config['xaxis'][0],config['xaxis'][1]
	if not (config['yaxis'][0]==0 and config['yaxis'][1]==0):
		R.GetYaxis().SetRangeUser(config['yaxis'][0],config['yaxis'][1]);

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
	name= config["Out"]+("/C_Ht_%s_nJets_%s_ptJet_%s.tex"%cut)
	if options.table:
		txt = open(name,"w")
		txt.write( ConvertToLatex(Table) )
		txt.write("\n")
		txt.close()
	AllCanvas.append(C)


