#define NICEPLOTS_CXX

#include "NicePlots.h"
//#include "TMathText.h"

using NicePlots::NicePlotsBase;
using NicePlots::SingleLowerPlot;
using NicePlots::SingleUpperPlot;
using NicePlots::SingleRatioPlot;
using NicePlots::SingleRatioLowerPlot;
using NicePlots::NiceRange;

TCanvas* NicePlotsBase::DrawCanvas(){

TCanvas *c=new TCanvas("c","c",600,500);
                c->SetTopMargin(0.10);
                c->SetRightMargin(0.03);
                c->SetLogy();
return c;
}

TCanvas * NicePlotsBase::Draw(){
	//cout<< "NiceRangeFactors"<<RangeFactors.first<<" "<<RangeFactors.second<<endl;
	TCanvas *c=DrawCanvas();
	SetSystStyle();
	SetMCStyle();
	SetDataStyle();
	TH1D *data2=NiceRange(data,Range,RangeFactors.first,RangeFactors.second);
	TH1D *syst2=NiceRange(syst,Range,RangeFactors.first,RangeFactors.second);

	int nRowLeg=mc.size()+1+1;//data/syst/header
	if(legendHeader != "") nRowLeg += 1;
	float unitLeg=(legendPos2.second-legendPos1.second)/3.;
	if (autoLegend == 1)
	{
		if (legendPos1.second > 0.5) autoLegend=2;
		if (legendPos1.second <= 0.5) autoLegend=3;
	}

	if (autoLegend == 2){
		float y1=legendPos2.second - unitLeg*nRowLeg;
	        float y2=legendPos2.second;
		legend=new TLegend(legendPos1.first,y1,legendPos2.first,y2);
	}
	else if (autoLegend==3){ // down fixed
		float y1=legendPos1.second ;
	        float y2=legendPos1.second + unitLeg*nRowLeg; 
		legend=new TLegend(legendPos1.first,y1,legendPos2.first,y2);
		}
	else legend=new TLegend(legendPos1.first,legendPos1.second,legendPos2.first,legendPos2.second);
	legend->SetTextFont(43);
	legend->SetTextSize(16);

	cout<<"Setting Legend Header "<<legendHeader<<endl;
	legend->SetHeader(legendHeader.c_str());

	data2->Draw("P AXIS");
	data2->GetXaxis()->SetRangeUser(Range.first,Range.second);
	if (RangeY.first >-99 && RangeY.second>-99)
		data2->GetYaxis()->SetRangeUser(RangeY.first,RangeY.second);
	legend->AddEntry(data2,"data","P");
	syst2->Draw("E2 SAME");
	legend->AddEntry(syst2,"stat+syst","F");

	for ( int iMC=0;iMC< int(mc.size()) ;iMC++){
        	TH1D* mc2 = NiceRange(mc[iMC],Range,RangeFactors.first,RangeFactors.second);
		mc2->Draw("HIST SAME ][");
		//legend->AddEntry(mc2,mcLabels[iMC].c_str(),"F");
		legend->AddEntry(mc2,mcLabels[iMC].c_str(),"L");
		}
	DrawLegend();
	DrawCMS();
	//redraw axis and data points
        data2->Draw("AXIS X+ Y+ SAME");
        data2->Draw("AXIS SAME");
        data2->Draw("P SAME");
	return c;
}

void NicePlotsBase::DrawLegend(){
        legend->SetFillStyle(0);
        legend->SetBorderSize(0);
	legend->Draw();
}

