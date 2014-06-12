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

#Range=[39.99,801.]
Range=[41,799]
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
plotter.drawBands=0
plotter.data=H
plotter.syst=H_TOT
plotter.xtitle="p_{T}^{Z} [GeV]"
plotter.ytitle="d#sigma/dp_{T} [fb GeV^{-1}]"
plotter.mc.push_back(H_MG);
plotter.mcLabels.push_back("MadGraph k_{NNLO}");
plotter.mc.push_back(H_SH);
plotter.mcLabels.push_back("Sherpa k_{NNLO}");
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
	#Range[1]=3.2
	Range[1]=2.9
	plotter.xtitle="p_{T}^{Z}/p_{T}^{j1}"
	plotter.ytitle="d#sigma/d(p_{T}^{Z}/p_{T}^{j1})"
if is_Zpt_o_Ht and not isLog:
	Range[0]=0
	#Range[1]=3
	Range[1]=2.5
	plotter.xtitle="p_{T}^{Z}/H_{T}"
	plotter.ytitle="d#sigma/d(p_{T}^{Z}/H_{T})"
if is_Zpt_o_Ht and nJets == 3 and not isLog:
	Range[1]=1.7
if is_Zpt_o_pt1 and isLog:
	Range[0]=-1.
	Range[1]=0.7
	plotter.xtitle="log_{10} (p_{T}^{Z}/p_{T}^{j1})"
	plotter.ytitle="d#sigma/d log_{10}(p_{T}^{Z}/p_{T}^{j1})"
if is_Zpt_o_Ht and isLog:
	#Range[0]=-1.28
	#Range[1]=1.2
	Range[0]=-1.2
	Range[1]=0.35
	plotter.xtitle="log_{10} (p_{T}^{Z}/H_{T})"
	plotter.ytitle="d#sigma/d log_{10}(p_{T}^{Z}/H_{T})"

if  is_Zpt_o_Ht or is_Zpt_o_pt1 or isLog:
	plotter.legendPos1.first=0.35
	plotter.legendPos1.second=0.13
	plotter.legendPos2.first=0.70
	plotter.legendPos2.second=0.33

if is_Zpt_o_Ht and nJets == 2 and not isLog:
	plotter.legendPos1.first=0.20
	plotter.legendPos2.first=0.55
#if isLog:
#	plotter.legendPos1.first=0.65
#	plotter.legendPos1.second=0.13
#	plotter.legendPos2.first=0.97
#	plotter.legendPos2.second=0.33
	
plotter.SetHeader('Z',nJets,Ht)
if is_Zpt_o_pt1 or is_Zpt_o_Ht:
	plotter.legendHeader += ", p_{T}^{ll}>40 "
if Y<3:
	plotter.extraText="|Y^{Z}|<%.1f"%Y
plotter.RangeFactors.first=0.00
plotter.RangeFactors.second=0.00
#if isLog:
	#plotter.cmsPosition.second=0.89
	#xleg 0.70 .97
	#yleg 0.11 .31
#	plotter.RangeFactors.first=0.05
#	plotter.RangeFactors.second=0.05
plotter.Range.first=Range[0]
plotter.Range.second=Range[1]

R_H=Ratio(H,H,NoErrorH=True); 
R_TOT=Ratio(H,H_TOT,True);
xtitle=plotter.xtitle

plot_L=ROOT.NicePlots.SingleLowerPlot();
plot_L.data=R_H
plot_L.syst=R_TOT
plot_L.xtitle=xtitle
plot_L.ytitle="MC/Data"
R_MG=Ratio(H,H_MG,True);
R_SH=Ratio(H,H_SH,True);
plot_L.mc.push_back(R_MG);
plot_L.mcLabels.push_back("MadGraph k_{NNLO}");
plot_L.mc.push_back(R_SH);
plot_L.mcLabels.push_back("Sherpa k_{NNLO}");
## add stat bands

