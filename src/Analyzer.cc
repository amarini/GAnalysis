#define Analyzer_cxx
#include "Analyzer.h"
#include <TH2.h>
#include <TStyle.h>
#include <TCanvas.h>
#include "TDirectory.h"
#include <assert.h>

void Analyzer::MakeTree(string name){
	treeContainer[name]=new TTree(name.c_str(),name.c_str());
	treeContainer[name]->Branch("photoniso",&TreeVar.photoniso,"photoniso/F");

}
int Analyzer::SetCutsJetPtThreshold(){
	for (int i=0;i<int(cutsContainer.size());i++)
		{
		cutsContainer[i].JetPtThreshold=JetPtThreshold;
		}
	}

void inline Analyzer::checkDuty(Long64_t jentry){
	//-- check to decide if do dutyCycle checks
	if (!doDutyCycle) return;
	if (nBench<=0) return;
	if (thrBench<=0) return;
	if (doTimeUsage) return; //Can't do both
	//---
	if ( dutyCount>0 && (dutyCount % nBench == 0) ) {
		stopWatch.Stop();
		float realTime=stopWatch.RealTime();
		float cpuTime=stopWatch.CpuTime();
		float bench=cpuTime/(cpuTime+realTime);
		if (bench<thrBench && realTime>startBench * 60.) {
				cout<<"Exiting: too slow"<<endl;
				cout<<"RealTime: "<< realTime<<endl;
				cout<<"CpuTime: "<< cpuTime<<endl;
				if( outputFileName.find(".root") != string::npos ){//already written part of the file
				cout<<"removing file "<<outputFileName<<endl;
				system(Form("rm %s",outputFileName.c_str()));
			       	}
				exit(1001);
				}
		dutyCount = 0; // work with small numbers
		} //jentry of dutycount
	if (dutyCount == 0) stopWatch.Start();
	dutyCount++;	
	return;
}

void Analyzer::checkTimeUsage(int n, string name=""){
if (!doTimeUsage) return;

stopWatch.Stop();
if(n>0){
	if(timeNames.size() <= n)
		{
		timeNames.resize(n+1);
		timeUsage.resize(n+1);
		timeNames[n]=name;
		}
	timeUsage[n].first += stopWatch.RealTime();
	timeUsage[n].second += stopWatch.CpuTime();
	}
if(n>=0){ 
	stopWatch.Reset();
	stopWatch.Start();
	}
if(n<0){
	//print
	cout<<"***********************"<<endl;
	float SumCpu=0;
	float SumReal=0;
	for(int i=0;i<timeUsage.size();i++)
		{
		cout<<"* TIME "<<timeNames[i]<<" "<<timeUsage[i].first<<" "<<timeUsage[i].second<<" *"<<endl;
		SumReal+=timeUsage[i].first;
		SumCpu+=timeUsage[i].second;
		}
	cout<<"***********************"<<endl;
	for(int i=0;i<timeUsage.size();i++){
		cout<<"* TIME "<<timeNames[i]<<" "<<timeUsage[i].first/SumReal*100<<"% "<<timeUsage[i].second/SumCpu*100<<"% *"<<endl;
		}
	cout<<"***********************"<<endl;
	}
return;
}

void Analyzer::SetBranchStatus(){
    if(debug>0)printf("start loop\n");
    fChain->SetBranchStatus("*",0);  // disable all branches
    if(useReWeights && !isRealData)fChain->SetBranchStatus("puTrueINT");
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
    fChain->SetBranchStatus("jetPuId*",1);  // activate branchname
//	fChain->GetEntry(0); done in init
   if(!isRealData) {
	if(debug>0)printf("Running on mc: activating branches\n");
    	fChain->SetBranchStatus("PUWeight*",1);  // activate branchname
    	fChain->SetBranchStatus("eventWeight*",1);  // activate branchname
	fChain->SetBranchStatus("photon*GEN",1);
	fChain->SetBranchStatus("jet*GEN",1);
    	fChain->SetBranchStatus("lep*",1);  // activate branchname

	if(useRDWeight){
		if(debug>0)printf("--> Also RD\n");
		fChain->SetBranchStatus("RDW*",1);
		}
	}
}

