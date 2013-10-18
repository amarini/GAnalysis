#include "TMath.h"
#include <cstdio>

int bins(int nBins=20, float xmin=100, float xmax=800,int log=1,int before=0,int after=0)
{
if(log){
	double a= TMath::Power( xmax/xmin,1./nBins );
	
	if(before>0)
		for(int i=before;i>0;i--)
		{
		printf("%.1f ",xmin/TMath::Power(a,i));
		}
	for(int i=0;i<nBins+1;i++)
		printf("%.1f ",TMath::Power(a,i)*xmin);
	if(after>0)
		for(int i=1;i<=after;i++)
		{
		printf("%.1f ",xmax*TMath::Power(a,i));
		}
	printf("\n");
}
else
{
	double a=(xmax-xmin)/nBins;
	if(before>0)
		for(int i=before;i>0;i--)
		{
		printf("%.1f ",xmin-a*i);
		}
	for(int i=0;i<nBins+1;i++)
		printf("%.1f ",xmin+a*i);
	if(after>0)
		for(int i=1;i<=after;i++)
		{
		printf("%.1f ",xmax+a*i);
		}
	printf("\n");
		
}
return 0;
}
