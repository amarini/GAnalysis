
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

class FIT{
public:
static float fit(TObject *o, TH1F* sig, TH1F* bkg,const char *fileName="",const char *name="",vector<float> *pars=NULL); //o=TH1F or TTre to be fitted , fileName=.root , pars: push back extra floats
};

#include "TRandom3.h"
#include "TRandom.h"
#include "time.h"
#include <vector>
#include <algorithm>

//namespace TOYS {
class TOYS{
public:

static void RandomVar(TH1F*h,TRandom *r,int sumw2=0);
//static float GetMedian(std::vector<float> &v);
//static float GetMean(std::vector<float> &v);
//static float GetRMS(std::vector<float> &v);
//static float GetCI(std::vector<float> &v,std::pair<float,float>&r,float Q=.68);
static float toy(TH1F*h, TH1F* sig, TH1F* bkg,int nToys=100,TRandom *random=NULL,const char *fileName=""); //fileName will save output to the toys


};//END OF TOYS
