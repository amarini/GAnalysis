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
	if(iBin>= histoContainer[s].histo.size()){ fprintf(stderr,"Error Bin not found\n");return ;}
	histoContainer[s].histo.at(iBin).events.push_back(e);
	if (maxn>0){
		in++;
		if (in >=maxn)Dump();
		};
	return;
}


unsigned long long int Histo::FindBin(double x){
	unsigned long long int size=histo.size(); 
	vector<Bin>::iterator it=find(histo.begin(),histo.end(),x);
	if ( it == histo.end() ) return -1;
	return it-histo.begin();
}

void DumpAscii::Dump(){
	if((fw==NULL) && !compress && fileName!="")fw=fopen(fileName.c_str(),"w");	
	#ifndef __CINT__
	if((fz==NULL) && compress && fileName!="")fz=gzopen(fileName.c_str(),"w");	
	#endif
	
	#ifdef __CINT__
	if(compress) fprintf("DUMP ERROR: can't use zlib in CINT. Try to turn it off\n");
	#endif

	for (map<string,Histo>::iterator i=histoContainer.begin();i!=histoContainer.end();i++)
		{
		if(!compress)i->second.Dump(i->first,fw);
	#ifndef __CINT__
		if(compress)i->second.Dump(i->first,fz);
	#endif
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
#ifndef __CINT__
void Histo::Dump(string name,gzFile fz){
	for(unsigned long long int  i=0;i<histo.size();i++)
		{
		histo.at(i).Dump(name,fz);
		}
	return;
	}
#endif

void Bin::Dump(string name,FILE *fw){
	for (unsigned long long i=0;i<events.size();i++)
		events.at(i).Dump(name,range.first,range.second,fw);
	events.clear();
	return ;
	}

#ifndef __CINT__
void Bin::Dump(string name,gzFile fz){
	for (unsigned long long i=0;i<events.size();i++)
		events.at(i).Dump(name,range.first,range.second,fz);
	events.clear();
	return ;
	}
#endif

void Event::Dump(string name,double x, double y,FILE *fw){
	if (fw == NULL) return;
	fprintf(fw,"name:%s\tBinLow:%lf\tBinHigh:%lf\trun:%llu\tlumi:%llu\tevent:%llu\n",name.c_str(),x,y,run,lumi,event);
	return;
	}

#ifndef __CINT__
void Event::Dump(string name,double x, double y,gzFile fz){
	if (fz == NULL) return;
	string str=Form("name:%s\tBinLow:%lf\tBinHigh:%lf\trun:%llu\tlumi:%llu\tevent:%llu\n",name.c_str(),x,y,run,lumi,event);
	gzwrite(fz,str.c_str(),strlen(str.c_str()));
	return;
	}
#endif
