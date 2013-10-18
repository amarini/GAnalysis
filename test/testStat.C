{
TH2F *h2=new TH2F("h2","h2",100,-100,100,100,-100,100);

TRandom *r=new TRandom();

for(int i=0;i<10000;i++){
                float x1=r->Gaus(0,10);
                float y1=r->Gaus(0,10);
                h2->Fill( x1,x1+y1);
                }
TProfile *hP=h2->ProfileX();
TH1F *h=new TH1F("h","h",100,-100,100);
for(int i=1;i<=100;i++)
        {
        h->SetBinContent(i,hP->GetBinContent(i));
        h->SetBinError(i,hP->GetBinError(i));
        }
#include <vector>
vector<float> x,y,e_y,e2;
for(int i=1;i<=h->GetNbinsX();i++) { if(h->GetBinContent(i)>0){ x.push_back(h->GetBinCenter(i));y.push_back(h->GetBinContent(i));e_y->push_back(h->GetBinError(i));};}
cout<<"SIZE IS "<<x.size()<<endl;
gSystem->Load("stat.so");

pair<float,float> R=STAT::regression(x,y,e_y,e2);
TF1 *f=new TF1("lin","[0]+[1]*x",-100,100);
f->SetParameter(0,R.first);
f->SetParameter(1,R.second);

h->SetLineColor(kRed);
h->Draw();

TH1F *h_e_1=h->Clone("h_e");
STAT::drawFitError(h_e_1,R,e2,1);
TH1F *h_e_2=h->Clone("h_e_2");
STAT::drawFitError(h_e_2,R,e2,2);

h_e_1->SetFillColor(41);
h_e_2->SetFillColor(kGreen-4);

h2->Draw("SAME");
h_e_2->Draw("E3 SAME");
h_e_1->Draw("E3 SAME");
h->Draw("SAME");
f->DrawClone("SAME");
}