void Analyzer::Loop()
{
    if (fChain == 0) return;
    SetBranchStatus();
    //
    if(debug>0)printf("Reset Pt Threshold in all cuts\n");
	SetCutsJetPtThreshold();

   //exit if syst does not make sense for data or mc	
   if(currentSyst == PUUP && isRealData) return;	
   if(currentSyst == PUDN && isRealData) return;	
   if(currentSyst == JERUP && isRealData) return;	
   if(currentSyst == JERDN && isRealData) return;	
   if(currentSyst == UNFOLD ) return;	
   if(currentSyst == SIGSHAPE ) return;	
   if(currentSyst == BKGSHAPE ) return;	
   if(currentSyst == FIT ) return;	
   if(currentSyst == LUMIUP ) return;	
   if(currentSyst == LUMIDN ) return;	
   if(currentSyst == BIAS ) return;	
   if(currentSyst == SMEARUP && isRealData ) return;	
   if(currentSyst == SMEARDN && isRealData ) return;	
   if(currentSyst == ESCALEUP && !isRealData ) return;	
   if(currentSyst == ESCALEDN && !isRealData ) return;	

   Long64_t nentries = fChain->GetEntries();

   //Set Matrix Bins -> Moved to member
   //bins for matrix
   //Float_t ptbinsForMatrix[1023];
   nbinsForMatrix=-1;
   //ptbinsForMatrix[nbinsForMatrix]=0;
   for(int iPt=0;iPt<int(PtCuts.size()) && PtCuts[iPt]>0;iPt++)
   	{nbinsForMatrix++;ptbinsForMatrix[nbinsForMatrix]=PtCuts[iPt];}

   //
   const double EtaMax=1.4;

   bool JobCheck=true;
	if( entryBegin >0 || entryEnd>0) JobCheck=false;

   if (nJobs >0 && entryBegin<=0 && entryEnd<=0) 
		{
		entryBegin=(nentries/nJobs+1)*jobId;
		entryEnd=(nentries/nJobs+1)*(jobId+1);
		}	   
   if(entryBegin<=0 && entryEnd<=0) {entryBegin=0; entryEnd=nentries; }
   if (entryEnd>=nentries) entryEnd=nentries;
   cout<<"***  jentry in [ "<< entryBegin  <<","<< entryEnd <<") of "<<nentries<<" ***"<<endl; // +1 instead of doing ceil. 

   //LOOP
   for (Long64_t jentry=entryBegin; jentry<entryEnd;jentry++) {
	if(doTimeUsage) checkTimeUsage(0,"begin");	
	//just a check
	if( (JobCheck) && (nJobs >0) && ( jentry< (nentries/nJobs+1)*jobId  || jentry >= (nentries/nJobs+1)*(jobId+1) ) ) continue; // +1 instead of doing ceil. 

	if(doTimeUsage) checkTimeUsage(1,"checkJobs");	

	if(debug>1)printf("-> Loding entry %lld\n",jentry);
	if( (jentry&16383)==0 && debug>0) {
				printf("-> Getting entry %lld/%lld\n",jentry,nentries);
				if(doTimeUsage) checkTimeUsage(-1,"print");	
	}
	fChain->GetEntry(jentry);
	if( fCurrent != fChain->GetTreeNumber()) //new file
		{
		cout<<"Opening file "<<fChain->GetCurrentFile()->GetName()<<endl;
		fCurrent=fChain->GetTreeNumber();
		}
	if(doTimeUsage) checkTimeUsage(2,"GetEntry");
	if(currentSyst==NONE)Sel->FillAndInit("All"); //Selection

	//duty cycle
	checkDuty(jentry);

	int GammaIdxGEN=-1;
	int HtGEN=0;
	int mynJetsGEN=0;
	vector<int> JetIdxGEN;

	if (!isRealData && useReWeights) ApplyReWeights();
	if (useEnergyRegression) ApplyEnergyRegression();
	if (useEnergyScale) ApplyEnergyScale();
	if (useEnergySmear) ApplyEnergySmear();

	if(useRDWeight && !isRealData)
		{
			//printf("RDWeight=%lf\n",RDWeight);
			eventWeight=RDWeightBare;
			PUWeight=RDWeight;
			PUWeightSysUp=RDWeightSysUp;
			PUWeightSysDown=RDWeightSysDown;
		}

	//SYST SMEARINGS - JER JES
	Smear();

	if(doTimeUsage) checkTimeUsage(3,"Smearings");

	if(!isRealData) //only MC -- FILL GEN Plots
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
			if((*jetPtGEN)[iJetGEN]<JetPtThreshold) continue;
			if( fabs((*jetEtaGEN)[iJetGEN])>=JetEta) continue; //jetEta
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
			Fill( string("gammaPtGEN_")+cutsContainer[iCut].name()+SystName()  ,  gGEN.Pt()  ,  eventWeight,"");
			Fill( string("gammaEtaGEN_")+cutsContainer[iCut].name()+SystName() , gGEN.Eta(),eventWeight,"");
			Fill( string("HtGEN_")+cutsContainer[iCut].name()+SystName() , HtGEN,eventWeight,"");
			//-----
			//fill Madgraph GJets only
			string fname=fChain->GetCurrentFile()->GetName();
			if( fname.find("GJets") != string::npos)
				Fill( string("gammaPtGEN_MG_")+cutsContainer[iCut].name()+SystName()  ,  gGEN.Pt()  ,  eventWeight,"");
			if( fname.find("DiPho") !=string::npos) 
				Fill( string("gammaPtGEN_DiPho_")+cutsContainer[iCut].name()+SystName()  ,  gGEN.Pt()  ,  eventWeight,"");
			if( fname.find("EMEnr") !=string::npos) 
				Fill( string("gammaPtGEN_EM_")+cutsContainer[iCut].name()+SystName()  ,  gGEN.Pt()  ,  eventWeight,"");
			if( fname.find("BCtoE") !=string::npos) 
				Fill( string("gammaPtGEN_EM_")+cutsContainer[iCut].name()+SystName()  ,  gGEN.Pt()  ,  eventWeight,"");
			} // iCut
	} //isMC
	if(doTimeUsage) checkTimeUsage(4,"GEN");
	
	Int_t GammaIdx=-1;
	float GammaMVA=-999;
	float ScaleTrigger=1.0;
	float RhoCorr=0;
	if(debug>1)printf("-> Starting GammaLoop\n");
	for(Int_t iGamma=0;iGamma<Int_t(photonPt->size());++iGamma)
		{
		if(currentSyst==NONE)Sel2->FillAndInit("All"); //Selection
		//TODO Gamma ID with CiC
		//if( photonid_hadronicOverEm2012->at(iGamma) >0.1 ) continue;	
			//set variables for tmva
		//compute mva
		if(loadMVA)
			{
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
			GammaMVA = tmvaReaderID_Single_Barrel->EvaluateMVA("AdaBoost");
			}
		//if (GammaMVA <-.1)continue; //comment? -> no id use this to cut instead of sieie? - better sieie is less correleted with iso. Otherwise the id will use iso to kill the bkg
		//select the leading photon in |eta|<1.4
		if(fabs( (*photonEta)[iGamma] )>=EtaMax ) continue;
		if(currentSyst==NONE)Sel2->FillAndInit("Eta"); //Selection
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
			RhoCorr= it->second * rho; //EffA *rho
			}
		
		}
	} //RhoCorr

		if( int((*photonPassConversionVeto)[iGamma]) == 0  ) continue; //it is a float, why - always 1 .
	
		//selection = Hgg PreSelection	
		if(!PassHggPreSelection(iGamma,RhoCorr))continue;	
	
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

		if(currentSyst==NONE)Sel2->FillAndInit("Trigger"); //Selection
		
		if( (jentry%10000)==0 && debug>0) printf("--> Trigger %s Prescale %f Pt: %f\n",triggerMenu.c_str(),ScaleTrigger,(*photonPt)[iGamma]);

		//pass all the cuts
		GammaIdx=iGamma;
		break;
		}

	if(doTimeUsage) checkTimeUsage(5,"Gamma Search");

	if(GammaIdx<0) continue; //--no gamma candidate found
	if(currentSyst==NONE)Sel->FillAndInit("GammaSelection"); //Selection

	TLorentzVector gamma;
	if(photonPt->at(GammaIdx)<10) {fprintf(stderr,"Error: Photon pT too low\n");continue;}// minimum check on photon pt
	gamma.SetPtEtaPhiE(photonPt->at(GammaIdx),photonEta->at(GammaIdx),photonPhi->at(GammaIdx),photonE->at(GammaIdx));	

	if(!isRealData) //ScaleFactors
			{
			//Preselection SF on Zee AN-13-008
			double sf1=0.997,sf2=0.978;
			if((*photonid_r9)[GammaIdx]>=0.9){PUWeight*=sf1;PUWeightSysUp*=sf1;PUWeightSysDown*=sf1;}
			else {PUWeight*=sf2; PUWeightSysUp*=sf2;PUWeightSysDown*=sf2;}
			//ElectronSafeConversionVeto SF on Zuug
			sf1=0.995; sf2=0.998;
			if((*photonid_r9)[GammaIdx]>=0.94){PUWeight*=sf1;PUWeightSysUp*=sf1;PUWeightSysDown*=sf1;}
			else {PUWeight*=sf2; PUWeightSysUp*=sf2;PUWeightSysDown*=sf2;}
			
			}
	int isEMatched=0;			
	if(useEGscaleFactors && !isRealData )isEMatched=ApplyEGscaleFactors(gamma,GammaIdx); 
	//--- jet founding -------------
	JetIdx.clear();
	Int_t mynJets=jetPt->size();
	Float_t Ht=0;

	if(debug>1)printf("-> Starting Jet Loop\n");
	for(Int_t iJet=0;iJet<mynJets;++iJet)
		{
		//construct TLV
		TLorentzVector j;
		if( (*jetPt)[iJet]<JetPtThreshold)continue;
		if( fabs((*jetEta)[iJet])>=JetEta)continue;
		j.SetPtEtaPhiE((*jetPt)[iJet],(*jetEta)[iJet],(*jetPhi)[iJet],(*jetE)[iJet]);
		//Delta R Cut wrt the leading selected photon
		if(j.DeltaR(gamma)<0.5) continue;	

		//PU ID -- cut based
		 //if(1.-(*jetBeta)[iJet] >= 0.2*TMath::Log(nVtx-0.64))  continue;
                 //if((*jetRMS)[iJet] > TMath::Sqrt(0.06) ) continue;
		 //
		 if ( (*jetPuIdFlagsMva)[iJet] == 0 ) continue; //loose

		//book the jet
		JetIdx.push_back(iJet);
		Ht+=(*jetPt)[iJet];
		} // jet Loop

	mynJets=JetIdx.size();

	if(doTimeUsage) checkTimeUsage(6,"Jets");

	//my selection 
	if(mynJets<1) continue; 
	if(currentSyst==NONE)Sel->FillAndInit("OneJet"); //Selection

	if( (jentry%10000 ==0) && debug>0)fprintf(stderr,"RhoCorr=%f photonRC=%f\n",RhoCorr,(*photonIsoFPRPhoton)[GammaIdx]);
	//end rho corrections
	
	if(isRealData) PUWeight=1;

	for(int iCut=0;iCut<int(cutsContainer.size());++iCut)
		{
		//if(doTimeUsage) checkTimeUsage(timeUsage.size(),Form("-> Fill&Cuts %d: VPt_%.0f_%.0f_Ht_%.0f_%.0f_phid_%.3f_%.3f_nJets_%d",iCut,cutsContainer[iCut].VPt.first,cutsContainer[iCut].VPt.second,cutsContainer[iCut].Ht.first,cutsContainer[iCut].Ht.second,cutsContainer[iCut].phid.first, cutsContainer[iCut].phid.second));
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
		bool isDumpToBook=false;
		{ // the dumping is outside the fill function
		string name=string("gammaPt_")+cutsContainer[iCut].name()+SystName();
		if(histoContainer[name]==NULL) 
				isDumpToBook=true;
		}

		Fill( string("gammaPt_")+cutsContainer[iCut].name()+SystName() , gamma.Pt(), ScaleTrigger * PUWeight, "gammaPt" );

		{
		string name=string("gammaPt_")+cutsContainer[iCut].name()+SystName();
		//cant call before because Histo does not exists
		if(isDumpToBook && doDump)
				dump.BookHisto(histoContainer[name]);
		if(currentSyst==NONE && doDump){
				dump.FillHisto(name,gamma.Pt(),runNum,lumi,eventNum);
				}
		}
		Fill( string("Ht_")+cutsContainer[iCut].name()+SystName() , Ht , ScaleTrigger * PUWeight, "" );
		//-----
		Fill( string("gammaEta_")+cutsContainer[iCut].name()+SystName(), fabs(gamma.Eta()),ScaleTrigger*PUWeight,"gammaEta");
		//----- NOT WEIGHTED -> LOW STAT FIT -> Not work if mix samples, use PUWeight instead
		Fill(string("sieie_")+cutsContainer[iCut].name()+SystName(), (*photonid_sieie)[GammaIdx],PUWeight,"sieie");
		//-----
		Fill(string("photoniso_")+cutsContainer[iCut].name()+SystName(), (*photonIsoFPRPhoton)[GammaIdx]-RhoCorr,PUWeight,"photoniso");
		//FILL Tree
		//name="tree_"+cutsContainer[iCut].name()+SystName();
		//if(treeContainer[name]==NULL) MakeTree(name); 
		//TreeVar.photoniso=(*photonIsoFPRPhoton)[GammaIdx]-RhoCorr;
		//treeContainer[name]->Fill( );
		//-----
		Fill( string("photonisoRC_")+cutsContainer[iCut].name()+SystName(), (*photonIsoFPRRandomConePhoton)[GammaIdx]-RhoCorr,PUWeight, "photoniso") ;
		//-----
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

			Fill2D(string("gammaPt_MATRIX_")+cutsContainer[iCut].name()+SystName() , gamma.Pt(),gGEN.Pt(),ScaleTrigger*PUWeight,"");
			Fill2D(string("Ht_MATRIX_")+cutsContainer[iCut].name()+SystName() , Ht  ,  HtGEN  ,  ScaleTrigger*PUWeight,"");
			} //only for the inclusive cuts
			//-----
			Fill( string("photoniso_MATCHED_")+cutsContainer[iCut].name()+SystName() ,  (*photonIsoFPRPhoton)[GammaIdx]-RhoCorr,PUWeight, "photoniso");
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
			Fill ( string("photoniso_NOTMATCHED_")+cutsContainer[iCut].name()+SystName(),  (*photonIsoFPRPhoton)[GammaIdx]-RhoCorr,PUWeight, "photoniso" );
			} //RECO & GEN (but NOT PHOTON)

			// -- only for mc --
			if( cutsContainer[iCut].VPt.first==0 && GammaIdxGEN>=0 && gamma.DeltaR(gGEN) <0.3 ){ // should match with the purity fraction
				Fill ( string("gammaPt_RECO_UNFOLD_")+cutsContainer[iCut].name()+SystName(), gamma.Pt(),ScaleTrigger*PUWeight, "" );
				Fill ( string("Ht_RECO_UNFOLD_")+cutsContainer[iCut].name()+SystName(), Ht , ScaleTrigger*PUWeight, "" );
			}

			if (isEMatched  && cutsContainer[iCut].VPt.first==0 && useEGscaleFactors  )	
			{
				Fill( string("gammaPt_RECO_EMATCHED_")+cutsContainer[iCut].name()+SystName(), gamma.Pt(),ScaleTrigger*PUWeight,"") ;
				Fill( string("Ht_RECO_EMATCHED_")+cutsContainer[iCut].name()+SystName(), Ht ,ScaleTrigger*PUWeight,"") ;
			}
		}//end of only MC
		
		} //for iCut

	if(doTimeUsage) checkTimeUsage(7,"Fills & Cuts");
	
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
	
	if(currentSyst==NONE && doDump)dump.Dump();
