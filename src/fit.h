
#include "TH1D.h"
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


#include <map>
#include <string>
using namespace std;
using namespace RooFit;

class FIT{
public:
static float fit(TObject *o, TH1D* sig, TH1D* bkg,const char *fileName="",const char *name="",map<string,float> *pars=NULL); //o=TH1D or TTre to be fitted , fileName=.root , pars: push back extra floats
};

#include "TRandom3.h"
#include "TRandom.h"
#include "time.h"
#include <vector>
#include <algorithm>

//namespace TOYS {
class TOYS{
public:

static void RandomVar(TH1D*h,TRandom *r,int sumw2=0);
//static float GetMedian(std::vector<float> &v);
//static float GetMean(std::vector<float> &v);
//static float GetRMS(std::vector<float> &v);
//static float GetCI(std::vector<float> &v,std::pair<float,float>&r,float Q=.68);
static map<string,float> toy(TH1D*h, TH1D* sig, TH1D* bkg,int nToys=100,TRandom *random=NULL,const char *fileName=""); //fileName will save output to the toys


};//END OF TOYS
