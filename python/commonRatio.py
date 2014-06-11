
import math
import sys,os
import array

import ROOT
ROOT.gROOT.SetBatch()

DEBUG=1
### READ DAT#########
def ReadRatioDat( inputDat ):
	'''Read a Ratio Dat File. '''
	f=open( inputDat,"r" )
	R={}
	R['Cut']=[]
	R['Syst']=[]
	for l in f:
	   try:
		l0=l.split('#')[0]
		l0=l0.replace('@','#')
		if l0 == "" : continue;
		l0=l0.replace('\n','')
		l0=l0.replace('\r','')
		parts=l0.split(' ')
		if len(parts) == 0 : continue;
		if   parts[0] == 'file1': 
			R["file1"]=parts[1]
			if 'eventList1' not in R: R['eventList1']=''
		elif parts[0] == 'file2': 
			R["file2"]=parts[1]
			if 'eventList2' not in R: R['eventList2']=''
		elif parts[0] == 'lumi1': 
			R["lumi1"]=float(parts[1])
		elif parts[0] == 'lumi2': 
			R["lumi2"]=float(parts[1])
		elif parts[0] == 'eventList1': 
			R['eventList1Compress']=0
			R['eventList1HistoName']=''
			for i in range(1,len(parts)):
				if parts[i].split('=')[0] == 'file':
					R['eventList1']=parts[i].split('=')[1]
				elif parts[i].split('=')[0] == 'compress':
					R['eventList1Compress']=int(parts[i].split('=')[1])
				elif parts[i].split('=')[0] == 'histoName':
					R['eventList1HistoName']=parts[i].split('=')[1]
		elif parts[0] == 'eventList2': 
			R['eventList2Compress']=0
			R['eventList2HistoName']=''
			for i in range(1,len(parts)):
				if parts[i].split('=')[0] == 'file':
					R['eventList2']=parts[i].split('=')[1]
				elif parts[i].split('=')[0] == 'compress':
					R['eventList2Compress']=int(parts[i].split('=')[1])
				elif parts[i].split('=')[0] == 'histoName':
					R['eventList2HistoName']=parts[i].split('=')[1]
		elif parts[0] == 'histoName1': R["histoName1"]=parts[1]
		elif parts[0] == 'histoName2': R["histoName2"]=parts[1]
		elif parts[0] == 'mcName1' or parts[0]=='mcName2' or parts[0]=='mcLeg': 
			if parts[0] not in R: R[parts[0]]=[]
			R[parts[0]].append(parts[1])
		elif parts[0] == 'mcLO1' or parts[0] == 'mcLO2':
			if parts[0] not in R: R[parts[0]]=[]
			R[ parts[0] ].append( float(parts[1]) )
		elif parts[0] =='mcErr1' or parts[0] =='mcErr2':
			if parts[0] not in R:
				R[ parts[0] ] = []
			# mcErr1 0 s NAME the id is needed wrt to the type
			R[ parts[0] ].append( (int(parts[1]),parts[2],parts[3]) )
		elif parts[0] =='mcErrCorr':
			# [-1,1] that correlation
			# >1 FullCorr
			# <-1 o not existing Uncorrelated
			if parts[0] not in R: R[ parts[0] ] =[]
			R[ parts[0] ].append(float(parts[1]))
		elif parts[0] == 'mcErrLeg':
			if parts[0] not in R:
				R[ parts[0] ] = []
			R[ parts[0] ].append(parts[1])
		elif parts[0] == 'NoMC':
			R['mcErr1']=[]
			R['mcErr2']=[]
			R['mcErrLeg']=[]
			R['mcErrCorr']=[]
			R['mcName1']=[]
			R['mcName2']=[]
			R['mcLeg']=[]
			R['mcLO1']=[]
			R['mcLO2']=[]
		elif parts[0] == 'NoMCErr':
			R['mcErr1']=[]
			R['mcErr2']=[]
			R['mcErrLeg']=[]
			R['mcErrCorr']=[]
		#elif parts[0] == 'mcName1': R["mcName1"]=parts[1]
		#elif parts[0] == 'mcName2': R["mcName2"]=parts[1]
		elif parts[0] == 'cov1': R["cov1"]=parts[1]
		elif parts[0] == 'cov2': R["cov2"]=parts[1]
		elif parts[0] == 'NoCut':
			R['Cut']=[]
		elif parts[0] == 'Cut':
			#default
			ht=0
			nj=1
			ptj=30
			for j in range(1,len(parts)):
				if 'Ht' == parts[j].split('=')[0]:ht=parts[j].split('=')[1]
				if 'nJets' == parts[j].split('=')[0]:nj=parts[j].split('=')[1]
				if 'ptJet' == parts[j].split('=')[0]:ptj=parts[j].split('=')[1]
			R['Cut'].append( (ht,nj,ptj) );
		elif parts[0] == 'Syst':
			name=parts[1]
			typ=parts[2]
			hn1=parts[3]
			hn2=parts[4]
			R['Syst'].append( (name,typ,hn1,hn2) )
		elif parts[0] == 'RhoSyst':
			name=parts[1]
			rho=float(parts[2])
			if 'RhoSyst' not in R:
				R['RhoSyst']={}
			R[ 'RhoSyst' ][name]=rho
		elif parts[0] == 'Up':
			R['Up']=[]
			R['Up'].append(parts[1])
			R['Up'].append(parts[2])
		elif parts[0] == 'Down':
			R['Down']=[]
			R['Down'].append(parts[1])
			R['Down'].append(parts[2])
		elif parts[0] == 'Out':
			R['Out']=parts[1]
		elif parts[0] == 'OutName':
			R['OutName']=parts[1]
		elif parts[0] == 'PrePendSyst':
			K =  parts[1:]
			R['PrePendSyst']=[]
			for s in K:
				s=s.replace("'","")
				s=s.replace('"',"")
				R['PrePendSyst'].append(s)
		elif parts[0] == 'xaxis' or parts[0]=='yaxis':
			R[parts[0]]=[ float(parts[1]), float(parts[2] )]
		elif parts[0] == 'xleg' or parts[0]=='yleg':
			R[parts[0]]=[ float(parts[1]), float(parts[2] )]
		elif parts[0] == 'xtitle' or parts[0]=='ytitle' or parts[0]=='text':
			R[parts[0]]= parts[1].replace('~',' ')
		elif parts[0] == 'ylog' or parts[0]=='xlog':
			R[parts[0]] = int(parts[1])
		elif parts[0] == 'Merge1' or parts[0]=='Merge2':
			if parts[0] not in R:
				R[parts[0]]=[]
			R[parts[0]].append( (float(parts[1]),float(parts[2])) )
		elif parts[0] == 'include':
			tmp = ReadRatioDat( parts[1] )
			for key in tmp:
				R[ key ] = tmp[ key ]
		elif parts[0] == 'mc' or parts[0] == 'table' or parts[0] == 'StatCorr': ## set mc in the config file
			R[ parts[0] ] = int(parts[1])
		else:
			if len(parts)>0 and parts[0].replace(' ','').replace('\t','') != '' :print "Malformed line (probably ignored):"+l
	   except: 
		print "Malformed line (probably ignored):"+l
	#set default if not specified in dat file
	if 'xaxis' not in R:
		R['xaxis']=[0,0]
	if 'yaxis' not in R:
		R['yaxis']=[0,0]
	if 'xlog' not in R:
		R['xlog']=0
	if 'ylog' not in R:
		R['ylog']=0
	if 'OutName' not in R:
		R['OutName']="Ht_${.0fHT}_nJets_${.0fNJETS}_ptJet_${.0fPTJ}"
	if 'mcLO1' not in R: R['mcLO1']=[1.]
	if 'mcLO2' not in R: R['mcLO2']=[1.]
	if 'mcLeg' not in R: R['mcLeg']=["MG"]
	if 'mcErr1' not in R: R['mcErr1']=[]
	if 'mcErr2' not in R: R['mcErr2']=[]
	if 'mcErrLeg' not in R: R['mcErrLeg']=[]
	if len(R['mcName1'] ) != len(R['mcName2']): print "Config error in Len mc Name"
	for i in range(len(R['mcLO1']),len(R['mcName1'])):
		R['mcLO1'].append(1.)
	for i in range(len(R['mcLO2']),len(R['mcName2'])):
		R['mcLO2'].append(1.)
	for i in range(len(R['mcLeg']),len(R['mcName1'])):
		R['mcLeg'].append("XXX")
	return R;

