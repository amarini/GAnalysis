#!/usr/bin/python
import sys,os
import array
import time
import math
from glob import glob
from optparse import OptionParser

DEBUG=1


if(DEBUG>0):print "----- BEGIN -----"

if(DEBUG>0):print "-PARSING OPTIONS-"
usage = "usage: %prog [options] arg1 arg2. Options are referrend to the string of files outputted by jetphox itself"
parser=OptionParser(usage=usage)
parser.add_option("","--jetphox" ,dest='jetphox',type='string',help="JetPhox file",default="")
parser.add_option("","--jetphox2" ,dest='jetphox2',type='string',help="JetPhox file",default="")
parser.add_option("","--scale" ,dest='scale',type='string',help="JetPhox file",default="")
parser.add_option("","--pdf" ,dest='pdf',type='string',help="JetPhox file",default="")
parser.add_option("","--plotdir" ,dest='plot',type='string',help="PlotDirectory",default="")
parser.add_option("","--out" ,dest='out',type='string',help="OutRootFile. Default=%default",default="JetPhox.root")
(options,args)=parser.parse_args()


import ROOT
ROOT.gROOT.SetBatch()
ROOT.gStyle.SetOptStat(0)
ROOT.gStyle.SetOptTitle(0)

print "inserting in path cwd"
sys.path.insert(0,os.getcwd())
print "inserting in path cwd/python"
sys.path.insert(0,os.getcwd()+'/python')
from common import *
from commonRatio import MergeBins,ReadRatioDat
from commonRatio import sqrtSum,makeBands,Ratio
from commonRatio import NiceRange 

# GLOBAL in order to avoid that ROOT uses random file as buffers
outFile=ROOT.TFile.Open(options.out,"RECREATE");

def GetJetPhoxPrediction(jetphox,histName="hp40"): 
	''' Get the TH1D jetfox prediction out of a list of jetphox files '''
	#fileList=jetphox.split(',')	 ### I use glob so it is already a filelist
	fileList=jetphox
	if(DEBUG>0):print "Adding JetPhox compontent ", fileList[0]
	f_JP=ROOT.TFile.Open(fileList[0])
	outFile.cd()
	h_JetPhox_tmp=f_JP.Get(histName).Clone()
	for i in range(1,len(fileList)):
		if(DEBUG>0):print "Adding JetPhox compontent ", fileList[i]
		f2_JP=ROOT.TFile.Open(fileList[i])
		outFile.cd()
		h_i=f2_JP.Get(histName)
		h_JetPhox_tmp.Add(h_i)
		f2_JP.Close()
	h_JetPhox_tmp.Scale(1000.) # pb->fb
	if(DEBUG>0):print "JetPhox Mean between",len(fileList)/2.,"components"
	h_JetPhox_tmp.Scale(2./len(fileList)) # if more than one fileset (direct+frag), do the mean
	f_JP.Close()
	return h_JetPhox_tmp;


def Envelope(listH):
	'''Return the envelope of N histograms. This is an generalization of make bands. (Mean option)'''
	H=listH[0].Clone(listH[0].GetName()+"_band")
	for iBin in range(1,listH[0].GetNbinsX()+1):
	    low=listH[0].GetBinContent(iBin);
	    high=listH[0].GetBinContent(iBin);
	    for iHisto in range(0, len(listH)):
		low=  min(low,   listH[iHisto].GetBinContent(iBin) )
		high= max(high,  listH[iHisto].GetBinContent(iBin) )
	    H.SetBinContent(iBin, (low+high)/2.0)
	    H.SetBinError  (iBin, math.fabs(high-low )/2.0)
	return H

def GetAllHisto(histoName="hp40",BaseName="jp"):
	Scale=[]
	Pdf=[]
	##first prediction
	jetphoxlist=glob( options.jetphox + "_[0-9]/*root" )
	jetphoxlist.extend(glob( options.jetphox + "_[0-9][0-9]/*root" ))
	outFile.cd()
	h=GetJetPhoxPrediction(jetphoxlist,histoName);	
	h.SetName(BaseName);
	h.Write();
	Scale.append(h)
	Pdf.append(h)
	### second prediction
	if options.jetphox2 != "":
		jetphoxlist2=glob( options.jetphox2 + "_[0-9]/*root" )
		jetphoxlist2.extend(glob( options.jetphox2 + "_[0-9][0-9]/*root" ))
		h=GetJetPhoxPrediction(jetphoxlist2,histoName);	
		h.SetName(BaseName+"_FRIXIONE");
		h.Write();
	### envelope	
	if options.scale != "":
		for fl in options.scale.split(","):
			jp_list= glob( fl + "_[0-9]/*root");
			jp_list.extend( glob( fl + "_[0-9][0-9]/*root")  );
			h=GetJetPhoxPrediction(jp_list,histoName);
			Scale.append(h);
		h=Envelope(Scale);
		h.SetName(BaseName+ "_SCALE");
	if options.pdf != "":
		for fl in options.pdf.split(","):
			jp_list= glob( fl + "_[0-9]/*root");
			jp_list.extend( glob( fl + "_[0-9][0-9]/*root") );
			h=GetJetPhoxPrediction(jp_list,histoName);
			Pdf.append(h);
		h=Envelope(Pdf);
		h.SetName(BaseName+ "_PDF");
	outFile.Write()
	
###   KEY: TH1D	hp20;1	dsigmalo/dptgamma
###   KEY: TH1D	hp21;1	dsigmanlo/dptgamma
###   KEY: TH1D	hp22;1	dsigmanlo/dptjet
###   KEY: TH1D	hp23;1	dsigmanlo/dptjt
###   KEY: TH1D	hp24;1	dsigmanlo/dyjet
###   KEY: TH1D	hp25;1	dsigmanlo/dyjet
###   KEY: TH1D	hp40;1	dsigmanlo/dptgamma
###   KEY: TH1D	hp41;1	dsigmalo/dptgamma
###   KEY: TH1D	hp42;1	dsigmanlo_forComp
###   KEY: TH1D	hp43;1	dsigmalo_forComp 
if __name__=="__main__":
	GetAllHisto("hp40","jp");
	if options.plot != "":
		GetAllHisto("hp22","jp_ptjet");
		GetAllHisto("hp24","jp_yjet");

		GetAllHisto("hp23","jp_LO_ptjet");
		GetAllHisto("hp25","jp_LO_yjet");
		outFile.Close() ## open the file in RO mode
		outFile=ROOT.TFile.Open(options.out,"");
		for histoName in ["jp","jp_ptjet","jp_yjet","jp_LO_ptjet","jp_LO_yjet"]:	
			C=ROOT.TCanvas()
			h0=outFile.Get(histoName)
			h0.SetLineColor(ROOT.kBlue);
			h0.Draw("AXIS")
			if options.scale!="":
				hScale=outFile.Get(histoName + "_SCALE")
				hScale.SetFillColor(ROOT.kOrange)
				hScale.Draw("E2 SAME");
			if options.pdf!="":
				hPdf=outFile.Get(histoName + "_PDF")
				hPdf.SetFillColor(ROOT.kMagenta+2)
				hPdf.SetFillStyle(3004)
				hPdf.Draw("E2 SAME");
			if options.jetphox2 != "":
				hFrx=outFile.Get(histoName + "_FRIXIONE")
				hFrx.SetLineColor(ROOT.kGreen+2);
				hFrx.Draw("HIST SAME")
			h0.Draw("HIST SAME")
			if histoName=="jp": C.SetLogx();
			C.SetLogy();
			C.SaveAs(options.plot + "/" + histoName + ".pdf")
	