return;
}//Analyzer::Loop

void Analyzer::ApplyEnergyScale()
{
if( !isRealData) return;
if( !useEnergyScale) return;
for(unsigned int i=0;i < photonPt->size();i++)
	{
	float pt = photonPt->at(i);
	float eta= fabs(photonEta->at(i));
	float r9 = photonid_r9->at(i);
	for( map<string,float>::iterator it=energyScale.begin();it!=energyScale.end();it++)
		{
		float ptmin,ptmax,etamin,etamax,r9min,r9max;
		long runmin,runmax;
		sscanf(it->first.c_str(),"%f_%f_%f_%f_%f_%f_%ld_%ld",&ptmin,&ptmax,&etamin,&etamax,&r9min,&r9max,&runmin,&runmax);
		if (!(pt>=ptmin && pt<ptmax)	) continue;
		if (!(eta>=etamin && eta<etamax)	) continue;
		if (!(r9>=r9min && r9<r9max) 	)continue;
		if (!(runNum>=runmin && runNum<runmax)	) continue;
		double sf=(1-it->second);
		double err=energyScaleError[it->first];
		if (currentSyst==ESCALEUP) sf+=err;
		if (currentSyst==ESCALEDN) sf-=err;
		photonPt->at(i)*=sf;
		photonE->at(i)*=sf;
		break;
		}
//	if (currentSyst==ESCALEUP) // GAIN SWITCH ? 
//		{
//		if (photonPt->at(i)< pt+.3)
//			{
//			//change in photonPt in pt+.3 
//			double sf=(pt+.3 )/  photonPt->at(i) ;
//			photonPt->at(i) *= sf;
//			photonE->at(i) *= sf;
//			}
//		}
	}//loop over photons
}

