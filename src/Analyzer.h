//////////////////////////////////////////////////////////
// This class has been automatically generated on
// Thu Aug  8 16:55:20 2013 by ROOT version 5.32/00
// from TTree events/events
// found on file: SinglePhoton_Run2012C-22Jan2013-v1_AOD/PATZJetsExpress_111_1_Hqc.root
//////////////////////////////////////////////////////////

#ifndef Analyzer_h
#define Analyzer_h


#include "TH1F.h"
#include "TH2F.h"
#include "TFile.h"
#include "TTree.h"
#include "TChain.h"
#include "TLorentzVector.h"

// Header file for the classes stored in the TTree if any.
#include <vector>
#include <map>
using namespace std;

// --- Headers for TMVA - photonID --------------
#include "TMVA/Reader.h"

// Fixed size dimensions of array or collections stored in the TTree if any.

class Analyzer: public TObject {
public :
   TChain          *fChain;   //!pointer to the analyzed TTree or TChain
   Int_t           fCurrent; //!current Tree number in a TChain

   // Declaration of leaf types
   Int_t           isRealData;
   double 	 PUWeight;
   ULong64_t       eventNum;
   Int_t           runNum;
   Int_t           lumi;
   Int_t           nVtx;
   Int_t           nLeptons;
   Int_t           nPhotons;
   Int_t           nJets;
   Int_t           fwnJets;
   Float_t         rho;
   Float_t         rho25;
   Float_t         rhoQG;
   Float_t         pfmet;
   Float_t         pfmetPhi;
   Float_t         pfhadPt;
   Float_t         pfSumEt;
   Float_t         llM;
   Float_t         llPt;
   Float_t         llPhi;
   Float_t         llDPhi;
   Float_t         llY;
   Float_t         llEta;
   vector<float>   *photonPt;
   vector<float>   *photonE;
   vector<float>   *photonEta;
   vector<float>   *photonPhi;
   vector<float>   *photonPassConversionVeto;
   vector<float>   *photonPfIsoChargedHad;
   vector<float>   *photonPfIsoNeutralHad;
   vector<float>   *photonPfIsoPhoton;
   vector<float>   *photonPfIsoPhoton03ForCic;
   vector<float>   *photonPfIsoNeutrals03ForCic;
   vector<float>   *photonPfIsoCharged03ForCicVtx0;
   vector<float>   *photonPfIsoCharged03BadForCic;
   vector<float>   *photonPfIsoPhoton04ForCic;
   vector<float>   *photonPfIsoNeutrals04ForCic;
   vector<float>   *photonPfIsoCharged04ForCicVtx0;
   vector<float>   *photonPfIsoCharged04BadForCic;
   vector<float>   *photonid_sieie;
   vector<float>   *photonid_sieip;
   vector<float>   *photonid_etawidth;
   vector<float>   *photonid_phiwidth;
   vector<float>   *photonid_r9;
   vector<float>   *photonid_lambdaRatio;
   vector<float>   *photonid_s4Ratio;
   vector<float>   *photonid_e25;
   vector<float>   *photonid_sceta;
   vector<float>   *photonid_ESEffSigmaRR;
   vector<float>   *photonid_hadronicOverEm;
   vector<float>   *photonid_hadronicOverEm2012;
   vector<float>   *photonhcalTowerSumEtConeDR04;
   vector<float>   *photonecalRecHitSumEtConeDR04;
   vector<float>   *photonnTrkSolidConeDR04;
   vector<float>   *photontrkSumPtSolidConeDR04;
   vector<float>   *photonnTrkHollowConeDR04;
   vector<float>   *photontrkSumPtHollowConeDR04;
   vector<float>   *photonIsoFPRCharged;
   vector<float>   *photonIsoFPRNeutral;
   vector<float>   *photonIsoFPRPhoton;
   vector<float>   *photonIsoFPRRandomConeCharged;
   vector<float>   *photonIsoFPRRandomConeNeutral;
   vector<float>   *photonIsoFPRRandomConePhoton;
   vector<int>     *photonBit;
   vector<int>     *TriMatchF4Path_photon;
   vector<int>     *fired;
   vector<int>     *prescaleL1;
   vector<int>     *prescaleHLT;
   Int_t           isTriggered;
   vector<float>   *lepPt;
   vector<float>   *lepEta;
   vector<float>   *lepPhi;
   vector<float>   *lepE;
   vector<float>   *lepPFIsoUnc;
   vector<float>   *lepPFIsoDBCor;
   vector<float>   *lepPFIsoRhoCor;
   vector<int>     *lepChId;
   vector<float>   *lepR9orChi2ndof;
   vector<int>     *lepId;
   vector<int>     *TriMatchF1Path_doubleMu;
   vector<int>     *TriMatchF2Path_doubleEle;
   vector<int>     *TriMatchF3Path_MuEle_muon;
   vector<int>     *TriMatchF3Path_MuEle_electron;
   vector<int>     *TriMatchF5Path_singleMu;
   vector<int>     *TriMatchF6Path_singleEle;
   vector<int>     *jetVeto;
   vector<float>   *jetPt;
   vector<float>   *jetPtRES;
   vector<float>   *jetPtRESup;
   vector<float>   *jetPtRESdown;
   vector<float>   *jetEta;
   vector<float>   *jetPhi;
   vector<float>   *jetE;
   vector<float>   *jetArea;
   vector<float>   *jetBeta;
   vector<float>   *jetQGL;
   vector<int>     *jetPdgId;
   vector<float>   *jetQGMLP;
   vector<float>   *jetQG_axis2_L;
   vector<float>   *jetQG_ptD_L;
   vector<int>     *jetQG_mult_L;
   vector<float>   *jetQG_axis1_MLP;
   vector<float>   *jetQG_axis2_MLP;
   vector<float>   *jetQG_ptD_MLP;
   vector<int>     *jetQG_mult_MLP;
   vector<float>   *jetRMS;
   vector<float>   *jetBtag;
   vector<float>   *jetTagInfoNVtx;
   vector<float>   *jetTagInfoNTracks;
   vector<float>   *jetTagInfoVtxMass;
   vector<int>     *jetMCFlavour;
   vector<float>   *jetJEC;
   vector<float>   *jetUNC;
   vector<float>   *jetllDPhi;
   vector<float>   *fwjetPt;
   vector<float>   *fwjetPtRES;
   vector<float>   *fwjetPtRESup;
   vector<float>   *fwjetPtRESdown;
   vector<float>   *fwjetEta;
   vector<float>   *fwjetPhi;
   vector<float>   *fwjetE;
   vector<float>   *vtxZ;
   vector<float>   *vtxNdof;
   Int_t           puINT;
   Int_t           puOOT;
   Int_t           puTrueINT;
   Int_t           puTrueOOT;
   Int_t           nLeptonsGEN;
   Int_t           nJetsGEN;
   Float_t         llMGEN;
   Float_t         llPtGEN;
   Float_t         llPhiGEN;
   Float_t         llDPhiGEN;
   Float_t         llYGEN;
   Float_t         llEtaGEN;
   vector<float>   *lepPtGEN;
   vector<float>   *lepEtaGEN;
   vector<float>   *lepPhiGEN;
   vector<float>   *lepEGEN;
   vector<int>     *lepChIdGEN;
   vector<float>   *lepMatchedDRGEN;
   vector<int>     *lepMatchedGEN;
   vector<float>   *jetPtGEN;
   vector<float>   *jetPtRESGEN;
   vector<float>   *jetPtRESupGEN;
   vector<float>   *jetPtRESdownGEN;
   vector<float>   *jetEtaGEN;
   vector<float>   *jetPhiGEN;
   vector<float>   *jetEGEN;
   vector<int>     *jetVetoGEN;
   vector<float>   *jetllDPhiGEN;
   vector<int>     *jetIdGEN;
   vector<int>     *jetNpartonsGEN;
   Float_t         HTParSum;
   Int_t           nParton;
   Float_t         mcWeight;
   Float_t         qScale;
   Float_t         alphaQED;
   Float_t         alphaQCD;
   Float_t         x1;
   Float_t         x2;
   Int_t           pdf1Id;
   Int_t           pdf2Id;
   Float_t         scalePDF;
   Int_t           nPhotonsGEN;
   Float_t         photonPtGEN;
   Float_t         photonEGEN;
   Float_t         photonEtaGEN;
   Float_t         photonPhiGEN;
   Float_t         photonIsoPtDR03GEN;
   Float_t         photonIsoSumPtDR03GEN;
   Float_t         photonIsoEDR03GEN;
   Float_t         photonIsoPtDR04GEN;
   Float_t         photonIsoSumPtDR04GEN;
   Float_t         photonIsoEDR04GEN;
   Float_t         photonIsoPtDR05GEN;
   Float_t         photonIsoSumPtDR05GEN;
   Float_t         photonIsoEDR05GEN;
   Int_t           photonMotherIdGEN;
   Float_t         photonRECODRGEN;
   Int_t           VBPartonDM;
   Float_t         VBPartonM;
   Float_t         VBPartonE;
   Float_t         VBPartonPt;
   Float_t         VBPartonEta;
   Float_t         VBPartonPhi;
   vector<float>   *lepSigmaIEtaIEta;
   vector<float>   *lepHadronicOverEm;

