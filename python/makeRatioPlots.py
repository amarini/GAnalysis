#!/usr/bin/python
import sys,os
import array
import time
import math
from optparse import OptionParser
from subprocess import call

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

ROOT.gSystem.Load("libGAnalysis.so")
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

	# MERGE BINS IF NECESSARY
	if 'Merge1' in config:
		#print "Bins not merged"
		if 'cov1' in config:
			cov1Name=FixNames(config['cov1'],cut,'')
			print "Getting cov1 "+ cov1Name
			cov1=file1.Get(cov1Name)
		else:
			print "no cov1"
			cov1=None
		h1Raw=MergeBins(config['Merge1'],h1Raw,cov1)

	if 'Merge2' in config:
		#print "Bins not merged"
		if 'cov2' in config:
			cov2Name=FixNames(config['cov2'],cut,'')
			print "Getting cov2 "+ cov2Name
			cov2=file2.Get(cov2Name)
		else:
			cov2=None

		h2Raw=MergeBins(config['Merge2'],h2Raw,cov2)

	h1Raw.Scale(1./config['lumi1'])
	h2Raw.Scale(1./config['lumi2'])

	#k=ROOT.TCanvas("k","k")
	#h2Raw.Draw("HIST");
	
	print "Histo1 Available Bins:"
	h1Bin=[]
	for iBin in range(1,h1Raw.GetNbinsX()+2):
		h1Bin.append( int(round(h1Raw.GetBinLowEdge(iBin))) )
		if DEBUG>1:print str(h1Raw.GetBinLowEdge(iBin))+"->"+str(h1Bin[-1]),
	print
	print "Histo2 Available Bins:"
	h2Bin=[]
	for iBin in range(1,h2Raw.GetNbinsX()+2):
		h2Bin.append( int(round(h2Raw.GetBinLowEdge(iBin))) )
		if DEBUG>1:print str(h2Raw.GetBinLowEdge(iBin))+"->"+str(h2Bin[-1]),
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
	#for dumping tot syst files 1,2
	#SinglePlots
	h1_TOT=h1.Clone("H1_TOT")
	h2_TOT=h2.Clone("H2_TOT")
	print "Ratio"
	for iBin in range(1,h2.GetNbinsX()+1):
		if DEBUG>1:print str(R.GetBinContent(iBin)),
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
	if 'StatCorr' in config and config['StatCorr']:
	   print "Stat Errors: A/(A+B)"
	   for i in range(1,h1.GetNbinsX()+1):
		e1=h1.GetBinError(i)
		c1=h1.GetBinContent(i)
		e2=h2.GetBinError(i)
		c2=h2.GetBinContent(i)
		a=c1
		da=e1
		b=c2-c1
		if e2<e1:
			print "Stat Error:", e2,">",e1 ," -- c2,c1 ", c2,">",c1
			print "Setting db/b= dc2/c2"
			db= e2/c2*b
		else:
			db=math.sqrt(e2**2-e1**2)
		if a+b >0:
			r=a/(a+b)
			dr = math.sqrt( ( (b * da)**2 + (a * db )**2 ) / (a+b)**4)
			#dr=r*math.sqrt( db**2/(a+b)**2 + b**2/(a**2 * (a+b)**2)) 
		else :
			r=0
			dr=1
		if r> 0 and math.fabs(R.GetBinContent(i) - r)/r >0.02 : 
			print "Error in ratio from different computations"
		R.SetBinError(i,dr)

	if options.mc:
	    mcR=[]
	    #SinglePlots
	    SingleMC1=[]
	    SingleMC2=[]
	    colors=[ROOT.kBlue,ROOT.kRed,ROOT.kGreen+2]
	    styles=[1,2,3]
	    for iMC in range(0,len(config['mcName1'])):
		mc1name=FixNames(config['mcName1'][iMC],cut)
		mc2name=FixNames(config['mcName2'][iMC],cut)
		print "Going to Get",mc1name,"from ",config['file1'],"and",mc2name,"from",config['file2']
		mc1Raw=file1.Get(mc1name)
		mc2Raw=file2.Get(mc2name)
		if 'Merge1' in config:
			mc1Raw=MergeBins(config['Merge1'],mc1Raw)
		if 'Merge2' in config:
			mc2Raw=MergeBins(config['Merge2'],mc2Raw)

		mc1=ROOT.TH1D("mc1_"+config['mcLeg'][iMC]+"_Ht_%s_nJets_%s_ptJet_%s"%cut ,"h1",hBinCommon.nBins-1,hBinCommon.PtBins)
		mc2=ROOT.TH1D("mc2_"+config['mcLeg'][iMC]+"_Ht_%s_nJets_%s_ptJet_%s"%cut ,"h2",hBinCommon.nBins-1,hBinCommon.PtBins)
		mc1=ConvertToTargetTH1(mc1,mc1Raw)
		mc2=ConvertToTargetTH1(mc2,mc2Raw)

		mc1.Scale(1./config['lumi1'])
		mc2.Scale(1./config['lumi2'])

		mc1.SetName("MC_"+str(iMC)+"_Ht_%s_nJets_%s_ptJet_%s"%cut )
	
		mcR.append(Ratio(mc2,mc1,False))
		mcR[-1].SetLineColor( colors[iMC] )
		mcR[-1].SetLineStyle( styles[iMC])
		
		#SinglePlots
		mc1.SetLineColor( colors[iMC] )
		mc1.SetLineStyle( styles[iMC] )
		mc2.SetLineColor( colors[iMC] )
		mc2.SetLineStyle( styles[iMC] )
		SingleMC1.append(mc1)
		SingleMC2.append(mc2)

	if options.table:
		print "Going to open ROOT File:",  config["Out"]+"/R_"+FixNames(config['OutName'],cut) + ".root"
		OutROOT=ROOT.TFile.Open( config["Out"]+"/R_"+FixNames(config['OutName'],cut) + ".root" , "RECREATE")
		OutROOT.cd()
		R.Write()
		h1.Write()
		h2.Write()
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
			r=0
			try: r=R.GetBinError(i)/R.GetBinContent(i) * 100
			except: pass
			Table[5].append( "$%.1f$"%(r) )
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
		s1=ReadSyst(config,typ,0,cut,syst,hns1,file1,h1)
		s2=ReadSyst(config,typ,1,cut,syst,hns2,file2,h2)
		if ('RhoSyst'  in config ) and (syst in config['RhoSyst'] ):
			print "Using rho=",config['RhoSyst'][syst],'for syst',syst
			s=Ratio(s2,s1,NoErrorH=False,FullCorr=False,rho=config['RhoSyst'][syst])
		else:
			s=Ratio(s2,s1,NoErrorH=False,FullCorr=True)
		print "Syst %s:"%syst
		for i in range(1,s.GetNbinsX()): 
			if DEBUG>1: print s.GetBinError(i),
		print
		if options.table:
			OutROOT.cd()
			s.Write()

			curRow=len(Table)
			Table.append(["%s ($\%%$)"%(syst)])
			for i in range(1,R.GetNbinsX()+1):
				if R.GetBinContent(i) != 0:
					r=s.GetBinError(i)/R.GetBinContent(i) * 100.
				else: 
					r=0
				Table[curRow].append("$%.1f$" % (r))
			# Z #
			curRow=len(Table)
			Table.append(["%s:Z ($\%%$)"%(syst)])
			for i in range(1,R.GetNbinsX()+1):
				if h1.GetBinContent(i) !=0:
					r=s1.GetBinError(i)/h1.GetBinContent(i) * 100.
				else:
					r=0
				Table[curRow].append("$%.1f$" % (r))
			curRow=len(Table)
			Table.append(["%s:$\\gamma$ ($\%%$)"%(syst)])
			for i in range(1,R.GetNbinsX()+1):
				if h2.GetBinContent(i) !=0:
					r=s2.GetBinError(i)/h2.GetBinContent(i) * 100.
				else:
					r=0
				Table[curRow].append("$%.1f$" % (r))
		#SinglePlots
		sqrtSum(h1_TOT,s1)
		sqrtSum(h2_TOT,s2)
		#
		sqrtSum(S,s)
		#DEBUG
		try:
		   if DEBUG>1:
			print
			print "Relative Errors [tot s1 s2 TOT]%% %s:"%syst
			for i in range(1,s.GetNbinsX()) :print "[%.1f %.1f %.1f -> %.1f]"%(s.GetBinError(i)/s.GetBinContent(i)*100, s1.GetBinError(i)/s1.GetBinContent(i)*100,s2.GetBinError(i)/s2.GetBinContent(i) *100, S.GetBinError(i)/S.GetBinContent(i) *100),
			print
			print "Absolute Vales"
			for i in range(1,s.GetNbinsX()):print "[%.1f %.1f %.1f -> %f]"%(s.GetBinContent(i), s1.GetBinContent(i),s2.GetBinContent(i) , S.GetBinContent(i)),
			print
			print
		except: pass
		#ENDDEBUG
	## ADD TOT SYST
	if options.table:
		OutROOT.cd()
		S.Write()
		curRow=len(Table)
		Table.append(["Tot Syst ($\\%$)"])
		for i in range(1,R.GetNbinsX()+1):
			if R.GetBinContent(i) !=0:
				r=S.GetBinError(i)/R.GetBinContent(i) * 100.
			else:
				r=0
			Table[curRow].append("$%.1f$" % (r))

	plotter=ROOT.NicePlots.SingleRatioPlot();
	#C=ROOT.TCanvas("C_Ht_%s_nJets_%s_ptJet_%s"%cut)
	#ROOT.gPad.SetBottomMargin(0.15)
	#ROOT.gPad.SetTopMargin(0.05)
	#ROOT.gPad.SetLeftMargin(0.15)
	#ROOT.gPad.SetRightMargin(0.05)
	#xshift= ( ROOT.gPad.GetLeftMargin() - ROOT.gPad.GetRightMargin() )/2.0
	#yshift= ( ROOT.gPad.GetBottomMargin() - ROOT.gPad.GetTopMargin() )/2.0

	#R.SetMarkerStyle(20)
	#R.SetMarkerColor(ROOT.kBlack)
	#R.SetLineColor(ROOT.kBlack)
	#S.SetLineColor(ROOT.kOrange)
	#S.SetFillColor(ROOT.kRed)
	#S.SetFillColor(50)##blue=38
	#S.SetFillColor(ROOT.kOrange-4);
	#S.SetFillStyle(3001);
	#S.SetFillStyle(0)
	plotter.data=R
	plotter.syst=S
	plotter.xtitle="P_{T}^{Z/#gamma}[GeV]"
	if 'xtitle' in config:
		plotter.xtitle=config['xtitle']

	plotter.ytitle="d#sigma/dP_{T}^{Z} / d#sigma/dP_{T}^{#gamma}"
	if'ytitle' in config:
		plotter.ytitle=config['ytitle']

	#L=ROOT.TLegend(0.75+xshift,0.75+yshift,.89+xshift,.89+yshift)
	#L.SetFillStyle(0);
	#L.SetBorderSize(0);
	
	#R.GetXaxis().SetTitle("P_{T}^{Z/#gamma}[GeV]")
	#if 'xtitle' in config:
	#	R.GetXaxis().SetTitle(config['xtitle'])
	#R.GetYaxis().SetTitle()
	#if 'ytitle' in config:
	#	R.GetYaxis().SetTitle(config['ytitle'])
	#R.GetYaxis().SetTitleOffset(1.5)
	#R.GetXaxis().SetTitleOffset(1.5)
	#R.GetYaxis().SetDecimals()
	#R.GetYaxis().SetRangeUser(0,2)
	plotter.RangeY.first=0
	plotter.RangeY.second=R.GetMaximum()*1.2
	plotter.RangeFactors.first=1
	plotter.RangeFactors.second=0.05
	if 'xleg' in config and 'yleg' in config:
		plotter.legendPos1.first=config['xleg'][0]
		plotter.legendPos2.first=config['xleg'][1]
		plotter.legendPos1.second=config['yleg'][0]
		plotter.legendPos2.second=config['yleg'][1]
	#R.GetYaxis().SetRangeUser(0,R.GetMaximum()*1.2)

	#R.Draw("AXIS P")
	#S.Draw("P E2 SAME")
	#R.Draw("P SAME")
	#R.Draw("AXIS X+ Y+ SAME")
	#R.Draw("AXIS SAME")
	#L.AddEntry(R,"Data","P");
	#L.AddEntry(S,"Stat+Syst","F");
	if options.mc:
	   for iMC in range(0,len(config['mcName1'])):
		#mcR[iMC].Draw("HIST SAME")
		#mcN=mcR.Clone("MG_Norm")
		#mcN.SetLineStyle(ROOT.kDashed)
		print "Z Scale: %.3f"%(h1.Integral()/ mc1.Integral())
		print "G Scale: %.3f"%(h2.Integral()/ mc2.Integral())
		#mcN.Scale(h1.Integral() * mc2.Integral() / (h2.Integral() * mc1.Integral() ))
		#           LO   NNLO      
		#mcN.Scale((2590./3503.71)/(1./1.))
		mcR[iMC].Scale(config['mcLO1'][iMC]/(config['mcLO2'][iMC]))
		#mcR[iMC].Draw("HIST SAME")
		#L.AddEntry(mcR[iMC],config['mcLeg'][iMC],"F");
		#L.AddEntry(mcN,"MG (LO/LO)","F");
		plotter.mc.push_back(mcR[iMC])
		plotter.mcLabels.push_back(config['mcLeg'][iMC])
		if options.table:
			OutROOT.cd()
			mcR[iMC].Write()
			###
			curRow=len(Table)
			Table.append(["MC Z (%s)"%config['mcLeg'][iMC] ])
			for i in range(1,mcR[iMC].GetNbinsX()+1):
				Table[curRow].append("$%f$" % ( SingleMC1[iMC].GetBinContent(i) * config['mcLO1'][iMC]) )
			###
			curRow=len(Table)
			Table.append(["MC G (%s)"%config['mcLeg'][iMC] ])
			for i in range(1,mcR[iMC].GetNbinsX()+1):
				Table[curRow].append("$%f$" % ( SingleMC2[iMC].GetBinContent(i) * config['mcLO2'][iMC]  ) )
			###
			curRow=len(Table)
			Table.append(["MC R (%s)"%config['mcLeg'][iMC] ])
			for i in range(1,mcR[iMC].GetNbinsX()+1):
				Table[curRow].append("$%.5f$" % (mcR[iMC].GetBinContent(i) ) )
			##
			curRow=len(Table)
			Table.append(["MC Stat (%s \\%%)"%config['mcLeg'][iMC] ])
			for i in range(1,mcR[iMC].GetNbinsX()+1):
				try:
					e1=SingleMC1[iMC].GetBinError(i)/ SingleMC1[iMC].GetBinContent(i)
					e2=SingleMC2[iMC].GetBinError(i)/ SingleMC2[iMC].GetBinContent(i)
					Table[curRow].append("$%.2f$" % ( math.sqrt(e1*e1+e2*e2) *100 ) )
				except:
					Table[curRow].append("$%f$" % ( -1 ) )
		# end mc				

	#L.Draw();
	#lat=ROOT.TLatex()
	#lat.SetNDC()
	#lat.SetTextFont(62)
	#lat.SetTextSize(0.04)
	#lat.SetTextAlign(11)
	if not (config['xaxis'][0]==0 and config['xaxis'][1]==0):
		plotter.Range.first=config['xaxis'][0]
		plotter.Range.second=config['xaxis'][1]
		print "x range set to ",config['xaxis'][0],config['xaxis'][1]
	else:
		plotter.Range.first=99.99
		plotter.Range.second=1093
	if not (config['yaxis'][0]==0 and config['yaxis'][1]==0):
		plotter.RangeY.first=config['yaxis'][0]
		plotter.RangeY.second=config['yaxis'][1]
	text=""
	if int(cut[0]) > 10 :
		text +="Ht > %.0f"%(float(cut[0])) 
	text+="N_{jets} #geq %.0f "%(float(cut[1]))
	if ( float(cut[2])> 30 ) : text += " p_{T}^{jet} #geq %.0f"%(float(cut[2]))
	if 'text' in config:
		text=FixNames(config['text'],cut)
	#lat.DrawLatex(.15+xshift,.85+yshift,"CMS Preliminary,")
	#lat.SetTextFont(42)
	#lat.DrawLatex(.15+xshift,.80+yshift,"#sqrt{s} = 8TeV, L=19.7fb^{-1}")
	#lat.DrawLatex(.15+xshift,.75+yshift,text)
	plotter.extraText=text;
	C=plotter.Draw()
	C.Update()
	ROOT.gPad.Update()

	if config['xlog']: 
		C.SetLogx()
		R.GetXaxis().SetMoreLogLabels()
		R.GetXaxis().SetNoExponent()
	if config['ylog']: 
		C.SetLogy()
		R.GetYaxis().SetMoreLogLabels()
		R.GetYaxis().SetNoExponent()
	if not (config['xaxis'][0]==0 and config['xaxis'][1]==0):
		R.GetXaxis().SetRangeUser(config['xaxis'][0],config['xaxis'][1]);
		S.GetXaxis().SetRangeUser(config['xaxis'][0],config['xaxis'][1]);
		print "x range set to ",config['xaxis'][0],config['xaxis'][1]
	if not (config['yaxis'][0]==0 and config['yaxis'][1]==0):
		R.GetYaxis().SetRangeUser(config['yaxis'][0],config['yaxis'][1]);
		S.GetYaxis().SetRangeUser(config['yaxis'][0],config['yaxis'][1]);

	C.Update()
	ROOT.gPad.Update()
	if not options.batch:
		a=raw_input("Press Enter");
	extensions=["pdf","root","png"]
	for ext in extensions:
		name= config["Out"]+("/C_"+FixNames(config['OutName'],cut) + "."+ext)
		print "Going to save '"+ name+"'"
		C.SaveAs( name )	
	if options.table:
		name= config["Out"]+("/C_"+FixNames(config['OutName'],cut) + ".tex")
		txt = open(name,"w")
		txt.write( ConvertToLatex(Table) )
		txt.write("\n")
		txt.close()
	AllCanvas.append(C)

	#SinglePlots:
	plotter1=ROOT.NicePlots.SingleUpperPlot();
	plotter2=ROOT.NicePlots.SingleUpperPlot();
	plotter1.data=h1
	plotter2.data=h2
	plotter1.syst=h1_TOT
	plotter2.syst=h2_TOT
	plotter1.xtitle="p_{T}^{Z} [GeV]"
	plotter1.ytitle="d#sigma/dp_{T} [fb GeV^{-1}]"
	plotter2.xtitle="p_{T}^{#gamma} [GeV]"
	plotter2.ytitle="d#sigma/dp_{T} [fb GeV^{-1}]"
	for iMC in range(0,len(config['mcName1'])):
		plotter1.mc.push_back(SingleMC1[iMC]);
		plotter1.mcLabels.push_back(config['mcLeg'][iMC])
		plotter2.mc.push_back(SingleMC2[iMC]);
		plotter2.mcLabels.push_back(config['mcLeg'][iMC])
	plotter1.RangeFactors.first=1.0
	plotter1.RangeFactors.second=0.05
	plotter2.RangeFactors.first=1.0
	plotter2.RangeFactors.second=0.05
	if not (config['xaxis'][0]==0 and config['xaxis'][1]==0):
		plotter1.Range.first=config['xaxis'][0]
		plotter1.Range.second=config['xaxis'][1]
		plotter2.Range.first=config['xaxis'][0]
		plotter2.Range.second=config['xaxis'][1]
	else:
		plotter1.Range.first=99.99
		plotter1.Range.second=1093
		plotter2.Range.first=99.99
		plotter2.Range.second=1093

	C1up=plotter1.Draw()
	C1up.SetName("c1up")
	C2up=plotter2.Draw()
	C2up.SetName("c2up")
	AllCanvas.append(C1up)
	AllCanvas.append(C2up)

	call(["mkdir",config["Out"]+"/single/" ])
	for ext in extensions:
		name= config["Out"]+("/single/file1_up_"+FixNames(config['OutName'],cut) + "."+ext)
		print "Going to save '"+ name+"'"
		C1up.SaveAs( name )	
		name= config["Out"]+("/single/file2_up_"+FixNames(config['OutName'],cut) + "."+ext)
		print "Going to save '"+ name+"'"
		C2up.SaveAs( name )	

	plotter1=ROOT.NicePlots.SingleLowerPlot();
	plotter2=ROOT.NicePlots.SingleLowerPlot();
	plotter1.data=Ratio(h1,h1,NoErrorH=True)
	plotter2.data=Ratio(h2,h2,NoErrorH=True)
	plotter1.syst=Ratio(h1,h1_TOT,NoErrorH=True)
	plotter2.syst=Ratio(h2,h2_TOT,NoErrorH=True);
	plotter1.xtitle="p_{T}^{Z} [GeV]"
	plotter1.ytitle="MC/Data"
	plotter2.xtitle="p_{T}^{#gamma} [GeV]"
	plotter2.ytitle="MC/Data"
	for iMC in range(0,len(config['mcName1'])):
		plotter1.mc.push_back(Ratio( h1,SingleMC1[iMC],NoErrorH=True ));
		plotter1.mcLabels.push_back(config['mcLeg'][iMC])
		plotter2.mc.push_back(Ratio( h2,SingleMC2[iMC],NoErrorH=True));
		plotter2.mcLabels.push_back(config['mcLeg'][iMC])
	plotter1.RangeFactors.first=1.0
	plotter1.RangeFactors.second=0.05
	plotter2.RangeFactors.first=1.0
	plotter2.RangeFactors.second=0.05
	if not (config['xaxis'][0]==0 and config['xaxis'][1]==0):
		plotter1.Range.first=config['xaxis'][0]
		plotter1.Range.second=config['xaxis'][1]
		plotter2.Range.first=config['xaxis'][0]
		plotter2.Range.second=config['xaxis'][1]
	else:
		plotter1.Range.first=99.99
		plotter1.Range.second=1093
		plotter2.Range.first=99.99
		plotter2.Range.second=1093
	C1dn=plotter1.Draw();
	C1dn.SetName("c1dn")
	C2dn=plotter2.Draw();
	C2dn.SetName("c2dn")

	AllCanvas.append(C2dn)
	AllCanvas.append(C1dn)
	
	for ext in extensions:
		name= config["Out"]+("/single/file1_dn_"+FixNames(config['OutName'],cut) + "."+ext)
		print "Going to save '"+ name+"'"
		C1dn.SaveAs( name )	
		name= config["Out"]+("/single/file2_dn_"+FixNames(config['OutName'],cut) + "."+ext)
		print "Going to save '"+ name+"'"
		C2dn.SaveAs( name )	
	#------------- Ratio Lower --------------------
	plot_L = ROOT.NicePlots.SingleRatioLowerPlot();
	if 'ytitle' in config:
		plot_L.extraText=config['ytitle']+", "+text;
	else:
		plot_L.extraText="d#sigma/dP_{T}^{Z}/d#sigma/dP_{T}^{#gamma}, "+text;

	if not (config['xaxis'][0]==0 and config['xaxis'][1]==0):
		plot_L.Range.first=config['xaxis'][0]
		plot_L.Range.second=config['xaxis'][1]
	else:
		plot_L.Range.first=99.99
		plot_L.Range.second=1093

	data2 = plotter.data.Clone("dataLower")
	syst2 = plotter.syst.Clone("systLower")
	data_L = Ratio(data2,data2,NoErrorH=True)
	syst_L = Ratio(data2,syst2,NoErrorH=True)
	plot_L.data= data_L
	plot_L.syst= syst_L
	for iMC in range(0,len(config['mcName1'])):
		mcRi=mcR[iMC].Clone("mc_%d_Lower"%iMC)
		iB=mcRi.FindBin(100.1)
		mc_L=Ratio(data2,mcRi,NoErrorH=True)
		print "DEBUG data/MC data/MC:",data2.GetBinContent(iB),mcRi.GetBinContent(iB),mc_L.GetBinContent(iB)
		#mc_L.Scale(config['mcLO1'][iMC]/config['mcLO2'][iMC])
		#mcR[iMC].Scale(config['mcLO1'][iMC]/(config['mcLO2'][iMC]))
                plot_L.mc.push_back(mc_L)
		plot_L.mcLabels.push_back(config['mcLeg'][iMC])
	Cdn=plot_L.Draw();

	AllCanvas.append(Cdn)

	for ext in extensions:
		name= config["Out"]+("/Lower_"+FixNames(config['OutName'],cut) + "."+ext)
		print "Going to save '"+ name+"'"
		Cdn.SaveAs( name )	
	#for cut in Cuts