def makeBands(h1,h2,type="Mean"):
	H=h1.Clone(h1.GetName()+"_band")
	for i in range(1,h1.GetNbinsX()+1):
		if type=="First":
			H.SetBinContent(i, h1.GetBinContent(i))
			H.SetBinError  (i, math.fabs(h1.GetBinContent(i)-h2.GetBinContent(i) ))
		else: #type = "Mean"
			H.SetBinContent(i, (h1.GetBinContent(i)+h2.GetBinContent(i) )/2.0)
			H.SetBinError  (i, math.fabs(h1.GetBinContent(i)-h2.GetBinContent(i) )/2.0)
	return H

def sqrtSum(h1,h2,epsilon=0.0001):
	for i in range (1,h2.GetNbinsX()+1):
		if h1.GetBinError(i)  > epsilon and h2.GetBinError(i)  > epsilon:
			e=math.sqrt( h1.GetBinError(i)**2 + h2.GetBinError(i)**2 )
		elif h1.GetBinError(i) <= epsilon and h2.GetBinError(i) <= epsilon:
			e=epsilon
		elif h1.GetBinError(i) > epsilon:
			e=h1.GetBinError(i)
		elif h2.GetBinError(i) > epsilon:
			e=h2.GetBinError(i)
		elif ROOT.TMath.IsNaN( h1.GetBinError(i) ) or ROOT.TMath.IsNaN( h2.GetBinError(i) ):
			e=epsilon
		else:
			print "-- assertion error -- %f -- %f -- %f"%(h1.GetBinError(i),h2.GetBinError(i),epsilon)
			e=epsilon
		h1.SetBinError(i, e)

