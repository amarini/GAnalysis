#include "TH1F.h"
#include "TH1D.h"
#include "TCanvas.h"
#include "TMathText.h"
#include "TLatex.h"
#include "TLegend.h"

#include <iostream>
#include <vector>
#include <map>

using namespace std;

namespace NicePlots
{

const Int_t mcColors[]={kBlue+2,kRed,kGreen+2};
const Int_t mcStyles[]={1,2,3};

class NicePlotsBase;
class SingleUpperPlot;
class SingleLowerPlot ;
class SingleRatioPlot ;
class SingleRatioLowerPlot ;

TH1D* NiceRange(TH1*H,pair<double,double> Range, double f1,double f2);
};

class NicePlots::NicePlotsBase
{

public: 
	NicePlotsBase();
	virtual TCanvas * Draw();
	virtual TCanvas * DrawCanvas();
	virtual void DrawCMS();
	virtual void DrawLegend();
	virtual void SetDataStyle();
	virtual void SetSystStyle();
	virtual void SetMCStyle();
	virtual void SetHeader(char type='G',int nJets=1,int Ht=0);

	//utility
	TH1D* data;
	TH1D* syst;
	TLegend* legend;
	int autoLegend; // change X,Y according to number of entries
	vector<TH1D*> mc;
	vector<string> mcLabels;
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
