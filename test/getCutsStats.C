
int getCutsStats()
{
gSystem->Load("../src/Selection.so");

Selection Sel("selection");
Selection Sel2("selectionAllGamma");

TFile *f=TFile::Open("~/work/V00-12/output.root");

Sel.Read(f);
Sel2.Read(f);

Sel.getStats();
Sel2.getStats();

}