void Analyzer::InitEnergyScale(){
  FILE *fr=fopen(energyScaleFile.c_str(),"r");
  if(fr==NULL) fprintf(stderr,"Error opening: %s",energyScaleFile.c_str());
  char name[1023],buf[2048];
  float ptmin,ptmax,etamin,etamax,value,err,r9min,r9max;
  long runmin,runmax,type;
  while(fgets(buf,2048,fr)!=NULL)
	{
	if(buf[0]=='#') continue;
	if(buf[0]=='\n') continue;
	if(buf[0]=='\0') continue;
	int i=0;
	while(buf[i]!='\n' && buf[i]!='\0') i++;
	buf[i]='\0';
  	sscanf(buf,"%s %ld %f %f %f %f %f %f %ld %ld %f %f",&name,&type,&ptmin,&ptmax,&etamin,&etamax,&r9min,&r9max,&runmin,&runmax,&value,&err);


	string name=Form("%.1f_%.1f_%.1f_%.1f_%.1f_%.1f_%ld_%ld",ptmin,ptmax,etamin,etamax,r9min,r9max,runmin,runmax);
	energyScale[name]=value;
	energyScaleError[name]=err;
	
	}
   for(map<string,float>::iterator it=energyScale.begin();it!=energyScale.end();it++)
	{
	string name=it->first;
	fprintf(stderr,"Loaded %s in EGScaleFactors Corrections with val %f +- %f\n",name.c_str(), energyScale[name],energyScaleError[name] );
	}
  return;
	
}
void Analyzer::ApplyEnergySmear()
{
if(isRealData)return;
if(!useEnergySmear)return;
for(unsigned int i=0;i < photonPt->size();i++)
	{
	float pt = photonPt->at(i);
	float eta= fabs(photonEta->at(i));
	float r9 = photonid_r9->at(i);
	for( map<string,pair<float,float> >::iterator it=energySmear.begin();it!=energySmear.end();it++)
		{
		float ptmin,ptmax,etamin,etamax,r9min,r9max;
		long runmin,runmax;
		sscanf(it->first.c_str(),"%f_%f_%f_%f_%f_%f_%ld_%ld",&ptmin,&ptmax,&etamin,&etamax,&r9min,&r9max,&runmin,&runmax);
		if (!(pt>=ptmin && pt<ptmax)	) continue;
		if (!(eta>=etamin && eta<etamax)	) continue;
		if (!(r9>=r9min && r9<r9max) 	)continue;
		if (!(runNum>=runmin && runNum<runmax)	) continue;
		float rho=it->second.first;
		float phi=it->second.second;
		if(currentSyst == SMEARUP)
			{
			rho+=energySmearErr[it->first].first;
			phi-=energySmearErr[it->first].second; //I maximaze/min the smearing sigma = rho^2 * [ (1-Et2)/Et2 *Sin*2phi + 1/Et2 ], sin2phi is crescient and the coefficient is negative. rho and phi are factorized
			}
		else if (currentSyst == SMEARDN)
			{
			rho-=energySmearErr[it->first].first;
			phi+=energySmearErr[it->first].second;
			}
		float sigma=sqrt( TMath::Power(rho*TMath::Sin(phi),2) + TMath::Power(rho*TMath::Cos(phi)/pt,2));
		
		float newpt=rEnergySmear->Gaus(photonPt->at(i),sigma);
		if (newpt<1) newpt=1; // a photon of 1GeV will not pass any reasonable selection
		photonE->at(i)*=newpt/photonPt->at(i);
		photonPt->at(i)=newpt;
		break;
		}
	}
}

void Analyzer::InitEnergySmear(){
	FILE *fr=fopen(energySmearFile.c_str(),"r");
  if(fr==NULL) fprintf(stderr,"Error opening: %s",energySmearFile.c_str());
  char name[1023],buf[2048];
  float ptmin,ptmax,etamin,etamax,rho,rhoerr,phi,phierr,r9min,r9max;
  long runmin,runmax,type;
  while(fgets(buf,2048,fr)!=NULL)
	{
	if(buf[0]=='#') continue;
	if(buf[0]=='\n') continue;
	if(buf[0]=='\0') continue;
	int i=0;
	while(buf[i]!='\n' && buf[i]!='\0') i++;
	buf[i]='\0';
  	sscanf(buf,"%s %ld %f %f %f %f %ld %ld %f %f %f %f",&name,&type,&etamin,&etamax,&r9min,&r9max,&runmin,&runmax,&rho,&rhoerr,&phi,&phierr);


	string name=Form("%.1f_%.1f_%.1f_%.1f_%.1f_%.1f_%ld_%ld",ptmin,ptmax,etamin,etamax,r9min,r9max,runmin,runmax);
	energySmear[name]=pair<float,float>(rho,phi);
	energySmearErr[name]=pair<float,float>(rhoerr,phierr);
	
	}
   for(map<string,pair<float,float> >::iterator it=energySmear.begin();it!=energySmear.end();it++)
	{
	string name=it->first;
	fprintf(stderr,"Loaded %s in EGSmearFactors Corrections with val %f %f - \n",name.c_str(), energySmear[name].first ,energySmear[name].second );
	}
  return;
	
}

