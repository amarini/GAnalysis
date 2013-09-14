#!/usr/bin/python
import sys,os
import array

def read_dat(filename,Analyzer):
	try:
		f=open(filename,"r")
	except IOError:	
		print "File "+filename+" does not exist"
		return
	lines= f.readlines()
	member_lines=[]
	for ll in lines:
		if "#" in ll:
			l2=ll.split("#")[0]
		else:
			l2=ll
		if "=" in l2: 
			member_lines.append(l2)
	for ll in member_lines:
		parts=ll.split("=")
		if(len(parts)>2):
			print "Line: \""+ll+"\" ignored"
			continue
		if(parts[0] == "DATATREE"):
			for tree in parts[1].split(" ") :
				Analyzer.AddTree(tree)
		if(parts[0] == "PtCuts"):
			PtCuts=[]
			for pt in parts[1].split(" "):
				PtCuts.append(pt)
		if(parts[0] == "SigPhId"):
			SigPhId=[]
			for id in parts[1].split(" "):
				SigPhId.append(id)
		if(parts[0] == "BkgPhId"):
			BkgPhId=[]
			for id in parts[1].split(" "):
				BkgPhId.append(id)
		if(parts[0] == "outputFileName"):
			Analyzer.outputFileName=parts[1];
		
	
