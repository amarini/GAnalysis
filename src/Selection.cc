
#define SEL_cxx

#include "Selection.h"
#include "TDirectory.h"
#include "TList.h"
#include "TCanvas.h"
#include "TH1F.h"
#include "TLatex.h"
#include "TROOT.h"
#include "TStyle.h"

#include <cstdio>
#include <iostream>

#ifdef SEL_cxx
using namespace std;
Selection::Selection(const char *dir)
	{
	nCuts=0;
	dirName=string(dir);
	};
Selection::~Selection()
	{
	};
int Selection::getNcuts()
	{
	return nCuts;
	};
int Selection::initCut(string cutName)
	{
	cuts[nCuts]=pair<string,TH1F*> (cutName,new TH1F( (cutName+Form("_%d",nCuts)).c_str(),cutName.c_str(),1,-0.5,0.5 )    );
	names[cutName]=nCuts;
	nCuts++;
	}
int Selection::Fill(string cutName,float weight)
	{
	//cuts[ names[cutName] ].second->Fill(0,weight);	
	return Fill( names[cutName] );
	}
int Selection::Fill(int iCut,float weight)
	{
	cuts[iCut].second->Fill(0.,weight);	
	return 0;
	}
int Selection::Write(TFile *f)
	{
	cerr<<" -- STARTING WRITING SELECTION TO FILE --"<<endl;
	if(f==NULL) cerr<<" -> File is not opened"<<endl;
	f->mkdir(dirName.c_str());
	f->cd(dirName.c_str());
	cerr<<" -> going to write selection"<<endl;
	for( map<int,pair<string,TH1F*> >::iterator it=cuts.begin();it!=cuts.end();it++)
		{
		cerr<<" --> Writing histogram: "<<it->second.first<<endl;
		if(it->second.second==NULL)cerr<<" --->  histogram doesn't exist "<<endl;
		it->second.second->Write();
		}
	cerr<<" -- END WRITING --"<<endl;
	}
int Selection::Read(TFile *f)
	{
	TDirectory *d=(TDirectory*)f->Get(dirName.c_str());
	TList *l=d->GetListOfKeys();	
	Clear();
	//nCuts=0;
	//cuts.clear();names.clear();
	for(int i=0;i< l->GetEntries();i++)
		{
		if(  l->At(i) == NULL ) continue;
		TObject *o = d->Get( l->At(i)->GetName()  );
		if(!( o->InheritsFrom("TH1F")) ) continue;
		TH1F *h=(TH1F*)o;
		string name( h->GetName());
		string name2(name);
		int pos=name2.rfind("_"); name2[pos]=' ';
		char cutName[1023];int iCut;
		sscanf(name2.c_str(),"%s %d",cutName,&iCut);
		cuts[iCut]=pair<string,TH1F*>(string(cutName),(TH1F*)h->Clone());
		names[cutName]=iCut;
		nCuts++;
		}

	for(int i=0;i<nCuts;i++) if( cuts.count(i) ==0 ) {fprintf(stderr,"READING ERROR\n");return 1;}
	return 0;
	}
int Selection::getStats()
	{
	gStyle->SetOptStat(0);
	//gStyle->SetOptTitle(0);
	TH1F*h=new TH1F("stats","Cuts Efficiencies",nCuts,0,nCuts);
	for(int iCut=0;iCut<nCuts;iCut++)	
		{
		h->GetXaxis()->SetBinLabel(iCut+1,cuts[iCut].first.c_str()) ;
		h->SetBinContent(iCut+1,cuts[iCut].second->GetBinContent(1)   );
		}
	TCanvas *c=new TCanvas();
	c->SetLogy();
	h->Draw();
	h->SetLineColor(kBlue+2);
	h->SetLineWidth(3);
	TLatex *l=new TLatex();
		//l->SetNDC();
		l->SetTextFont(42);
		l->SetTextSize(0.03);
		l->SetTextAlign(22);
	for(int iCut=0;iCut<nCuts;iCut++)	
		{
		l->SetTextFont(42);
		if(iCut>0)l->DrawLatex(iCut+.5,cuts[0].second->GetBinContent(1),Form("%.1f%%",cuts[iCut].second->GetBinContent(1)/cuts[iCut-1].second->GetBinContent(1)*100  )  );
		l->SetTextFont(62);
		l->DrawLatex(iCut+.5,cuts[iCut].second->GetBinContent(1)+2,Form("%.0f",cuts[iCut].second->GetBinContent(1)  )  );
		}

	return 0;
	}
int Selection::FillAndInit(std::string cutName,float weight)
	{
	if( names.count(cutName) ==0 ) initCut(cutName);
	Fill(cutName,weight);
	}
int Selection::Clear()
	{
	nCuts=0;
	for(std::map<int,std::pair<std::string,TH1F*> >::iterator it=cuts.begin();it!=cuts.end();it++)
		{
		it->second.second->Delete();
		it->second.second=NULL;
		}
	cuts.clear();
	names.clear();
	}
#endif