def SetStatCorr(h1,h2,R):
   print "Stat Errors: A/(A+B)"
   for i in range(1,h1.GetNbinsX()+1):
	e1=h1.GetBinError(i)
	c1=h1.GetBinContent(i)
	e2=h2.GetBinError(i)
	c2=h2.GetBinContent(i)
	a=c1
	da=e1
	b=c2-c1
	if e2<e1:
		print "Stat Error:", e2,">",e1 ," -- c2,c1 ", c2,">",c1
		print "Setting db/b= dc2/c2"
		db= e2/c2*b
	else:
		db=math.sqrt(e2**2-e1**2)
	if a+b >0:
		r=a/(a+b)
		dr = math.sqrt( ( (b * da)**2 + (a * db )**2 ) / (a+b)**4)
		#dr=r*math.sqrt( db**2/(a+b)**2 + b**2/(a**2 * (a+b)**2)) 
	else :
		r=0
		dr=1
	if r> 0 and math.fabs(R.GetBinContent(i) - r)/r >0.02 : 
		print "Error in ratio from different computations"
	R.SetBinError(i,dr)
   return

def Ratio(H,H1,NoErrorH=False,FullCorr=False,rho=-2):
	''' Make Ratio between two histograms: H1/H\n\tNoErroron H -> Ratio wrt data,\n\t FullCorr=consider error as fully correlated'''
	R=H1.Clone(H1.GetName()+"_ratio")
	hTmp=H.Clone("tmp")
	#in order to account error properly in ratios
	if NoErrorH:
		for i in range(1,hTmp.GetNbinsX()+1):
			hTmp.SetBinError(i,0)
	R.Divide(hTmp)
	if FullCorr:
		for i in range(1,R.GetNbinsX()+1):
			if H.GetBinContent(i)+H.GetBinError(i) != 0:
				up=(H1.GetBinContent(i)+H1.GetBinError(i))/(H.GetBinContent(i)+H.GetBinError(i))
				dn=(H1.GetBinContent(i)-H1.GetBinError(i))/(H.GetBinContent(i)-H.GetBinError(i))
			else: 
				up=0
				dn=0
			err = math.fabs((up-dn)/2.0)
			R.SetBinError(i,err)
	elif (rho >= -1 and rho <=1):
		for i in range(1,R.GetNbinsX()+1):
			e1=H1.GetBinError(i)
			c1=H1.GetBinContent(i)
			e2=H.GetBinError(i)
			c2=H.GetBinContent(i)
			if c1 > 0 and c2>0 :
				erOr = math.sqrt( (e1/c1)**2+(e2/c2)**2 - 2*rho*(e1/c1)*(e2/c2) )
			else:
				erOr = 0
			R.SetBinError(i,R.GetBinContent(i)*erOr)
		

	return R