void NicePlotsBase::DrawCMS()
{
	TLatex *l=new TLatex();
	l->SetNDC();
	l->SetTextFont(43);
	l->SetTextSize(18);
	l->SetTextAlign(22);
	l->DrawLatex(cmsPosition.first,cmsPosition.second,"CMS Preliminary, #sqrt{s}=8TeV, L=19.7fb^{-1}");
//	l->SetTextFont(43);
//	l->SetTextSize(18);
//	l->DrawLatex(cmsPosition.first,cmsPosition.second-0.04,"#sqrt{s} = 8TeV, L=19.7fb^{-1}");
	l->SetTextSize(15);
	if( extraText != "")
		l->DrawLatex(cmsPosition.first-0.10,cmsPosition.second-0.08,extraText.c_str());
	//TMathText*m=new TMathText();
	//m->SetTextFont(43);
	//m->SetTextSize(20);
	//m->SetTextAlign(22);
	//m->DrawMathText(cmsPosition.first,cmsPosition.second-0.04,"\\sqrt{s} = 8TeV, \\mathcal{L=19.7fb^{-1}}");

	return;
}

void  NicePlotsBase::SetDataStyle()
{
	data->SetMarkerStyle(20);
	data->SetMarkerColor(kBlack);
	data->SetLineColor(kBlack);
	data->SetLineStyle(1);
	data->SetLineWidth(1);
        data->GetXaxis()->SetRangeUser(Range.first,Range.second);
        data->GetXaxis()->SetNoExponent();
        data->GetXaxis()->SetMoreLogLabels();

	data->GetXaxis()->SetTitle(xtitle.c_str());
	data->GetYaxis()->SetTitle(ytitle.c_str());

        data->GetYaxis()->SetTitleOffset(0.9);
        data->GetXaxis()->SetTitleOffset(0.9);
        data->GetXaxis()->SetTitleFont(43);
        data->GetYaxis()->SetTitleFont(43);
        data->GetXaxis()->SetTitleSize(22);
        data->GetYaxis()->SetTitleSize(22);
        data->GetXaxis()->SetLabelFont(43);
        data->GetYaxis()->SetLabelFont(43);
        data->GetXaxis()->SetLabelSize(16);
        data->GetYaxis()->SetLabelSize(16);
	return ;
}
void  NicePlotsBase::SetSystStyle(){
	syst->SetMarkerStyle(0);
	syst->SetMarkerColor(kOrange-4);
	syst->SetFillColor(kOrange-4);
	syst->SetLineColor(kOrange-4);
	syst->SetLineStyle(1);
	syst->SetLineWidth(2);
	syst->SetFillStyle(3001);
        syst->GetXaxis()->SetRangeUser(Range.first,Range.second);
	return ;
}
void  NicePlotsBase::SetMCStyle()
{
	for ( int iMC=0;iMC< int(mc.size()) ;iMC++)
	{
              mc[iMC]->GetXaxis()->SetRangeUser(Range.first,Range.second);
              mc[iMC]->SetLineColor(mcColors[iMC]);
              mc[iMC]->SetLineWidth(2);
              mc[iMC]->SetLineStyle(mcStyles[iMC]);
	}
	return;
}

void NicePlotsBase::SetHeader(char type,int nJets,int Ht)
{
	switch (type)
	{
	case 'G' :
	case 'g' :
		legendHeader=""	;
		break;
	case 'Z' : 
	case 'z' : 
//legendHeader = "Z/\\gamma^{*}\\rightarrow \\ell^{+}\\ell^{-}, " ;
		legendHeader = "Z/#gamma^{*} #rightarrow l^{+}l^{-}, " ;
		break;
	default: break;
	}
legendHeader += Form("N_{jets} #geq %d",nJets);
if (Ht>0)
	legendHeader += Form(", H_{T} #geq %d GeV",Ht);
return; 
}

NicePlotsBase::NicePlotsBase()
{
xtitle="p_{T}^{#gamma} [GeV]";
ytitle="d#sigma/dp_{T} [fb GeV^{-1}]";
Range=pair<double,double>(99.99,1093);
RangeY=pair<double,double>(-100.,-100.);
legendPos1=pair<double,double>(.70,.70);
legendPos2=pair<double,double>(.89,.89);
legendHeader="";
cmsPosition=pair<double,double>(.45,.94);
autoLegend=1;
}

//---------------------- LOWER PLOTS-------------

