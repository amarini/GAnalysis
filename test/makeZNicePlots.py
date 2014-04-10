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
parser.add_option("-i","--inputFile" ,dest='inputFile',type='string',help="Input file",default="")
parser.add_option("-o","--outputFile" ,dest='outputFile',type='string',help="Output file",default="")

(options,args)=parser.parse_args()

print "inserting in path cwd"
sys.path.insert(0,os.getcwd())
print "inserting in path cwd/python"
sys.path.insert(0,os.getcwd()+'/python')
#from common import *
#from commonRatio import MergeBins,ReadRatioDat
#from commonRatio import sqrtSum,makeBands,Ratio
from commonRatio import Ratio
#from commonRatio import NiceRange 

inputFile=options.inputFile
outputFile=options.outputFile

ROOT.gSystem.Load("libGAnalysis.so") ##for syst names
fRoot= ROOT.TFile.Open(inputFile)

Range=[39.99,801.]
H_f=fRoot.Get("hData_leptons_combined")
H=ROOT.TH1D()
H_f.Copy(H)
H_TOT=H.Clone("syst")
systBand=fRoot.Get("h_tot_unc_band_comb")
for iBin in range(1,H_TOT.GetNbinsX()+1):
	H_TOT.SetBinError(iBin,systBand.GetBinContent(iBin))
H_MG_f=fRoot.Get("h_MG_GEN_leptons_combined")
H_SH_f=fRoot.Get("h_SH_GEN_leptons_combined")
H_BH_f=fRoot.Get("h_BH_rebinned_mumu")
H_MG=ROOT.TH1D()
H_SH=ROOT.TH1D()
H_MG_f.Copy(H_MG)
H_SH_f.Copy(H_SH)

plotter=ROOT.NicePlots.SingleUpperPlot();
plotter.data=H
plotter.syst=H_TOT
plotter.xtitle="p_{T}^{Z} [GeV]"
plotter.ytitle="d#sigma/dp_{T} [fb GeV^{-1}]"
plotter.mc.push_back(H_MG);
plotter.mcLabels.push_back("MadGraph");
plotter.mc.push_back(H_SH);
plotter.mcLabels.push_back("Sherpa");
if H_BH_f != None :
	H_BH=ROOT.TH1D()
	H_BH_f.Copy(H_BH)
	plotter.mc.push_back(H_BH);
	plotter.mcLabels.push_back("BlackHat");

nJets=1
Ht=0
Y=100
pt1=30
is_Zpt_o_Ht=False
is_Zpt_o_pt1=False
isLog=False
if 'njets2plus' in inputFile:
	nJets=2
if 'njets3plus' in inputFile:
	nJets=3
if 'HT_300' in inputFile:
	Ht=300
if 'HT_100' in inputFile:
	Ht=100
if 'BY_Inf' in inputFile:
	Y=100
if 'BY_1_40' in inputFile:
	Y=1.4
if  'pt1_300' in inputFile:
	pt1=300
if 'Zpt_over_HT' in inputFile:
	is_Zpt_o_Ht=True
if 'Zpt_over_pt1' in inputFile:
	is_Zpt_o_pt1=True
if 'log10' in inputFile:
	isLog=True

if is_Zpt_o_pt1 and not isLog:
	Range[0]=0
	Range[1]=3
if is_Zpt_o_Ht and not isLog:
	Range[0]=0
	Range[1]=3
if is_Zpt_o_pt1 and isLog:
	Range[0]=-1.4
	Range[1]=0.8
if is_Zpt_o_Ht and isLog:
	Range[0]=-1.4
	Range[1]=0.8
if isLog:
	plotter.cmsPosition.second=0.89
	xshift=0.1
	plotter.legendPos1.first=-0.2 + 0.5+ xshift
	plotter.legendPos1.second=0.15
	plotter.legendPos2.first=0.2 + 0.5 + xshift
	plotter.legendPos2.second=0.45
	plotter.RangeFactors.first=0.1
	plotter.RangeFactors.second=0.1

plotter.SetHeader('Z',nJets,Ht)
if is_Zpt_o_pt1 or is_Zpt_o_Ht:
	plotter.legendHeader += ", p_{T}^{ll}>40 "
if Y<3:
	plotter.extraText="|Y^{Z}|<%.1f"%Y
plotter.RangeFactors.first=1.0
plotter.RangeFactors.second=0.05
plotter.Range.first=Range[0]
plotter.Range.second=Range[1]
C1=plotter.Draw()
C1.SaveAs(outputFile)		

R_H=Ratio(H,H,NoErrorH=True); 
R_TOT=Ratio(H,H_TOT,True);
plotter=ROOT.NicePlots.SingleLowerPlot();
plotter.data=R_H
plotter.syst=R_TOT
plotter.xtitle="p_{T}^{Z} [GeV]"
plotter.ytitle="MC/Data"
R_MG=Ratio(H,H_MG,True);
R_SH=Ratio(H,H_SH,True);
plotter.mc.push_back(R_MG);
plotter.mcLabels.push_back("MadGraph");
plotter.mc.push_back(R_SH);
plotter.mcLabels.push_back("Sherpa");
if H_BH_f != None:
	R_BH=Ratio(H,H_BH,True);
	plotter.mc.push_back(R_BH);
	plotter.mcLabels.push_back("BlackHat");
plotter.SetHeader('Z',nJets,Ht)
if Y<3:
	plotter.extraText="|Y^{Z}|<%.1f"%Y
plotter.RangeFactors.first=1.0
plotter.RangeFactors.second=0.05
plotter.Range.first=Range[0]
plotter.Range.second=Range[1]
C2=plotter.Draw()

if 'pdf' in outputFile:
	name=outputFile.replace(".pdf","")
	name += "_lower.pdf"
elif 'png' in outputFile:
	name=outfile.replace(".png","")
	name += "_lower.png"
elif 'eps' in outputFile:
	name=outfile.replace(".eps","")
	name += "_lower.eps"
elif 'root' in outputFile:
	name=outfile.replace(".root","")
	name += "_lower.root"
else: print 'unsupported format'
C2.SaveAs(name)