import gzip
def computeOverlap(eventList1,compress1,name1,pt1,eventList2,compress2,name2,pt2):
	if eventList1=='' or eventList2=='': return (0,1,1);
	l1=glob(eventList1);
	l2=glob(eventList2);
	EventList1={}
	EventList2={}
	for fileName in l1:
		if compress1:file1 = gzip.open(fileName,"r")
		else:        file1 =      open(fileName,"r")
		
		for l in file1:
			parts=l.split();
			run = -1 
			lumi= -1
			event= -1
			name=''
			high=-1
			low=-1
			for p in parts:
				if p.split(':')[0]=='run':run = int (p.split(':')[1] )
				elif p.split(':')[0]=='lumi':lumi = int (p.split(':')[1] )
				elif p.split(':')[0]=='event':event = int (p.split(':')[1] )
				elif p.split(':')[0]=='name':name = str (p.split(':')[1] )
				elif p.split(':')[0]=='high':high = float (p.split(':')[1] )
				elif p.split(':')[0]=='low':low = float (p.split(':')[1] )
			if (not (pt1>=low and pt1<high)) and pt1>=0:continue;
			if name1 != "" and name != name1:continue;
			EventList1[ (run,lumi,event) ] = 1
		file1.close();
	for fileName in l2:
		if compress2:file2 = gzip.open(fileName,"r")
		else:        file2 =      open(fileName,"r")
		
		for l in file2:
			parts=l.split();
			run = -1 
			lumi= -1
			event= -1
			name=''
			high=-1
			low=-1
			for p in parts:
				if p.split(':')[0]=='run':run = int (p.split(':')[1] )
				elif p.split(':')[0]=='lumi':lumi = int (p.split(':')[1] )
				elif p.split(':')[0]=='event':event = int (p.split(':')[1] )
				elif p.split(':')[0]=='name':name = str (p.split(':')[1] )
				elif p.split(':')[0]=='high':high = float (p.split(':')[1] )
				elif p.split(':')[0]=='low':low = float (p.split(':')[1] )
			if (not (pt2>=low and pt2<high)) and pt2>=0:continue;
			if name2 != "" and name != name2:continue;
			EventList2[ (run,lumi,event) ] = 1
		file2.close();
	common=0;
	only1=0;
	only2=0
	for (run,lumi,event) in EventList1:
		if (run,lumi,event) in EventList2:
			common+=1	
			EventList2[(run,lumi,event)]=0
		else: only1+=1
	for (run,lumi,event) in EventList2:
		if EventList2[(run,lumi,event)] == 0: only2+=1
	return (common,only1,only2)				

