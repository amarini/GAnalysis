#!/usr/bin/python
import sys,os
import array

def read_dat(filename):
	''' Read A dat file configuration from filename 
	'''
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
		elif(parts[0] == "Lumi"):
			Dat["Lumi"]=float(parts[1])
		elif(parts[0] == "Attribute"):
			if "Attribute" not in Dat: Dat["Attribute"]=[]
			for attr in parts[1].split(';'):
				if len(attr.split(':')) > 1: Dat["Attribute"].append( (attr.split(':')[0],attr.split(':')[1]) )
		elif(parts[0] == "Functions"):
			if "Functions" not in Dat: Dat["Functions"]=[]
			for attr in parts[1].split(':'):
				attr=attr.replace('\n','')
				attr=attr.replace('\r','')
				if attr!="":Dat["Functions"].append( attr )
		elif(parts[0] == "dumpAscii"):
			Dat["dumpAscii"]=int(parts[1])
		elif(parts[0] == "DoSyst"):
			Dat["DoSyst"]=int(parts[1])
		elif(parts[0] == "DoShapeCorrFit"):
			Dat["DoShapeCorrFit"]=int(parts[1])
		elif(parts[0] == "DoBiasStudies"):
			Dat["DoBiasStudies"]=int(parts[1])
		elif(parts[0] == "UsePUWeightHLT"):
			Dat["UsePUWeightHLT"]=int(parts[1])
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
		elif(parts[0] == "JetPt"):
			Dat["JetPt"]=[]
			for pt in parts[1].split(" "):
				Dat["JetPt"].append(float(pt))
		elif(parts[0] == "JetEta"):
			Dat["JetEta"]=float(parts[1])
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
					if (name=="Attribute" or name=="Functions" )and name in Dat:
						Dat[name]+=Dat2[name]
					else:
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
	''' Print a Dat File '''
	print "--------------------------------------------------------"
	for name in dat:
		print "Dat contains key " +str(name) + " with value: " + str(dat[name])
	print "--------------------------------------------------------"
	print 
	print 
def ReadFromDat(dat,what,default,Error):
	''' Read From a Dat file:
	dat is the dat file
	what is the parameter
	default is the default value
	Error is the error message if what is not found 
	'''
	try:
		return dat[what]
	except KeyError:
		print Error
		return default
def SetAttribute(Analyzer, attr,value ):
	''' Set Attribute attr with value in the Analyzer'''
	print "Set Attribute %s to %s"%(attr,value)
	exec("Analyzer.%s=%s"%(attr,value))
	return
def SetFunction(Analyzer, attr ):
	'''Call Function attr in the analyzer: attr=Init() ->Analyzer.Init()'''
	print "Executing Functions '%s'"%attr
	print "Analyzer.%s"%(attr)
	exec("Analyzer.%s"%(attr))
	return
def SetAttributes(Analyzer, dat):
	for (attr,value) in dat["Attribute"]:
		SetAttribute(Analyzer,attr,value)
	for attr in dat["Functions"]:
		SetFunction(Analyzer,attr)
	return
