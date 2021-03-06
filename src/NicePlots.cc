#define NICEPLOTS_CXX
#define DEBUG 1

#include "NicePlots.h"
//#include "TMathText.h"

using NicePlots::NicePlotsBase;
using NicePlots::SingleLowerPlot;
using NicePlots::SingleUpperPlot;
using NicePlots::SingleRatioPlot;
using NicePlots::SingleRatioLowerPlot;
using NicePlots::NiceRange;

TCanvas* NicePlotsBase::DrawCanvas(){
if (DEBUG) cout<< "Draw BasePlot Canvas "<<
	"T0.1 R0.03 LY"<<endl;
TCanvas *c=new TCanvas("c","c",600,500);
                c->SetTopMargin(0.10);
                c->SetRightMargin(0.03);
                c->SetLogy();
return c;
}

TCanvas *NicePlotsBase::DrawStandaloneLegend()
{

	TCanvas *c=new TCanvas("legendCanvas","legendCanvas",300,300);
	legend->Draw();
	legend->SetHeader("Legend");
	legend->SetX1(0.1);
	legend->SetX2(0.9);
	legend->SetY1(0.1);
	legend->SetY2(0.9);
        legend->SetFillStyle(0);
        legend->SetBorderSize(1);
	legend->Draw();

	TLatex *l=new TLatex();
	l->SetNDC();
	//l->SetTextFont(63); //helvetica Bold
	//l->SetTextSize(24);  // ratio CMS/Preliminary Size is 0.76
	//l->SetTextAlign(11);
	//l->DrawLatex(0.15,.92,"CMS");
	//l->SetText(0.15,0.92,"CMS"); // this is not draw it is used for figure out the dimensions
	//unsigned int w,h;
	//l->GetBoundingBox(w,h);
	//unsigned int ww=gPad->GetWw();
	//unsigned int wh=gPad->GetWh();

	//l->SetTextFont(53);//helvetica italics
	//l->SetTextSize(18);
	//l->SetTextAlign(11);
	//l->DrawLatex(0.15+ float(w)/ww + 0.04,0.92,"Preliminary");
	l->SetTextFont(43);
	l->SetTextSize(24);
	l->SetTextAlign(11);
	l->DrawLatex(.15,.92,Form("#bf{CMS} #scale[0.75]{#it{%s}}",cmsPreliminary.c_str()));

	c->Update();
return c;
}