def FixNames(histoName,cut,syst=''):
	n=histoName.find('$')
	if n<0: return histoName;
	if histoName[n+1] != '{': print 'PUT ${} things that must be sub'
	#look for first }
	r=histoName.find('}')
	if (r<n):print "error } $"
	
	#copy from n to r
	substring=histoName[n+2:r] ## keep out ${}
	#cut[0]=ht cut[1]=njets cut[2]=pt
	if 'HT' in substring:
		var =float(cut[0])
		substring=substring.replace('HT','')
		if substring=='': substring='%d'
		else: substring='%'+substring
	elif 'NJETS' in substring:
		var=float(cut[1])
		substring=substring.replace('NJETS','')
		if substring=='': substring='%d'
		else: substring='%'+substring
	elif 'PTJ' in substring:
		var=float(cut[2])
		substring=substring.replace('PTJ','')
		if substring=='': substring='%d'
		else: substring='%'+substring
	elif 'SYST' in substring:
		var=syst
		substring=substring.replace('SYST','')
		if substring=='': substring='%s'
		else: substring='%'+substring
	else: 
		print "error: unknown substitution"
		var=''
	#print "histoname=" + histoName[:n] + "   substri="+ substring + "    histoname="+histoName[r+1:] 
	name=(histoName[:n] + substring + histoName[r+1:] )%(var)
	return FixNames(name,cut,syst)

def ConvertToTargetTH1( h1, h2):
	h2.SetName("old_"+h2.GetName())
	h=h1.Clone(h2.GetName());
	for iBin in range(1,h.GetNbinsX()+1):
		h.SetBinContent(iBin,  h2.GetBinContent(h2.FindBin(h.GetBinCenter(iBin)) ))
		h.SetBinError(iBin,    h2.GetBinError  (h2.FindBin(h.GetBinCenter(iBin)) ))
	return h


ROOT.gROOT.ProcessLine("struct Bins{ \
		Double_t PtBins[1023];\
		int nBins;\
		};")

from ROOT import Bins

