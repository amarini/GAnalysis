
#include "TH1F.h"
#include "TFile.h"
#include "TObject.h"

#include <string>
#include <vector>
#include <map>

#ifndef SEL_H
#define SEL_H

class Selection: public TObject {
public:
	//selection();
	Selection(const char dir[]="selection");
	~Selection();
	int Write(TFile *f);
	int Read(TFile *f);
	int initCut(std::string cutName);
	int getNcuts();
	int Fill(std::string cutName,float weight=1);
	int FillAndInit(std::string cutName,float weight=1);
	int Fill(int iCut,float weight=1);
	int getStats();
	int Clear();
	int setDir(std::string dir){dirName=dir;};
	std::string getDir(){return dirName;};
private:
	std::string dirName;
	int nCuts;
	std::map<int,std::pair<std::string,TH1F*> > cuts;
	std::map<std::string,int> names;

	ClassDef(Selection, 1);
};

#endif