TCanvas * NicePlotsBase::Draw(){
	//cout<< "NiceRangeFactors"<<RangeFactors.first<<" "<<RangeFactors.second<<endl;
	if (RangeY.first==0.5) RangeY.first+=0.0001;
	if (RangeY.second==1.5) RangeY.second-=0.0001;
	TCanvas *c=DrawCanvas();
	cout<<"Setting Canvas Size to "<< c->GetWw() <<" "<<c->GetWh() <<endl;
	c->SetCanvasSize(c->GetWw(),c->GetWh());
	SetSystStyle();
	SetMCStyle();
	SetMCErrStyle();
	SetDataStyle();
	TH1D *data2=NiceRange(data,Range,RangeFactors.first,RangeFactors.second);
	TH1D *syst2=NiceRange(syst,Range,RangeFactors.first,RangeFactors.second);

	int nRowLeg=mc.size()+1+1;//data/syst/header
	if(legendHeader != "") nRowLeg += 1;
	float unitLeg=(legendPos2.second-legendPos1.second)/3.;
	if (autoLegend == 1) // change legend in order to preserve size
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

	cout<<"Data Drawing "<<endl;
	data2->Draw("P AXIS");
	data2->GetXaxis()->SetRangeUser(Range.first,Range.second);
	if (RangeY.first >-99 && RangeY.second>-99)
		data2->GetYaxis()->SetRangeUser(RangeY.first,RangeY.second);
	legend->AddEntry(data2,"data","P");
	syst2->Draw("E2 SAME");
	legend->AddEntry(syst2,"stat+syst","F");
	
	//Draw bands before
	cout<<"Bands Drawing "<<endl;
	if(drawBands)
	for (int iMcErr=0;iMcErr<mcErr.size();iMcErr++){
		//
		cout<<" --> Drawing Band for "<< mcLabelsErr[iMcErr] <<endl;
		TH1D* mcErr2=NiceRange( mcErr[iMcErr],Range,RangeFactors.first,RangeFactors.second);
		mcErr2->Draw("E2 SAME");
		//if( mcLabelsErr[iMcErr]!="")legend->AddEntry(mcErr2,mcLabelsErr[iMcErr].c_str(),"F");
		//DEBUG
			int iBin=mcErr2->FindBin(600);
			cout<<" --> ERROR "<<mcErr2->GetName() <<" ON BIN 600:"<<mcErr2->GetBinError(iBin)/mcErr2->GetBinContent(iBin)<<endl;
			cout<<" --> ERROR "<<mcErr2->GetName() <<" ON BIN 600: E,C"<<mcErr2->GetBinError(iBin)<<","<<mcErr2->GetBinContent(iBin)<<endl;
		}

	cout<<"MC Drawing "<<endl;
	//for ( int iMC=0;iMC< int(mc.size()) ;iMC++){
	for ( int iMC=int(mc.size())-1;iMC>=0 ;iMC--){
		if(!isMcToDraw(iMC)) continue;
        	TH1D* mc2 = NiceRange(mc[iMC],Range,RangeFactors.first,RangeFactors.second);
		mc2->Draw("HIST SAME ][");
		//legend->AddEntry(mc2,mcLabels[iMC].c_str(),"F");
		//legend->AddEntry(mc2,mcLabels[iMC].c_str(),"L");
		}
	//--localLegend
			float x1=c->GetLeftMargin()+0.02;
			float y1=c->GetBottomMargin()+0.02;
			float x2=x1+.5;
			if( mc.size() ==1) x2=x1+.3; 
			float y2=y1+.1;
			
			int bin=1;
			if(Range.first>-90)bin=syst2->FindBin(Range.first+0.001);
			if( (syst2->GetBinContent(bin)-syst2->GetBinError(bin) < RangeY.first + 0.2) || ( mc.size() > 0 && mc[0]->GetBinContent(bin)-mc[0]->GetBinError(bin) < RangeY.first + 0.2 ) )
				{x1+=0.2;x2+=.2;}
			TLegend *localLegend=new TLegend(x1,y1,x2,y2);
			localLegend->SetBorderSize(0);
			localLegend->SetFillStyle(0);
			localLegend->SetNColumns(2);
	//Add legend
	cout<<"Make MC Legend"<<endl;
	AutoAssociation();
	for ( int iMC=int(mc.size())-1;iMC>=0 ;iMC--){
		if(!isMcToDraw(iMC))continue;
		map<int,int>::const_iterator mcAss=mcAssociation.find(iMC);
		bool isAss=false;
		if (mcAss != mcAssociation.end() ) isAss=true;
		if (isAss) continue;
		legend->AddEntry(mc[iMC],mcLabels[iMC].c_str(),"L");
	}
	//now draw ass mc with right order
	//	for ( int iMC=int(mc.size())-1;iMC>=0 ;iMC--){
	for ( int iMC=0;iMC< int(mc.size()) ;iMC++){
		if(!isMcToDraw(iMC))continue;
		map<int,int>::const_iterator mcAss=mcAssociation.find(iMC);
		bool isAss=false;
		if (mcAss != mcAssociation.end() ) isAss=true;
		if (!isAss) continue;
		legend->AddEntry(mc[iMC],mcLabels[iMC].c_str(),"L");
	}
	//Bands legends are the last

	cout<<"Auto Association "<<endl;
	AutoAssociation();
	cout<<"Bands Errors in legend "<<endl;
	if(drawBands )
	for (int iMcErr=0;iMcErr<mcErr.size();iMcErr++){
		// figure out if there is an association - for ErrorBandsLegend only
		cout<<"MC Err "<<iMcErr<<endl;
		if (mcErrAssociation.size()< iMcErr) continue;
		int mc_ln  = mcErrAssociation[iMcErr];//line number
		cout<<"MC ln "<<mc_ln<<endl;
		bool isAssMC=false;
		map<int,int>::const_iterator mcA=mcAssociation.find(mc_ln);
		if( mcA!=mcAssociation.end() ){isAssMC=true;}
		if (isAssMC) continue;
		
		cout<<"Adding mcErrorBands "<<mcLabelsErr[iMcErr]<<" to the legend "<< " mc_ln "<<mc_ln<<" isAssMC="<<isAssMC<<endl;
		if( mcLabelsErr[iMcErr]!="")legend->AddEntry(mcErr[iMcErr],mcLabelsErr[iMcErr].c_str(),"F");
		if( mcLabelsErr[iMcErr]!="")localLegend->AddEntry(mcErr[iMcErr],mcLabelsErr[iMcErr].c_str(),"F");
		}
	cout<<"Draw legend "<<endl;
	DrawLegend();
	cout<<"Draw local legend "<<endl;
	if (data2->GetBinContent(1)==1 && data2->GetBinContent(2)==1) //???
		localLegend->Draw();
	cout<<"Draw CMS "<<endl;
	DrawCMS();
	//redraw axis and data points
	cout<<"Redraw Axis plots & co"<<endl;
	syst2->Draw("E2 SAME");
        data2->Draw("AXIS X+ Y+ SAME");
        data2->Draw("AXIS SAME");
        data2->Draw("P SAME");

	cout<<"Draw END "<<endl;
	return c;
}