def MergeBins(l,h,cov=None):
	#l=[ (Bin0,Bin1),(Bin0,Bin1)]
	if len(l)==0: return h

	listOfBins=ROOT.Bins()
	listOfBins.nBins=0;
	for iBin in range(1,h.GetNbinsX()+2):
		isVeto=False
		for bound in l:
			if iBin==1 and DEBUG >1: print "Veto Bound:",bound[0],bound[1] ### DEBUG
			if ( bound[0]<=h.GetBinLowEdge(iBin) and h.GetBinLowEdge(iBin)<bound[1]):
				isVeto=True
		if DEBUG>1:print "Merge: iBin=",iBin,"Bound=",h.GetBinLowEdge(iBin),"is  a valid bin=",not isVeto
		if not isVeto:
			listOfBins.PtBins[listOfBins.nBins] = h.GetBinLowEdge(iBin)
			listOfBins.nBins += 1
	listOfBins.nBins -= 1
	h2 = ROOT.TH1D(h.GetName()+"_rebin",h.GetTitle(),listOfBins.nBins,listOfBins.PtBins)

	#doCov= (cov==None)
	if isinstance(cov,ROOT.TH2D) or isinstance(cov,ROOT.TH2F): doCov=True
	else: doCov=False

	if cov==None: doCov=False
	##########################
	#doCov=False
	##########################
	if not doCov:
	   print "Merging No Cov"
	   for iBin in range(1,h.GetNbinsX()+1):
		Bin2=h2.FindBin( h.GetBinCenter(iBin) )
		w1=h.GetBinWidth( iBin )
		w2=h2.GetBinWidth( Bin2 )

		e1=h.GetBinError( iBin ) * w1
		e2=h2.GetBinError( Bin2 ) * w2
		c1=h.GetBinContent( iBin ) * w1
		c2=h2.GetBinContent( Bin2 ) * w2
		
		if e1 != 0 and e2 !=0:
			#mean
			#h2.SetBinContent(Bin2, ( c1/(e1**2) + c2/(e2**2) ) / ( 1./(e1**2) + 1./(e2**2)  ) )
			#h2.SetBinError(Bin2, math.sqrt(1./ ( 1./(e1**2) + 1./(e2**2) )) )
			h2.SetBinContent(Bin2, c1 + c2  ) 
			h2.SetBinError(Bin2, math.sqrt(e1**2 + e2**2) )
		elif e1 !=0:
			h2.SetBinContent(Bin2,c1)
			h2.SetBinError(Bin2,e1)
		elif e2 !=0:
			h2.SetBinContent(Bin2,c2)
			h2.SetBinError(Bin2,e2)

		h2.SetBinContent(Bin2, h2.GetBinContent(Bin2)/w2)
		h2.SetBinError(Bin2, h2.GetBinError(Bin2)/w2)
	else: #cov!=NULL
		print "Merging Using Cov"
		cov2 = ROOT.TH2D(cov.GetName()+"_rebin",h.GetTitle(),listOfBins.nBins,listOfBins.PtBins, listOfBins.nBins,listOfBins.PtBins)
		for iBin in range(1,h.GetNbinsX()+1):
		     iBin2=h2.FindBin( h.GetBinCenter(iBin) )
		     w1=h.GetBinWidth( iBin )
		     w2=h2.GetBinWidth( iBin2 )

		     #e1=h.GetBinError( iBin ) * w1
		     #e2=h2.GetBinError( Bin2 ) * w2
		     c1=h.GetBinContent( iBin ) * w1
		     c2=h2.GetBinContent( iBin2 ) * w2

		     h2.SetBinContent(iBin2, c1 + c2  ) 

		     for jBin in range(1,h.GetNbinsX()+1):
			     jBin2 = h2.FindBin( h.GetBinCenter(jBin) ) 
		             v1=h.GetBinWidth( jBin )
		             v2=h2.GetBinWidth( jBin2 )
			     cov2.SetBinContent(iBin2,jBin2, cov2.GetBinContent(iBin2,jBin2)*w2*v2 + cov.GetBinContent(iBin,jBin) * w1 * v1 )
			     cov2.SetBinContent(iBin2,jBin2, cov2.GetBinContent(iBin2,jBin2) / (w2*v2))


		     h2.SetBinContent(iBin2, h2.GetBinContent(iBin2)/w2)

		for iBin2 in range(1,h2.GetNbinsX()+1):
		     h2.SetBinError(iBin2, math.sqrt(cov2.GetBinContent(iBin2,iBin2) ))
		### END COV


	if DEBUG>1:
	   for iBin2 in range(1,h2.GetNbinsX()+1):
		x=h2.GetBinCenter(iBin2)
		line1="Bin %.0f <- ["%(x)
		line2="    (%.3f +o- %.3f) <- ["%(h2.GetBinContent(iBin2),h2.GetBinError(iBin2))
		for jBin in range(1,h.GetNbinsX()+1):
			if h.GetBinCenter(jBin)>h2.GetBinLowEdge(iBin2)  and h.GetBinCenter(jBin)<h2.GetBinLowEdge(iBin2+1):
					line1 += " %.0f" % h.GetBinCenter(jBin)
					line2 += " (%.3f +- %.3f) , " % (h.GetBinContent(jBin),h.GetBinError(jBin))
		line1 += "]"
		line2 += "]"
		print line1
		print line2
	return h2

def ConvertToLatex(T):
	L="\\begin{tabular}{c|"
	for i in range(1,len(T[0])): #n.of cols
		L+= "c"
	L += "}\n\\hline\n"
	L += " &".join(T[0])
	L+=" \\\\ \n \\hline\n"
	for row in T[1:-1]:
		L+=" & ".join(row)
		L+=" \\\\ \n "
	L += " &".join(T[-1])
	L += "\n" # no \\
	L += "\\end{tabular}"
	return L


