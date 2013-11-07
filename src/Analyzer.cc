#define Analyzer_cxx
#include "Analyzer.h"
#include <TH2.h>
#include <TStyle.h>
#include <TCanvas.h>
#include "TDirectory.h"

//
void Analyzer::MakeTree(string name){
	treeContainer[name]=new TTree(name.c_str(),name.c_str());
	treeContainer[name]->Branch("photoniso",&TreeVar.photoniso,"photoniso/F");

}

void Analyzer::Loop()
{
    if(debug>0)printf("start loop\n");
    fChain->SetBranchStatus("*",0);  // disable all branches
    fChain->SetBranchStatus("photon*",1);  // activate branchname
    fChain->SetBranchStatus("jetPt",1);  // activate branchname
    fChain->SetBranchStatus("jetEta",1);  // activate branchname
    fChain->SetBranchStatus("jetPhi",1);  // activate branchname
    fChain->SetBranchStatus("jetE",1);  // activate branchname
    fChain->SetBranchStatus("jetBeta",1);  // activate branchname
    fChain->SetBranchStatus("jetRMS",1);  // activate branchname
    fChain->SetBranchStatus("jetUNC",1);  // activate branchname
    fChain->SetBranchStatus("prescale*",1);  // activate branchname
    fChain->SetBranchStatus("TriMatchF4Path_photon",1);  // activate branchname
    fChain->SetBranchStatus("rho",1);  // activate branchname
    fChain->SetBranchStatus("nVtx",1);  // activate branchname
    fChain->SetBranchStatus("runNum",1);  // activate branchname
    fChain->SetBranchStatus("isRealData",1);  // activate branchname
    fChain->SetBranchStatus("jetPtRES*",1);  // activate branchname
    if (fChain == 0) return;
//	fChain->GetEntry(0); done in init
   if(!isRealData) {
	if(debug>0)printf("Running on mc: activating branches\n");
    	fChain->SetBranchStatus("PUWeight*",1);  // activate branchname
    	fChain->SetBranchStatus("eventWeight*",1);  // activate branchname
	fChain->SetBranchStatus("photon*GEN",1);
	fChain->SetBranchStatus("jet*GEN",1);
	}

   //exit if syst does not make sense for data or mc	
   if(currentSyst == SYST::PUUP && isRealData) return;	
   if(currentSyst == SYST::PUDN && isRealData) return;	
   if(currentSyst == SYST::JERUP && isRealData) return;	
   if(currentSyst == SYST::JERDN && isRealData) return;	
   if(currentSyst == SYST::UNFOLD ) return;	
   if(currentSyst == SYST::SIGSHAPE ) return;	
   if(currentSyst == SYST::BKGSHAPE ) return;	
   if(currentSyst == SYST::FIT ) return;	
   if(currentSyst == SYST::LUMIUP ) return;	
   if(currentSyst == SYST::LUMIDN ) return;	

   Long64_t nentries = fChain->GetEntries();

   //bins for matrix
   Float_t ptbinsForMatrix[1023];int nbinsForMatrix=-1;
   //ptbinsForMatrix[nbinsForMatrix]=0;
   for(int iPt=0;iPt<int(PtCuts.size()) && PtCuts[iPt]>0;iPt++)
   	{nbinsForMatrix++;ptbinsForMatrix[nbinsForMatrix]=PtCuts[iPt];}
   //
   const double EtaMax=1.4;
	printf("ETA =1.0\n");

   for (Long64_t jentry=0; jentry<nentries;jentry++) {
	//select jobs
	//if(  (  nJobs >0)  && ( jentry%nJobs!=jobId) ) continue; // slow on eos
	if( (nJobs >0) && ( jentry< (nentries/nJobs+1)*jobId  || jentry >= (nentries/nJobs+1)*(jobId+1) ) ) continue; // +1 instead of doing ceil. 

	if(debug>1)printf("-> Loding entry %lld\n",jentry);
     // Long64_t ientry = LoadTree(jentry);
	if( (jentry%10000)==0 && debug>0) printf("-> Getting entry %lld/%lld\n",jentry,nentries);
	fChain->GetEntry(jentry);
	if(currentSyst==SYST::NONE)Sel->FillAndInit("All"); //Selection
	//SYST SMEARINGS
	Smear();
     // if (ientry < 0) break;

	int GammaIdxGEN=-1;
	int HtGEN=0;
	int mynJetsGEN=0;
	vector<int> JetIdxGEN;

	if(!isRealData) //only MC
	{
		//look for Gamma	
			if( fabs(photonEtaGEN)<EtaMax && photonPtGEN>=0  && photonIsoSumPtDR04GEN < 5) { // photonPtGEN=-999 initialized
			//isolation at GEN LEVEL - tighter than the preselection abs = 10
			//pass all selections
			GammaIdxGEN=1;
			}
		TLorentzVector gGEN;
			gGEN.SetPtEtaPhiE( photonPtGEN,photonEtaGEN,photonPhiGEN,photonEGEN);
		//look for Jets
		for(int iJetGEN=0;iJetGEN< int(jetPtGEN->size());iJetGEN++)
			{
			if((*jetPtGEN)[iJetGEN]<30) continue;
			TLorentzVector jGEN;
				jGEN.SetPtEtaPhiE((*jetPtGEN)[iJetGEN],(*jetEtaGEN)[iJetGEN],(*jetPhiGEN)[iJetGEN],(*jetEGEN)[iJetGEN]);
			if(jGEN.DeltaR(gGEN)<0.5) continue;
			//pass all selection
			mynJetsGEN++;
			HtGEN+=jGEN.Pt();
			JetIdxGEN.push_back(iJetGEN);
			}
		/////---end of object selection---
		
		for(int iCut=0;iCut<int(cutsContainer.size());++iCut)
			{
			if( GammaIdxGEN <0 ) break; //gamma not selected
			if(gGEN.Pt() < cutsContainer[iCut].VPt.first)continue;
			if(gGEN.Pt() > cutsContainer[iCut].VPt.second)continue;
			if(HtGEN         < cutsContainer[iCut].Ht.first)continue;
			if(HtGEN         > cutsContainer[iCut].Ht.second)continue;
		//	if((*photonid_sieie)[GammaIdx]         < cutsContainer[iCut].phid.first)continue;
		//	if((*photonid_sieie)[GammaIdx]         >= cutsContainer[iCut].phid.second)continue;
			if( mynJetsGEN < cutsContainer[iCut].nJets) continue;
			
			//Going to fill
			//-----
			{
				string name=string("gammaPtGEN_")+cutsContainer[iCut].name()+SystName();
					if(histoContainer[name]==NULL){ histoContainer[name]=new TH1D(name.c_str(),name.c_str(),nbinsForMatrix,ptbinsForMatrix);histoContainer[name]->Sumw2();}
				histoContainer[name]->Fill(gGEN.Pt(),eventWeight);
			}
			{
				string name=string("gammaEtaGEN_")+cutsContainer[iCut].name()+SystName();
					if(histoContainer[name]==NULL){ histoContainer[name]=new TH1D(name.c_str(),name.c_str(),binsContainer["gammaEta"].nBins,binsContainer["gammaEta"].xMin,binsContainer["gammaEta"].xMax);histoContainer[name]->Sumw2();}
				histoContainer[name]->Fill(gGEN.Eta(),eventWeight);
			}
			//-----
			} // iCut
	} //isMC
	
	Int_t GammaIdx=-1;
	float GammaMVA=-999;
	float ScaleTrigger=1.0;
	float RhoCorr=0;
	if(debug>1)printf("-> Starting GammaLoop\n");
	for(Int_t iGamma=0;iGamma<Int_t(photonPt->size());++iGamma)
		{
		if(currentSyst==SYST::NONE)Sel2->FillAndInit("All"); //Selection
		//TODO Gamma ID with CiC
		//if( photonid_hadronicOverEm2012->at(iGamma) >0.1 ) continue;	
			//set variables for tmva
       			 idvars.tmva_photonid_r9			=(*photonid_r9)[iGamma];
       			 idvars.tmva_photonid_sieie			=(*photonid_sieie)[iGamma];
       			 idvars.tmva_photonid_etawidth			=(*photonid_etawidth)[iGamma];
       			 idvars.tmva_photonid_phiwidth			=(*photonid_phiwidth)[iGamma];
       			 idvars.tmva_photonid_sieip			=(*photonid_sieip)[iGamma];
       			 idvars.tmva_photonid_s4ratio			=(*photonid_s4Ratio)[iGamma];
       			 idvars.tmva_photonid_pfphotoniso03		=(*photonPfIsoPhoton03ForCic)[iGamma];
       			 idvars.tmva_photonid_pfchargedisogood03	=(*photonPfIsoCharged03ForCicVtx0)[iGamma];
       			 idvars.tmva_photonid_pfchargedisobad03		=(*photonPfIsoCharged03BadForCic)[iGamma];
       			 idvars.tmva_photonid_sceta			=(*photonid_sceta)[iGamma];
       			 idvars.tmva_photonid_eventrho			=rho; //TODO check that it is the correct rho
		//compute mva
		if(loadMVA)
			GammaMVA = tmvaReaderID_Single_Barrel->EvaluateMVA("AdaBoost");
		//if (GammaMVA <-.1)continue; //comment? -> no id use this to cut instead of sieie? - better sieie is less correleted with iso. Otherwise the id will use iso to kill the bkg
		//select the leading photon in |eta|<1.4
		if(fabs( (*photonEta)[iGamma] )>=EtaMax ) continue;
		if(currentSyst==SYST::NONE)Sel2->FillAndInit("Eta"); //Selection
		//loose iso req
	//compute RhoCorrections
	if(useEffArea){
		//search in the database for the correct bin
   		for(map<string,float>::iterator it=effAreaCorr.begin();it!=effAreaCorr.end();it++)
		{
		string name=it->first;
		float ptmin,ptmax,etamin,etamax;
  		sscanf(name.c_str(),"%f_%f_%f_%f",&ptmin,&ptmax,&etamin,&etamax);
		//fprintf(stderr,"GPt=%f pt in [%f,%f] GETA=%f et=[%f,%f]\n",gamma.Pt(),ptmin,ptmax,gamma.Eta(),etamin,etamax);
		if( (*photonPt)[iGamma]>ptmin && (*photonPt)[iGamma]<ptmax && fabs((*photonEta)[iGamma])> etamin && fabs((*photonEta)[iGamma]) <etamax)
			{
			RhoCorr= it->second * rho;
			}
		
		}
	} //RhoCorr

		if( int((*photonPassConversionVeto)[iGamma]) == 0  ) continue; //it is a float, why - always 1 .
		//---- OLD
		//if( (*photonid_hadronicOverEm)[iGamma] >0.05) continue; 
		//if(currentSyst==SYST::NONE)Sel2->FillAndInit("HoE"); //Selection
		//if( (*photonPfIsoChargedHad)[iGamma]>1.5) continue;
		//if(currentSyst==SYST::NONE)Sel2->FillAndInit("IsoCharged"); //Selection
		//if( (*photonPfIsoNeutralHad)[iGamma]>1.0+ 0.04*(*photonPt)[iGamma]) continue;
		//if(currentSyst==SYST::NONE)Sel2->FillAndInit("IsoNeutral"); //Selection
		////if( (*photonPfIsoPhoton)[iGamma]>0.7+0.005*(*photonPt)[iGamma]) continue;
		
		//PRESELECTION H-GG
		if( (*photonid_sieie)[iGamma] >0.014) continue;
		if(currentSyst==SYST::NONE)Sel2->FillAndInit("SieieLoose");
		if( (*photonid_r9)[iGamma]>0.9){
			if( (*photonid_hadronicOverEm)[iGamma] >0.082) continue; 
			if(currentSyst==SYST::NONE)Sel2->FillAndInit("HoE"); //Selection
			if( (*photonhcalTowerSumEtConeDR04)[iGamma]*9./16. > 50 + 0.005*(*photonPt)[iGamma] )continue;
			if(currentSyst==SYST::NONE)Sel2->FillAndInit("hcalIso"); //Selection
			if( (*photontrkSumPtHollowConeDR04)[iGamma]*9./16. > 50 + 0.002*(*photonPt)[iGamma] )continue;
			if(currentSyst==SYST::NONE)Sel2->FillAndInit("trkIso"); //Selection
		}
		else{
			if( (*photonid_hadronicOverEm)[iGamma] >0.075) continue; 
			if(currentSyst==SYST::NONE)Sel2->FillAndInit("HoE"); //Selection
			if( (*photonhcalTowerSumEtConeDR04)[iGamma]*9./16. > 4 + 0.005*(*photonPt)[iGamma] )continue;
			if(currentSyst==SYST::NONE)Sel2->FillAndInit("hcalIso"); //Selection
			if( (*photontrkSumPtHollowConeDR04)[iGamma]*9./16. > 4 + 0.002*(*photonPt)[iGamma] )continue;
			if(currentSyst==SYST::NONE)Sel2->FillAndInit("trkIso"); //Selection
		}
		if( (*photonPfIsoCharged03ForCicVtx0)[iGamma]* 4./9. > 4 ) continue;
			if(currentSyst==SYST::NONE)Sel2->FillAndInit("chgIso"); //Selection
		if( (*photonIsoFPRPhoton)[iGamma]-RhoCorr>10) continue;  // loose 
		if(currentSyst==SYST::NONE)Sel2->FillAndInit("IsoPhoton"); //Selection
		
	
		unsigned long long trigger=TriMatchF4Path_photon->at(iGamma);
		string triggerMenu="";
		
		for(map<string,pair<float,float> >::iterator it=triggerMenus.begin();it!=triggerMenus.end();it++)
			{
			if( (*photonPt)[iGamma] >= it->second.first && (*photonPt)[iGamma] < it->second.second )
				{
				triggerMenu=it->first;
				}
			}
		if(isRealData) 
		//if(true)
		{
		if(triggerMenu=="") continue; //doesn't have a trigger selection
		else if(triggerMenu=="HLT_Photon20_CaloIdVL_v*"  && !(trigger &  1     ) ) continue;
		else if(triggerMenu=="HLT_Photon20_CaloIdVL_IsoL_v*"  && !(trigger &  2     ) ) continue;
		else if(triggerMenu=="HLT_Photon30_v*"  && !(trigger &  4     ) ) continue;
		else if(triggerMenu=="HLT_Photon30_CaloIdVL_v*"  && !(trigger &  8     ) ) continue;
		else if(triggerMenu=="HLT_Photon30_CaloIdVL_IsoL_v*"  && !(trigger &  16    ) ) continue;
		else if(triggerMenu=="HLT_Photon50_CaloIdVL_v*"  && !(trigger &  32    ) ) continue;
		else if(triggerMenu=="HLT_Photon50_CaloIdVL_IsoL_v*"  && !(trigger &  64    ) ) continue;
		else if(triggerMenu=="HLT_Photon75_CaloIdVL_v*"  && !(trigger &  128   ) ) continue;
		else if(triggerMenu=="HLT_Photon75_CaloIdVL_IsoL_v*"  && !(trigger &  256   ) ) continue;
		else if(triggerMenu=="HLT_Photon90_CaloIdVL_v*"  && !(trigger &  512   ) ) continue;
		else if(triggerMenu=="HLT_Photon90_CaloIdVL_IsoL_v*"  && !(trigger &  1024  ) ) continue;
		else if(triggerMenu=="HLT_Photon135_v*"  && !(trigger &  2048  ) ) continue;
		else if(triggerMenu=="HLT_Photon150_v*"  && !(trigger &  4096  ) ) continue;
		//trigger -- from twiki
		//	0000000000001 	1 	HLT_Photon20_CaloIdVL_v*
		//  	0000000000010 	2 	HLT_Photon20_CaloIdVL_IsoL_v*
		//  	0000000000100 	4 	HLT_Photon30_v*
		//  	0000000001000 	8 	HLT_Photon30_CaloIdVL_v*
		//  	0000000010000 	16 	HLT_Photon30_CaloIdVL_IsoL_v*
		//  	0000000100000 	32 	HLT_Photon50_CaloIdVL_v*
		//  	0000001000000 	64 	HLT_Photon50_CaloIdVL_IsoL_v*
		//  	0000010000000 	128 	HLT_Photon75_CaloIdVL_v*
		//  	0000100000000 	256 	HLT_Photon75_CaloIdVL_IsoL_v*
		//  	0001000000000 	512 	HLT_Photon90_CaloIdVL_v*
		//  	0010000000000 	1024 	HLT_Photon90_CaloIdVL_IsoL_v*
		//  	0100000000000 	2048 	HLT_Photon135_v*
		//  	1000000000000 	4096 	HLT_Photon150_v* 
		ScaleTrigger=triggerScales[triggerMenu];
		}//DATA
		else
		ScaleTrigger=1; //MC --> Check What we can do -- & for GEN?

		if(usePUWeightHLT && !isRealData)
			{
			if(triggerMenu == "HLT_Photon150_v*") {PUWeight=PUWeightHLT_Photon150; PUWeightSysUp=PUWeightHLT_Photon150SysUp;PUWeightSysDown=PUWeightHLT_Photon150SysDown;}
			if(triggerMenu == "HLT_Photon135_v*") {PUWeight=PUWeightHLT_Photon135; PUWeightSysUp=PUWeightHLT_Photon135SysUp;PUWeightSysDown=PUWeightHLT_Photon135SysDown;}
			if(triggerMenu == "HLT_Photon90_CaloIdVL_v*") {PUWeight=PUWeightHLT_Photon90; PUWeightSysUp=PUWeightHLT_Photon90SysUp;PUWeightSysDown=PUWeightHLT_Photon90SysDown;}
			if(triggerMenu == "HLT_Photon75_CaloIdVL_v*") {PUWeight=PUWeightHLT_Photon75; PUWeightSysUp=PUWeightHLT_Photon75SysUp;PUWeightSysDown=PUWeightHLT_Photon75SysDown;}
			if(triggerMenu == "HLT_Photon50_CaloIdVL_v*") {PUWeight=PUWeightHLT_Photon50; PUWeightSysUp=PUWeightHLT_Photon50SysUp;PUWeightSysDown=PUWeightHLT_Photon50SysDown;}
			if(triggerMenu == "HLT_Photon30_CaloIdVL_v*") {PUWeight=PUWeightHLT_Photon30; PUWeightSysUp=PUWeightHLT_Photon30SysUp;PUWeightSysDown=PUWeightHLT_Photon30SysDown;}
			}
	
		if(currentSyst==SYST::NONE)Sel2->FillAndInit("Trigger"); //Selection
		
		if( (jentry%10000)==0 && debug>0) printf("--> Trigger %s Prescale %f Pt: %f\n",triggerMenu.c_str(),ScaleTrigger,(*photonPt)[iGamma]);

		//pass all the cuts
		GammaIdx=iGamma;
		break;
		}


	if(GammaIdx<0) continue; //--no gamma candidate found
	if(currentSyst==SYST::NONE)Sel->FillAndInit("GammaSelection"); //Selection

	TLorentzVector gamma;
	if(photonPt->at(GammaIdx)<10) {fprintf(stderr,"Error: Photon pT too low\n");continue;}// minimum check on photon pt
	gamma.SetPtEtaPhiE(photonPt->at(GammaIdx),photonEta->at(GammaIdx),photonPhi->at(GammaIdx),photonE->at(GammaIdx));	
	//--- jet founding -------------
	JetIdx.clear();
	Int_t mynJets=jetPt->size();
	Float_t Ht=0;

	if(debug>1)printf("-> Starting Jet Loop\n");
	for(Int_t iJet=0;iJet<mynJets;++iJet)
		{
		//construct TLV
		TLorentzVector j;
		if( (*jetPt)[iJet]<30)continue;
		j.SetPtEtaPhiE((*jetPt)[iJet],(*jetEta)[iJet],(*jetPhi)[iJet],(*jetE)[iJet]);
		//Delta R Cut wrt the leading selected photon
		if(j.DeltaR(gamma)<0.5) continue;	

		//PU ID -- cut based
		 if(1.-(*jetBeta)[iJet] >= 0.2*TMath::Log(nVtx-0.64))  continue;
                 if((*jetRMS)[iJet] > TMath::Sqrt(0.06) ) continue;

		//book the jet
		JetIdx.push_back(iJet);
		Ht+=(*jetPt)[iJet];
		}
	mynJets=JetIdx.size();
	//my selection 
	if(mynJets<1) continue; 
	if(currentSyst==SYST::NONE)Sel->FillAndInit("OneJet"); //Selection


	if( (jentry%10000 ==0) && debug>0)fprintf(stderr,"RhoCorr=%f photonRC=%f\n",RhoCorr,(*photonIsoFPRPhoton)[GammaIdx]);
	//end rho corrections
	
	if(isRealData) PUWeight=1;

	for(int iCut=0;iCut<int(cutsContainer.size());++iCut)
		{
		if(gamma.Pt() < cutsContainer[iCut].VPt.first)continue;
		if(gamma.Pt() > cutsContainer[iCut].VPt.second)continue;
		if(Ht         < cutsContainer[iCut].Ht.first)continue;
		if(Ht         > cutsContainer[iCut].Ht.second)continue;
		//if(GammaMVA         < cutsContainer[iCut].phid.first)continue;
		//if(GammaMVA         > cutsContainer[iCut].phid.second)continue;
		if((*photonid_sieie)[GammaIdx]         < cutsContainer[iCut].phid.first)continue;
		if((*photonid_sieie)[GammaIdx]         >= cutsContainer[iCut].phid.second)continue;
		if( mynJets < cutsContainer[iCut].nJets) continue;
		
		//Going to fill
		//-----
		{
		string name=string("gammaPt_")+cutsContainer[iCut].name()+SystName();
			if(histoContainer[name]==NULL) {histoContainer[name]=new TH1D(name.c_str(),name.c_str(),binsContainer["gammaPt"].nBins,binsContainer["gammaPt"].xMin,binsContainer["gammaPt"].xMax); histoContainer[name]->Sumw2();}
		histoContainer[name]->Fill(gamma.Pt(),ScaleTrigger*PUWeight);
		}
		//-----
		if( !isRealData ){  //only for MC
			TLorentzVector gGEN;
			if(GammaIdxGEN>=0)
				gGEN.SetPtEtaPhiE(photonPtGEN,photonEtaGEN,photonPhiGEN,photonEGEN);
		
			if(
			GammaIdxGEN >=0 && // Gamma is ok
			photonPtGEN > cutsContainer[iCut].VPt.first && 
			photonPtGEN < cutsContainer[iCut].VPt.second && 
			HtGEN > cutsContainer[iCut].Ht.first && 
			HtGEN < cutsContainer[iCut].Ht.second && 
			mynJetsGEN >= cutsContainer[iCut].nJets &&
			gamma.DeltaR(gGEN) <0.3	 //--------------<-------
			){
			if(cutsContainer[iCut].VPt.first == 0 ){ //only for the inclusive cuts
			string name=string("gammaPt_MATRIX_")+cutsContainer[iCut].name()+SystName();
			if(histo2Container[name]==NULL){
				//histo2Container[name]=new TH2D(name.c_str(),name.c_str(),binsContainer["gammaPt"].nBins,binsContainer["gammaPt"].xMin,binsContainer["gammaPt"].xMax,binsContainer["gammaPt"].nBins,binsContainer["gammaPt"].xMin,binsContainer["gammaPt"].xMax);
				histo2Container[name]=new TH2D(name.c_str(),name.c_str(),nbinsForMatrix,ptbinsForMatrix,nbinsForMatrix,ptbinsForMatrix);
				histo2Container[name]->Sumw2();
				}
			//histo2Container[name]->Fill(gamma.Pt(),photonPtGEN,ScaleTrigger*PUWeight);
			histo2Container[name]->Fill(gGEN.Pt(),gamma.Pt(),ScaleTrigger*PUWeight);
			} //only for the inclusive cuts
			//-----
			{
			string name=string("photoniso_MATCHED_")+cutsContainer[iCut].name()+SystName();
			if(histoContainer[name]==NULL) {histoContainer[name]=new TH1D(name.c_str(),name.c_str(),binsContainer["photoniso"].nBins,binsContainer["photoniso"].xMin,binsContainer["photoniso"].xMax); histoContainer[name]->Sumw2();}
			histoContainer[name]->Fill( (*photonIsoFPRPhoton)[GammaIdx]-RhoCorr,1.0);
			}
			//-----
			}//RECO & GEN
			
			if(
			photonPtGEN > cutsContainer[iCut].VPt.first && 
			photonPtGEN < cutsContainer[iCut].VPt.second && 
			HtGEN > cutsContainer[iCut].Ht.first && 
			HtGEN < cutsContainer[iCut].Ht.second && 
			mynJetsGEN >= cutsContainer[iCut].nJets &&
			(GammaIdxGEN <0 || // Gamma is NOT ok
			gamma.DeltaR(gGEN) >0.3 )	 //--------------<-------
			){
			string name=string("photoniso_NOTMATCHED_")+cutsContainer[iCut].name()+SystName();
			if(histoContainer[name]==NULL) {histoContainer[name]=new TH1D(name.c_str(),name.c_str(),binsContainer["photoniso"].nBins,binsContainer["photoniso"].xMin,binsContainer["photoniso"].xMax); histoContainer[name]->Sumw2();}
			histoContainer[name]->Fill( (*photonIsoFPRPhoton)[GammaIdx]-RhoCorr,1.0);
			} //RECO & GEN (but NOT PHOTON)

			// -- only for mc --
			if( cutsContainer[iCut].VPt.first==0 && gamma.DeltaR(gGEN) <0.3 ){ // should match with the purity fraction
				string name=string("gammaPt_RECO_UNFOLD_")+cutsContainer[iCut].name()+SystName();
				if(histoContainer[name]==NULL) {
					histoContainer[name]=new TH1D(name.c_str(),name.c_str(),nbinsForMatrix,ptbinsForMatrix);
					histoContainer[name]->Sumw2();
					}
			histoContainer[name]->Fill(gamma.Pt(),ScaleTrigger*PUWeight);	
			}
		}//end of only MC
		//-----
		{
		string name=string("gammaEta_")+cutsContainer[iCut].name()+SystName();
			if(histoContainer[name]==NULL){ histoContainer[name]=new TH1D(name.c_str(),name.c_str(),binsContainer["gammaEta"].nBins,binsContainer["gammaEta"].xMin,binsContainer["gammaEta"].xMax); histoContainer[name]->Sumw2();}
		histoContainer[name]->Fill(fabs(gamma.Eta()),ScaleTrigger*PUWeight);
		}
		//----- NOT WEIGHTED -> LOW STAT FIT
		{
		string name=string("sieie_")+cutsContainer[iCut].name()+SystName();
		if(histoContainer[name]==NULL) {histoContainer[name]=new TH1D(name.c_str(),name.c_str(),binsContainer["sieie"].nBins,binsContainer["sieie"].xMin,binsContainer["sieie"].xMax); histoContainer[name]->Sumw2();}
		//histoContainer[name]->Fill(  (*photonid_sieie)[GammaIdx],ScaleTrigger);
		histoContainer[name]->Fill(  (*photonid_sieie)[GammaIdx],1.0);
		//histoContainer[name]->Fill(  GammaMVA);
		}
		//-----
		{
		string name=string("photoniso_")+cutsContainer[iCut].name()+SystName();
		if(histoContainer[name]==NULL) {histoContainer[name]=new TH1D(name.c_str(),name.c_str(),binsContainer["photoniso"].nBins,binsContainer["photoniso"].xMin,binsContainer["photoniso"].xMax); histoContainer[name]->Sumw2();}
		//histoContainer[name]->Fill( (*photonIsoFPRPhoton)[GammaIdx]-RhoCorr,ScaleTrigger);
		histoContainer[name]->Fill( (*photonIsoFPRPhoton)[GammaIdx]-RhoCorr,1.0);
		//FILL Tree
		//name="tree_"+cutsContainer[iCut].name()+SystName();
		//if(treeContainer[name]==NULL) MakeTree(name); 
		//TreeVar.photoniso=(*photonIsoFPRPhoton)[GammaIdx]-RhoCorr;
		//treeContainer[name]->Fill( );
		}
		//-----
		{
		string name=string("photonisoRC_")+cutsContainer[iCut].name()+SystName();
		if(histoContainer[name]==NULL){ histoContainer[name]=new TH1D(name.c_str(),name.c_str(),binsContainer["photoniso"].nBins,binsContainer["photoniso"].xMin,binsContainer["photoniso"].xMax); histoContainer[name]->Sumw2();}
		//histoContainer[name]->Fill( (*photonIsoFPRRandomConePhoton)[GammaIdx]-RhoCorr,ScaleTrigger);
		histoContainer[name]->Fill( (*photonIsoFPRRandomConePhoton)[GammaIdx]-RhoCorr,1.0);
		}
		//-----
		
		} //for iCut
	
   } //Loop over entries
	//WRITE
	//open output
	if( outputFileName.find(".root") == string::npos ){
	if(nJobs>0)outputFileName+=Form("_%d_%d",jobId,nJobs);
	outputFileName+=".root";
	}

	TFile *f;
	 f = TFile::Open(outputFileName.c_str(),"RECREATE");
	f->cd();
	for(map<string,TH1D*>::iterator it=histoContainer.begin();it!=histoContainer.end();it++)
		{
		printf("going to Write %s\n",it->first.c_str());
		it->second->SetDirectory(gDirectory);
		it->second->Write("",TObject::kOverwrite);
		}
	for(map<string,TH2D*>::iterator it=histo2Container.begin();it!=histo2Container.end();it++)
		{
		printf("going to Write %s\n",it->first.c_str());
		it->second->SetDirectory(gDirectory);
		it->second->Write("",TObject::kOverwrite);
		}

	Sel->Write(f);
	Sel2->Write(f);
	/*
	for(map<string,TTree*>::iterator it=treeContainer.begin();it!=treeContainer.end();it++)
		{
		printf("going to Write %s\n",it->first.c_str());
		it->second->SetDirectory(gDirectory);
		it->second->Write("",TObject::kOverwrite);
		}
	*/
return;
}//Analyzer::Loop

