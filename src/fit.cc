
#include "TH1F.h"
#include "TFile.h"
#include "TFitResultPtr.h"
#include "TFitResult.h"
#include "TLatex.h"
#include "TText.h"
#include "TROOT.h"
#include "TDirectory.h"

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


using namespace std;
using namespace RooFit;


float FIT::fit(TObject *o, TH1F* sig, TH1F* bkg,const char *fileName,const char *name)
{
	bool binned=false;
	if(o->InheritsFrom("TH1") ) binned=true;
	else if (o->InheritsFrom("TTree")) binned=false;
	else printf("ERROR NO TREE OR TH1F provided\n");
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
	//bkg fit to Landau
	vector<float> bkgPar; bkgPar.resize(10);
	TFitResultPtr bkgR=bkg->Fit("landau","LS");
	bkgPar[0]=bkgR->Parameter(0);
	bkgPar[1]=bkgR->Parameter(1);
	bkgPar[2]=bkgR->Parameter(2);
	cout<<"--> LANDAU PARS "<<bkgPar[0]<<" "<<bkgPar[1]<<" " <<bkgPar[2]<<endl;
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

		if(fracEstimator>1.0 || fracEstimator<0)fracEstimator=0.8;
		cout<<"---> @@ Fraction Estimation"<<frac1<<" "<<frac2<<": "<<fracEstimator <<" @@"<<endl;
		}

	//create real var
	RooRealVar f("f","fraction",fracEstimator,0.60,1.) ;
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
		RooDataHist HistToFit("hist","hist",x,h); 
		//r = PdfModel.fitTo(HistToFit,SumW2Error(kTRUE),Save());
		r = PdfModel.fitTo(HistToFit,Save(),SumW2Error(kFALSE));
		//if(r->status() != 0 ) { //bad fit
		//		cout<<"---> !!! BAD FIT - PASS TO CHI2!!!"<<endl;
		//		r=PdfModel.chi2FitTo(HistToFit,SumW2Error(kTRUE),Save());
		//		if(r->status() != 0 ) cout<<"---> !!! STILL BAD. DON'T DO ANYTHING!!!!" <<endl;
		//		}
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
	
	TText* txt = new TText(.2,.85,Form("Fraction=%.1f\%",f.getVal()*100)) ;
  	txt->SetTextSize(0.04) ;
  	txt->SetTextColor(kBlack) ;
	txt->SetNDC();
  	frame->addObject(txt) ;	
	
	  // Access basic information
	  cout << "EDM = " << r->edm() << endl ;
	  cout << "-log(L) at minimum = " << r->minNll() << endl ;
	  cout << "Error = "<<f.getError()<<endl;
	  cout << "--> FractionFitted = "<<f.getVal()<<endl;
	
	//
	if(name[0]!='\0')
		{
		TFile file(fileName,"UPDATE") ;
		//r->Write(name);
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

void TOYS::RandomVar(TH1F*h,TRandom *r,int sumw2){
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

float TOYS::GetMedian(std::vector<float> &v)
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
float TOYS::GetMean(std::vector<float> &v){
	float S=0;
	int n=int(v.size()); //start from 0
	if(n==0)return -1;
	for(int i=0;i<n;++i)
		S+=v[i];
	return S/n;
	}
float TOYS::GetRMS(std::vector<float> &v){
	float S=0;
	float m=GetMean(v);
	int n=int(v.size()); 
	if(n<=1) return -1;
	for(int i=0;i<n;++i)
		S+=(v[i]-m)*(v[i]-m);
	return sqrt(S/(n-1));
}

float TOYS::GetCI(std::vector<float> &v,std::pair<float,float>&r,float Q){
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


float TOYS::toy(TH1F*h, TH1F* sig, TH1F* bkg,int nToys,TRandom *random)
{
vector<float> r; //result
	if(random==NULL){
			long long seed=(unsigned)time(NULL); 
			random=new TRandom3((unsigned)seed);
			printf("Seed=%lld\n",seed);
			}
		
	for(int iToy=0;iToy<nToys;++iToy){
	TH1F *h1=(TH1F*)h->Clone("tmp_h");
	TH1F *s1=(TH1F*)sig->Clone("tmp_s");
	TH1F *b1=(TH1F*)sig->Clone("tmp_b");
	
	RandomVar(h1,random,0);//poisson
	RandomVar(s1,random,0);//poisson
	RandomVar(b1,random,0);//poisson
	//RandomVar(h1,random,1);//gaus
	//RandomVar(s1,random,1);//gaus
	//RandomVar(b1,random,1);//gaus
	
	if(h1->Integral()==0 || s1->Integral()==0 || b1->Integral()==0)
		{cout<<"SKIP TOY EVENT: INTEGRAL=0"<<endl;continue;}
	
	float a= FIT::fit(h1,s1,b1);
	
	r.push_back(a);
		
	h1->Delete();
	s1->Delete();
	b1->Delete();	
	}
	return  GetRMS(r);
	pair<float,float> b; //store low-hi for asymmetric
	return  GetCI(r,b,0.68);
}


//}; //namespace TOYS