bool NicePlotsBase::isMcToDraw(int i)
{
	if( (mcLabels[i].find("NNPDF") != string::npos )
	    || (mcLabels[i].find("CT10") != string::npos )
	  ) return false;
	else return true;
}

void NicePlotsBase::AutoAssociation(){
	int bh=-1;
	for(unsigned int i=0;i<mcLabels.size() ;i++)
	{
		if (mcLabels[i].find("BlackHat") != string::npos && mcLabels[i].find("NNPDF") == string::npos && (mcLabels[i].find("CT10") != string::npos ) ) 
		{
			bh=i;
			break;
		}
	
	}

	for(unsigned int i=0;i<mcLabels.size() ;i++)
	{
	if( (mcLabels[i].find("NNPDF") != string::npos )
	    || (mcLabels[i].find("CT10") != string::npos )
	  )
		mcAssociation[i]=2; //todo put here bh
	}
	return;
}

TCanvas *NicePlotsBase::DrawSeparateLine(){
	AutoAssociation();
	if (RangeY.first==0.5) RangeY.first+=0.0001;
	if (RangeY.second==1.5) RangeY.second-=0.0001;
	int nMC=mc.size() - mcAssociation.size();
	TCanvas *c=DrawCanvas();
	cout<<"Setting Canvas Size to "<< c->GetWw() <<" "<<c->GetWh()*nMC <<endl;
	c->SetCanvasSize(c->GetWw(),c->GetWh()*nMC);
	SetSystStyle();
	SetMCStyle();
	SetMCErrStyle();
	SetDataStyle();
	//DrawLegend() ; // no legend
	vector<TPad*> pads;
	vector<TLegend*> legs;
	float dY=1./(nMC+.6);

	for ( int iMC=0;iMC< int(mc.size()) ;iMC++){
		TH1D *data2=NiceRange(data,Range,RangeFactors.first,RangeFactors.second);
		TH1D *syst2=NiceRange(syst,Range,RangeFactors.first,RangeFactors.second);
		data2->SetName(Form("data_for_mc%d",iMC));
		syst2->SetName(Form("syst_for_mc%d",iMC));
		float X1=0.;
		float X2=1.;
		float Y1=dY*(iMC+0.3);
		if(iMC==0) //bottom
			Y1=0;
		float Y2=dY*(iMC+1+.3);
		if(iMC==nMC-1) //top
			Y2=1.;

		//draw the pad in the canvas
		bool isAssMC=false;
		map<int,int>::const_iterator mcA=mcAssociation.find(iMC);
		if( mcA==mcAssociation.end() ){
			TPad *p=new TPad(Form("p%d",iMC),"pad",X1,Y1,X2,Y2);
			pads.push_back(p);
			p->SetBottomMargin(0);
			p->SetTopMargin(0);
                	p->SetLeftMargin(c->GetLeftMargin());
                	p->SetRightMargin(c->GetRightMargin());

			if (iMC==nMC-1) //top
			{
				p->SetTopMargin(0.3);
			}
			if (iMC==0)//bottom
				p->SetBottomMargin(0.3);
			c->cd();
			p->Draw();
			p->cd();

			float x1=p->GetLeftMargin()+0.02;
			float y1=p->GetBottomMargin()+0.02;
			float x2=x1+.5;
			float y2=y1+.1;
			
			int bin=1;
			if(Range.first>-90)bin=syst2->FindBin(Range.first+0.001);
			if(syst2->GetBinContent(bin)-syst2->GetBinError(bin) < RangeY.first + 0.2 )
				{x1+=0.2;x2+=.2;}
			TLegend *localLegend=new TLegend(x1,y1,x2,y2);
			localLegend->SetBorderSize(0);
			localLegend->SetFillStyle(0);
			localLegend->SetNColumns(2);
			legs.push_back(localLegend);	
		}
		else {
		pads[ mcA->second ]->cd();
		isAssMC=true;
		}
		//Draw Data & SYST
		if( !isAssMC){
			data2->Draw("P AXIS");
			data2->GetXaxis()->SetRangeUser(Range.first,Range.second);
			if (RangeY.first >-99 && RangeY.second>-99)
				data2->GetYaxis()->SetRangeUser(RangeY.first,RangeY.second);
		//data2->GetYaxis()->SetTitleSize(10); //very small
			data2->GetYaxis()->SetTitle(   ( mcLabels[iMC]+"/Data").c_str()   ); //very small
		}
		// this works for nMC==3
		if (nMC==3){
		data2->GetYaxis()->SetTitleOffset(1.5);
		data2->GetXaxis()->SetTitleOffset(3.0); //this needs to be huge because the pad is small
		}
		else if (nMC==5){
			data2->GetYaxis()->SetTitleOffset(2.5);
			data2->GetXaxis()->SetTitleOffset(5.5); //this needs to be huge because the pad is small
		}
		else if (nMC==1){
			data2->GetYaxis()->SetLabelSize(12);
			data2->GetXaxis()->SetLabelOffset(0.02);
			data2->GetYaxis()->SetTitleOffset(0.5);
			data2->GetXaxis()->SetTitleOffset(1.0); //this needs to be huge because the pad is small
		}
		if(!isAssMC)
			syst2->Draw("E2 SAME");
	
		if(drawBands && !isAssMC)	
		for(int iMcErr=0;iMcErr<mcErrAssociation.size();iMcErr++)
		{
			if(iMcErr>= mcErr.size())continue; //no band -- wtf?
			if(mcErrAssociation[iMcErr]!=iMC) continue; //not draw it here
			TH1D* mcErr2=NiceRange( mcErr[iMcErr],Range,RangeFactors.first,RangeFactors.second);
			for(int bin=1;bin<=mcErr2->GetNbinsX();bin++)
			{
				if( mcErr2->GetBinContent(bin) <RangeY.first)
					{
					double c=mcErr2->GetBinContent(bin) ;
					double e=mcErr2->GetBinError(bin) ;
					double newcontent=RangeY.first+0.0001;
					if( c+e>RangeY.first){ //do it only if it would appear
						mcErr2->SetBinContent(bin,newcontent);
						mcErr2->SetBinError(bin,c+e-newcontent);
						double newerr=mcErr2->GetBinError(bin);
						printf("************* D old=%f new= %f\n",c+e,newcontent+newerr);
						}
					}
				if( mcErr2->GetBinContent(bin) >RangeY.second)
					{
					double c=mcErr2->GetBinContent(bin) ;
					double e=mcErr2->GetBinError(bin) ;
					double newcontent=RangeY.second-0.0001;
					if( c - e <RangeY.second ){
						mcErr2->SetBinContent(bin,newcontent);
						mcErr2->SetBinError(bin,newcontent-(c-e));
						double newerr=mcErr2->GetBinError(bin);

						printf("************* U old=%f new= %f\n",c-e,newcontent-newerr);
						}
					}
			}
			legs[iMC]->AddEntry(mcErr2,mcLabelsErr[iMcErr].c_str(),"F"); // iMC==mcErrAss[iMcErr]
			mcErr2->Draw("E2 SAME");
		}

		//draw MC
        	TH1D* mc2 = NiceRange(mc[iMC],Range,RangeFactors.first,RangeFactors.second);
		mc2->Draw("HIST SAME ][");

		//drawLeg
		if (!isAssMC)
			legs[iMC]->Draw();
	
		//redraw AXIS and data Points
		if(!isAssMC)
			syst2->Draw("E2 SAME");
        	data2->Draw("AXIS X+ Y+ SAME");
        	data2->Draw("AXIS SAME");
        	data2->Draw("P SAME");

	}//iMC loop
	c->cd();
	pair<float,float> cmsOrig(cmsPosition);
	pair<float,float> lumiOrig(lumiPosition);
	cmsPosition.first=c->GetLeftMargin()+0.03; //Moving CMS

	int bin;
	if(Range.first>-90)bin=syst->FindBin(Range.first+0.001);
	if(syst->GetBinContent(bin)+syst->GetBinError(bin) > RangeY.second - 0.15 )
		{cmsPosition.first+=0.2;}

	cmsPosition.second=.93;
 	//float cmsSpaceOrig=cmsSpace;
	int drawLumiOrig=drawLumi;
	string extraTextTmp(extraText);
	//DrawCMS();
	//if nMC==3	
	if (nMC==3){
//	cmsPosition.first=.22;
	cmsPosition.second=1.-0.3 * dY - 0.06;
	lumiPosition.first=.96;
	lumiPosition.second=1.-0.3* dY - 0.01 ;
	extraText="";
	//cmsSpace=0.03;
	drawLumi=1;
	}

	if (nMC==5){
//	cmsPosition.first=.22;
	cmsPosition.second=1.-0.3 * dY - 0.04;
	lumiPosition.first=.96;
	lumiPosition.second=1.-0.3* dY - 0.01 ;
	string extraTextTmp(extraText);
	extraText="";
	//cmsSpace=0.05;
	drawLumi=1;
	}
	if (nMC==1){
//	cmsPosition.first=.20;
	cmsPosition.second=1.-0.3 * dY - 0.09;
	lumiPosition.first=.96;
	lumiPosition.second=1.-0.3* dY - 0.09 ;
	string extraTextTmp(extraText);
	extraText="";
	//cmsSpace=0.05;
	drawLumi=1;
	}

	NicePlotsBase::DrawCMS();

	extraText=extraTextTmp;
	cmsPosition=cmsOrig;//restore
	lumiPosition=lumiOrig;//restore
	//cmsSpace=cmsSpaceOrig;
	drawLumi=drawLumiOrig;

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
	l->SetTextAlign(11);
	l->SetTextFont(43); //helvetica Bold
	l->SetTextSize(24);  // ratio CMS/Preliminary Size is 0.76
	l->DrawLatex(cmsPosition.first,cmsPosition.second,Form("#bf{CMS} #scale[0.75]{#it{%s}}",cmsPreliminary.c_str()));
	//l->SetTextFont(63); //helvetica Bold
	//l->SetTextSize(24);  // ratio CMS/Preliminary Size is 0.76
	//l->SetTextAlign(11);
	//l->DrawLatex(cmsPosition.first,cmsPosition.second,"CMS");
	//l->SetText(cmsPosition.first,cmsPosition.second,"CMS"); // this is not draw it is used for figure out the dimensions
	//unsigned int w,h;
	//l->GetBoundingBox(w,h);
	//unsigned int ww=gPad->GetWw();
	//unsigned int wh=gPad->GetWh();

	//l->SetTextFont(53);//helvetica italics
	//l->SetTextSize(18);
	//l->SetTextAlign(11);
	//l->DrawLatex(cmsPosition.first+ float(w)/ww + cmsSpace,cmsPosition.second,"Preliminary");

	l->SetTextFont(43);
	l->SetTextSize(18);
	l->SetTextAlign(31);
	////oldlumi
	//if(drawLumi)l->DrawLatex(lumiPosition.first,lumiPosition.second,"#sqrt{s}=8TeV, L=19.7fb^{-1}");
	if(drawLumi)l->DrawLatex(lumiPosition.first,lumiPosition.second,"19.7fb^{-1} (8TeV)");
//	//l->SetTextFont(43);
//	//l->SetTextSize(18);
//	//l->DrawLatex(cmsPosition.first,cmsPosition.second-0.04,"#sqrt{s} = 8TeV, L=19.7fb^{-1}");
	l->SetTextSize(15);
	l->SetTextAlign(11);
	if( extraText != "")
		l->DrawLatex(cmsPosition.first,cmsPosition.second-0.05,extraText.c_str());
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
	//syst->SetMarkerColor(kOrange-4);
	//syst->SetFillColor(kOrange-4);
	//syst->SetLineColor(kOrange-4);
	//syst->SetFillStyle(3001);
	syst->SetLineStyle(1);
	syst->SetLineWidth(2);
        syst->GetXaxis()->SetRangeUser(Range.first,Range.second);

	syst->SetMarkerColor(kBlack);
	syst->SetFillColor(kBlack);
	syst->SetLineColor(kBlack);
	syst->SetFillStyle(3004);
	unsigned int ww=gPad->GetWw();
	unsigned int wh=gPad->GetWh();
	if (wh > ww)
		syst->SetFillStyle(3005);
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

void  NicePlotsBase::SetMCErrStyle()
{
	gStyle->SetHatchesLineWidth(3);
	int offset=0;
	for ( int iMC=0;iMC< int(mcErr.size()) ;iMC++)
	{
	     //if( mcErr.size()< mc.size() ) offset=3;
	     if ( // set a slight different style for scale and pdf unc
		iMC< mcLabelsErr.size() && (
		mcLabelsErr[iMC].find("pdf") !=string::npos ||
		mcLabelsErr[iMC].find("Pdf") !=string::npos ||
		mcLabelsErr[iMC].find("PDF") !=string::npos )
		) offset=3 - iMC;
	     if (
		iMC< mcLabelsErr.size() && (
		mcLabelsErr[iMC].find("Scale") !=string::npos ||
		mcLabelsErr[iMC].find("scale") !=string::npos ||
		mcLabelsErr[iMC].find("SCALE") !=string::npos )
		) offset=4 - iMC;
	
              mcErr[iMC]->GetXaxis()->SetRangeUser(Range.first,Range.second);
              mcErr[iMC]->SetLineColor(mcErrColors[iMC+offset]);
              mcErr[iMC]->SetLineStyle(mcErrLineStyles[iMC+offset]);
              mcErr[iMC]->SetFillColor(mcErrColors[iMC+offset]);
              mcErr[iMC]->SetFillStyle(mcErrStyles[iMC+offset]);
              mcErr[iMC]->SetLineWidth(2);
              mcErr[iMC]->SetMarkerStyle(0);
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
if (Ht==0)
	legendHeader += Form("N_{jets} #geq %d",nJets);
if (Ht>0)
	{
	legendHeader += Form("H_{T} #geq %d GeV",Ht);
	if (nJets>1)
		legendHeader += Form(", N_{jets} #geq %d",nJets);
	}
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
//cmsPosition=pair<double,double>(.45,.94);
cmsPosition=pair<double,double>(.20,.84); // position is Top Left
lumiPosition=pair<double,double>(.98,.91); // position is bottom right
autoLegend=1;
//cmsSpace=0.02;
cmsPreliminary="Preliminary";
drawBands=1;
drawLumi=1;
}

//---------------------- LOWER PLOTS-------------

TCanvas* SingleLowerPlot::DrawCanvas(){
if (DEBUG) cout<< "Draw SingleLowerPlot Canvas"
	<<"T0.02 R0.03 B0.2"<<endl;
		TCanvas *c=new TCanvas("c","c",600,300);
                c->SetTopMargin(0.10);
                c->SetRightMargin(0.03);
                c->SetBottomMargin(0.2);
               // c->SetLogy();
return c;
}

SingleLowerPlot::SingleLowerPlot() : NicePlotsBase(){
	ytitle="MadGraph/Data";
	RangeY.first=0.5;
	RangeY.second=1.5;
}

void SingleLowerPlot::DrawLegend(){
	return; //no legend
}

void SingleLowerPlot::SetDataStyle(){
	NicePlotsBase::SetDataStyle();
		data->GetYaxis()->SetTitleOffset(0.5);
		data->GetYaxis()->SetTitle("MadGraph/Data");
		data->GetYaxis()->SetNdivisions(510);
		data->GetYaxis()->SetDecimals();
		data->GetYaxis()->SetRangeUser(0.5,1.5);
		data->GetYaxis()->SetTitleOffset(0.5);
		data->GetXaxis()->SetTitleOffset(1.2);
		data->GetXaxis()->SetLabelOffset(0.02);
		data->GetXaxis()->SetTitleSize(20);
	return; //no legend
}

void SingleLowerPlot::DrawCMS(){
	//return; //no cms CHANGEME
	//c->cd();
	pair<float,float> cmsOrig(cmsPosition);
	pair<float,float> lumiOrig(lumiPosition);
	//float cmsSpaceOrig(cmsSpace);
	
	//cmsPosition.first=.12;
//	cmsPosition.second=0.85;
	cmsPosition.first=gPad->GetLeftMargin()+0.01;
	cmsPosition.second=1.0-gPad->GetTopMargin()-0.08;
	lumiPosition.first=.96;
	//lumiPosition.second=.9;
	lumiPosition.second=1.0-gPad->GetTopMargin()+0.01;
	//drawLumi=0;
	string extraTextTmp(extraText);
	extraText="";
	//cmsSpace=0.05;

	NicePlotsBase::DrawCMS();

	extraText=extraTextTmp;
	cmsPosition=cmsOrig;//restore
	lumiPosition=lumiOrig;//restore
	//cmsSpace=cmsSpaceOrig;
	return;
}

//---------------------- RATIO PLOTS-------------
SingleRatioPlot::SingleRatioPlot() : NicePlotsBase(){
legendPos1=pair<double,double>(.70,.75);
legendPos2=pair<double,double>(.97,.94);
}
TCanvas* SingleRatioPlot::DrawCanvas(){
if (DEBUG) cout<< "Draw SingleRatioPlot Canvas"
	<<"T0.10 L0.18  R0.02 B0.1 "<<endl;

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
SingleRatioLowerPlot::SingleRatioLowerPlot() : NicePlotsBase(){
	//constructor
cmsPosition.first=0.25;
cmsPosition.second=0.76;
}

TCanvas* SingleRatioLowerPlot::DrawCanvas(){
if (DEBUG) cout<< "Draw SingleRatioLowerPlot Canvas"
	<<"T0.15 L0.18  R0.02 B0.15 "<<endl;

TCanvas *c=new TCanvas("cL","cL",600,300);
                c->SetLeftMargin(0.18);
                c->SetTopMargin(0.15);
                c->SetBottomMargin(0.15);
                c->SetRightMargin(0.02);
return c;
}
void SingleRatioLowerPlot::DrawLegend(){
	return; //no legend
}
void SingleRatioLowerPlot::DrawCMS(){
//	TLatex *l=new TLatex();
//	l->SetNDC();
//	l->SetTextFont(43);
//	l->SetTextSize(15);
//	l->SetTextAlign(12);
//	if( extraText != "")
//		//l->DrawLatex(cmsPosition.first,cmsPosition.second,extraText.c_str());
//		l->DrawLatex(cmsPosition.first,cmsPosition.second,extraText.c_str());
//	return; //only extraText
	pair<float,float> cmsOrig(cmsPosition);
	pair<float,float> lumiOrig(lumiPosition);
	//float cmsSpaceOrig(cmsSpace);
	
	cmsPosition.first=.20;
	cmsPosition.second=0.78;
	lumiPosition.first=.96;
	lumiPosition.second=.9;
	//drawLumi=1;
	string extraTextTmp(extraText);
	extraText="";
	//cmsSpace=0.05;

	NicePlotsBase::DrawCMS();

	extraText=extraTextTmp;
	cmsPosition=cmsOrig;//restore
	lumiPosition=lumiOrig;//restore
	//cmsSpace=cmsSpaceOrig;

	TLatex *l=new TLatex();
	l->SetNDC();
	l->SetTextFont(43);
	l->SetTextSize(15);
	l->SetTextAlign(31);
	if( extraText != "")
		//l->DrawLatex(cmsPosition.first,cmsPosition.second,extraText.c_str());
		l->DrawLatex(.96,.22,extraText.c_str());
	return; //only extraText
}
void SingleRatioLowerPlot::SetDataStyle(){
	NicePlotsBase::SetDataStyle();
	RangeY.first=0.5;
	RangeY.second=1.5;
		data->GetYaxis()->SetTitleOffset(0.5);
		data->GetYaxis()->SetTitle("MadGraph/Data");
		data->GetYaxis()->SetNdivisions(510);
		data->GetYaxis()->SetDecimals();
		data->GetYaxis()->SetRangeUser(0.5,1.5);
        	data->GetYaxis()->SetTitleSize(20);
		data->GetXaxis()->SetTitleSize(20);
	return; 
}


bool SingleRatioLowerPlot::isMcToDraw(int i)
{
	return true; //always draw in ratio plot
}

bool SingleLowerPlot::isMcToDraw(int i)
{
	return true; //always draw in ratio plot
}

//-----------     GENERAL FUNCTIONS --
TH1D* NicePlots::NiceRange(TH1*h,pair<double,double> Range, double f1=0.2,double f2=0.2){
	//disable
	TH1D *r=(TH1D*) h->Clone();
	return r;
	//
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