void Analyzer::Smear()
{
	float newPt,newE;
	switch (currentSyst)
	{
	case SYST::NONE : return;
	case SYST::JESUP : 
		for(int i=0;i<int(jetPt->size());i++){
			if(i>=int(jetE->size())) printf("ERROR JETE SIZE < JETPT SIZE\n");
			if(i>=int(jetUNC->size())) printf("ERROR JETUNC SIZE < JETPT SIZE\n");
			newPt= (*jetPt)[i]*(1+(*jetUNC)[i]);
			newE= (*jetE)[i]*(1+(*jetUNC)[i]);
			if(newPt<5){ (*jetPt)[i]=5;(*jetE)[i]=5;}
			else{
			(*jetPt)[i]=newPt;
			(*jetE)[i]=newE;
			}
		}
		break;
	case SYST::JESDN:
		for(int i=0;i<int(jetPt->size());i++){
			newPt= (*jetPt)[i]*(1-(*jetUNC)[i]);
			newE= (*jetE)[i]*(1-(*jetUNC)[i]);
			if(newPt<5){ (*jetPt)[i]=5;(*jetE)[i]=5;}
			else{
			(*jetPt)[i]=newPt;
			(*jetE)[i]=newE;
			}
		}
		break;
	case SYST::PUUP: 
		PUWeight=PUWeightSysUp;
		//TODO -- PUHLT
		break;
	case SYST::PUDN: 
		PUWeight=PUWeightSysDown;
		break;
	case SYST::JERUP: 
		for(int i=0;i<int(jetPt->size());i++){
			(*jetPt)[i]=(*jetPtRESup)[i] ;
		}
		
		break;
	case SYST::JERDN: 
		for(int i=0;i<int(jetPt->size());i++){
			(*jetPt)[i]=(*jetPtRESdown)[i] ;
		}
		break;
	default: return;
	}
};

string Analyzer::SystName(){
 return SystName(currentSyst)	;
}

string Analyzer::SystName(enum SYST a){
	switch (a)
	{
	case SYST::NONE : return string("");
	case SYST::JESUP : 
		return string("_JESUP");
		break;
	case SYST::JESDN:
		return string("_JESDN");
		break;
	case SYST::PUUP: 
		return string("_PUUP");
		break;
	case SYST::PUDN: 
		return string("_PUDN");
		break;
	case SYST::JERUP: 
		return string("_JERUP");
		break;
	case SYST::JERDN: 
		return string("_JERDN");
		break;
	case SYST::SIGSHAPE: 
		return string("_SIGSHAPE");
		break;
	case SYST::BKGSHAPE: 
		return string("_BKGSHAPE");
		break;
	case SYST::UNFOLD: 
		return string("_UNFOLD");
		break;
	case SYST::FIT: 
		return string("_FIT");
		break;
	case SYST::LUMIUP: 
		return string("_LUMIUP");
		break;
	case SYST::LUMIDN: 
		return string("_LUMIDN");
		break;
	default: return "";
	}
}