StatErrBands=True
if StatErrBands:
	R_MG_Err=R_MG.Clone("MG_Err")
	plot_L.mcErr.push_back(R_MG_Err);
	plot_L.mcLabelsErr.push_back("MG Stat Err");
	plot_L.mcErrAssociation.push_back(0);

	R_SH_Err=R_SH.Clone("SH_Err")
	plot_L.mcErr.push_back(R_SH_Err);
	plot_L.mcLabelsErr.push_back("SH Stat Err");
	plot_L.mcErrAssociation.push_back(1);
if H_BH_f != None:
	R_BH=Ratio(H,H_BH,True);
	plot_L.mc.push_back(R_BH);
	plot_L.mcLabels.push_back("BlackHat");

	#scale 
	H_pdf_up_f=fRoot.Get("h_band_BH_PDFUp_rebinned_total")
	H_pdf_dn_f=fRoot.Get("h_band_BH_PDFDown_rebinned_total")
	H_scale_up_f=fRoot.Get("h_band_BH_scaleUp_rebinned_total")
	H_scale_dn_f=fRoot.Get("h_band_BH_scaleDown_rebinned_total")

	if H_pdf_up_f !=None and H_pdf_dn_f != None:
		H_PDF=ROOT.TH1D()
		H_BH_f.Copy(H_PDF)
		for iBin in range(0,H_PDF.GetNbinsX()):
			c=H_PDF.GetBinContent(iBin+1)
			up=max(c,c+H_pdf_up_f.GetBinContent(iBin+1),c-H_pdf_dn_f.GetBinContent(iBin+1)) 
			dn=min(c,c+H_pdf_up_f.GetBinContent(iBin+1),c-H_pdf_dn_f.GetBinContent(iBin+1))
			H_PDF.SetBinContent(iBin+1,abs(up+dn)/2)
			H_PDF.SetBinError(iBin+1,abs(up-dn)/2)
		R_H_PDF=Ratio(H,H_PDF,NoErrorH=True); 
		plot_L.mcLabelsErr.push_back("PDF")
		plot_L.mcErr.push_back(R_H_PDF)
		plot_L.mcErrAssociation.push_back(2);
	if H_scale_up_f !=None and H_scale_dn_f != None:
		H_SCALE=ROOT.TH1D()
		H_BH_f.Copy(H_SCALE)
		for iBin in range(0,H_SCALE.GetNbinsX()):
			c=H_SCALE.GetBinContent(iBin+1)
			up=max(c,c+H_scale_up_f.GetBinContent(iBin+1),c-H_scale_dn_f.GetBinContent(iBin+1)) 
			dn=min(c,c+H_scale_up_f.GetBinContent(iBin+1),c-H_scale_dn_f.GetBinContent(iBin+1))
			H_SCALE.SetBinContent(iBin+1,abs(up+dn)/2)
			H_SCALE.SetBinError(iBin+1,abs(up-dn)/2)
		R_H_SCALE=Ratio(H,H_SCALE,NoErrorH=True); 
		plot_L.mcLabelsErr.push_back("Scale")
		plot_L.mcErr.push_back(R_H_SCALE)
		plot_L.mcErrAssociation.push_back(2);
	## more than one pdf
	H_BH_NNPDF_f =fRoot.Get("h_BH_NNPDF_rebinned_total")
	H_BH_CT10_f =fRoot.Get("h_BH_CT10_rebinned_total")

	H_BH_NNPDF_scale_up_f=fRoot.Get("h_band_BH_NNPDF_scaleUp_rebinned_total")
	H_BH_NNPDF_scale_dn_f=fRoot.Get("h_band_BH_NNPDF_scaleDown_rebinned_total")
	H_BH_CT10_scale_up_f=fRoot.Get("h_band_BH_CT10_scaleUp_rebinned_total")
	H_BH_CT10_scale_dn_f=fRoot.Get("h_band_BH_CT10_scaleDown_rebinned_total")
	
	if H_BH_CT10_f !=None and H_BH_CT10_scale_up_f !=None and H_BH_CT10_scale_dn_f != None:
		H_BH_CT10=ROOT.TH1D()
		H_BH_CT10_f.Copy(H_BH_CT10)

		H_BH_CT10_SCALE=ROOT.TH1D()
		H_BH_CT10_f.Copy(H_BH_CT10_SCALE)

		R_H_BH_CT10=Ratio(H,H_BH_CT10,NoErrorH=True); 

		for iBin in range(0,H_BH_CT10_SCALE.GetNbinsX()):
			c=H_BH_CT10_SCALE.GetBinContent(iBin+1)
			up=max(c,c+H_BH_CT10_scale_up_f.GetBinContent(iBin+1),c-H_BH_CT10_scale_dn_f.GetBinContent(iBin+1)) 
			dn=min(c,c+H_BH_CT10_scale_up_f.GetBinContent(iBin+1),c-H_BH_CT10_scale_dn_f.GetBinContent(iBin+1))
			H_BH_CT10_SCALE.SetBinContent(iBin+1,abs(up+dn)/2)
			H_BH_CT10_SCALE.SetBinError(iBin+1,abs(up-dn)/2)
		R_H_BH_CT10_SCALE=Ratio(H,H_BH_CT10_SCALE,NoErrorH=True); 
		
		plotter.mc.push_back(H_BH_CT10)
		plotter.mcLabels.push_back("BH CT10")
		plot_L.mc.push_back(R_H_BH_CT10)
		plot_L.mcLabels.push_back("BH CT10")
		plot_L.mcLabelsErr.push_back("Scale")
		plot_L.mcErr.push_back(R_H_BH_CT10_SCALE)
		plot_L.mcErrAssociation.push_back(3);

	if H_BH_NNPDF_f !=None and H_BH_NNPDF_scale_up_f !=None and H_BH_NNPDF_scale_dn_f != None:
		H_BH_NNPDF=ROOT.TH1D()
		H_BH_NNPDF_f.Copy(H_BH_NNPDF)

		H_BH_NNPDF_SCALE=ROOT.TH1D()
		H_BH_NNPDF_f.Copy(H_BH_NNPDF_SCALE)

		R_H_BH_NNPDF=Ratio(H,H_BH_NNPDF,NoErrorH=True); 

		for iBin in range(0,H_BH_NNPDF_SCALE.GetNbinsX()):
			c=H_BH_NNPDF_SCALE.GetBinContent(iBin+1)
			up=max(c,c+H_BH_NNPDF_scale_up_f.GetBinContent(iBin+1),c-H_BH_NNPDF_scale_dn_f.GetBinContent(iBin+1)) 
			dn=min(c,c+H_BH_NNPDF_scale_up_f.GetBinContent(iBin+1),c-H_BH_NNPDF_scale_dn_f.GetBinContent(iBin+1))
			H_BH_NNPDF_SCALE.SetBinContent(iBin+1,abs(up+dn)/2)
			H_BH_NNPDF_SCALE.SetBinError(iBin+1,abs(up-dn)/2)
		R_H_BH_NNPDF_SCALE=Ratio(H,H_BH_NNPDF_SCALE,NoErrorH=True); 
		
		plotter.mc.push_back(H_BH_NNPDF)
		plotter.mcLabels.push_back("BH NNPDF")
		plot_L.mc.push_back(R_H_BH_NNPDF)
		plot_L.mcLabels.push_back("BH NNPDF")
		plot_L.mcLabelsErr.push_back("Scale")
		plot_L.mcErr.push_back(R_H_BH_NNPDF_SCALE)
		plot_L.mcErrAssociation.push_back(4);
	

plot_L.SetHeader('Z',nJets,Ht)
if Y<3:
	plot_L.extraText="|Y^{Z}|<%.1f"%Y
plot_L.RangeFactors.first=0.05
plot_L.RangeFactors.second=0.05
plot_L.Range.first=Range[0]
plot_L.Range.second=Range[1]

C1=plotter.Draw()
C1.SaveAs(outputFile)		

C2=plot_L.Draw()

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

C3=plot_L.DrawSeparateLine()

name=name.replace('_lower','_lower2')
C3.SaveAs(name)
