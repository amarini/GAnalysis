
#include <vector>
#include "TH1F.h"
#include "TChain.h"
#include "TMath.h"
#include "TLorentzVector.h"
#include "TCanvas.h"
#include "TROOT.h"
#include "TDirectory.h"
#include <iostream>

#ifndef M_PI
#define M_PI 3.1416
#endif
#include <signal.h>
#include <stdlib.h>
#include <stdio.h>
#include <exception>

using namespace std;

class myexception: public exception
{
  virtual const char* what() const throw()
  {
    return "Caught signal CTRL+C";
  }
} myex;


void my_handler(int s){
           throw  myex;
}

int controlRCPtCut(){
 cout<<"-->Begin"<<endl;
 signal (SIGINT,my_handler);

 cout<<"-->Load Trees"<<endl;
 TChain *t=new TChain("accepted/events");
 //t->Add("root://eoscms///store/user/amarini/zjets_V00-12_dontuse/GJets*.root");
 t->Add("root://eoscms///store/user/amarini/zjets_V00-12/SinglePhoton*.root");
 t->Add("root://eoscms///store/user/amarini/zjets_V00-12/Photon*.root");
 
 cout<<"-->Book Histo"<<endl;
 TH1F* h_jetPt=new TH1F("H_JetPt","Jet P_{T}",100,0,100);
 TH1F* h_jetPtNOPU=new TH1F("H_JetPtNOPU","Jet P_{T} NO PU",100,0,100);
 
 cout<<"-->Set BranchAddress"<<endl;
 vector<float> *jetPt=0;
 vector<float> *jetEta=0;
 vector<float> *photonPt=0;
 vector<float> *photonEta=0;
 vector<float> *photonPhi=0;
 vector<float> *photonE=0;
 vector<float> *jetPhi=0;
 vector<float> *jetE=0;
 
 t->SetBranchAddress("jetPt",&jetPt);
 t->SetBranchAddress("jetEta",&jetEta);
 t->SetBranchAddress("jetPhi",&jetPhi);
 t->SetBranchAddress("jetE",&jetE);

 t->SetBranchAddress("photonPt",&photonPt);
 t->SetBranchAddress("photonEta",&photonEta);
 t->SetBranchAddress("photonPhi",&photonPhi);
 t->SetBranchAddress("photonE",&photonE);
//iso & selection
 vector<float> *photonIsoFPRPhoton=0;
 vector<float> *photonid_hadronicOverEm=0;
 vector<float> *photonPfIsoChargedHad=0;
 vector<float> *photonPfIsoNeutralHad=0;
	
 t->SetBranchAddress("photonIsoFPRPhoton",&photonIsoFPRPhoton);
 t->SetBranchAddress("photonid_hadronicOverEm",&photonid_hadronicOverEm);
 t->SetBranchAddress("photonPfIsoChargedHad",&photonPfIsoChargedHad);
 t->SetBranchAddress("photonPfIsoNeutralHad",&photonPfIsoNeutralHad);
 
 int isRealData;
 t->SetBranchAddress("isRealData",&isRealData);t->GetEntry(0);
 
 double PUWeight=1;
 if(!isRealData)
 	t->SetBranchAddress("PUWeight",&PUWeight);
	
 Float_t photonPtGEN;
 Float_t photonEtaGEN;
 Float_t photonPhiGEN;
 Float_t photonEGEN;
 
 t->SetBranchAddress("photonPtGEN",&photonPtGEN);
 t->SetBranchAddress("photonEtaGEN",&photonEtaGEN);
 t->SetBranchAddress("photonPhiGEN",&photonPhiGEN);
 t->SetBranchAddress("photonEGEN",&photonEGEN);
	
 cout<<"-->Start Loop"<<endl;
try
{
 for(int i=0;i<t->GetEntries();i++)
	{
	t->GetEntry(i);
	//Photon GEN
 	if(i%10000==0)cout<<"---> iEntry:"<<i<<"/"<<t->GetEntries()<<endl;
 	if(i<100)cout<<"---> iEntry:"<<i<<" Set PhotonGEN"<<endl;
	TLorentzVector gammaGEN;
        gammaGEN.SetPtEtaPhiE( photonPtGEN,photonEtaGEN,photonPhiGEN,photonEGEN);
	//Photon RECO
 	if(i<100)cout<<"---> iEntry:"<<i<<" Set Photon RECO"<<endl;
	TLorentzVector gamma;
	int GammaIdx=-1;
	for(int iGamma=0;iGamma<int(photonPt->size());iGamma++)
		{	
 		if(i<100)cout<<"---> iEntry:"<<i<<" phEta "<<long(photonEta)<<" phPt "<<long(photonPt)<<" phPhi "<<long(photonPhi)<<" phE " <<long(photonE)<<endl;
 		if(i<100)cout<<"---> iEntry:"<<i<<" photonIsoFPRPhoton "<<long(photonIsoFPRPhoton)<<" photonid_hadronicOverEm "<<long(photonid_hadronicOverEm)<<" photonPfIsoChargedHad "<<long(photonPfIsoChargedHad)<<" photonPfIsoNeutralHad " <<long(photonPfIsoNeutralHad)<<endl;
		if(fabs( (*photonEta)[iGamma] )>=1.4 ) continue;
		if( (*photonIsoFPRPhoton)[iGamma]>10) continue;  // loose 
                if( (*photonid_hadronicOverEm)[iGamma] >0.05) continue;
                if( (*photonPfIsoChargedHad)[iGamma]>1.5) continue;
                if( (*photonPfIsoNeutralHad)[iGamma]>1.0+ 0.04*(*photonPt)[iGamma]) continue;
		GammaIdx=iGamma;
                break;
		}//Gamma Loop
	if(GammaIdx<0)continue;
	gamma.SetPtEtaPhiE(photonPt->at(GammaIdx),photonEta->at(GammaIdx),photonPhi->at(GammaIdx),photonE->at(GammaIdx));
	if(gamma.Pt()<100 || gamma.Pt()>150) continue;
	//Loop On Jets
	for(int iJet=0;iJet<int(jetPt->size());iJet++)
		{
		TLorentzVector j;
		j.SetPtEtaPhiE(jetPt->at(iJet),jetEta->at(iJet),jetPhi->at(iJet),jetE->at(iJet) );
		float DR=gamma.DeltaR(j);
		if(DR<0.8)continue;
		float DPhi=fabs(gamma.DeltaPhi(j));
		if(DPhi>M_PI-0.8)continue; //the recoil can be at any eta
		float DEta=fabs(gamma.Eta()-j.Eta());
		if(DEta>0.1)continue;
		h_jetPt->Fill(j.Pt(),PUWeight);
		h_jetPtNOPU->Fill(j.Pt(),1);
		}
		
	}//Entries Loop
}//try
catch (exception& e)
  {
    cout << e.what() << endl;
  }

TCanvas *c1=new TCanvas(); 
h_jetPt->Draw();
h_jetPtNOPU->SetLineStyle(kDashed);
h_jetPtNOPU->Draw("SAME");
}
