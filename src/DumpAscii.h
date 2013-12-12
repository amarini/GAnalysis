// --- STD -----------
#include <map>
#include <vector>
#include <algorithm>
#include <string>
// --- ROOT ----------
#include "TH1D.h"
#include "TH1F.h"
#include "TObject.h"
// --- ZLIB ------
// for some reason cint doesn't like them
#ifndef __CINT__
#include <zlib.h>
#endif

// --- OTHER ----------
using namespace std;
// --- EVENT ----------
class Event:public TObject{
public:
	Event () {run=-1;lumi=-1;event=-1;}
	Event (unsigned long long int run_, unsigned long long int lumi_, unsigned long long int event_){ run=run_;lumi=lumi_;event=event_;}
	unsigned long long int event;
	unsigned long long int lumi;
	unsigned long long int run;
	void Dump(string,double x , double y,FILE *fw);
	#ifndef __CINT__
	void Dump(string,double x , double y,gzFile fz);
	#endif
   ClassDef(Event,1);
};

// --- BIN ----------
class Bin:public TObject{
public:
	Bin(){range.first=0;range.second=0;}
	Bin(double x,double y){range.first=x;range.second=y;};
	std::pair<float,float> range;
	std::vector<Event> events;
	const bool isIn(double x)const { return (x>=range.first && x<range.second);}
	const bool isBig(double x)const { return (x>=range.second);}
	const bool isSmall(double x)const { return (x>=range.second);}
	void Dump(string name,FILE *fw);
	#ifndef __CINT__
	void Dump(string name,gzFile fz);
	#endif
   ClassDef(Bin,1);
};

const inline bool operator<(const Bin&x,const float y){return x.isBig(y);}
const inline bool operator>(const Bin&x,const float y){return x.isSmall(y);}
const inline bool operator<(const float y,const Bin&x){return x.isSmall(y);}
const inline bool operator>(const float y,const Bin&x){return x.isBig(y);}
const inline bool operator==(const float y,const Bin&x){return x.isIn(y);}
const inline bool operator==(const Bin&x,const float y){return x.isIn(y);}

// --- HISTO ----------
class Histo:public TObject{
public:
	Histo(){};
	vector<Bin> histo; //bin are supposed sorted
	unsigned long long int FindBin(double x);
	void Dump(string name,FILE *fw);
	#ifndef __CINT__
	void Dump(string name,gzFile fz);
	#endif
   ClassDef(Histo,1);
};

// --- DUMP ----------
class DumpAscii:public TObject{

public:
	void BookHisto(TH1*h);
	void FillHisto(string s,double x,const Event &e);
	// -- overload
	void FillHisto(TH1*h,double x,const Event &e){return FillHisto(h->GetName(),x,e);};
	void FillHisto(TH1*h,double x,unsigned long long int run, unsigned long long int lumi, unsigned long long int event) {return  FillHisto(h,x,Event(run,lumi,event));};
	void FillHisto(string s,double x,unsigned long long int run, unsigned long long int lumi, unsigned long long int event) {return  FillHisto(s,x,Event(run,lumi,event));};
	void Dump();

	DumpAscii(){fw=NULL;maxn=-1;in=0;
	#ifndef __CINT__
		fz=NULL;
	#endif
		}
	~DumpAscii(){
		Dump();
		if(fw)fclose(fw);
	#ifndef __CINT__
		 if(fz)gzclose(fz);
	#endif
		}
	string fileName;
	long long maxn;
	bool compress;
private:
	map<string,Histo> histoContainer;
	FILE *fw;
	#ifndef __CINT__
		gzFile fz;
	#endif
	long long in;
public:
   ClassDef(DumpAscii,1);
};