   // List of branches
   TBranch        *b_PUWeight;   //!
   TBranch        *b_isRealData;   //!
   TBranch        *b_eventNum;   //!
   TBranch        *b_runNum;   //!
   TBranch        *b_lumi;   //!
   TBranch        *b_nVtx;   //!
   TBranch        *b_nLeptons;   //!
   TBranch        *b_nPhotons;   //!
   TBranch        *b_nJets;   //!
   TBranch        *b_fwnJets;   //!
   TBranch        *b_rho;   //!
   TBranch        *b_rho25;   //!
   TBranch        *b_rhoQG;   //!
   TBranch        *b_pfmet;   //!
   TBranch        *b_pfmetPhi;   //!
   TBranch        *b_pfhadPt;   //!
   TBranch        *b_pfSumEt;   //!
   TBranch        *b_llM;   //!
   TBranch        *b_llPt;   //!
   TBranch        *b_llPhi;   //!
   TBranch        *b_llDPhi;   //!
   TBranch        *b_llY;   //!
   TBranch        *b_llEta;   //!
   TBranch        *b_photonPt;   //!
   TBranch        *b_photonE;   //!
   TBranch        *b_photonEta;   //!
   TBranch        *b_photonPhi;   //!
   TBranch        *b_photonPassConversionVeto;   //!
   TBranch        *b_photonPfIsoChargedHad;   //!
   TBranch        *b_photonPfIsoNeutralHad;   //!
   TBranch        *b_photonPfIsoPhoton;   //!
   TBranch        *b_photonPfIsoPhoton03ForCic;   //!
   TBranch        *b_photonPfIsoNeutrals03ForCic;   //!
   TBranch        *b_photonPfIsoCharged03ForCicVtx0;   //!
   TBranch        *b_photonPfIsoCharged03BadForCic;   //!
   TBranch        *b_photonPfIsoPhoton04ForCic;   //!
   TBranch        *b_photonPfIsoNeutrals04ForCic;   //!
   TBranch        *b_photonPfIsoCharged04ForCicVtx0;   //!
   TBranch        *b_photonPfIsoCharged04BadForCic;   //!
   TBranch        *b_photonid_sieie;   //!
   TBranch        *b_photonid_sieip;   //!
   TBranch        *b_photonid_etawidth;   //!
   TBranch        *b_photonid_phiwidth;   //!
   TBranch        *b_photonid_r9;   //!
   TBranch        *b_photonid_lambdaRatio;   //!
   TBranch        *b_photonid_s4Ratio;   //!
   TBranch        *b_photonid_e25;   //!
   TBranch        *b_photonid_sceta;   //!
   TBranch        *b_photonid_ESEffSigmaRR;   //!
   TBranch        *b_photonid_hadronicOverEm;   //!
   TBranch        *b_photonid_hadronicOverEm2012;   //!
   TBranch        *b_photonhcalTowerSumEtConeDR04;   //!
   TBranch        *b_photonecalRecHitSumEtConeDR04;   //!
   TBranch        *b_photonnTrkSolidConeDR04;   //!
   TBranch        *b_photontrkSumPtSolidConeDR04;   //!
   TBranch        *b_photonnTrkHollowConeDR04;   //!
   TBranch        *b_photontrkSumPtHollowConeDR04;   //!
   TBranch        *b_photonIsoFPRCharged;   //!
   TBranch        *b_photonIsoFPRNeutral;   //!
   TBranch        *b_photonIsoFPRPhoton;   //!
   TBranch        *b_photonIsoFPRRandomConeCharged;   //!
   TBranch        *b_photonIsoFPRRandomConeNeutral;   //!
   TBranch        *b_photonIsoFPRRandomConePhoton;   //!
   TBranch        *b_photonBit;   //!
   TBranch        *b_TriMatchF4Path_photon;   //!
   TBranch        *b_fired;   //!
   TBranch        *b_prescaleL1;   //!
   TBranch        *b_prescaleHLT;   //!
   TBranch        *b_isTriggered;   //!
   TBranch        *b_lepPt;   //!
   TBranch        *b_lepEta;   //!
   TBranch        *b_lepPhi;   //!
   TBranch        *b_lepE;   //!
   TBranch        *b_lepPFIsoUnc;   //!
   TBranch        *b_lepPFIsoDBCor;   //!
   TBranch        *b_lepPFIsoRhoCor;   //!
   TBranch        *b_lepChId;   //!
   TBranch        *b_lepR9orChi2ndof;   //!
   TBranch        *b_lepId;   //!
   TBranch        *b_TriMatchF1Path_doubleMu;   //!
   TBranch        *b_TriMatchF2Path_doubleEle;   //!
   TBranch        *b_TriMatchF3Path_MuEle_muon;   //!
   TBranch        *b_TriMatchF3Path_MuEle_electron;   //!
   TBranch        *b_TriMatchF5Path_singleMu;   //!
   TBranch        *b_TriMatchF6Path_singleEle;   //!
   TBranch        *b_jetVeto;   //!
   TBranch        *b_jetPt;   //!
   TBranch        *b_jetPtRES;   //!
   TBranch        *b_jetPtRESup;   //!
   TBranch        *b_jetPtRESdown;   //!
   TBranch        *b_jetEta;   //!
   TBranch        *b_jetPhi;   //!
   TBranch        *b_jetE;   //!
   TBranch        *b_jetArea;   //!
   TBranch        *b_jetBeta;   //!
   TBranch        *b_jetQGL;   //!
   TBranch        *b_jetPdgId;   //!
   TBranch        *b_jetQGMLP;   //!
   TBranch        *b_jetQG_axis2_L;   //!
   TBranch        *b_jetQG_ptD_L;   //!
   TBranch        *b_jetQG_mult_L;   //!
   TBranch        *b_jetQG_axis1_MLP;   //!
   TBranch        *b_jetQG_axis2_MLP;   //!
   TBranch        *b_jetQG_ptD_MLP;   //!
   TBranch        *b_jetQG_mult_MLP;   //!
   TBranch        *b_jetRMS;   //!
   TBranch        *b_jetBtag;   //!
   TBranch        *b_jetTagInfoNVtx;   //!
   TBranch        *b_jetTagInfoNTracks;   //!
   TBranch        *b_jetTagInfoVtxMass;   //!
   TBranch        *b_jetMCFlavour;   //!
   TBranch        *b_jetJEC;   //!
   TBranch        *b_jetUNC;   //!
   TBranch        *b_jetllDPhi;   //!
   TBranch        *b_fwjetPt;   //!
   TBranch        *b_fwjetPtRES;   //!
   TBranch        *b_fwjetPtRESup;   //!
   TBranch        *b_fwjetPtRESdown;   //!
   TBranch        *b_fwjetEta;   //!
   TBranch        *b_fwjetPhi;   //!
   TBranch        *b_fwjetE;   //!
   TBranch        *b_vtxZ;   //!
   TBranch        *b_vtxNdof;   //!
   TBranch        *b_puINT;   //!
   TBranch        *b_puOOT;   //!
   TBranch        *b_puTrueINT;   //!
   TBranch        *b_puTrueOOT;   //!
   TBranch        *b_nLeptonsGEN;   //!
   TBranch        *b_nJetsGEN;   //!
   TBranch        *b_llMGEN;   //!
   TBranch        *b_llPtGEN;   //!
   TBranch        *b_llPhiGEN;   //!
   TBranch        *b_llDPhiGEN;   //!
   TBranch        *b_llYGEN;   //!
   TBranch        *b_llEtaGEN;   //!
   TBranch        *b_lepPtGEN;   //!
   TBranch        *b_lepEtaGEN;   //!
   TBranch        *b_lepPhiGEN;   //!
   TBranch        *b_lepEGEN;   //!
   TBranch        *b_lepChIdGEN;   //!
   TBranch        *b_lepMatchedDRGEN;   //!
   TBranch        *b_lepMatchedGEN;   //!
   TBranch        *b_jetPtGEN;   //!
   TBranch        *b_jetPtRESGEN;   //!
   TBranch        *b_jetPtRESupGEN;   //!
   TBranch        *b_jetPtRESdownGEN;   //!
   TBranch        *b_jetEtaGEN;   //!
   TBranch        *b_jetPhiGEN;   //!
   TBranch        *b_jetEGEN;   //!
   TBranch        *b_jetVetoGEN;   //!
   TBranch        *b_jetllDPhiGEN;   //!
   TBranch        *b_jetIdGEN;   //!
   TBranch        *b_jetNpartonsGEN;   //!
   TBranch        *b_HTParSum;   //!
   TBranch        *b_nParton;   //!
   TBranch        *b_mcWeight;   //!
   TBranch        *b_qScale;   //!
   TBranch        *b_alphaQED;   //!
   TBranch        *b_alphaQCD;   //!
   TBranch        *b_x1;   //!
   TBranch        *b_x2;   //!
   TBranch        *b_pdf1Id;   //!
   TBranch        *b_pdf2Id;   //!
   TBranch        *b_scalePDF;   //!
   TBranch        *b_nPhotonsGEN;   //!
   TBranch        *b_photonPtGEN;   //!
   TBranch        *b_photonEGEN;   //!
   TBranch        *b_photonEtaGEN;   //!
   TBranch        *b_photonPhiGEN;   //!
   TBranch        *b_photonIsoPtDR03GEN;   //!
   TBranch        *b_photonIsoSumPtDR03GEN;   //!
   TBranch        *b_photonIsoEDR03GEN;   //!
   TBranch        *b_photonIsoPtDR04GEN;   //!
   TBranch        *b_photonIsoSumPtDR04GEN;   //!
   TBranch        *b_photonIsoEDR04GEN;   //!
   TBranch        *b_photonIsoPtDR05GEN;   //!
   TBranch        *b_photonIsoSumPtDR05GEN;   //!
   TBranch        *b_photonIsoEDR05GEN;   //!
   TBranch        *b_photonMotherIdGEN;   //!
   TBranch        *b_photonRECODRGEN;   //!
   TBranch        *b_VBPartonDM;   //!
   TBranch        *b_VBPartonM;   //!
   TBranch        *b_VBPartonE;   //!
   TBranch        *b_VBPartonPt;   //!
   TBranch        *b_VBPartonEta;   //!
   TBranch        *b_VBPartonPhi;   //!
   TBranch        *b_lepSigmaIEtaIEta;   //!
   TBranch        *b_lepHadronicOverEm;   //!

