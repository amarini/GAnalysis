
#include "TH1F.h"
#include "TFile.h"

#include <string>
#include <vector>
#include <map>

#ifndef SEL_H
#define SEL_H

class selection{
public:
	selection();
	~selection();
	int Write(TFile *f);
	int Read(TFile *f);
	int initCut(std::string cutName);
	int getNcuts();
	int Fill(std::string cutName,float weight=1);
	int Fill(int iCut,float weight=1);
	int getStats();
private:
	int nCuts;
	std::map<int,std::pair<std::string,TH1F*> > cuts;
	std::map<std::string,int> names;
};

#endif