void Analyzer::InitEGscaleFactors(){
   //e->g s.f.
//   int useEGscaleFactors;
//   string EGscaleFactorsFile;
//   map<string,float> EGsf;
 return;// s.f. is 1.45

 // FILE *fr=fopen(EGscaleFactorsFile.c_str(),"r"); 
 // if(fr==NULL) fprintf(stderr,"Error opening: %s",EGscaleFactorsFile.c_str());
 // char what[1023],buf[2048];
 // float ptmin,ptmax,etamin,etamax,value;
 // while(fgets(buf,2048,fr)!=NULL)
 //       {
 //       if(buf[0]=='#') continue;
 //       if(buf[0]=='\n') continue;
 //       if(buf[0]=='\0') continue;
 //       int i=0;
 //       while(buf[i]!='\n' && buf[i]!='\0') i++;
 //       buf[i]='\0';
 // 	sscanf(buf,"%f %f %f %f %f",&ptmin,&ptmax,&etamin,&etamax,&value);

 //       if(debug>0){
 //       fprintf(stderr,"Buffer is %s\n",buf);
 //       fprintf(stderr,"Going to scan %f %f %f %f %f\n",ptmin,ptmax,etamin,etamax,value);
 //       }

 //       string name=Form("%.1f_%.1f_%.1f_%.1f",ptmin,ptmax,etamin,etamax);
 //       EGscaleFactors[name]=value;
 //       
 //       }
 //  for(map<string,float>::iterator it=EGscaleFactors.begin();it!=EGscaleFactors.end();it++)
 //       {
 //       string name=it->first;
 //       fprintf(stderr,"Loaded %s in EGScaleFactors Corrections with val %f - \n",name.c_str(), EGscaleFactors[name] );
 //       }
 // return;
	
}

void Analyzer::ApplyEnergyRegression(){
if( !useEnergyRegression) return;
	for(int i=0 ;i<photonPt->size();i++)
		{
		float corr;
		corr=photonRegressionCorr->at(i)/photonE->at(i);
			//corr = (photonRegressionCorr->at(i) - photonRegressionCorrErr->at(i) )/photonE->at(i);   
			//corr = (photonRegressionCorr->at(i) + photonRegressionCorrErr->at(i) )/photonE->at(i);   
		if( currentSyst == REGRUP)
			corr+= photonRegressionCorrErr->at(i);
		if( currentSyst == REGRDN)
			corr-=photonRegressionCorrErr->at(i) ;
		float newE=photonE->at(i)*corr;
		float newPt=photonPt->at(i)*corr;
		photonPt->at(i)=newPt;
		photonE->at(i)=newE;
		}
	// re order per Pt
	vector<TLorentzVector> photons;
	for(int i=0 ;i<photonPt->size();i++)
		{
		TLorentzVector g;
		g.SetPtEtaPhiE( photonPt->at(i),photonEta->at(i),photonPhi->at(i),photonE->at(i))	;
		photons.push_back(g);
		}
	sort(photons.begin(),photons.end(), SortingRule );
	for(int i=0 ;i<photonPt->size();i++)
		{
		(*photonPt)[i] = photons[i].Pt();
		(*photonEta)[i] = photons[i].Eta();
		(*photonE)[i] = photons[i].E();
		(*photonPhi)[i] = photons[i].Phi();
		}
	
};

