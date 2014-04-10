#/bin/python



from glob import glob 
from subprocess import call

l=glob('h_*.pdf')


for f in l:
	outName="res_"
	if 'lower' in f:
		outName += 'rat_'
	else:
		outName += 'up_'
	#
	#if 'comb' in f:
	outName += 'comb_'
	#elif '_ee_' in f:
	#	outName += 'ee_'
	#elif '_mumu_' in f:
	#	outName += 'mumu_'
	#
	if 'log10' in f:
		outName += 'log10_'
	#
	if 'Zpt_over_pt1' in f:
		outName += 'Zpt_over_pt1_'
	elif 'Zpt_over_HT' in f:
		outName += 'Zpt_over_HT_'
	#elif 'Zpt_hist' in f:
	#	outName += 'Zpt_'
	#
	if 'Zpt40' in f:
		outName += 'ptz40_'
	else:
		outName += 'ptz100_'
	#
	if 'BY_Inf' in f:
		outName += 'yz_inf_'
	else:
		outName += 'yz_1_40_'
	#
	if 'njets3plus_' in f:
		outName += 'njets3plus_'
	#
	if 'njets2plus_' in f:
		outName += 'njets2plus_'
	#
	outName += "data_MG_SH_BH.pdf"

	cmd=["mv", f, outName]
	for i in cmd:
		print i,
	print