   TMVA::Reader * tmvaReaderID_Single_Barrel;
   TMVA::Reader * tmvaReaderID_Single_Endcap;
//------------------------PUBLIC----------------
   Analyzer();
   virtual void      AddTree(const char *fileName);
   virtual ~Analyzer();
   virtual Int_t    GetEntry(Long64_t entry);
   virtual Long64_t LoadTree(Long64_t entry);
   virtual void     Init();
   virtual void     Loop();
	
   
   int loadMVA;
   virtual void InitMVA();
   struct PHOTONID{
	float tmva_photonid_r9;
	float tmva_photonid_sieie;
	float tmva_photonid_etawidth;
	float tmva_photonid_phiwidth;
	float tmva_photonid_sieip;
	float tmva_photonid_s4ratio;
	float tmva_photonid_pfphotoniso03;
	float tmva_photonid_pfchargedisogood03;
	float tmva_photonid_pfchargedisobad03;
	float tmva_photonid_sceta;
	float tmva_photonid_eventrho;
	};
   PHOTONID idvars;

   class CUTS{
		public:
		CUTS(float vpt1=0,float vpt2=8000,float ht1=0,float ht2=8000,float phid0=-10,float phid1=10,int nJ=1){Ht=pair<float,float>(ht1,ht2);VPt=pair<float,float>(vpt1,vpt2);phid=pair<float,float>(phid0,phid1); nJets=nJ;};
		pair<float,float> Ht;
		pair<float,float> VPt;
		pair<float,float> phid;
		int nJets;
		string name() { return string(Form("VPt_%.0f_%.0f_Ht_%.0f_%.0f_phid_%.3f_%.3f_nJets_%d",VPt.first,VPt.second,Ht.first,Ht.second,phid.first,phid.second,nJets));}
		};

   class BINS{
		public:
		BINS(int nB=100,float x0=0,float x1=1){nBins=nB;xMin=x0;xMax=x1;}
		float xMin;
		float xMax;
		int nBins;
		};

   vector<int> JetIdx;
   map<string,TH1F*> histoContainer;
   map<string,TH2F*> histo2Container;
   map<string,TTree*> treeContainer;
   vector<CUTS> cutsContainer;
   map<string,BINS> binsContainer;

   void MakeTree(string name);

   struct TREE_VAR{
		float photoniso;
		};
   TREE_VAR TreeVar;

   virtual void InitCuts();

