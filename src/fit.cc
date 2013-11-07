
#include "TH1D.h"
#include "TFile.h"
#include "TFitResultPtr.h"
#include "TFitResult.h"
#include "TLatex.h"
#include "TText.h"
#include "TROOT.h"
#include "TDirectory.h"
#include "TCanvas.h"

//----------ROOFIT-----------
//Roofit
#ifndef __CINT__
#include "RooGlobalFunc.h"
#endif

#include "RooRealVar.h"
#include "RooDataSet.h"
#include "RooDataHist.h"
#include "RooGaussian.h"
#include "RooPlot.h"
#include "RooPolynomial.h"
#include "RooExponential.h"
#include "RooDataSet.h"
#include "RooAddPdf.h"
#include "RooGenericPdf.h"
#include "RooSimultaneous.h"
#include "RooCategory.h"
#include "RooFitResult.h"
#include "RooHistPdf.h"
#include "RooVoigtian.h"
#include "RooWorkspace.h"
#include "RooLandau.h"

#include "fit.h"
#include "stat.h"


using namespace std;
using namespace RooFit;


float FIT::fit(TObject *o, TH1D* sig, TH1D* bkg,const char *fileName,const char *name,vector<float> *pars)
{
	printf("DEBUG: NAME=%s FILE=%s\n",name,fileName);
	bool binned=false;
	if(o->InheritsFrom("TH1") ) binned=true;
	else if (o->InheritsFrom("TTree")) binned=false;
	else printf("ERROR NO TREE OR TH1D provided\n");
	TTree *t;
	TH1D *h;
	if (binned) h=(TH1D*)o;
	else t=(TTree*)o;
	
	int nBins=sig->GetNbinsX();
	float xMin=sig->GetBinLowEdge(1);
	float xMax=sig->GetBinLowEdge(nBins+1);
	
	//Normalization
	sig->Sumw2();
	bkg->Sumw2();
	if(sig->Integral()>0)
		sig->Scale(1./sig->Integral());
	if(bkg->Integral()>0)
		bkg->Scale(1./bkg->Integral());
	if(binned)
		{
		h->Sumw2();
		if(h->Integral()>0)
			h->Scale(1./h->Integral());
		}
	//bkg fit to Landau
	vector<float> bkgPar; bkgPar.resize(10);
	TFitResultPtr bkgR=bkg->Fit("landau","LS");
	bkgPar[0]=bkgR->Parameter(0);
	bkgPar[1]=bkgR->Parameter(1);
	bkgPar[2]=bkgR->Parameter(2);
	cout<<"--> LANDAU PARS "<<bkgPar[0]<<" "<<bkgPar[1]<<" " <<bkgPar[2]<<endl;
	if(pars!=NULL) {
		pars->resize(10);	
		(*pars)[0]=bkgPar[0];
		(*pars)[1]=bkgPar[1];
		(*pars)[2]=bkgPar[2];
		}
	//parameter estimation for binned
	float fracEstimator=0;
	if(binned){
		int nTailSum=5;
		float sigMax= sig->GetMaximum();// get the peak
		float sigInt= sig->Integral();
		int bkgN=bkg->GetNbinsX();
		float bkgTail=0;for(int i=0;i<nTailSum;i++) bkgTail+= bkg->GetBinContent(bkgN-i);
		float bkgInt= bkg->Integral();
		float targetMax = h->GetMaximum();
		float targetInt = h->Integral();
		int targetN=h->GetNbinsX();
		float targetTail=0;for(int i=0;i<nTailSum;i++) targetTail+= h->GetBinContent(targetN-i);
		float frac1=(targetMax/targetInt)/(sigMax/sigInt);
		float frac2=1.- (targetTail/targetInt)/(bkgTail/bkgInt);
		fracEstimator=(frac1+frac2)/2.;
		if(targetInt==0) fracEstimator=0.8;
		else if(sigInt==0 && bkgInt==0) fracEstimator=0.8;
		else if(sigInt==0) fracEstimator=frac2;
		else if(bkgInt==0) fracEstimator=frac1;
		else if(bkgTail==0) fracEstimator=frac1;
		else if(frac1 <0 || frac1>1)fracEstimator=frac2;
		else if(frac2 <0 || frac2>1)fracEstimator=frac1;

		if(fracEstimator>1.0 || fracEstimator<0)fracEstimator=0.8;

		cout<<"---> @@ Fraction Estimation"<<frac1<<" "<<frac2<<": "<<fracEstimator <<" @@"<<endl;
		}

	//create real var
	RooRealVar f("f","fraction",fracEstimator,0.01,10.) ;
		//f.setRange(0.10,1.0);
	RooRealVar x("photoniso","photoniso",xMin,xMax) ;
	//Import Histogram in RooFit
	RooDataHist HistSig("sig","hist sig",x,sig);
	RooDataHist HistBkg("bkg","hist bkg",x,bkg);
	//Convert histogram in pdfs - build model	
	RooHistPdf PdfSig("pdfsig","pdfsig",x,HistSig,0);
	RooHistPdf PdfBkg("pdfbkg","pdfbkg",x,HistBkg,0);
		RooRealVar bkgPar1("bkgPar1","bkgPar1",bkgPar[1]);
		RooRealVar bkgPar2("bkgPar2","bkgPar2",bkgPar[2]);
	RooLandau PdfBkgL("pdfbkgL","pdfbkgL",x,bkgPar1,bkgPar2);

	//Use template	
	//RooAddPdf PdfModel("model","model",RooArgList(PdfSig,PdfBkg),f);
	//Use Landau model for bkg
	RooAddPdf PdfModel("model","model",RooArgList(PdfSig,PdfBkgL),f);

	//----FIT---
	RooFitResult *r;
	RooPlot *frame=x.frame();
	if(binned){
		printf("----> Going to create RooDataHist\n");
		RooDataHist HistToFit("hist","hist",x,h); 
		//r = PdfModel.fitTo(HistToFit,SumW2Error(kTRUE),Save());
		printf("----> Going to fit\n");
		r = PdfModel.fitTo(HistToFit,Save(),SumW2Error(kFALSE));
		printf("----> Going to plot\n");
		HistToFit.plotOn(frame,DataError(RooAbsData::SumW2));
		}
	else {
		RooDataSet  DataToFit("data","data",RooArgSet(x),Import(*t));
		r = PdfModel.fitTo(DataToFit,Save());
		DataToFit.plotOn(frame);
		}
	//----SAVE---
	PdfModel.plotOn(frame);
	PdfModel.plotOn(frame,Components(PdfBkgL),LineColor(kRed)); // Landau
	PdfBkg.plotOn(frame,LineStyle(kDashed),LineColor(kBlue),Normalization(1.-f.getVal(),RooAbsReal::Relative)); // Landau
	PdfModel.plotOn(frame,Components(PdfSig),LineColor(kGreen+2),LineStyle(kDashed));
	
	TCanvas *c=new TCanvas((string(name)+"_canvas").c_str(),"Canvas");
	c->cd();
	c->Draw();
	frame->Draw();
	
	TLatex* txt = new TLatex();//Form("Fraction=%.1f\%",f.getVal()*100) ;
  	txt->SetTextSize(0.03) ;
  	txt->SetTextColor(kBlack) ;
	txt->SetNDC();
	txt->SetTextAlign(22);
	//txt->AddText(Form("Fraction=%.1f\%",f.getVal()*100) );
	txt->DrawLatex(.3,.85,Form("Fraction=%.1f%%",float(f.getVal()*100)));
	//Get VPt Ht e Njets from name	
		{
		float ptmin,ptmax,ht,nj;
		string n(name);
		int pos=0;
		//"Bin_PT_111.0_123.1_HT_0.0_nJets_1"
		while ( (pos=n.find("_")) != string::npos) n[pos]=' ';
		//"Bin PT 111.0 123.1 HT 0.0 nJets 1"
		printf("--> STRING=%s\n",n.c_str());
		sscanf(n.c_str(),"%*s %*s %f %f %*s %f %*s %f",&ptmin,&ptmax,&ht,&nj);
		txt->SetTextSize(0.02);
		txt->SetTextFont(42);
		if( ht>1 ) txt->DrawLatex(.3,.82,Form("%.1f<P_{T}<%.1f H_{T}>%.0f N_{jets}#geq%.0f",ptmin,ptmax,ht,nj));
		else txt->DrawLatex(.3,.82,Form("%.1f<P_{T}<%.1f N_{jets}#geq%.0f",ptmin,ptmax,nj));
		}
  	frame->addObject(txt) ;	
	
	  // Access basic information
	  cout << "EDM = " << r->edm() << endl ;
	  cout << "-log(L) at minimum = " << r->minNll() << endl ;
	  cout << "Error = "<<f.getError()<<endl;
	  cout << "--> FractionFitted = "<<f.getVal()<<endl;
	if(pars!=NULL)	
		(*pars)[3]=f.getError();
	//
	if(name[0]!='\0')
		{
		TFile file(fileName,"UPDATE") ;
		c->Write();
		RooWorkspace *ws=NULL;
			ws=(RooWorkspace*)file.Get("fit_ws");
		if(ws==NULL) {ws=new RooWorkspace("fit_ws");}
		frame->SetName((string(name)+"_plot").c_str());
		f.SetName((string(name)+"_f").c_str());
		r->SetName((string(name)+"_r").c_str());
		ws->import(RooArgSet(f,PdfModel));
		ws->Write("fit_ws",TObject::kOverwrite);
		frame->Write( (string(name)+"_plot" ).c_str());
		file.Close();
		}

	//-----RETURN ---
	return f.getVal();
} //End Of Fit


