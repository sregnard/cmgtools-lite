#!/usr/bin/env python

import ROOT
import os, sys, re, optparse,pickle,shutil,json,random




parser = optparse.OptionParser()

parser.add_option("-l","--launch",dest="launch",type=int,default=0,help="also launch the jobs")
parser.add_option("-q","--queue",dest="queue",help="Batch Queue",default='8nh')
parser.add_option("-s","--signalType",dest="signalType",default='',help="XWW or XWZ")
parser.add_option("-c","--cats",dest="categories",default='',help="bb or charge")
parser.add_option("-b","--differentBinning",action="store_true",dest="differentBinning",help="use other binning for bb category",default=False)
parser.add_option("-i","--input",dest="inputFile",default='combined.root',help="input root datacard")
parser.add_option("-u","--doUncBand",dest="doUncBand",type=int,default=0,help="do uncertainty band")
(options,args) = parser.parse_args()




s = options.signalType
c = options.categories

for v in ['mjj','mvv']:
#for v in ['mvv']:
#for v in ['mjj']:
    for p in ['HP','LP']:
        for l in ['e','mu']:

            scriptname="submit_runPostFit_{s}_{v}_{p}_{l}.sh".format(s=s,v=v,p=p,l=l)


            f=open(scriptname,'w')
            execScript = 'cd {cwd} \n'.format(cwd=os.getcwd())
            execScript += 'eval `scramv1 runtime -sh` \n\n'
            execScript += "python $CMSSW_BASE/src/CMGTools/VVResonances/interactive/runPostFit.py -i {i} -s '{s}' {R} -v {v} -p {p} -l {l} {c} {b} -u {u} 2>&1 | tee log_runPostFit_{s}_{v}_{p}_{l}_u{u}.txt\n".format(i=options.inputFile,s=s,R=('-r 0.' if s=='' else ''),v=v,p=p,l=l,c=(('-c '+c) if c!='' else ''),b=('-b' if options.differentBinning else ''),u=options.doUncBand)
            f.write(execScript)
            f.close()
            os.system('chmod +x {script}'.format(script=scriptname))
 
            if options.launch:           
                if options.queue!="local":
                    os.system('bsub -q {queue} {script} -J job_runPostFit_{s}_{v}_{p}_{l}_u{u}'.format(queue=options.queue,script=scriptname,s=s,v=v,p=p,l=l,u=options.doUncBand))
                else:    
                    os.system('sh {script}'.format(script=scriptname))





