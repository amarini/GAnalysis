
class AnalyzerBranches {
public:
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
   vector<float>   *photonRegressionCorr;
   vector<float>   *photonRegressionCorrErr;
   vector<float>   *photonPassConversionVeto;
   vector<float>   *photonPfIsoChargedHad;
   vector<float>   *photonPfIsoNeutralHad;
   vector<float>   *photonPfIsoPhoton;
   vector<float>   *photonPfIsoPhoton03ForCic;
   vector<float>   *photonPfIsoNeutrals03ForCic;
   vector<float>   *photonPfIsoCharged02ForCicVtx0;
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
   vector<float>   *photonhcalTowerSumEtConeDR03;
   vector<float>   *photonecalRecHitSumEtConeDR04;
   vector<float>   *photonnTrkSolidConeDR04;
   vector<float>   *photontrkSumPtSolidConeDR04;
   vector<float>   *photonnTrkHollowConeDR04;
   vector<float>   *photontrkSumPtHollowConeDR04;
   vector<float>   *photontrkSumPtHollowConeDR03;
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
   vector<float>   *jetPuId;
   vector<float>   *jetPuIdMva;
   vector<int>     *jetPuIdFlags;
   vector<int>     *jetPuIdFlagsMva;
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
   TBranch        *b_eventWeight;   //!
   TBranch        *b_PUWeight;   //!
   TBranch        *b_PUWeightSysUp;   //!
   TBranch        *b_PUWeightSysDown;   //!

   TBranch 	 *b_PUWeightHLT_Photon150,*b_PUWeightHLT_Photon150SysUp,*b_PUWeightHLT_Photon150SysDown;
   TBranch 	 *b_PUWeightHLT_Photon135,*b_PUWeightHLT_Photon135SysUp,*b_PUWeightHLT_Photon135SysDown;
   TBranch 	 *b_PUWeightHLT_Photon90,*b_PUWeightHLT_Photon90SysUp,*b_PUWeightHLT_Photon90SysDown;
   TBranch 	 *b_PUWeightHLT_Photon75,*b_PUWeightHLT_Photon75SysUp,*b_PUWeightHLT_Photon75SysDown;
   TBranch 	 *b_PUWeightHLT_Photon50,*b_PUWeightHLT_Photon50SysUp,*b_PUWeightHLT_Photon50SysDown;
   TBranch 	 *b_PUWeightHLT_Photon30,*b_PUWeightHLT_Photon30SysUp,*b_PUWeightHLT_Photon30SysDown;
   
   TBranch        *b_RDWeight;   //!
   TBranch        *b_RDWeightBare;   //!
   TBranch        *b_RDWeightSysUp;   //!
   TBranch        *b_RDWeightSysDown;   //!

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
   TBranch        *b_photonRegressionCorr;   //!
   TBranch        *b_photonRegressionCorrErr;   //!
   TBranch        *b_photonPassConversionVeto;   //!
   TBranch        *b_photonPfIsoChargedHad;   //!
   TBranch        *b_photonPfIsoNeutralHad;   //!
   TBranch        *b_photonPfIsoPhoton;   //!
   TBranch        *b_photonPfIsoPhoton03ForCic;   //!
   TBranch        *b_photonPfIsoNeutrals03ForCic;   //!
   TBranch        *b_photonPfIsoCharged03ForCicVtx0;   //!
   TBranch        *b_photonPfIsoCharged02ForCicVtx0;   //!
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
   TBranch        *b_photonhcalTowerSumEtConeDR03;   //!
   TBranch        *b_photonecalRecHitSumEtConeDR04;   //!
   TBranch        *b_photonnTrkSolidConeDR04;   //!
   TBranch        *b_photontrkSumPtSolidConeDR04;   //!
   TBranch        *b_photonnTrkHollowConeDR04;   //!
   TBranch        *b_photontrkSumPtHollowConeDR04;   //!
   TBranch        *b_photontrkSumPtHollowConeDR03;   //!
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
   TBranch	  *b_jetPuId;
   TBranch   	  *b_jetPuIdMva;
   TBranch   	  *b_jetPuIdFlags;
   TBranch   	  *b_jetPuIdFlagsMva;
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
};
