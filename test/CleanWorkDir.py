#!/usr/bin/python
import sys,os
import array
import time
from optparse import OptionParser


usage = "usage: %prog [options] arg1 arg2"
parser=OptionParser(usage=usage)
parser.add_option("","--inputDat" ,dest='inputDat',type='string',help="Input Configuration file",default="")
parser.add_option("-0","--eff" ,dest='step0',action='store_true',help="Clean step0",default=False)
parser.add_option("-1","--output" ,dest='step1',action='store_true',help="Clean step1",default=False)
parser.add_option("-2","--fit"    ,dest='step2',action='store_true',help="Clean step2",default=False)
parser.add_option("-3","--unfold" ,dest='step3',action='store_true',help="Clean step3",default=False)
parser.add_option("-4","--plots" ,dest='step4',action='store_true',help="Clean step4 - Plots",default=False)
parser.add_option("","--only" ,dest='only',action='store_true',help="Clean only selected steps",default=False)
parser.add_option("","--partial" ,dest='partial',action='store_true',help="implies -only -1. Clean only intermidiate steps not hadded one",default=False)
parser.add_option("-n","--dryrun" ,dest='dryrun',action='store_true',help="DryRun",default=False)

(options,args)=parser.parse_args()

#      0 1 2 3 
Clean=[0,0,0,0,0]

if options.partial:
	options.step0=0
	options.step1=0
	options.step2=0
	options.step3=0
	options.step4=0

def CleanValues( value, only=False):
	Clean[value]=1
	if not options.only:
		for i in range(value,len(Clean)):
			Clean[i]=1
if options.step0: CleanValues(0,options.only);
if options.step1: CleanValues(1,options.only);
if options.step2: CleanValues(2,options.only);
if options.step3: CleanValues(3,options.only);
if options.step4: CleanValues(4,options.only);


print "inserting in path cwd"
sys.path.insert(0,os.getcwd())
print "inserting in path cwd/python"
sys.path.insert(0,os.getcwd()+'/python')
from common import *

print "--> load dat file: "+options.inputDat

config=read_dat(options.inputDat)

print "--------- DATA CONFIG -----------"
PrintDat(config)

WorkDir=ReadFromDat(config,"WorkDir","./","-->Set Default WDIR")


from glob import glob
files=[]
if Clean[0]:
	print "------ Cleaning 0 ------"
	files+=glob(WorkDir+"/effarea*")	
if Clean[1]:
	print "------ Cleaning 1 ------"
	files+=glob(WorkDir+"/output*")
if Clean[2]:
	print "------ Cleaning 2 ------"
	files+=glob(WorkDir+"/fit*")
	files+=glob(WorkDir+"/bias*")
	files+=glob(WorkDir+"/toys*")
if Clean[3]:
	print "------ Cleaning 3 ------"
	files+=glob(WorkDir+"/Unfold*")
if Clean[4]:
	print "------ Cleaning 3 ------"
	files+=glob(WorkDir+"/C_*")
	files+=glob(WorkDir+"/plots/*")
if options.partial:
	print "------ Partial Cleaning 1 ------"
	files+=glob(WorkDir+"/output_*")

from subprocess import call
for file in files:
	if options.dryrun:
		print "rm -v "+file
	else:
		cmd=['rm','-v',file]
		call(cmd)
