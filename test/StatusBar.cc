#include <iostream>
#include <iomanip>
using namespace std;

int inline PrintStatusBar(int iEntry,int nEntries, int nSpace=30,int color=0)
{
 int nEntOverSp = nEntries / nSpace;
 if( iEntry%nEntOverSp  == 0 )       //print progress bar
      {
      int j;
      int count = iEntry/nEntOverSp;
	char Fraction[1023];
      if(color) cout<<"\033[0m" ;// NORMAL
      cout<<"[";
	if(color) cout<<"\033[31;1m" ;// RED
	for(j=0;j< count ; j++)
		{
		if(color && j>nSpace *0.2) cout<<"\033[33;1m" ;//yellow
		if(color && j>nSpace*0.8) cout<<"\033[32;1m"; //green // 34 blue
		if(color && j==nSpace-1 ) cout<<"\033[34;1m";
		cout<<"="; 
		}
	for(;j<nSpace;j++)cout<<" "; 
      if(color) cout<<"\033[0m" ;// NORMAL
      cout<<"] "<< setiosflags(ios::fixed) << setprecision(0)<<float(iEntry)/float(nEntries) * 100<<"%\r";cout.flush();
      }
return 0;
}

int TestStatusBar(){
for(int j=0;j<=1000;j++){PrintStatusBar(j,1000,30,0);system("usleep 10000");} ; cout<<endl;
for(int j=0;j<=1000;j++){PrintStatusBar(j,1000,30,1);system("usleep 10000");} ; cout<<endl;
}
