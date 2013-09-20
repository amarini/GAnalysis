#define Analyzer_cxx
#include "Analyzer.h"
#include <TH2.h>
#include <TStyle.h>
#include <TCanvas.h>
#include "TDirectory.h"

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
    fChain->SetBranchStatus("prescale*",1);  // activate branchname
    fChain->SetBranchStatus("TriMatchF4Path_photon",1);  // activate branchname
    fChain->SetBranchStatus("rho",1);  // activate branchname
    fChain->SetBranchStatus("nVtx",1);  // activate branchname
    fChain->SetBranchStatus("runNum",1);  // activate branchname
   if (fChain == 0) return;

   Long64_t nentries = fChain->GetEntries();

   for (Long64_t jentry=0; jentry<nentries;jentry++) {
	if(  (  nJobs >0)  && ( jentry%nJobs!=jobId) ) continue;
	if(debug>1)printf("-> Loding entry %lld\n",jentry);
     // Long64_t ientry = LoadTree(jentry);
	if( (jentry%10000)==0) printf("-> Getting entry %lld/%lld\n",jentry,nentries);
	fChain->GetEntry(jentry);
	//error
     // if (ientry < 0) break;
	Int_t GammaIdx=-1;
	float GammaMVA=-999;
	if(debug>1)printf("-> Starting GammaLoop\n");
	for(Int_t iGamma=0;iGamma<Int_t(photonPt->size());++iGamma)
		{
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
		if(fabs( (*photonEta)[iGamma] )>=1.4 ) continue;

		//pass all the cuts
		GammaIdx=iGamma;
		break;
		}

	if(GammaIdx<0) continue; //--no gamma candidate found

	TLorentzVector gamma;
	if(photonPt->at(GammaIdx)<10) {fprintf(stderr,"Error: Photon pT too low\n");continue;}// minimum check on photon pt
	gamma.SetPtEtaPhiE(photonPt->at(GammaIdx),photonEta->at(GammaIdx),photonPhi->at(GammaIdx),photonE->at(GammaIdx));	
	//--- jet founding -------------
	JetIdx.clear();
	Int_t mynJets=jetPt->size();
	Float_t Ht=0;
	//---------Smearings
	//	for(Int_t iJet=0;iJet<nJets;++iJet)
	//		{
	//		//syst smearing JES
	//		//(*jetPt)[iJet]*=
	//		}
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

	//compute RhoCorrections
	float RhoCorr=0;
	if(useEffArea){
		//search in the database for the correct bin
   		for(map<string,float>::iterator it=effAreaCorr.begin();it!=effAreaCorr.end();it++)
		{
		string name=it->first;
		float ptmin,ptmax,etamin,etamax;
  		sscanf(name.c_str(),"%f_%f_%f_%f",&ptmin,&ptmax,&etamin,&etamax);
		//fprintf(stderr,"GPt=%f pt in [%f,%f] GETA=%f et=[%f,%f]\n",gamma.Pt(),ptmin,ptmax,gamma.Eta(),etamin,etamax);
		if(gamma.Pt()>ptmin && gamma.Pt()<ptmax && fabs(gamma.Eta())> etamin && fabs(gamma.Eta()) <etamax)
			{
			RhoCorr= it->second * rho;
			}
		
		}
	}

	if( (jentry%10000 ==0) && debug>0)fprintf(stderr,"RhoCorr=%f photonRC=%f\n",RhoCorr,(*photonIsoFPRPhoton)[GammaIdx]);
	//end rho corrections

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
		//Going to fill
		//-----
		{
		string name=string("gammaPt_")+cutsContainer[iCut].name();
			if(histoContainer[name]==NULL) histoContainer[name]=new TH1F(name.c_str(),name.c_str(),binsContainer["gammaPt"].nBins,binsContainer["gammaPt"].xMin,binsContainer["gammaPt"].xMax);
		histoContainer[name]->Fill(gamma.Pt());
		}
		//-----
		{
		string name=string("sieie_")+cutsContainer[iCut].name();
		if(histoContainer[name]==NULL) histoContainer[name]=new TH1F(name.c_str(),name.c_str(),binsContainer["sieie"].nBins,binsContainer["sieie"].xMin,binsContainer["sieie"].xMax);
		histoContainer[name]->Fill(  (*photonid_sieie)[GammaIdx]);
		//histoContainer[name]->Fill(  GammaMVA);
		}
		//-----
		{
		string name=string("photoniso_")+cutsContainer[iCut].name();
		if(histoContainer[name]==NULL) histoContainer[name]=new TH1F(name.c_str(),name.c_str(),binsContainer["photoniso"].nBins,binsContainer["photoniso"].xMin,binsContainer["photoniso"].xMax);
		histoContainer[name]->Fill( (*photonIsoFPRPhoton)[GammaIdx]-RhoCorr);
		//FILL Tree
		name="tree_"+cutsContainer[iCut].name();
		if(treeContainer[name]==NULL) MakeTree(name); 
		TreeVar.photoniso=(*photonIsoFPRPhoton)[GammaIdx]-RhoCorr;
		treeContainer[name]->Fill( );
		}
		//-----
		{
		string name=string("photonisoRC_")+cutsContainer[iCut].name();
		if(histoContainer[name]==NULL) histoContainer[name]=new TH1F(name.c_str(),name.c_str(),binsContainer["photoniso"].nBins,binsContainer["photoniso"].xMin,binsContainer["photoniso"].xMax);
		histoContainer[name]->Fill( (*photonIsoFPRRandomConePhoton)[GammaIdx]-RhoCorr);
		}
		//-----
		
		} //for iCut
	
   } //Loop over entries
	//WRITE
	//open output
	if(nJobs>0)outputFileName+=Form("_%d_%d",jobId,nJobs);
	outputFileName+=".root";
	TFile *f=TFile::Open(outputFileName.c_str(),"RECREATE");
	f->cd();
	for(map<string,TH1F*>::iterator it=histoContainer.begin();it!=histoContainer.end();it++)
		{
		printf("going to Write %s\n",it->first.c_str());
		it->second->SetDirectory(gDirectory);
		it->second->Write("",TObject::kOverwrite);
		}
	for(map<string,TTree*>::iterator it=treeContainer.begin();it!=treeContainer.end();it++)
		{
		printf("going to Write %s\n",it->first.c_str());
		it->second->SetDirectory(gDirectory);
		it->second->Write("",TObject::kOverwrite);
		}
return;
}//Analyzer::Loop