def ReadSyst(config,typ,n,cut,syst,hns1,file1,h1):
		''' Type are: \n\t+ for a double band wrt to the content of UP/DN\n\t: for a single band  wrt to the content\n\t. for ignore\n\t% for a fixed %\n\t& for an absolute syst error wrt to the content (content is the syst itself and not mean+-syst)\n\ts error is the syst'''
		if hns1=='None' and n==0: typ='.'+typ[1]
		if hns1=='None' and n==1: typ=typ[0]+'.'

		if typ[n]=='+': #h1 double band
			h1nup=FixNames(hns1,cut,config["PrePendSyst"][n]+syst+config['Up'][n])
			h1ndn=FixNames(hns1,cut,config["PrePendSyst"][n]+syst+config['Down'][n])
			print "Going to get Histo " +h1nup + " - " + h1ndn
			h1up=file1.Get(h1nup)
			h1dn=file1.Get(h1ndn)
			if 'Merge%d'%(n+1) in config:
				h1up=MergeBins(config['Merge%d'%(n+1)],h1up)
				h1dn=MergeBins(config['Merge%d'%(n+1)],h1dn)
			h1up=ConvertToTargetTH1(h1,h1up)
			h1dn=ConvertToTargetTH1(h1,h1dn)
			h1up.Scale(1./config["lumi%d"%(n+1)])
			h1dn.Scale(1./config["lumi%d"%(n+1)])
			s1=makeBands(h1up,h1dn,"Mean")
		elif typ[n]==':':
			h1nfirst=FixNames(hns1,cut,config["PrePendSyst"][n]+syst)
			print "Going to get Histo " + h1nfirst
			h1first=file1.Get(h1nfirst)
			if 'Merge%d'%(n+1) in config:
				h1first=MergeBins(config['Merge%d'%(n+1)],h1first)
			h1first=ConvertToTargetTH1(h1,h1first)
			h1first.Scale(1./config["lumi%d"%(n+1)])
			s1=makeBands(h1,h1first,"First")
		elif typ[n]=='.':
			s1=h1.Clone("syst%d_"%(n+1)+syst) #h1 is already scaled
			for i in range(1,s1.GetNbinsX()+1): s1.SetBinError(i,0);
		elif typ[n]=='&': #content of the histo is the error itsef
			h1nerr=FixNames(hns1,cut,config["PrePendSyst"][n]+syst)
			print "Going to get Histo "+ h1nerr 
			h1err=file1.Get(h1nerr)
			h1err=ConvertToTargetTH1(h1,h1err)
			h1err.Scale(1./config["lumi%d"%(n+1)])
			s1=h1.Clone("syst%d_"%(n+1)+syst) #h1 is already scaled
			if 'Merge%d'%(n+1) in config:
				s1=MergeBins(config['Merge%d'%(n+1)],s1)
			for i in range(1,s1.GetNbinsX()+1): 
				#print "DEBUG Z ",syst,"Bin%d"%i,"%.0f %%"%( h1err.GetBinContent(i)/h1.GetBinContent(i) ), " %.0f-%.0f"%( h1err.GetBinCenter(i),h1.GetBinCenter(i) ),"%f/%f"%(h1err.GetBinContent(i),h1.GetBinContent(i))
				s1.SetBinError(i,h1err.GetBinContent(i) );
		elif typ[n]=='^': #h1 double band, content is the error
			h1nup=FixNames(hns1,cut,config['Up'][n])
			h1ndn=FixNames(hns1,cut,config['Down'][n])
			print "Going to get Histo " +h1nup + " - " + h1ndn
			h1up=file1.Get(h1nup)
			h1dn=file1.Get(h1ndn)
			if 'Merge%d'%(n+1) in config:
				h1up=MergeBins(config['Merge%d'%(n+1)],h1up)
				h1dn=MergeBins(config['Merge%d'%(n+1)],h1dn)
			h1up.Scale(1./config["lumi%d"%(n+1)])
			h1dn.Scale(1./config["lumi%d"%(n+1)])
			h1up=ConvertToTargetTH1(h1,h1up)
			h1dn=ConvertToTargetTH1(h1,h1dn)
			#s1=h1.Clone("syst%d_"%(n+1)+syst) #h1 is already scaled
			for i in range(1,h1up.GetNbinsX()+1): 
				print "Syst",h1nup,"h1up=",h1up.GetBinContent(i)/h1.GetBinContent(i) *100,"%% h1dn=",h1dn.GetBinContent(i)/h1.GetBinContent(i) *100,"%%"
				upUnc=h1.GetBinContent(i)
				dnUnc=h1.GetBinContent(i)
				upUnc=max(upUnc,h1.GetBinContent(i)+h1up.GetBinContent(i))
				upUnc=max(upUnc,h1.GetBinContent(i)-h1dn.GetBinContent(i))
				dnUnc=min(dnUnc,h1.GetBinContent(i)+h1dn.GetBinContent(i))
				dnUnc=min(dnUnc,h1.GetBinContent(i)-h1dn.GetBinContent(i))
				h1.GetBinContent(i)-h1dn.GetBinContent(i)
				h1up.SetBinContent(i,upUnc );
				h1dn.SetBinContent(i,dnUnc );
			s1=makeBands(h1up,h1dn,"Mean")
		elif typ[n]=='%': #content of the histo is the error itsef
			e=float(hns1)/100.
			s1=h1.Clone("syst%d_"%(n+1)+syst) #h1 is already scaled
			for i in range(1,s1.GetNbinsX()+1): s1.SetBinError(i,h1.GetBinContent(i) * e );
		elif typ[n]=='s':
			h1nerr=FixNames(hns1,cut,config["PrePendSyst"][n]+syst)
			print "Going to get Histo "+ h1nerr 
			h1err=file1.Get(h1nerr)
			h1err=ConvertToTargetTH1(h1,h1err)
			h1err.Scale(1./config["lumi%d"%(n+1)])
			s1=h1.Clone("syst%d_"%(n+1)+syst) #h1 is already scaled
			if 'Merge%d'%(n+1) in config:
				s1=MergeBins(config['Merge%d'%(n+1)],s1)
			for i in range(1,s1.GetNbinsX()+1): 
				s1.SetBinError(i,h1err.GetBinError(i) );
			return s1
		else: print "error on type "+str(n)+" of "+typ	
		s1.SetName("syst%d_"%(n+1)+syst)
		return s1

