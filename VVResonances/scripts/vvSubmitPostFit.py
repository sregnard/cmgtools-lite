#!/usr/bin/env python

import ROOT
import os, sys, re, pickle, shutil, json, random

import optparse
parser = optparse.OptionParser()
parser.add_option("-q","--queue",dest="queue",help="where to launch: norun, local, condor",default='condor')
parser.add_option("-t","--time",dest="time",type=int,help="MaxRuntime in minutes",default=480)
parser.add_option("-o","--options",dest="options",help="Options for runPostFit.py",default='')
(options,args) = parser.parse_args()




leptons = ['mu','e']
purities = ['LP','HP']
categories = ['bb','nobb','vbf']
deltaetas = ['DEtaLo','DEtaMi','DEtaHi']



for v in ['mjj','mvv']:
    for l in leptons:
        for p in purities:
            for c in categories:
              for e in deltaetas:

                scriptname="submit_runPostFit_{v}_{l}_{p}_{c}_{e}".format(v=v,l=l,p=p,c=c,e=e)

                f=open('{script}.sh'.format(script=scriptname),'w')
                execScript = '#!/bin/sh \n'
                execScript += 'cd {cwd} \n'.format(cwd=os.getcwd())
                execScript += 'eval `scramv1 runtime -sh` \n\n'
                execScript += "python $CMSSW_BASE/src/CMGTools/VVResonances/interactive/runPostFit.py {options} -i {input} -v {v} -l {l} -p {p} -c {c} -e {e} 2>&1 | tee log_runPostFit_{v}_{l}_{p}_{c}_{e}.txt\n".format(options=options.options,input=args[0],v=v,l=l,p=p,c=c,e=e)
                execScript += 'cp *.C {cwd}\n cp *.eps {cwd}\n cp *.pdf {cwd}\n cp *.png {cwd}\n cp *.root {cwd}\n'.format(cwd=os.getcwd())

                f.write(execScript)
                f.close()

                f=open("{script}.sub".format(script=scriptname),'w')
                subScript = """
Universe              = vanilla

Executable            = {cwd}/{script}.sh
Output                = {cwd}/{script}.out
Error                 = {cwd}/{script}.err
Log                   = {cwd}/{script}.log
getenv                = True   
+MaxRuntime           = {time}
queue 1
""".format(script=scriptname,cwd=os.getcwd(),time=60*options.time)
                f.write(subScript)
                f.close()

                os.system('chmod +x {script}.sh'.format(script=scriptname))
 
                if options.queue=="norun":
                    print 'Not submitting'
                elif options.queue=="local":
                    os.system('sh {script}.sh'.format(script=scriptname))
                elif options.queue=="condor":
                    os.system('condor_submit {script}.sub '.format(queue=options.queue,script=scriptname))