TCanvas* SingleLowerPlot::DrawCanvas(){
		TCanvas *c=new TCanvas("c","c",600,300);
                c->SetTopMargin(0.02);
                c->SetRightMargin(0.03);
                c->SetBottomMargin(0.2);
               // c->SetLogy();
return c;
}

SingleLowerPlot::SingleLowerPlot() : NicePlotsBase(){
	ytitle="MC/Data";
	RangeY.first=0.5;
	RangeY.second=1.5;
}

void SingleLowerPlot::DrawLegend(){
	return; //no legend
}

void SingleLowerPlot::SetDataStyle(){
	NicePlotsBase::SetDataStyle();
		data->GetYaxis()->SetTitleOffset(0.5);
		data->GetYaxis()->SetTitle("MC/Data");
		data->GetYaxis()->SetNdivisions(510);
		data->GetYaxis()->SetDecimals();
		data->GetYaxis()->SetRangeUser(0.5,1.5);
	return; //no legend
}

void SingleLowerPlot::DrawCMS(){
	return; //no cms
}

//---------------------- RATIO PLOTS-------------
SingleRatioPlot::SingleRatioPlot() : NicePlotsBase(){
cmsPosition.first=0.45;
cmsPosition.second=0.94;
legendPos1=pair<double,double>(.70,.75);
legendPos2=pair<double,double>(.97,.94);
}
TCanvas* SingleRatioPlot::DrawCanvas(){

TCanvas *c=new TCanvas("c","c",600,500);
                c->SetLeftMargin(0.18);
                c->SetTopMargin(0.10);
                c->SetBottomMargin(0.10);
                c->SetRightMargin(0.02);
return c;
}
void SingleRatioPlot::SetDataStyle(){
	NicePlotsBase::SetDataStyle();
		data->GetYaxis()->SetTitleOffset(1.3);
		data->GetXaxis()->SetTitleOffset(0.8);
		//data->GetYaxis()->SetTitleSize(22);
		data->GetYaxis()->SetDecimals();
}
//---------------------- UPPER PLOTS-------------
SingleUpperPlot::SingleUpperPlot() : NicePlotsBase(){
}

//---------------------- RATIO LOWER PLOTS-------------
SingleRatioLowerPlot::SingleRatioLowerPlot() : SingleRatioPlot(){
	//constructor
}
TCanvas* SingleRatioLowerPlot::DrawCanvas(){

TCanvas *c=new TCanvas("c","c",600,300);
                c->SetLeftMargin(0.18);
                c->SetTopMargin(0.10);
                c->SetBottomMargin(0.10);
                c->SetRightMargin(0.02);
return c;
}
void SingleRatioLowerPlot::DrawLegend(){
	return; //no legend
}
void SingleRatioLowerPlot::DrawCMS(){
	TLatex *l=new TLatex();
	l->SetNDC();
	l->SetTextFont(43);
	l->SetTextSize(15);
	if( extraText != "")
		l->DrawLatex(cmsPosition.first-0.10,cmsPosition.second-0.08,extraText.c_str());
	return; //only extraText
}
void SingleRatioLowerPlot::SetDataStyle(){
	NicePlotsBase::SetDataStyle();
		data->GetYaxis()->SetTitleOffset(0.5);
		data->GetYaxis()->SetTitle("MC/Data");
		data->GetYaxis()->SetNdivisions(510);
		data->GetYaxis()->SetDecimals();
		data->GetYaxis()->SetRangeUser(0.5,1.5);
	return; 
}




