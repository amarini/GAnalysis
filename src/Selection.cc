
#define SEL_cxx

#include "Selection.h"
#include "TDirectory.h"
#include "TList.h"
#include <cstdio>

#ifdef SEL_cxx
using namespace std;
selection::selection()
	{
	nCuts=0;
	};
int selection::getNcuts()
	{
	return nCuts;
	};
int selection::initCut(string cutName)
	{
	cuts[nCuts]=pair<string,TH1F*> (cutName,new TH1F( (cutName+Form("_%d",nCuts)).c_str(),cutName.c_str(),1,-0.5,0.5 )    );
	names[cutName]=nCuts;
	nCuts++;
	}
int selection::Fill(string cutName,float weight)
	{
	//cuts[ names[cutName] ].second->Fill(0,weight);	
	return Fill( names[cutName] );
	}
int selection::Fill(int iCut,float weight)
	{
	cuts[iCut].second->Fill(0.,weight);	
	return 0;
	}
int selection::Write(TFile *f)
	{
	f->mkdir("selection");
	f->cd("selection");
	for( map<int,pair<string,TH1F*> >::iterator it=cuts.begin();it!=cuts.end();it++)
		{
		it->second.second->Write();
		}
	}
int selection::Read(TFile *f)
	{
	TDirectory *d=(TDirectory*)f->Get("selection");
	TList *l=d->GetList();	
	nCuts=0;
	cuts.clear();names.clear();
	for(int i=0;i< l->GetEntries();i++)
		{
		if(  l->At(i) == NULL ) continue;
		if(!(l->At(i)->InheritsFrom("TH1F")) ) continue;
		TH1F* h = (TH1F*)l->At(i);
		string name( h->GetName());
		string name2(name);
		int pos=name2.rfind("_"); name2[pos]=' ';
		char cutName[1023];int iCut;
		sscanf(name2.c_str(),"%s %d",&cutName,&iCut);
		cuts[iCut]=pair<string,TH1F*>(string(cutName),(TH1F*)h->Clone());
		names[cutName]=iCut;
		nCuts++;
		}

	for(int i=0;i<nCuts;i++) if( cuts.count(i) ==0 ) {fprintf(stderr,"READING ERROR:%s\n");return 1;}
	return 0;
	}
int selection::getStats()
	{
	return 0;
	}
#endif
