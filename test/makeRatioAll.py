#!/usr/bin/python
from subprocess import call

cmd0=["python", "python/makeRatioPlots.py","--mc" ,"-b"]

cmd= cmd0 + ["--inputDat=data/configRatio.dat" ]
call(cmd)
cmd= cmd0+ ["--inputDat=data/configRatio_PTJ300.dat" ]
call(cmd)
cmd= cmd0+ ["--inputDat=data/configRatio_NJets2.dat" ]
call(cmd)
cmd= cmd0+ ["--inputDat=data/configRatio_HT300.dat" ]
call(cmd)


TMP="/tmp"
for Bin in ["Ht_0_nJets_1_ptJet_30","Ht_0_nJets_1_ptJet_300","Ht_0_nJets_2_ptJet_30","Ht_300_nJets_1_ptJet_30"]:

	tex=open("%s/table_%s.tex"%(TMP,Bin),"w")
	tex.write("\\documentclass[8pt,landscape]{article}\n\\usepackage[usenames]{color} %used for font color\n \\usepackage{amssymb} %maths\n\\usepackage{amsmath} %maths \n\\usepackage{amsfonts} %mats\n\\usepackage[utf8]{inputenc} %useful to type directly diacritic characters\n\\usepackage{mathrsfs}\n\\usepackage{graphicx} % rotatebox reflectbox\n")
	tex.write("\\usepackage[margin=1cm]{geometry}\n")
	tex.write("\\begin{document}\n \n\\footnotesize{\n")
	tex.close()

	#cmd = ["cat","../V00-14/C_%s.tex"%Bin,"> /tmp/table_%s.tex"%Bin]
	#call(cmd)
	with open('%s/table_%s.tex'%(TMP,Bin),'a') as outFile:
		with open('../V00-14/C_%s.tex'%Bin, 'r') as inFile:
			outFile.write(inFile.read())

	tex=open("%s/table_%s.tex"%(TMP,Bin),"a")
	tex.write("} %end small\n %\\end{table}\n\\end{document}")
	tex.close()

	cmd=["pdflatex","-output-directory=/tmp/","/tmp/table_%s.tex"%Bin]
	call(cmd)
	#cmd=["mv","/tmp/C_%s.pdf"%Bin,"../V00-14/table_%s.pdf"%Bin]
	cmd=["mv","%s/table_%s.pdf"%(TMP,Bin),"../V00-14/table_%s.pdf"%Bin]
	call(cmd)