//--------------------------------------------TOYS------------------------------------
#include "TRandom3.h"
#include "TRandom.h"
#include "time.h"
#include <vector>
#include <algorithm>

//namespace TOYS {

void TOYS::RandomVar(TH1D*h,TRandom *r,int sumw2){
	for(int i=1;i<=h->GetNbinsX();i++)
		{
		float bc=h->GetBinContent(i);
		float be=h->GetBinError(i);
		if(sumw2)
			{
			h->SetBinContent(i, r->Gaus(bc,be) );
			if(h->GetBinContent(i)<0)h->SetBinContent(i,0);
			}
		else
			h->SetBinContent(i, r->Poisson(bc) );
		}
	if(h->Integral()==0) 
		if(sumw2)
			printf("ERROR INTEGRAL IS 0 in TOYS\n ");
		else 
			{
			printf("ERROR INTEGRAL IS 0 in TOYS: switch to Sumw2\n");
			RandomVar(h,r,1);
			}
	
}

float TOYS::toy(TH1D*h, TH1D* sig, TH1D* bkg,int nToys,TRandom *random,const char*fileName)
{
vector<float> r; //result
	if(random==NULL){
			long long seed=(unsigned)time(NULL); 
			random=new TRandom3((unsigned)seed);
			printf("Seed=%lld\n",seed);
			}
		
	for(int iToy=0;iToy<nToys;++iToy){
	TH1D *h1=(TH1D*)h->Clone("tmp_h");
	TH1D *s1=(TH1D*)sig->Clone("tmp_s");
	TH1D *b1=(TH1D*)bkg->Clone("tmp_b");
	
	RandomVar(h1,random,0);//poisson
	RandomVar(s1,random,0);//poisson
	RandomVar(b1,random,0);//poisson
	//RandomVar(h1,random,1);//gaus
	//RandomVar(s1,random,1);//gaus
	//RandomVar(b1,random,1);//gaus
	
	if(h1->Integral()==0 || s1->Integral()==0 || b1->Integral()==0)
		{cout<<"SKIP TOY EVENT: INTEGRAL=0"<<endl;continue;}

	printf("DEBUG: PASSING %s as fileName\n",fileName);
	float a= FIT::fit(h1,s1,b1,fileName,Form("toy%d_PT_0_0_HT_0_nJet_0\0",iToy)); //string should be formatted
	
	r.push_back(a);
		
	h1->Delete();
	s1->Delete();
	b1->Delete();	
	}
	return  STAT::rms(r);
	pair<float,float> b; //store low-hi for asymmetric
	return  STAT::ConfidenceInterval(r,b,0.68);
}


//}; //namespace TOYS
