import os, sys
import ROOT
ROOT.gROOT.SetBatch()
from optparse import OptionParser

parser=OptionParser()
parser.add_option("","--inputDat" ,dest='inputDat',type='string',help="Input Configuration file",default="")
(options,args)=parser.parse_args()



Dir1="V00-13"
Dir2="V00-14"

f1=ROOT.TFile.Open("root://eoscms///store/user/amarini/"+Dir1+"/"+ args[0])
f2=ROOT.TFile.Open("root://eoscms///store/user/amarini/"+Dir2+"/"+ args[0])


t1=f1.Get("accepted/processedData")
t2=f2.Get("accepted/processedData")

k1=f1.Get("accepted/events")
k2=f2.Get("accepted/events")

t1E=t1.GetEntries()
t2E=t2.GetEntries()
k1E=k1.GetEntries()
k2E=k2.GetEntries()
p=float(t1E)/float(t2E)-1
q=float(k1E)/float(k2E)-1
print "------------------------------------"
print "Processed  %s - %s     ||     selected  %s - %s "%(Dir1,Dir2,Dir1,Dir2)
print "%5.3f | %d - %d || %5.3f | %d - %d"%(p,t1E,t2E,q,k1E,k2E,) 
print "------------------------------------"