def NiceRange(h,Range,factor=0.2,factor2=0.2):
	''' Change Bins of histograms in order to add an empty (smaller by factor) bin at the begin and end, within the given range\n
	'''
	listOfBins=ROOT.Bins()
	listOfBins.nBins=0;
	l=[]
	#use List
	for iBin in range(1,h.GetNbinsX()+2): ## bin boundaries
		if Range[0] <= h.GetBinLowEdge(iBin) and h.GetBinLowEdge(iBin) <= Range[1]:
			l.append( h.GetBinLowEdge(iBin) )
	l = [ l[0] - (l[1]-l[0])*factor ]+ l
	l += [ l[-1] + (l[-1]-l[-2]) *factor2 ] 
	# prepare ROOT structure
	for binBound in l:
			listOfBins.PtBins[ listOfBins.nBins ] = binBound
			listOfBins.nBins += 1
	listOfBins.nBins -= 1

	h2 = ROOT.TH1D(h.GetName()+"_nicerange",h.GetTitle(),listOfBins.nBins,listOfBins.PtBins)
	for iBin in range(1,h.GetNbinsX()+1):
		if Range[0]<h.GetBinCenter(iBin) and h.GetBinCenter(iBin) < Range[1]:
			h2.SetBinContent(h2.FindBin(h.GetBinCenter(iBin)), h.GetBinContent( iBin  ) )
			h2.SetBinError(h2.FindBin(h.GetBinCenter(iBin)), h.GetBinError( iBin  ) )
	h2.SetLineColor( h.GetLineColor())
	h2.SetLineStyle( h.GetLineStyle())
	h2.SetLineWidth( h.GetLineWidth())
	h2.SetFillColor( h.GetFillColor())
	h2.SetFillStyle( h.GetFillStyle())
	h2.SetMarkerColor( h.GetMarkerColor())
	h2.SetMarkerStyle( h.GetMarkerStyle())
	h2.GetXaxis().SetTitle(h.GetXaxis().GetTitle())
	h2.GetYaxis().SetTitle(h.GetYaxis().GetTitle())
	return h2