   //READ IN INITCUTS and loaded in Cuts Container
   vector<float> PtCuts;
   pair<float,float> SigPhId;
   pair<float,float> BkgPhId;
	
   //BATCH RUN
   int nJobs;
   int jobId;
   string outputFileName;
	
   //effarea
   int useEffArea;
   string effAreaFile;
   map<string,float> effAreaCorr;
   void InitEffArea();
	
   //TRIGGER MENUS
   map<string,pair<float,float> > triggerMenus; 
   map<string,float> triggerScales;
   void LoadTrigger(string menu,float ptmin,float ptmax, float scale=1.0);
	
   //activate extra cout	
   int debug;
	
   //
   ClassDef(Analyzer,1);
};

#endif

#ifdef Analyzer_cxx

void Analyzer::LoadTrigger(string menu,float ptmin,float ptmax, float scale)
{
triggerMenus[menu]= pair<float,float>(ptmin,ptmax);
triggerScales[menu]= scale;
return;
}

Analyzer::Analyzer() : fChain(0) 
{
   debug=0;
   nJobs=-1;
   jobId=-1;
   outputFileName="output";
   loadMVA=0;
   useEffArea=0;
   effAreaFile="";
}
void Analyzer::InitCuts()
{
	if(debug>0)printf("Init cuts and bins\n");
	cutsContainer.push_back( CUTS(0,8000,0,8000) );
	binsContainer["gammaPt"] = BINS(1000.-90.,90,1000);
	binsContainer["gammaEta"] = BINS(100,0,5.);
	binsContainer["sieie"] = BINS(1000,0,.1);
	binsContainer["phid"] = BINS(100,-1.,1.);
	binsContainer["photoniso"] = BINS(100,-10,10);
	for(int p=0; p<int(PtCuts.size())-1 ;p++)	
		{
		if(PtCuts[p]<0)continue;
		if(PtCuts[p+1]<0)continue;
			//need to check if the cut already exist in pt
		int exists=0;
			for(int pp=0;pp<p-1;pp++)
				if( PtCuts[pp]==PtCuts[p] && PtCuts[pp+1]==PtCuts[p+1])
					exists=1;
		if(exists)
			{
			if(debug>0)cout<<"--> PtBin "<<PtCuts[p]<<" "<<PtCuts[p+1]<<" already exists"<<endl;
			continue;}
		cutsContainer.push_back(CUTS(PtCuts[p],PtCuts[p+1],0,8000,BkgPhId.first,BkgPhId.second ));
		cutsContainer.push_back(CUTS(PtCuts[p],PtCuts[p+1],0,8000,SigPhId.first,SigPhId.second ));
		}
}

void Analyzer::InitEffArea()
{
   map<string,float> effArea_rho;
   map<string,float> effArea_iso;

  FILE *fr=fopen(effAreaFile.c_str(),"r"); 
  if(fr==NULL) fprintf(stderr,"Error opening: %s",effAreaFile.c_str());
  char what[1023],buf[2048];
  float ptmin,ptmax,etamin,etamax,value;
  while(fgets(buf,2048,fr)!=NULL)
	{
	if(buf[0]=='#') continue;
	if(buf[0]=='\n') continue;
	if(buf[0]=='\0') continue;
	int i=0;
	while(buf[i]!='\n' && buf[i]!='\0') i++;
	buf[i]='\0';
  	sscanf(buf,"%s %f %f %f %f %f",what,&ptmin,&ptmax,&etamin,&etamax,&value);

	if(debug>0){
	fprintf(stderr,"Buffer is %s\n",buf);
	fprintf(stderr,"Going to scan %s %f %f %f %f %f\n",what,ptmin,ptmax,etamin,etamax,value);
	}

	if( string(what).find("iso") !=string::npos )  //it is iso
		{
		string name=Form("%.1f_%.1f_%.1f_%.1f",ptmin,ptmax,etamin,etamax);
		effArea_iso[name]=value;
		}
	else if( string(what).find("rho") !=string::npos )  //it is rho
		{
		string name=Form("%.1f_%.1f_%.1f_%.1f",ptmin,ptmax,etamin,etamax);
		effArea_rho[name]=value;
		}
	
	}
   //check that rho <-> iso and fill corr
   for(map<string,float>::iterator it=effArea_rho.begin();it!=effArea_rho.end();it++)
	{
	string name=it->first;
	if(effArea_iso.find(name) == effArea_iso.end())	
		{
		fprintf(stderr,"Error in effArea.txt: value [%s] in rho but not iso\n",name.c_str());	
		}
	else {
		effAreaCorr[name]=effArea_iso[name]/effArea_rho[name];
		fprintf(stderr,"Loaded %s in EffArea Corrections with val %f - \n",name.c_str(), effArea_iso[name]/effArea_rho[name]);
		}
	}
   for(map<string,float>::iterator it=effArea_iso.begin();it!=effArea_iso.end();it++)
	{
	string name=it->first;
	if(effArea_rho.find(name) == effArea_rho.end())	
		{
		fprintf(stderr,"Error in effArea.txt: value [%s] in iso but not rho\n",name.c_str());	
		}
	}
  return;
}

void Analyzer::InitMVA(){
//from h2gglobe GeneralFunctions
	if(debug>0)printf("booking mvas\n");
    tmvaReaderID_Single_Barrel = new TMVA::Reader("!Color:Silent");
    tmvaReaderID_Single_Barrel->AddVariable("ph.r9"		,   &idvars.tmva_photonid_r9 );
    tmvaReaderID_Single_Barrel->AddVariable("ph.sigietaieta"	,   &idvars.tmva_photonid_sieie );
    tmvaReaderID_Single_Barrel->AddVariable("ph.scetawidth"	,   &idvars.tmva_photonid_etawidth );
    tmvaReaderID_Single_Barrel->AddVariable("ph.scphiwidth"	,   &idvars.tmva_photonid_phiwidth );
    tmvaReaderID_Single_Barrel->AddVariable("ph.idmva_CoviEtaiPhi", &idvars.tmva_photonid_sieip );
    tmvaReaderID_Single_Barrel->AddVariable("ph.idmva_s4ratio"	,   &idvars.tmva_photonid_s4ratio );
    tmvaReaderID_Single_Barrel->AddVariable("ph.idmva_GammaIso"	,   &idvars.tmva_photonid_pfphotoniso03 );
    tmvaReaderID_Single_Barrel->AddVariable("ph.idmva_ChargedIso_selvtx",   &idvars.tmva_photonid_pfchargedisogood03 );
    tmvaReaderID_Single_Barrel->AddVariable("ph.idmva_ChargedIso_worstvtx", &idvars.tmva_photonid_pfchargedisobad03 );
    tmvaReaderID_Single_Barrel->AddVariable("ph.sceta"		,   &idvars.tmva_photonid_sceta );
    tmvaReaderID_Single_Barrel->AddVariable("rho"		,   &idvars.tmva_photonid_eventrho );
    //found this files in aux of h2gglobe
    tmvaReaderID_Single_Barrel->BookMVA("AdaBoost", "aux/2012ICHEP_PhotonID_Barrel_BDT.weights.xml");

//    tmvaReaderID_Single_Endcap = new TMVA::Reader("!Color:Silent");
//    tmvaReaderID_Single_Endcap->AddVariable("ph.r9",   &tmva_photonid_r9 );
//    tmvaReaderID_Single_Endcap->AddVariable("ph.sigietaieta",   &tmva_photonid_sieie );
//    tmvaReaderID_Single_Endcap->AddVariable("ph.scetawidth",   &tmva_photonid_etawidth );
//    tmvaReaderID_Single_Endcap->AddVariable("ph.scphiwidth",   &tmva_photonid_phiwidth );
//    tmvaReaderID_Single_Endcap->AddVariable("ph.idmva_CoviEtaiPhi",   &tmva_photonid_sieip );
//    tmvaReaderID_Single_Endcap->AddVariable("ph.idmva_s4ratio",   &tmva_photonid_s4ratio );
//    tmvaReaderID_Single_Endcap->AddVariable("ph.idmva_GammaIso",   &tmva_photonid_pfphotoniso03 );
//    tmvaReaderID_Single_Endcap->AddVariable("ph.idmva_ChargedIso_selvtx",   &tmva_photonid_pfchargedisogood03 );
//    tmvaReaderID_Single_Endcap->AddVariable("ph.idmva_ChargedIso_worstvtx",   &tmva_photonid_pfchargedisobad03 );
//    tmvaReaderID_Single_Endcap->AddVariable("ph.sceta",   &tmva_photonid_sceta );
//    tmvaReaderID_Single_Endcap->AddVariable("rho",   &tmva_photonid_eventrho );
//    tmvaReaderID_Single_Endcap->AddVariable("ph.idmva_PsEffWidthSigmaRR",   &tmva_photonid_ESEffSigmaRR );

}

