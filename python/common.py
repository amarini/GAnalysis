#!/usr/bin/python
import sys,os
import array

def read_dat(filename):
	Dat={}
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
			member_lines.append(l2.strip())
	for ll in member_lines:
		parts=ll.split("=")
		if(len(parts)>2):
			print "Line: \""+ll+"\" ignored"
			continue
		elif(parts[0] == "DATATREE"):
			Dat["DataTree"]=[]
			for tree in parts[1].split(" ") :
				#Analyzer.AddTree(tree)
				Dat["DataTree"].append(tree)
		elif(parts[0] == "PtCuts"):
			Dat["PtCuts"]=[]
			for pt in parts[1].split(" "):
				Dat["PtCuts"].append(float(pt))
		elif(parts[0] == "HtCuts"):
			Dat["HtCuts"]=[]
			for ht in parts[1].split(" "):
				Dat["HtCuts"].append(float(ht))
		elif(parts[0] == "nJetsCuts"):
			Dat["nJetsCuts"]=[]
			for nj in parts[1].split(" "):
				Dat["nJetsCuts"].append(float(nj))
		elif(parts[0] == "SigPhId"):
			Dat["SigPhId"]=[]
			for id in parts[1].split(" "):
				Dat["SigPhId"].append(float(id))
		elif(parts[0] == "BkgPhId"):
			Dat["BkgPhId"]=[]
			for id in parts[1].split(" "):
				Dat["BkgPhId"].append(float(id))
		elif(parts[0] == "outputFileName"):
			Dat["outputFileName"]=parts[1];
		elif(parts[0] == "WorkDir"):
			Dat["WorkDir"]=parts[1];
			if( Dat["WorkDir"][-1] != '/' ): Dat["WorkDir"]+="/";
		elif(parts[0] == "PtBins"):
			Dat["PtBins"]=[]
			for id in parts[1].split(" "):
				Dat["PtBins"].append(float(id))
		elif(parts[0] == "EtaBins"):
			Dat["EtaBins"]=[]
			for id in parts[1].split(" "):
				Dat["EtaBins"].append(float(id))
		elif(parts[0] == "TriggerMenus"):
			Dat["TriggerMenus"]=[]
			for value in parts[1].split(" "):
				Dat["TriggerMenus"].append(value)
		elif(parts[0] == "PtTriggers"):
			Dat["PtTriggers"]=[]
			for pair in parts[1].split(" "):
				str2=pair.replace("[","")
				str2=str2.replace("]","")
				str3=str2.split(",")
				Dat["PtTriggers"].append([float(str3[0]),float(str3[1])])
		elif(parts[0] == "PreScale"):
			Dat["PreScale"]=[]
			for s in parts[1].split(" "):
				Dat["PreScale"].append(float(s))
		elif(parts[0] == "include"):
			filename2=parts[1].replace(" ","")
			k=filename.rfind("/")
			if k>=0:
				dir=filename[:k] + "/"
			else: 
				dir="./"
			try:
				f=open(dir+filename2);
				f.close();
				print "Reading configuration from "+dir+filename2
				Dat2=read_dat(dir+filename2)
				for name in Dat2:
					Dat[name]=Dat2[name]
			except IOError:
				try:
					f=open("./"+filename2);
					f.close();
					print "Reading configuration from ./"+filename2
					Dat2=read_dat("./"+filename2)
					for name in Dat2:
						Dat[name]=Dat2[name]
				except IOError:
					print "ERROR: "+dir+filename2+" - ./"+filename2+" - No such file or directory"
		else: print "Config parameter "+parts[0]+" ignored"
	return Dat

def PrintDat(dat):
	print "--------------------------------------------------------"
	for name in dat:
		print "Dat contains key " +str(name) + " with value: " + str(dat[name])
	print "--------------------------------------------------------"
	print 
	print 
	
