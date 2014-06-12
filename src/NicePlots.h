#include "TH1F.h"
#include "TH1D.h"
#include "TCanvas.h"
//#include "TMathText.h"
#include "TLatex.h"
#include "TLegend.h"
#include "TStyle.h"

#include <iostream>
#include <vector>
#include <map>

using namespace std;

//       pattern_number = ijk      (FillStyle = 3ijk)
// 
//      i (1-9) : specify the space between each hatch
//                1 = 1/2mm  9 = 6mm
// 
//      j (0-9) : specify angle between 0 and 90 degrees
//                0 = 0
//                1 = 10
//                2 = 20
//                3 = 30
//                4 = 45
//                5 = Not drawn
//                6 = 60
//                7 = 70
//                8 = 80
//                9 = 90
//  
//      k (0-9) : specify angle between 90 and 180 degrees
//                0 = 180
//                1 = 170
//                2 = 160
//                3 = 150
//                4 = 135
//                5 = Not drawn
//                6 = 120
//                7 = 110
//                8 = 100
//                9 = 90

namespace NicePlots
{

const Int_t mcColors[]={kBlue+2,kRed,kGreen+2,kOrange+2,38,kYellow};
const Int_t mcStyles[]={1,2,3,1,2,3};
//                                                 \/ Scale and pdf
const Int_t mcErrColors[]={kBlue+2,kRed,kGreen+2,kMagenta+2,kGreen+2,kOrange};
const Int_t mcErrStyles[]={3002,3003,3017,3254,3445,3644};
//                                          /\ Scale and pdf
//17-18 == 04 05 

class NicePlotsBase; // base Class everyone inheriths here if possible
class SingleUpperPlot; // Z or sigle G plots
class SingleLowerPlot ;
class SingleRatioPlot ; // ratio
class SingleRatioLowerPlot ;

TH1D* NiceRange(TH1*H,pair<double,double> Range, double f1,double f2);
};

class NicePlots::NicePlotsBase
{

public: 
	NicePlotsBase();
	virtual TCanvas * Draw();
	virtual TCanvas * DrawSeparateLine(); //intended for ratio to draw separetely the mc/data plots
	virtual TCanvas * DrawCanvas(); //draw the canvas and set the actual size
	virtual void DrawCMS();
	virtual void DrawLegend();
	virtual void SetDataStyle();
	virtual void SetSystStyle();
	virtual void SetMCStyle();
	virtual void SetMCErrStyle();
	virtual void SetHeader(char type='G',int nJets=1,int Ht=0);

	//utility
	TH1D* data;
	TH1D* syst;
	TLegend* legend;
	int autoLegend; // change X,Y according to number of entries
	vector<TH1D*> mc;
	vector<TH1D*> mcErr; // bands
	vector<int> mcErrAssociation;
	vector<string> mcLabels;
	vector<string> mcLabelsErr;
	pair<double,double>RangeFactors;
	pair<double,double>Range;
	pair<double,double>RangeY;
	string xtitle;
	string ytitle;
	
	pair<double,double> legendPos1;
	pair<double,double> legendPos2;
	string legendHeader;
	string extraText;
	pair<double,double> cmsPosition;
	pair<double,double> lumiPosition;
	float cmsSpace;//space between CMS, and preliminary
	int drawBands;
	int drawLumi;
};

class NicePlots::SingleUpperPlot : public NicePlots::NicePlotsBase {
	public:
	SingleUpperPlot();
};

class NicePlots::SingleLowerPlot : public NicePlots::NicePlotsBase {
	public:
	//virtual TCanvas * Draw();
	virtual TCanvas * DrawCanvas();
	virtual void DrawLegend();
	virtual void DrawCMS();
	virtual void SetDataStyle();
	SingleLowerPlot();
};

class NicePlots::SingleRatioPlot : public NicePlots::NicePlotsBase{
	public:
	virtual TCanvas * DrawCanvas();
	virtual void SetDataStyle();
	SingleRatioPlot();
	//virtual TCanvas * Draw();
};

//class NicePlots::SingleRatioLowerPlot : public NicePlots::SingleRatioPlot {
class NicePlots::SingleRatioLowerPlot : public NicePlots::NicePlotsBase {
	public:
	virtual TCanvas * DrawCanvas();
	SingleRatioLowerPlot();
	virtual void DrawLegend();
	virtual void DrawCMS();
	virtual void SetDataStyle();
};