void Analyzer::Smear()
{
	float newPt,newE;

	if(!isRealData) //smear Jet Energy resolution to match data
	for(int i=0;i<int(jetPt->size());i++){
		double sf=(*jetPtRES)[i]/(*jetPt)[i];
		(*jetPt)[i] = (*jetPtRES)[i] ;
		(*jetE)[i] *= sf;
		}

	switch (currentSyst)
	{
	case NONE : return;
	case JESUP : 
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
	case JESDN:
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
	case PUUP: 
		PUWeight=PUWeightSysUp;
		//TODO -- PUHLT
			PUWeightHLT_Photon150=PUWeightHLT_Photon150SysUp;
			PUWeightHLT_Photon135=PUWeightHLT_Photon135SysUp;
			PUWeightHLT_Photon90 =PUWeightHLT_Photon90SysUp; 
			PUWeightHLT_Photon75 =PUWeightHLT_Photon75SysUp; 
			PUWeightHLT_Photon50 =PUWeightHLT_Photon50SysUp; 
			PUWeightHLT_Photon30 =PUWeightHLT_Photon30SysUp; 
		break;
	case PUDN: 
		PUWeight=PUWeightSysDown;
			PUWeightHLT_Photon150=PUWeightHLT_Photon150SysDown;
			PUWeightHLT_Photon135=PUWeightHLT_Photon135SysDown;
			PUWeightHLT_Photon90 =PUWeightHLT_Photon90SysDown; 
			PUWeightHLT_Photon75 =PUWeightHLT_Photon75SysDown; 
			PUWeightHLT_Photon50 =PUWeightHLT_Photon50SysDown; 
			PUWeightHLT_Photon30 =PUWeightHLT_Photon30SysDown; 
		break;
	case JERUP: 
		for(int i=0;i<int(jetPt->size());i++){
			(*jetPt)[i]=(*jetPtRESup)[i] ;
		}
		
		break;
	case JERDN: 
		for(int i=0;i<int(jetPt->size());i++){
			(*jetPt)[i]=(*jetPtRESdown)[i] ;
		}
		break;
	case ESCALEUP:
		if (!useEnergyScale) //otherwise done with shervin uncertainties
			for(int i=0;i<int(photonPt->size());i++) //after regression
			{
			float oldE=(*photonE)[i];
			float newE=oldE*1.006;
			(*photonPt)[i]*=newE/oldE;
			(*photonE)[i]*=newE/oldE;
			}
		break;
	case ESCALEDN:
		if (!useEnergyScale) //otherwise done with shervin uncertainties
			for(int i=0;i<int(photonPt->size());i++) //after regression
			{
			float oldE=(*photonE)[i];
			float newE=oldE*(1-0.006);
			(*photonPt)[i]*=newE/oldE;
			(*photonE)[i]*=newE/oldE;
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
	case NONE : return string("");
	case JESUP : 
		return string("_JESUP");
		break;
	case JESDN:
		return string("_JESDN");
		break;
	case PUUP: 
		return string("_PUUP");
		break;
	case PUDN: 
		return string("_PUDN");
		break;
	case JERUP: 
		return string("_JERUP");
		break;
	case JERDN: 
		return string("_JERDN");
		break;
	case SIGSHAPE: 
		return string("_SIGSHAPE");
		break;
	case BKGSHAPE: 
		return string("_BKGSHAPE");
		break;
	case UNFOLD: 
		return string("_UNFOLD");
		break;
	case FIT: 
		return string("_FIT");
		break;
	case LUMIUP: 
		return string("_LUMIUP");
		break;
	case LUMIDN: 
		return string("_LUMIDN");
		break;
	case BIAS: 
		return string("_BIAS");
		break;
	case SMEARUP: 
		return string("_SMEARUP");
		break;
	case SMEARDN: 
		return string("_SMEARDN");
		break;
	case REGRUP: 
		return string("_REGRUP");
		break;
	case REGRDN: 
		return string("_REGRDN");
		break;
	case ESCALEUP:
		return string("_ESCALEUP");
		break;
	case ESCALEDN:
		return string("_ESCALEDN");
		break;
	default: return "";
	}
}

bool Analyzer::PassPhotonId2012(int iGamma){
		if( (*photonid_hadronicOverEm)[iGamma] >0.05) return false; 
		if(currentSyst==NONE)Sel2->FillAndInit("HoE"); //Selection
		if( (*photonPfIsoChargedHad)[iGamma]>1.5) return false;
		if(currentSyst==NONE)Sel2->FillAndInit("IsoCharged"); //Selection
		if( (*photonPfIsoNeutralHad)[iGamma]>1.0+ 0.04*(*photonPt)[iGamma]) return false;
		if(currentSyst==NONE)Sel2->FillAndInit("IsoNeutral"); //Selection
		//if( (*photonPfIsoPhoton)[iGamma]>0.7+0.005*(*photonPt)[iGamma]) return false;
		return true;
}

bool Analyzer::PassHggPreSelection(int iGamma,float RhoCorr)
{
		//PRESELECTION H-GG
		if( (*photonid_sieie)[iGamma] >0.014) return false;;
		if(currentSyst==NONE)Sel2->FillAndInit("SieieLoose");
		if( (*photonid_r9)[iGamma]>=0.9){
			if( (*photonid_hadronicOverEm)[iGamma] >0.082) return false;; 
			if(currentSyst==NONE)Sel2->FillAndInit("HoE"); //Selection
			//if( (*photonhcalTowerSumEtConeDR04)[iGamma]*9./16. > 50 + 0.005*(*photonPt)[iGamma] )return false;;
			if( (*photonhcalTowerSumEtConeDR03)[iGamma] > 50 + 0.005*(*photonPt)[iGamma] )return false;;
			if(currentSyst==NONE)Sel2->FillAndInit("hcalIso"); //Selection
			//if( (*photontrkSumPtHollowConeDR04)[iGamma]*9./16. > 50 + 0.002*(*photonPt)[iGamma] )return false;;
			if( (*photontrkSumPtHollowConeDR03)[iGamma] > 50 + 0.002*(*photonPt)[iGamma] )return false;;
			if(currentSyst==NONE)Sel2->FillAndInit("trkIso"); //Selection
		}
		else{
			if( (*photonid_hadronicOverEm)[iGamma] >0.075) return false;; 
			if(currentSyst==NONE)Sel2->FillAndInit("HoE"); //Selection
			//if( (*photonhcalTowerSumEtConeDR04)[iGamma]*9./16. > 4 + 0.005*(*photonPt)[iGamma] )return false;;
			if( (*photonhcalTowerSumEtConeDR03)[iGamma] > 4 + 0.005*(*photonPt)[iGamma] )return false;;
			if(currentSyst==NONE)Sel2->FillAndInit("hcalIso"); //Selection
			//if( (*photontrkSumPtHollowConeDR04)[iGamma]*9./16. > 4 + 0.002*(*photonPt)[iGamma] )return false;;
			if( (*photontrkSumPtHollowConeDR03)[iGamma] > 4 + 0.002*(*photonPt)[iGamma] )return false;;
			if(currentSyst==NONE)Sel2->FillAndInit("trkIso"); //Selection
		}
		//if( (*photonPfIsoCharged03ForCicVtx0)[iGamma]* 4./9. > 4 ) return false;;
		if( (*photonPfIsoCharged02ForCicVtx0)[iGamma] > 4 ) return false;;
			if(currentSyst==NONE)Sel2->FillAndInit("chgIso"); //Selection
		if( (*photonIsoFPRPhoton)[iGamma]-RhoCorr>10) return false;;  // loose 
		if(currentSyst==NONE)Sel2->FillAndInit("IsoPhoton"); //Selection
		return true;

}



void Analyzer::ApplyReWeights(){
    if (isRealData) return;
	double oldew=eventWeight,oldpuw=PUWeight; //DEBUG
    string name=fChain->GetCurrentFile()->GetName();
    //find index mc
    TObjArray *a=fChain->GetListOfFiles();
    int indexFile=fCurrent;
//   for(int i=0;i<  a->GetEntries();i++ )
//	{
//	if (string(a->At(i)->GetName()) == name ) indexFile=i;
//	}
    eventWeight=xSec[indexFile]*1000./nEvents[indexFile];
    if( fabs(oldew - eventWeight)/eventWeight > .4 ) {
	    cout<<"Possible errors in eventWeight: old="<<oldew<<" new="<<eventWeight<<endl;
	    cout << "Index="<<indexFile<<" nEv="<<nEvents[indexFile]<<" xSec="<<xSec[indexFile]<<" name="<<name <<endl;
   	 }
	
 	TH1D* PU=puMCHistos[indexFile];
    
    if(targetHisto["PUWeight"])PUWeight =eventWeight * (double) targetHisto["PUWeight"]->GetBinContent(targetHisto["PUWeight"]->FindBin(puTrueINT))/(double)PU->GetBinContent(PU->FindBin(   TMath::Max(puTrueINT,0) )) ;else PUWeight=-1;
    if(targetHisto["PUWeightSysUp"])PUWeightSysUp =eventWeight * (double) targetHisto["PUWeightSysUp"]->GetBinContent(targetHisto["PUWeightSysUp"]->FindBin(puTrueINT))/(double)PU->GetBinContent(PU->FindBin(   TMath::Max(puTrueINT,0) ));else PUWeightSysUp=-1;
    if(targetHisto["PUWeightSysDown"])PUWeightSysDown =eventWeight * (double) targetHisto["PUWeightSysDown"]->GetBinContent(targetHisto["PUWeightSysDown"]->FindBin(puTrueINT))/(double)PU->GetBinContent(PU->FindBin(   TMath::Max(puTrueINT,0) ));else PUWeightSysDown=-1;

    if(targetHisto["PUWeightHLT_Photon150"])PUWeightHLT_Photon150 =eventWeight * (double) targetHisto["PUWeightHLT_Photon150"]->GetBinContent(targetHisto["PUWeightHLT_Photon150"]->FindBin(puTrueINT))/(double)PU->GetBinContent(PU->FindBin(   TMath::Max(puTrueINT,0) ));else PUWeightHLT_Photon150=-1;
    if(targetHisto["PUWeightHLT_Photon150SysUp"])PUWeightHLT_Photon150SysUp =eventWeight * (double) targetHisto["PUWeightHLT_Photon150SysUp"]->GetBinContent(targetHisto["PUWeightHLT_Photon150SysUp"]->FindBin(puTrueINT))/(double)PU->GetBinContent(PU->FindBin(   TMath::Max(puTrueINT,0) ));else PUWeightHLT_Photon150SysUp=-1;
    if(targetHisto["PUWeightHLT_Photon150SysDown"])PUWeightHLT_Photon150SysDown =eventWeight * (double) targetHisto["PUWeightHLT_Photon150SysDown"]->GetBinContent(targetHisto["PUWeightHLT_Photon150SysDown"]->FindBin(puTrueINT))/(double)PU->GetBinContent(PU->FindBin(   TMath::Max(puTrueINT,0) ));else PUWeightHLT_Photon150SysDown=-1;

    if(targetHisto["PUWeightHLT_Photon135"])PUWeightHLT_Photon135 =eventWeight * (double) targetHisto["PUWeightHLT_Photon135"]->GetBinContent(targetHisto["PUWeightHLT_Photon135"]->FindBin(puTrueINT))/(double)PU->GetBinContent(PU->FindBin(   TMath::Max(puTrueINT,0) ));else PUWeightHLT_Photon135=-1;
    if(targetHisto["PUWeightHLT_Photon135SysUp"])PUWeightHLT_Photon135SysUp =eventWeight * (double) targetHisto["PUWeightHLT_Photon135SysUp"]->GetBinContent(targetHisto["PUWeightHLT_Photon135SysUp"]->FindBin(puTrueINT))/(double)PU->GetBinContent(PU->FindBin(   TMath::Max(puTrueINT,0) ));else PUWeightHLT_Photon135SysUp=-1;
    if(targetHisto["PUWeightHLT_Photon135SysDown"])PUWeightHLT_Photon135SysDown =eventWeight * (double) targetHisto["PUWeightHLT_Photon135SysDown"]->GetBinContent(targetHisto["PUWeightHLT_Photon135SysDown"]->FindBin(puTrueINT))/(double)PU->GetBinContent(PU->FindBin(   TMath::Max(puTrueINT,0) ));else PUWeightHLT_Photon135SysDown=-1;

    if(targetHisto["PUWeightHLT_Photon90"])PUWeightHLT_Photon90 =eventWeight * (double) targetHisto["PUWeightHLT_Photon90"]->GetBinContent(targetHisto["PUWeightHLT_Photon90"]->FindBin(puTrueINT))/(double)PU->GetBinContent(PU->FindBin(   TMath::Max(puTrueINT,0) ));else PUWeightHLT_Photon90=-1;
    if(targetHisto["PUWeightHLT_Photon90SysUp"])PUWeightHLT_Photon90SysUp =eventWeight * (double) targetHisto["PUWeightHLT_Photon90SysUp"]->GetBinContent(targetHisto["PUWeightHLT_Photon90SysUp"]->FindBin(puTrueINT))/(double)PU->GetBinContent(PU->FindBin(   TMath::Max(puTrueINT,0) ));else PUWeightHLT_Photon90SysUp=-1;
    if(targetHisto["PUWeightHLT_Photon90SysDown"])PUWeightHLT_Photon90SysDown =eventWeight * (double) targetHisto["PUWeightHLT_Photon90SysDown"]->GetBinContent(targetHisto["PUWeightHLT_Photon90SysDown"]->FindBin(puTrueINT))/(double)PU->GetBinContent(PU->FindBin(   TMath::Max(puTrueINT,0) ));else PUWeightHLT_Photon90SysDown=-1;

    if(targetHisto["PUWeightHLT_Photon75"])PUWeightHLT_Photon75 =eventWeight * (double) targetHisto["PUWeightHLT_Photon75"]->GetBinContent(targetHisto["PUWeightHLT_Photon75"]->FindBin(puTrueINT))/(double)PU->GetBinContent(PU->FindBin(   TMath::Max(puTrueINT,0) ));else PUWeightHLT_Photon75=-1;
    if(targetHisto["PUWeightHLT_Photon75SysUp"])PUWeightHLT_Photon75SysUp =eventWeight * (double) targetHisto["PUWeightHLT_Photon75SysUp"]->GetBinContent(targetHisto["PUWeightHLT_Photon75SysUp"]->FindBin(puTrueINT))/(double)PU->GetBinContent(PU->FindBin(   TMath::Max(puTrueINT,0) ));else PUWeightHLT_Photon75SysUp=-1;
    if(targetHisto["PUWeightHLT_Photon75SysDown"])PUWeightHLT_Photon75SysDown =eventWeight * (double) targetHisto["PUWeightHLT_Photon75SysDown"]->GetBinContent(targetHisto["PUWeightHLT_Photon75SysDown"]->FindBin(puTrueINT))/(double)PU->GetBinContent(PU->FindBin(   TMath::Max(puTrueINT,0) ));else PUWeightHLT_Photon75SysDown=-1;

    if(targetHisto["PUWeightHLT_Photon50"])PUWeightHLT_Photon50 =eventWeight * (double) targetHisto["PUWeightHLT_Photon50"]->GetBinContent(targetHisto["PUWeightHLT_Photon50"]->FindBin(puTrueINT))/(double)PU->GetBinContent(PU->FindBin(   TMath::Max(puTrueINT,0) ));else PUWeightHLT_Photon50=-1;
    if(targetHisto["PUWeightHLT_Photon50SysUp"])PUWeightHLT_Photon50SysUp =eventWeight * (double) targetHisto["PUWeightHLT_Photon50SysUp"]->GetBinContent(targetHisto["PUWeightHLT_Photon50SysUp"]->FindBin(puTrueINT))/(double)PU->GetBinContent(PU->FindBin(   TMath::Max(puTrueINT,0) ));else PUWeightHLT_Photon50SysUp=-1;
    if(targetHisto["PUWeightHLT_Photon50SysDown"])PUWeightHLT_Photon50SysDown =eventWeight * (double) targetHisto["PUWeightHLT_Photon50SysDown"]->GetBinContent(targetHisto["PUWeightHLT_Photon50SysDown"]->FindBin(puTrueINT))/(double)PU->GetBinContent(PU->FindBin(   TMath::Max(puTrueINT,0) ));else PUWeightHLT_Photon50SysDown=-1;

    if(targetHisto["PUWeightHLT_Photon30"])PUWeightHLT_Photon30 =eventWeight * (double) targetHisto["PUWeightHLT_Photon30"]->GetBinContent(targetHisto["PUWeightHLT_Photon30"]->FindBin(puTrueINT))/(double)PU->GetBinContent(PU->FindBin(   TMath::Max(puTrueINT,0) ));else PUWeightHLT_Photon30=-1;
    if(targetHisto["PUWeightHLT_Photon30SysUp"])PUWeightHLT_Photon30SysUp =eventWeight * (double) targetHisto["PUWeightHLT_Photon30SysUp"]->GetBinContent(targetHisto["PUWeightHLT_Photon30SysUp"]->FindBin(puTrueINT))/(double)PU->GetBinContent(PU->FindBin(   TMath::Max(puTrueINT,0) ));else PUWeightHLT_Photon30SysUp=-1;
    if(targetHisto["PUWeightHLT_Photon30SysDown"])PUWeightHLT_Photon30SysDown =eventWeight * (double) targetHisto["PUWeightHLT_Photon30SysDown"]->GetBinContent(targetHisto["PUWeightHLT_Photon30SysDown"]->FindBin(puTrueINT))/(double)PU->GetBinContent(PU->FindBin(   TMath::Max(puTrueINT,0) ));else PUWeightHLT_Photon30SysDown=-1;

       //printf("Weights: %lf->%lf %lf->%lf\n",oldew,eventWeight,oldpuw,PUWeight); //DEBUG
}

void Analyzer::InitReWeights(){
	//Get Target
	if(debug>0)cout<<"-- INIT REWEIGHTS --"<<endl;
	TDirectory *d=gDirectory;
	targetHisto.clear();
	for(map<string,string>::iterator it=PUFiles.begin();it!=PUFiles.end();it++)
		{
		TFile *f=TFile::Open(it->second.c_str());
		d->cd();
		targetHisto[it->first]=(TH1D*) f->Get("pileup")->Clone( (it->first+"_pileup").c_str() )	;
		if(targetHisto[it->first]==NULL) cout<<"PU Histo for file "<<it->first<<" look for "<<it->second<<" not found"<<endl;
		targetHisto[it->first]->Scale(1./targetHisto[it->first]->Integral());
		f->Close();
		}
	//
	TObjArray *a=fChain->GetListOfFiles();
	int nFiles=a->GetEntries();
	nEvents.clear();
	puMCHistos.clear(); //TODO destruction
	xSec.resize(nFiles);
	CrossSection xS;
	xS.ReadTxtFile( (xSecFile).c_str());
	for(int iFile=0;iFile<nFiles;iFile++)
		{	
		TChain *t=new TChain("accepted/processedData");
		string fileName=a->At(iFile)->GetTitle();
		cout << "Adding File: " << fileName <<" :";
		cout << t->Add( fileName.c_str() );
		cout << endl;

		Float_t mcWeight_;
		Int_t puTrueINT_;
		t->SetBranchAddress("mcWeight",&mcWeight_);
		t->SetBranchAddress("puTrueINT",&puTrueINT_);

		double SumEvents=0;

		TH1D* mcPU=(TH1D*)targetHisto["PUWeight"]->Clone(  Form("pileup_%d",iFile) );
		mcPU->Reset("ICES");
		//for(int iBin=1;iBin<mcPU->GetNbinsX()+1;iBin++){mcPU->SetBinContent(iBin,0);mcPU->SetBinError(iBin,0);}
		//mcPU->SetEntries(0);
		SumEvents=t->GetEntries();
		cout<<"PossibleError = SumEvents=fast"<<endl;
		for (unsigned long long iEntry=0;iEntry<t->GetEntries();iEntry++)
			{
			t->GetEntry(iEntry);
			//SumEvents+=mcWeight_;
			mcPU->Fill(puTrueINT_,mcWeight_);
			}
		mcPU->Scale(1./mcPU->Integral());
		nEvents.push_back(SumEvents);
		puMCHistos.push_back(mcPU);
		xSec[iFile]=xS.xSection( fileName.c_str() );
		cout<< "XSEC for file "<<fileName<<" is "<<xSec[iFile]<<endl;
		assert( xSec[iFile]>= 0 );
		delete t;
		}
	return;	
}

int Analyzer::ApplyEGscaleFactors(TLorentzVector gamma,int GammaIdx){
	if(useEGscaleFactors && !isRealData){ // move to a function
		//check if e is matched to G	
		for( int iLep=0;iLep<lepPtGEN->size();iLep++ )
			{
			//is e?
			if( abs(lepChIdGEN->at(iLep)) != 11) continue ;
			TLorentzVector e;
			e.SetPtEtaPhiE( (*lepPtGEN)[iLep],(*lepEtaGEN)[iLep],(*lepPhiGEN)[iLep],(*lepEGEN)[iLep] );
			if (gamma.DeltaR(e) < 0.3)
				{ //match to an electron -gen
					double sf=1.45;	
					PUWeight*=sf;
					PUWeightSysUp*=sf;
					PUWeightSysDown*=sf;
				  //break;
				  return 1;
				
				  }
			}
	}
	return  0;
}

void Analyzer::Fill(string name, double value, double weight,string bins){
	//string name=string("gammaPtGEN_")+cutsContainer[iCut].name()+SystName();
	if(histoContainer[name]==NULL){ 
		if (bins=="")histoContainer[name]=new TH1D(name.c_str(),name.c_str(),nbinsForMatrix,ptbinsForMatrix);
		else histoContainer[name]=new TH1D(name.c_str(),name.c_str(),binsContainer[bins].nBins,binsContainer[bins].xMin,binsContainer[bins].xMax);
		histoContainer[name]->Sumw2();
		}
	histoContainer[name]->Fill(value,weight);
}
void Analyzer::Fill2D(string name, double value1,double value2, double weight,string bins){
	if(histo2Container[name]==NULL){
		if(bins=="")histo2Container[name]=new TH2D(name.c_str(),name.c_str(),nbinsForMatrix,ptbinsForMatrix,nbinsForMatrix,ptbinsForMatrix);
		else histo2Container[name]=new TH2D(name.c_str(),name.c_str(),binsContainer[bins].nBins,binsContainer[bins].xMin,binsContainer[bins].xMax,binsContainer[bins].nBins,binsContainer[bins].xMin,binsContainer[bins].xMax);
		histo2Container[name]->Sumw2();
		}
		//"response" gives the response matrix, measured X truth.
		// "measured" and "truth" give the projections of "response" onto the X-axis and Y-axis respectively,
		histo2Container[name]->Fill(value1,value2,weight);
	return ;

}

int CrossSection::ReadTxtFile(const char*fileName)
        {
        FILE *fr=fopen(fileName,"r");
        if(fr==NULL) return CrossSection::noFile;
        char key[1023];
        double number;
        while(fscanf(fr,"%s %lf",key,&number)!=EOF){
                xSec[string(key)]=number;
                }
        return 0;
        }
double CrossSection::xSection(string match){
        float R=0;
        int m=0;
        for(map<string,double>::iterator it=xSec.begin();it!=xSec.end();it++)
                {
                if(match.find(it->first) != string::npos){ // I want to match what I put in the database and not the fileName
                        R=it->second;
                        m++;
                        //DEBUG
                        fprintf(stderr,"MATCH=%s\n",it->first.c_str());
                        }
                }
        if(m==1) return R;
        else if( m==0) return CrossSection::noMatch;
        else if( m>1) return CrossSection::multipleMatch;
        }


