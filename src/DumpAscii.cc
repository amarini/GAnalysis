#include <iostream>
#include <fstream>
#include "DumpAscii.h"
using namespace std;

void DumpAscii::BookHisto(TH1*h)
{
	histoContainer[h->GetName()].histo;
	for(int iBin=1;iBin<h->GetNbinsX()+1;iBin++)
	{
		histoContainer[h->GetName()].histo.push_back(Bin(h->GetBinLowEdge(iBin),h->GetBinLowEdge(iBin+1)));
	}
	return;
}
void DumpAscii::FillHisto(string s,double x,const Event &e){
	unsigned long long int iBin=histoContainer[s].FindBin(x);
	if(iBin<0){fprintf(stderr,"Error: Bin not found\n"); return ; };
	histoContainer[s].histo.at(iBin).events.push_back(e);
	return;
}


unsigned long long int Histo::FindBin(double x){
	unsigned long long int size=histo.size(); 
	vector<Bin>::iterator it=find(histo.begin(),histo.end(),x);
	if ( it == histo.end() ) return -1;
	return it-histo.begin();
}

void DumpAscii::Dump(){
	if(fw==NULL)fw=fopen(fileName.c_str(),"w");	
	for (map<string,Histo>::iterator i=histoContainer.begin();i!=histoContainer.end();i++)
		{
		i->second.Dump(i->first,fw);
		}
	return;
}

void Histo::Dump(string name,FILE*fw){
	for(unsigned long long int  i=0;i<histo.size();i++)
		{
		histo.at(i).Dump(name,fw);
		}
	return;
	}

void Bin::Dump(string name,FILE *fw){
	for (unsigned long long i=0;i<events.size();i++)
		events.at(i).Dump(name,range.first,range.second,fw);
	events.clear();
	return ;
	}

void Event::Dump(string name,double x, double y,FILE *fw){
	fprintf(fw,"%s\t%lf\t%lf\t%llu\t%llu\t%llu\n",name.c_str(),x,y,run,lumi,event);
	return;
	}
