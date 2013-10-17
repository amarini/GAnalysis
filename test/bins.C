#include "TMath.h"
#include <cstdio>

int bins(int nBins=20, int xmin=100, int xmax=800,int log=1)
{
double a= TMath::Power( xmax/xmin,1./nBins );

for(int i=0;i<nBins+1;i++)
	printf("%.1f ",TMath::Power(a,i)*xmin);
printf("\n");

}
