
int gamma_Pt_Incl(const char*fileName="../../V00-12/output.root",const char*histoName="gammaPt_VPt_0_8000_Ht_0_8000_phid_0.000_0.011_nJets_1",const char *outName=NULL)
{
   float xFac=2.3,yFac=2.2 ;
   int txtSize=15;

   gStyle->SetOptStat(0);
   gStyle->SetOptTitle(0);

   TFile *f=TFile::Open(fileName);

   TCanvas *Canvas_1 = new TCanvas("Canvas_1", "Canvas_1",666,97,976,717);
   Canvas_1->Range(1.270445,-1.564668,3.193932,8.644471);
   Canvas_1->SetFillColor(0);
   Canvas_1->SetBorderMode(0);
   Canvas_1->SetBorderSize(2);
   Canvas_1->SetLogx();
   Canvas_1->SetLogy();
   Canvas_1->SetFrameBorderMode(0);
   Canvas_1->SetFrameBorderMode(0);
   
   //TH1F *gammaPt = new TH1F("gammaPt_VPt_0_8000_Ht_0_8000_phid_0.000_0.011_nJets_1","gammaPt_VPt_0_8000_Ht_0_8000_phid_0.000_0.011_nJets_1",1000,0,1000);
   TH1F *gammaPt = (TH1F*)f->Get(histoName);
   
   Int_t ci;   // for color index setting
   ci = TColor::GetColor("#000099");
   gammaPt->SetLineColor(ci);
   gammaPt->GetXaxis()->SetTitle("P_{T}^{#gamma}");
   gammaPt->GetXaxis()->SetRange(30,1000);
   gammaPt->GetXaxis()->SetMoreLogLabels();
   gammaPt->GetXaxis()->SetNoExponent();
   gammaPt->GetXaxis()->SetLabelFont(42);
   gammaPt->GetXaxis()->SetLabelSize(0.035);
   gammaPt->GetXaxis()->SetTitleSize(0.035);
   gammaPt->GetXaxis()->SetTitleFont(42);
   gammaPt->GetYaxis()->SetTitle("Entries * PreScale");
   gammaPt->GetYaxis()->SetLabelFont(42);
   gammaPt->GetYaxis()->SetLabelSize(0.035);
   gammaPt->GetYaxis()->SetTitleSize(0.035);
   gammaPt->GetYaxis()->SetTitleFont(42);
   gammaPt->GetYaxis()->SetRangeUser(0.3,4e+07);
   gammaPt->Draw("AXIS");
   	
   TPave *pv;
   pv=new TPave(29,0.3,60,4e7,0,"");
   	pv->SetShadowColor(0);
	pv->SetFillColor(kGreen-4);
	pv->SetFillStyle(3002);
	pv->Draw();
   pv=new TPave(60,.3,90,4e7,0,"");
   	pv->SetShadowColor(0);
	pv->SetFillColor(kRed-4);
	pv->SetFillStyle(3002);
	pv->Draw();
   pv=new TPave(90,.3,100,4e7,0,"");
   	pv->SetShadowColor(0);
	pv->SetFillColor(kBlue-4);
	pv->SetFillStyle(3002);
	pv->Draw();
   pv=new TPave(100,.3,207.1,4e7,0,"");
   	pv->SetShadowColor(0);
	pv->SetFillColor(kMagenta-4);
	pv->SetFillStyle(3002);
	pv->Draw();
   pv=new TPave(207.1,.3,1000,4e7,0,"");
   	pv->SetShadowColor(0);
	pv->SetFillColor(kOrange-4);
	pv->SetFillStyle(3002);
	pv->Draw();
   

   gammaPt->Draw("AXIS SAME");
   gammaPt->Draw("AXIS X+ Y+ SAME");
   gammaPt->Draw("SAME");

   TLine *line = new TLine(60,0.3,60,4e+07);
   line->SetLineWidth(3);
   line->Draw();
   line = new TLine(90,0.3,90,4e+07);
   line->SetLineWidth(3);
   line->Draw();
   line = new TLine(100,0.3,100,4e+07);
   line->SetLineWidth(3);
   line->Draw();
   line = new TLine(207.1,0.33,207.1,4e+07);
   line->SetLineWidth(3);
   line->Draw();
  
   TPaveText *pt ;
   pt = new TPaveText(30,22,30*xFac,22*yFac,"br"); //x*xFac y*2,714
   pt->SetTextFont(63);
   pt->SetTextSize(txtSize);
   pt->SetShadowColor(0);
   text = pt->AddText("HLT_Photon30_CaloIdVL");
   pt->Draw();
   
   pt = new TPaveText(45,2500,45.*xFac,2500*yFac,"br");
   pt->SetTextFont(63);
   pt->SetTextSize(txtSize);
   pt->SetShadowColor(0);
   text = pt->AddText("HLT_Photon50_CaloIdVL");
   pt->Draw();
   
   pt = new TPaveText(65,220,65*xFac,220*yFac,"br");
   pt->SetTextFont(63);
   pt->SetTextSize(txtSize);
   pt->SetShadowColor(0);
   text = pt->AddText("HLT_Photon75_CaloIdVL");
   pt->Draw();
   
   pt = new TPaveText(97,22,97*xFac,22*yFac,"br");
   pt->SetTextFont(63);
   pt->SetTextSize(txtSize);
   pt->SetShadowColor(0);
   text = pt->AddText("HLT_Photon90_CaloIdVL");
   pt->Draw();
   
   pt = new TPaveText(310,3e4,310*2.5/3.0*xFac,3e4*yFac,"br");
   pt->SetTextFont(63);
   pt->SetTextSize(txtSize);
   pt->SetShadowColor(0);
   text = pt->AddText("HLT_Photon150");
   pt->Draw();
   	
   float PtCuts[]={100.0,111.0,123.1,136.6,151.6,168.2,186.6,207.1,229.7,254.9,282.8,313.8,348.2,386.4,428.7,475.7,527.8,585.6,649.8,721.0,800.0};
	    TArrow *a = new TArrow(100,1.e07,800,1e+07,0.02,"<|--|>");
	    a->Draw();
   for (int i=0;i<sizeof(PtCuts)/sizeof(float) ;i++)
	   {
            float yFac2=1.2;
	    line = new TLine(PtCuts[i],1.e07/yFac2,PtCuts[i],1e+07*yFac2);
	    line->Draw();
	   }	

   pt = new TPaveText(200,1.5e7,200*xFac,1.5e7*yFac,"br");
   pt->SetTextFont(43);
   pt->SetTextSize(txtSize);
   pt->SetShadowColor(0);
   pt->SetBorderSize(0);
   pt->SetFillStyle(0);
   text = pt->AddText("Bins");
   pt->Draw();

   Canvas_1->Modified();
   Canvas_1->cd();
   Canvas_1->SetSelected(Canvas_1);
   Canvas_1->ToggleToolBar();
	if(outName){
	Canvas_1->SaveAs(outName);
	}
}