//-----------     GENERAL FUNCTIONS --
TH1D* NicePlots::NiceRange(TH1*h,pair<double,double> Range, double f1=0.2,double f2=0.2){
	//equivalent of python one
        double Bins[100];
        int nBins=0;
        vector<double> l;
	int lastBin=0;
        for(int iBin=1; iBin <= h->GetNbinsX()+1;iBin++) // bin boundaries
                if ( Range.first <= h->GetBinLowEdge(iBin) && h->GetBinLowEdge(iBin) <= Range.second)
		{
			if (l.empty()){
				double l0=h->GetBinLowEdge(iBin);
				double l1=h->GetBinLowEdge(iBin+1);
				l.push_back(l0-f1*(l1-l0));
			}
                        l.push_back( h->GetBinLowEdge(iBin) );
			lastBin=iBin;
		}
	double l0=h->GetBinLowEdge(lastBin-1);
	double l1=h->GetBinLowEdge(lastBin);
        l.push_back( l1 + (l1-l0) * f2 );
	lastBin=h->GetNbinsX();
        // prepare ROOT structure
        for ( int bin =0 ; bin < int(l.size()) ; bin++)
			{
				//printf("Bin Boundary %lf\n",l[bin]);
                        Bins[ nBins ] = l[bin];
                        nBins += 1;

			}
        nBins -= 1;
	//create target
        TH1D *h2 = new TH1D( Form( "%s_%s",h->GetName(),"nicerange"),h->GetTitle(),nBins,Bins);
        for ( int iBin=1; iBin <= lastBin;iBin++)
                if (Range.first<h->GetBinCenter(iBin) && h->GetBinCenter(iBin) < Range.second)
		{
                        h2->SetBinContent(h2->FindBin(h->GetBinCenter(iBin)), h->GetBinContent( iBin  ) );
                        h2->SetBinError(h2->FindBin(h->GetBinCenter(iBin)), h->GetBinError( iBin  ) );
		}

        h2->SetLineColor( h->GetLineColor());
        h2->SetLineStyle( h->GetLineStyle());
        h2->SetLineWidth( h->GetLineWidth());
        h2->SetFillColor( h->GetFillColor());
        h2->SetFillStyle( h->GetFillStyle());
        h2->SetMarkerColor( h->GetMarkerColor());
        h2->SetMarkerStyle( h->GetMarkerStyle());
        h2->GetXaxis()->SetTitle(h->GetXaxis()->GetTitle());
        h2->GetYaxis()->SetTitle(h->GetYaxis()->GetTitle());
	h2->GetXaxis()->SetRangeUser(Range.first,Range.second);

        h2->GetXaxis()->SetNoExponent(     h->GetXaxis()->GetNoExponent()      );
        h2->GetXaxis()->SetMoreLogLabels(  h->GetXaxis()->GetMoreLogLabels()   );

        h2->GetYaxis()->SetTitleOffset(   h->GetYaxis()->GetTitleOffset() );
        h2->GetXaxis()->SetTitleOffset(   h->GetXaxis()->GetTitleOffset() );
        h2->GetXaxis()->SetTitleFont(     h->GetXaxis()->GetTitleFont()   );
        h2->GetYaxis()->SetTitleFont(     h->GetYaxis()->GetTitleFont()   );
        h2->GetXaxis()->SetTitleSize(     h->GetXaxis()->GetTitleSize()   );
        h2->GetYaxis()->SetTitleSize(     h->GetYaxis()->GetTitleSize()   );
        h2->GetXaxis()->SetLabelFont(     h->GetXaxis()->GetLabelFont()   );
        h2->GetYaxis()->SetLabelFont(     h->GetYaxis()->GetLabelFont()   );
        h2->GetXaxis()->SetLabelSize(     h->GetXaxis()->GetLabelSize()   );
        h2->GetYaxis()->SetLabelSize(     h->GetYaxis()->GetLabelSize()   );

        h2->GetXaxis()->SetDecimals(     h->GetXaxis()->GetDecimals()   );
        h2->GetYaxis()->SetDecimals(     h->GetYaxis()->GetDecimals()   );
	
//	h2->GetXaxis()->SetRangeUser( h->GetXaxis()->GetBinCenter(h->GetXaxis()->GetFirst()), h->GetXaxis()->GetBinCenter( h->GetXaxis()->GetLast())  );
//	h2->GetYaxis()->SetRangeUser( h->GetYaxis()->GetBinCenter(h->GetYaxis()->GetFirst()), h->GetYaxis()->GetBinCenter( h->GetYaxis()->GetLast())  );
        return h2;

}
