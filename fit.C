#include "TH1F.h"
#include "TFile.h"

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


using namespace std;
using namespace RooFit;


float fit(TObject *o, TH1F* sig, TH1F* bkg,const char *fileName="",const char *name="")
{
	bool binned=false;
	if(o->InheritsFrom("TH1") ) binned=true;
	else if (o->InheritsFrom("TTree")) binned=false;
	else printf("ERROR NO TREE OR TH1F provided");
	TTree *t;
	TH1F *h;
	if (binned) h=(TH1F*)o;
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

	//create real var
	RooRealVar f("f","fraction",0.01,1.) ;
	RooRealVar x("photoniso","photoniso",xMin,xMax) ;
	//Import Histogram in RooFit
	RooDataHist HistSig("sig","hist sig",x,sig);
	RooDataHist HistBkg("bkg","hist bkg",x,bkg);
	//Convert histogram in pdfs - build model	
	RooHistPdf PdfSig("pdfsig","pdfsig",x,HistSig,0);
	RooHistPdf PdfBkg("pdfbkg","pdfbkg",x,HistBkg,0);
	RooAddPdf PdfModel("model","model",RooArgList(PdfSig,PdfBkg),f);
	
	//----FIT---
	RooFitResult *r;
	RooPlot *frame=x.frame();
	if(binned){
		RooDataHist HistToFit("hist","hist",x,h); 
		r = PdfModel.fitTo(HistToFit,SumW2Error(kTRUE),Save());
		HistToFit.plotOn(frame);
		}
	else {
		RooDataSet  DataToFit("data","data",RooArgSet(x),Import(*t));
		r = PdfModel.fitTo(DataToFit,SumW2Error(kTRUE),Save());
		DataToFit.plotOn(frame,DataError(RooAbsData::SumW2));
		}
	//----SAVE---
	PdfModel.plotOn(frame);
	PdfModel.plotOn(frame,Components(PdfBkg),LineStyle(kDashed));
	
	  // Access basic information
	  cout << "EDM = " << r->edm() << endl ;
	  cout << "-log(L) at minimum = " << r->minNll() << endl ;
	  cout << "Error = "<<f.getError()<<endl;
	
	//
	if(name[0]!='\0')
		{
		TFile file(fileName,"UPDATE") ;
		r->Write(name);
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

namespace TOYS {

void RandomVar(TH1F*h,TRandom *r,int sumw2=0){
	for(int i=0;i<=h->GetNbinsX()+1;i++)
		{
		float bc=h->GetBinContent(i);
		float be=h->GetBinError(i);
		if(sumw2)
			h->SetBinContent(i, r->Gaus(bc,be) );
		else
			h->SetBinContent(i, r->Poisson(bc) );
		}
	
}

float GetMedian(std::vector<float> &v)
{
	sort(v.begin(),v.end());
	int n=int(v.size()); //start from 0
	if( (n&1)==0 )//even
		{
		return (v[n/2]+v[n/2-1])/2.;
		}
	else  //odd
		return v[n/2];
}
float GetMean(std::vector<float> &v){
	float S=0;
	int n=int(v.size()); //start from 0
	for(int i=0;i<n;++i)
		S+=v[i];
	return S/n;
	}
float GetRMS(std::vector<float> &v){
	float S=0;
	float m=GetMean(v);
	int n=int(v.size()); 
	for(int i=0;i<n;++i)
		S+=(v[i]-m)*(v[i]-m);
	return sqrt(S/(n-1));
}

float GetCI(std::vector<float> &v,std::pair<float,float>&r,float Q=.68){
	sort(v.begin(),v.end());
	int n=int(v.size()); 
	int m=ceil(n*Q);
	//Look for m consecutive bin such that the distance covered is minima
	vector<float> d;
	int min=0;
	for(int i=0;i<n-m;i++)
		{
		d.push_back(v[i+m]-v[i]);
		if(d[i]<d[min]) min=i;
		}
	r.first=v[min];
	r.second=v[min+m];
	return (r.second-r.first)/2.;
}


float toy(TH1F*h, TH1F* sig, TH1F* bkg,int nToys=100,TRandom *random=NULL)
{
vector<float> r; //result
	if(random==NULL){
			long long seed=(unsigned)time(NULL); 
			random=new TRandom3((unsigned)seed);
			printf("Seed=%lld",seed);
			}
		
	for(int iToy=0;iToy<nToys;++iToy){
	TH1F *h1=(TH1F*)h->Clone("tmp_h");
	TH1F *s1=(TH1F*)sig->Clone("tmp_s");
	TH1F *b1=(TH1F*)sig->Clone("tmp_b");
	
	RandomVar(h1,random,0);//poisson
	RandomVar(s1,random,0);//poisson
	RandomVar(b1,random,0);//poisson
	
	float a= fit(h1,s1,b1);
	
	r.push_back(a);
		
	h1->Delete();
	s1->Delete();
	b1->Delete();	
	}
	return  GetRMS(r);
	pair<float,float> b; //store low-hi for asymmetric
	return  GetCI(r,b,0.68);
}


}; //namespace TOYS