Analyzer::~Analyzer()
{}

void Analyzer::AddTree(const char *fileName)
{
	if(!fChain)fChain=new TChain("accepted/events");
	int N=fChain->Add(fileName);
	if(debug>0) std::cout<<"Added "<<N<<" Trees corresponding to filename: "<<string(fileName)<<endl;
}

Int_t Analyzer::GetEntry(Long64_t entry)
{
// Read contents of entry.
   if (!fChain) return 0;
   return fChain->GetEntry(entry);
}
Long64_t Analyzer::LoadTree(Long64_t entry)
{
// Set the environment to read one entry
   if (!fChain) return -5;
   Long64_t centry = fChain->LoadTree(entry);
   if (centry < 0) return centry;
   if (fChain->GetTreeNumber() != fCurrent) {
      fCurrent = fChain->GetTreeNumber();
   }
   return centry;
}

void Analyzer::Init()
{
   // Set object pointer
   if(debug>0)printf("INIT\n");
   photonPt = 0;
   photonE = 0;
   photonEta = 0;
   photonPhi = 0;
   photonPassConversionVeto = 0;
   photonPfIsoChargedHad = 0;
   photonPfIsoNeutralHad = 0;
   photonPfIsoPhoton = 0;
   photonPfIsoPhoton03ForCic = 0;
   photonPfIsoNeutrals03ForCic = 0;
   photonPfIsoCharged03ForCicVtx0 = 0;
   photonPfIsoCharged03BadForCic = 0;
   photonPfIsoPhoton04ForCic = 0;
   photonPfIsoNeutrals04ForCic = 0;
   photonPfIsoCharged04ForCicVtx0 = 0;
   photonPfIsoCharged04BadForCic = 0;
   photonid_sieie = 0;
   photonid_sieip = 0;
   photonid_etawidth = 0;
   photonid_phiwidth = 0;
   photonid_r9 = 0;
   photonid_lambdaRatio = 0;
   photonid_s4Ratio = 0;
   photonid_e25 = 0;
   photonid_sceta = 0;
   photonid_ESEffSigmaRR = 0;
   photonid_hadronicOverEm = 0;
   photonid_hadronicOverEm2012 = 0;
   photonhcalTowerSumEtConeDR04 = 0;
   photonecalRecHitSumEtConeDR04 = 0;
   photonnTrkSolidConeDR04 = 0;
   photontrkSumPtSolidConeDR04 = 0;
   photonnTrkHollowConeDR04 = 0;
   photontrkSumPtHollowConeDR04 = 0;
   photonIsoFPRCharged = 0;
   photonIsoFPRNeutral = 0;
   photonIsoFPRPhoton = 0;
   photonIsoFPRRandomConeCharged = 0;
   photonIsoFPRRandomConeNeutral = 0;
   photonIsoFPRRandomConePhoton = 0;
   photonBit = 0;
   TriMatchF4Path_photon = 0;
   fired = 0;
   prescaleL1 = 0;
   prescaleHLT = 0;
   lepPt = 0;
   lepEta = 0;
   lepPhi = 0;
   lepE = 0;
   lepPFIsoUnc = 0;
   lepPFIsoDBCor = 0;
   lepPFIsoRhoCor = 0;
   lepChId = 0;
   lepR9orChi2ndof = 0;
   lepId = 0;
   TriMatchF1Path_doubleMu = 0;
   TriMatchF2Path_doubleEle = 0;
   TriMatchF3Path_MuEle_muon = 0;
   TriMatchF3Path_MuEle_electron = 0;
   TriMatchF5Path_singleMu = 0;
   TriMatchF6Path_singleEle = 0;
   jetVeto = 0;
   jetPt = 0;
   jetPtRES = 0;
   jetPtRESup = 0;
   jetPtRESdown = 0;
   jetEta = 0;
   jetPhi = 0;
   jetE = 0;
   jetArea = 0;
   jetBeta = 0;
   jetQGL = 0;
   jetPdgId = 0;
   jetQGMLP = 0;
   jetQG_axis2_L = 0;
   jetQG_ptD_L = 0;
   jetQG_mult_L = 0;
   jetQG_axis1_MLP = 0;
   jetQG_axis2_MLP = 0;
   jetQG_ptD_MLP = 0;
   jetQG_mult_MLP = 0;
   jetRMS = 0;
   jetBtag = 0;
   jetTagInfoNVtx = 0;
   jetTagInfoNTracks = 0;
   jetTagInfoVtxMass = 0;
   jetMCFlavour = 0;
   jetJEC = 0;
   jetUNC = 0;
   jetllDPhi = 0;
   fwjetPt = 0;
   fwjetPtRES = 0;
   fwjetPtRESup = 0;
   fwjetPtRESdown = 0;
   fwjetEta = 0;
   fwjetPhi = 0;
   fwjetE = 0;
   vtxZ = 0;
   vtxNdof = 0;
   lepPtGEN = 0;
   lepEtaGEN = 0;
   lepPhiGEN = 0;
   lepEGEN = 0;
   lepChIdGEN = 0;
   lepMatchedDRGEN = 0;
   lepMatchedGEN = 0;
   jetPtGEN = 0;
   jetPtRESGEN = 0;
   jetPtRESupGEN = 0;
   jetPtRESdownGEN = 0;
   jetEtaGEN = 0;
   jetPhiGEN = 0;
   jetEGEN = 0;
   jetVetoGEN = 0;
   jetllDPhiGEN = 0;
   jetIdGEN = 0;
   jetNpartonsGEN = 0;
   lepSigmaIEtaIEta = 0;
   lepHadronicOverEm = 0;
   // Set branch addresses and branch pointers
if(debug>1) printf("-> SetBranchAddress A\n");
   fChain->SetBranchAddress("isRealData", &isRealData, &b_isRealData);
   fChain->SetBranchAddress("PUWeight", &PUWeight, &b_PUWeight);
if(debug>1) printf("-> SetBranchAddress A1\n");
   fChain->SetBranchAddress("eventNum", &eventNum, &b_eventNum);
   fChain->SetBranchAddress("runNum", &runNum, &b_runNum);
   fChain->SetBranchAddress("lumi", &lumi, &b_lumi);
   fChain->SetBranchAddress("nVtx", &nVtx, &b_nVtx);
   fChain->SetBranchAddress("nLeptons", &nLeptons, &b_nLeptons);
   fChain->SetBranchAddress("nPhotons", &nPhotons, &b_nPhotons);
   fChain->SetBranchAddress("nJets", &nJets, &b_nJets);
if(debug>1) printf("-> SetBranchAddress A2\n");
   fChain->SetBranchAddress("fwnJets", &fwnJets, &b_fwnJets);
   fChain->SetBranchAddress("rho", &rho, &b_rho);
   fChain->SetBranchAddress("rho25", &rho25, &b_rho25);
   fChain->SetBranchAddress("rhoQG", &rhoQG, &b_rhoQG);
   fChain->SetBranchAddress("pfmet", &pfmet, &b_pfmet);
   fChain->SetBranchAddress("pfmetPhi", &pfmetPhi, &b_pfmetPhi);
   fChain->SetBranchAddress("pfhadPt", &pfhadPt, &b_pfhadPt);
   fChain->SetBranchAddress("pfSumEt", &pfSumEt, &b_pfSumEt);
   fChain->SetBranchAddress("llM", &llM, &b_llM);
   fChain->SetBranchAddress("llPt", &llPt, &b_llPt);
   fChain->SetBranchAddress("llPhi", &llPhi, &b_llPhi);
   fChain->SetBranchAddress("llDPhi", &llDPhi, &b_llDPhi);
   fChain->SetBranchAddress("llY", &llY, &b_llY);
   fChain->SetBranchAddress("llEta", &llEta, &b_llEta);
if(debug>1) printf("-> SetBranchAddress B - photon vectors\n");
   fChain->SetBranchAddress("photonPt", &photonPt, &b_photonPt);
   fChain->SetBranchAddress("photonE", &photonE, &b_photonE);
   fChain->SetBranchAddress("photonEta", &photonEta, &b_photonEta);
   fChain->SetBranchAddress("photonPhi", &photonPhi, &b_photonPhi);
   fChain->SetBranchAddress("photonPassConversionVeto", &photonPassConversionVeto, &b_photonPassConversionVeto);
   fChain->SetBranchAddress("photonPfIsoChargedHad", &photonPfIsoChargedHad, &b_photonPfIsoChargedHad);
   fChain->SetBranchAddress("photonPfIsoNeutralHad", &photonPfIsoNeutralHad, &b_photonPfIsoNeutralHad);
   fChain->SetBranchAddress("photonPfIsoPhoton", &photonPfIsoPhoton, &b_photonPfIsoPhoton);
   fChain->SetBranchAddress("photonPfIsoPhoton03ForCic", &photonPfIsoPhoton03ForCic, &b_photonPfIsoPhoton03ForCic);
   fChain->SetBranchAddress("photonPfIsoNeutrals03ForCic", &photonPfIsoNeutrals03ForCic, &b_photonPfIsoNeutrals03ForCic);
   fChain->SetBranchAddress("photonPfIsoCharged03ForCicVtx0", &photonPfIsoCharged03ForCicVtx0, &b_photonPfIsoCharged03ForCicVtx0);
   fChain->SetBranchAddress("photonPfIsoCharged03BadForCic", &photonPfIsoCharged03BadForCic, &b_photonPfIsoCharged03BadForCic);
   fChain->SetBranchAddress("photonPfIsoPhoton04ForCic", &photonPfIsoPhoton04ForCic, &b_photonPfIsoPhoton04ForCic);
   fChain->SetBranchAddress("photonPfIsoNeutrals04ForCic", &photonPfIsoNeutrals04ForCic, &b_photonPfIsoNeutrals04ForCic);
   fChain->SetBranchAddress("photonPfIsoCharged04ForCicVtx0", &photonPfIsoCharged04ForCicVtx0, &b_photonPfIsoCharged04ForCicVtx0);
   fChain->SetBranchAddress("photonPfIsoCharged04BadForCic", &photonPfIsoCharged04BadForCic, &b_photonPfIsoCharged04BadForCic);
   fChain->SetBranchAddress("photonid_sieie", &photonid_sieie, &b_photonid_sieie);
   fChain->SetBranchAddress("photonid_sieip", &photonid_sieip, &b_photonid_sieip);
   fChain->SetBranchAddress("photonid_etawidth", &photonid_etawidth, &b_photonid_etawidth);
   fChain->SetBranchAddress("photonid_phiwidth", &photonid_phiwidth, &b_photonid_phiwidth);
   fChain->SetBranchAddress("photonid_r9", &photonid_r9, &b_photonid_r9);
   fChain->SetBranchAddress("photonid_lambdaRatio", &photonid_lambdaRatio, &b_photonid_lambdaRatio);
   fChain->SetBranchAddress("photonid_s4Ratio", &photonid_s4Ratio, &b_photonid_s4Ratio);
   fChain->SetBranchAddress("photonid_e25", &photonid_e25, &b_photonid_e25);
   fChain->SetBranchAddress("photonid_sceta", &photonid_sceta, &b_photonid_sceta);
   fChain->SetBranchAddress("photonid_ESEffSigmaRR", &photonid_ESEffSigmaRR, &b_photonid_ESEffSigmaRR);
   fChain->SetBranchAddress("photonid_hadronicOverEm", &photonid_hadronicOverEm, &b_photonid_hadronicOverEm);
   fChain->SetBranchAddress("photonid_hadronicOverEm2012", &photonid_hadronicOverEm2012, &b_photonid_hadronicOverEm2012);
   fChain->SetBranchAddress("photonhcalTowerSumEtConeDR04", &photonhcalTowerSumEtConeDR04, &b_photonhcalTowerSumEtConeDR04);
   fChain->SetBranchAddress("photonecalRecHitSumEtConeDR04", &photonecalRecHitSumEtConeDR04, &b_photonecalRecHitSumEtConeDR04);
   fChain->SetBranchAddress("photonnTrkSolidConeDR04", &photonnTrkSolidConeDR04, &b_photonnTrkSolidConeDR04);
   fChain->SetBranchAddress("photontrkSumPtSolidConeDR04", &photontrkSumPtSolidConeDR04, &b_photontrkSumPtSolidConeDR04);
   fChain->SetBranchAddress("photonnTrkHollowConeDR04", &photonnTrkHollowConeDR04, &b_photonnTrkHollowConeDR04);
   fChain->SetBranchAddress("photontrkSumPtHollowConeDR04", &photontrkSumPtHollowConeDR04, &b_photontrkSumPtHollowConeDR04);
   fChain->SetBranchAddress("photonIsoFPRCharged", &photonIsoFPRCharged, &b_photonIsoFPRCharged);
   fChain->SetBranchAddress("photonIsoFPRNeutral", &photonIsoFPRNeutral, &b_photonIsoFPRNeutral);
   fChain->SetBranchAddress("photonIsoFPRPhoton", &photonIsoFPRPhoton, &b_photonIsoFPRPhoton);
   fChain->SetBranchAddress("photonIsoFPRRandomConeCharged", &photonIsoFPRRandomConeCharged, &b_photonIsoFPRRandomConeCharged);
   fChain->SetBranchAddress("photonIsoFPRRandomConeNeutral", &photonIsoFPRRandomConeNeutral, &b_photonIsoFPRRandomConeNeutral);
   fChain->SetBranchAddress("photonIsoFPRRandomConePhoton", &photonIsoFPRRandomConePhoton, &b_photonIsoFPRRandomConePhoton);
   fChain->SetBranchAddress("photonBit", &photonBit, &b_photonBit);
   fChain->SetBranchAddress("TriMatchF4Path_photon", &TriMatchF4Path_photon, &b_TriMatchF4Path_photon);
   fChain->SetBranchAddress("fired", &fired, &b_fired);
   fChain->SetBranchAddress("prescaleL1", &prescaleL1, &b_prescaleL1);
   fChain->SetBranchAddress("prescaleHLT", &prescaleHLT, &b_prescaleHLT);
   fChain->SetBranchAddress("isTriggered", &isTriggered, &b_isTriggered);
   fChain->SetBranchAddress("lepPt", &lepPt, &b_lepPt);
   fChain->SetBranchAddress("lepEta", &lepEta, &b_lepEta);
   fChain->SetBranchAddress("lepPhi", &lepPhi, &b_lepPhi);
   fChain->SetBranchAddress("lepE", &lepE, &b_lepE);
   fChain->SetBranchAddress("lepPFIsoUnc", &lepPFIsoUnc, &b_lepPFIsoUnc);
   fChain->SetBranchAddress("lepPFIsoDBCor", &lepPFIsoDBCor, &b_lepPFIsoDBCor);
   fChain->SetBranchAddress("lepPFIsoRhoCor", &lepPFIsoRhoCor, &b_lepPFIsoRhoCor);
   fChain->SetBranchAddress("lepChId", &lepChId, &b_lepChId);
   fChain->SetBranchAddress("lepR9orChi2ndof", &lepR9orChi2ndof, &b_lepR9orChi2ndof);
   fChain->SetBranchAddress("lepId", &lepId, &b_lepId);
   fChain->SetBranchAddress("TriMatchF1Path_doubleMu", &TriMatchF1Path_doubleMu, &b_TriMatchF1Path_doubleMu);
   fChain->SetBranchAddress("TriMatchF2Path_doubleEle", &TriMatchF2Path_doubleEle, &b_TriMatchF2Path_doubleEle);
   fChain->SetBranchAddress("TriMatchF3Path_MuEle_muon", &TriMatchF3Path_MuEle_muon, &b_TriMatchF3Path_MuEle_muon);
   fChain->SetBranchAddress("TriMatchF3Path_MuEle_electron", &TriMatchF3Path_MuEle_electron, &b_TriMatchF3Path_MuEle_electron);
   fChain->SetBranchAddress("TriMatchF5Path_singleMu", &TriMatchF5Path_singleMu, &b_TriMatchF5Path_singleMu);
   fChain->SetBranchAddress("TriMatchF6Path_singleEle", &TriMatchF6Path_singleEle, &b_TriMatchF6Path_singleEle);
   fChain->SetBranchAddress("jetVeto", &jetVeto, &b_jetVeto);
   fChain->SetBranchAddress("jetPt", &jetPt, &b_jetPt);
   fChain->SetBranchAddress("jetPtRES", &jetPtRES, &b_jetPtRES);
   fChain->SetBranchAddress("jetPtRESup", &jetPtRESup, &b_jetPtRESup);
   fChain->SetBranchAddress("jetPtRESdown", &jetPtRESdown, &b_jetPtRESdown);
   fChain->SetBranchAddress("jetEta", &jetEta, &b_jetEta);
   fChain->SetBranchAddress("jetPhi", &jetPhi, &b_jetPhi);
   fChain->SetBranchAddress("jetE", &jetE, &b_jetE);
   fChain->SetBranchAddress("jetArea", &jetArea, &b_jetArea);
   fChain->SetBranchAddress("jetBeta", &jetBeta, &b_jetBeta);
   fChain->SetBranchAddress("jetQGL", &jetQGL, &b_jetQGL);
   fChain->SetBranchAddress("jetPdgId", &jetPdgId, &b_jetPdgId);
   fChain->SetBranchAddress("jetQGMLP", &jetQGMLP, &b_jetQGMLP);
   fChain->SetBranchAddress("jetQG_axis2_L", &jetQG_axis2_L, &b_jetQG_axis2_L);
   fChain->SetBranchAddress("jetQG_ptD_L", &jetQG_ptD_L, &b_jetQG_ptD_L);
   fChain->SetBranchAddress("jetQG_mult_L", &jetQG_mult_L, &b_jetQG_mult_L);
   fChain->SetBranchAddress("jetQG_axis1_MLP", &jetQG_axis1_MLP, &b_jetQG_axis1_MLP);
   fChain->SetBranchAddress("jetQG_axis2_MLP", &jetQG_axis2_MLP, &b_jetQG_axis2_MLP);
   fChain->SetBranchAddress("jetQG_ptD_MLP", &jetQG_ptD_MLP, &b_jetQG_ptD_MLP);
   fChain->SetBranchAddress("jetQG_mult_MLP", &jetQG_mult_MLP, &b_jetQG_mult_MLP);
   fChain->SetBranchAddress("jetRMS", &jetRMS, &b_jetRMS);
   fChain->SetBranchAddress("jetBtag", &jetBtag, &b_jetBtag);
   fChain->SetBranchAddress("jetTagInfoNVtx", &jetTagInfoNVtx, &b_jetTagInfoNVtx);
   fChain->SetBranchAddress("jetTagInfoNTracks", &jetTagInfoNTracks, &b_jetTagInfoNTracks);
   fChain->SetBranchAddress("jetTagInfoVtxMass", &jetTagInfoVtxMass, &b_jetTagInfoVtxMass);
   fChain->SetBranchAddress("jetMCFlavour", &jetMCFlavour, &b_jetMCFlavour);
   fChain->SetBranchAddress("jetJEC", &jetJEC, &b_jetJEC);
   fChain->SetBranchAddress("jetUNC", &jetUNC, &b_jetUNC);
   fChain->SetBranchAddress("jetllDPhi", &jetllDPhi, &b_jetllDPhi);
   fChain->SetBranchAddress("fwjetPt", &fwjetPt, &b_fwjetPt);
   fChain->SetBranchAddress("fwjetPtRES", &fwjetPtRES, &b_fwjetPtRES);
   fChain->SetBranchAddress("fwjetPtRESup", &fwjetPtRESup, &b_fwjetPtRESup);
   fChain->SetBranchAddress("fwjetPtRESdown", &fwjetPtRESdown, &b_fwjetPtRESdown);
   fChain->SetBranchAddress("fwjetEta", &fwjetEta, &b_fwjetEta);
   fChain->SetBranchAddress("fwjetPhi", &fwjetPhi, &b_fwjetPhi);
   fChain->SetBranchAddress("fwjetE", &fwjetE, &b_fwjetE);
   fChain->SetBranchAddress("vtxZ", &vtxZ, &b_vtxZ);
   fChain->SetBranchAddress("vtxNdof", &vtxNdof, &b_vtxNdof);
   fChain->SetBranchAddress("puINT", &puINT, &b_puINT);
   fChain->SetBranchAddress("puOOT", &puOOT, &b_puOOT);
   fChain->SetBranchAddress("puTrueINT", &puTrueINT, &b_puTrueINT);
   fChain->SetBranchAddress("puTrueOOT", &puTrueOOT, &b_puTrueOOT);
   fChain->SetBranchAddress("nLeptonsGEN", &nLeptonsGEN, &b_nLeptonsGEN);
   fChain->SetBranchAddress("nJetsGEN", &nJetsGEN, &b_nJetsGEN);
   fChain->SetBranchAddress("llMGEN", &llMGEN, &b_llMGEN);
   fChain->SetBranchAddress("llPtGEN", &llPtGEN, &b_llPtGEN);
   fChain->SetBranchAddress("llPhiGEN", &llPhiGEN, &b_llPhiGEN);
   fChain->SetBranchAddress("llDPhiGEN", &llDPhiGEN, &b_llDPhiGEN);
   fChain->SetBranchAddress("llYGEN", &llYGEN, &b_llYGEN);
   fChain->SetBranchAddress("llEtaGEN", &llEtaGEN, &b_llEtaGEN);
   fChain->SetBranchAddress("lepPtGEN", &lepPtGEN, &b_lepPtGEN);
   fChain->SetBranchAddress("lepEtaGEN", &lepEtaGEN, &b_lepEtaGEN);
   fChain->SetBranchAddress("lepPhiGEN", &lepPhiGEN, &b_lepPhiGEN);
   fChain->SetBranchAddress("lepEGEN", &lepEGEN, &b_lepEGEN);
   fChain->SetBranchAddress("lepChIdGEN", &lepChIdGEN, &b_lepChIdGEN);
   fChain->SetBranchAddress("lepMatchedDRGEN", &lepMatchedDRGEN, &b_lepMatchedDRGEN);
   fChain->SetBranchAddress("lepMatchedGEN", &lepMatchedGEN, &b_lepMatchedGEN);
   fChain->SetBranchAddress("jetPtGEN", &jetPtGEN, &b_jetPtGEN);
   fChain->SetBranchAddress("jetPtRESGEN", &jetPtRESGEN, &b_jetPtRESGEN);
   fChain->SetBranchAddress("jetPtRESupGEN", &jetPtRESupGEN, &b_jetPtRESupGEN);
   fChain->SetBranchAddress("jetPtRESdownGEN", &jetPtRESdownGEN, &b_jetPtRESdownGEN);
   fChain->SetBranchAddress("jetEtaGEN", &jetEtaGEN, &b_jetEtaGEN);
   fChain->SetBranchAddress("jetPhiGEN", &jetPhiGEN, &b_jetPhiGEN);
   fChain->SetBranchAddress("jetEGEN", &jetEGEN, &b_jetEGEN);
   fChain->SetBranchAddress("jetVetoGEN", &jetVetoGEN, &b_jetVetoGEN);
   fChain->SetBranchAddress("jetllDPhiGEN", &jetllDPhiGEN, &b_jetllDPhiGEN);
   fChain->SetBranchAddress("jetIdGEN", &jetIdGEN, &b_jetIdGEN);
   fChain->SetBranchAddress("jetNpartonsGEN", &jetNpartonsGEN, &b_jetNpartonsGEN);
   fChain->SetBranchAddress("HTParSum", &HTParSum, &b_HTParSum);
   fChain->SetBranchAddress("nParton", &nParton, &b_nParton);
   fChain->SetBranchAddress("mcWeight", &mcWeight, &b_mcWeight);
   fChain->SetBranchAddress("qScale", &qScale, &b_qScale);
   fChain->SetBranchAddress("alphaQED", &alphaQED, &b_alphaQED);
   fChain->SetBranchAddress("alphaQCD", &alphaQCD, &b_alphaQCD);
   fChain->SetBranchAddress("x1", &x1, &b_x1);
   fChain->SetBranchAddress("x2", &x2, &b_x2);
   fChain->SetBranchAddress("pdf1Id", &pdf1Id, &b_pdf1Id);
   fChain->SetBranchAddress("pdf2Id", &pdf2Id, &b_pdf2Id);
   fChain->SetBranchAddress("scalePDF", &scalePDF, &b_scalePDF);
   fChain->SetBranchAddress("nPhotonsGEN", &nPhotonsGEN, &b_nPhotonsGEN);
   fChain->SetBranchAddress("photonPtGEN", &photonPtGEN, &b_photonPtGEN);
   fChain->SetBranchAddress("photonEGEN", &photonEGEN, &b_photonEGEN);
   fChain->SetBranchAddress("photonEtaGEN", &photonEtaGEN, &b_photonEtaGEN);
   fChain->SetBranchAddress("photonPhiGEN", &photonPhiGEN, &b_photonPhiGEN);
   fChain->SetBranchAddress("photonIsoPtDR03GEN", &photonIsoPtDR03GEN, &b_photonIsoPtDR03GEN);
   fChain->SetBranchAddress("photonIsoSumPtDR03GEN", &photonIsoSumPtDR03GEN, &b_photonIsoSumPtDR03GEN);
   fChain->SetBranchAddress("photonIsoEDR03GEN", &photonIsoEDR03GEN, &b_photonIsoEDR03GEN);
   fChain->SetBranchAddress("photonIsoPtDR04GEN", &photonIsoPtDR04GEN, &b_photonIsoPtDR04GEN);
   fChain->SetBranchAddress("photonIsoSumPtDR04GEN", &photonIsoSumPtDR04GEN, &b_photonIsoSumPtDR04GEN);
   fChain->SetBranchAddress("photonIsoEDR04GEN", &photonIsoEDR04GEN, &b_photonIsoEDR04GEN);
   fChain->SetBranchAddress("photonIsoPtDR05GEN", &photonIsoPtDR05GEN, &b_photonIsoPtDR05GEN);
   fChain->SetBranchAddress("photonIsoSumPtDR05GEN", &photonIsoSumPtDR05GEN, &b_photonIsoSumPtDR05GEN);
   fChain->SetBranchAddress("photonIsoEDR05GEN", &photonIsoEDR05GEN, &b_photonIsoEDR05GEN);
   fChain->SetBranchAddress("photonMotherIdGEN", &photonMotherIdGEN, &b_photonMotherIdGEN);
   fChain->SetBranchAddress("photonRECODRGEN", &photonRECODRGEN, &b_photonRECODRGEN);
   fChain->SetBranchAddress("VBPartonDM", &VBPartonDM, &b_VBPartonDM);
   fChain->SetBranchAddress("VBPartonM", &VBPartonM, &b_VBPartonM);
   fChain->SetBranchAddress("VBPartonE", &VBPartonE, &b_VBPartonE);
   fChain->SetBranchAddress("VBPartonPt", &VBPartonPt, &b_VBPartonPt);
   fChain->SetBranchAddress("VBPartonEta", &VBPartonEta, &b_VBPartonEta);
   fChain->SetBranchAddress("VBPartonPhi", &VBPartonPhi, &b_VBPartonPhi);
   fChain->SetBranchAddress("lepSigmaIEtaIEta", &lepSigmaIEtaIEta, &b_lepSigmaIEtaIEta);
   fChain->SetBranchAddress("lepHadronicOverEm", &lepHadronicOverEm, &b_lepHadronicOverEm);
   if(loadMVA)InitMVA();
   InitCuts();
   if(useEffArea)InitEffArea();
}
#endif
