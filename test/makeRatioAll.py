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
