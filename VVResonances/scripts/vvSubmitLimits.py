#!/usr/bin/env python

import ROOT
import os, sys, re, optparse,pickle,shutil,json,random




parser = optparse.OptionParser()

parser.add_option("-s","--step",dest="step",type=float,help="step for mass points",default=1000.0)
parser.add_option("-m","--min",dest="min",type=float,help="minimum Mass point",default=1000.0)
parser.add_option("-M","--max",dest="max",type=float,help="maximum Mass point",default=5000.0)
parser.add_option("-o","--options",dest="options",help="Combine Options",default='-M Asymptotic')
parser.add_option("-q","--queue",dest="queue",help="Batch Queue",default='8nh')
parser.add_option("-r","--randomSeeds",dest="randomize",type=int,help="randomize seeds",default=0)
parser.add_option("-t","--time",dest="time",type=int,help="MaxRuntime in minutes",default=480)
(options,args) = parser.parse_args()


STEPS = int((options.max-options.min)/options.step)

massPoints=[]

for i in range(0,STEPS+1):
    massPoints.append(options.min+i*options.step)




for i,m in enumerate(massPoints):

    if options.randomize:
        suffixOpts=" -s {rndm}".format(rndm = int(random.random()*950000))
    else:
        suffixOpts=" "


    f=open("submit_{i}.sh".format(i=i),'w')
    execScript = '#!/bin/sh \n'
    execScript += 'cd {cwd} \n'.format(cwd=os.getcwd())
    execScript += 'eval `scramv1 runtime -sh` \n'
    execScript += "combine -m {mass} {options}  {file}\n".format(mass=m,options=options.options+suffixOpts,file=args[0])
    execScript += 'cp *.root {cwd} \n'.format(cwd=os.getcwd())

    f.write(execScript)
    f.close()

    f=open("submit_{i}.sub".format(i=i),'w')
    subScript = """
Universe              = vanilla

Executable            = {cwd}/submit_{i}.sh
Output                = {cwd}/submit_{i}.out
Error                 = {cwd}/submit_{i}.err
Log                   = {cwd}/submit_{i}.log
getenv                = True   
+MaxRuntime           = {time}
queue 1
""".format(i=i,cwd=os.getcwd(),time=60*options.time)
    f.write(subScript)
    f.close()
    


    os.system('chmod +x submit_{i}.sh'.format(i=i))

    if options.queue=="norun":
        print 'Not submitting'
    elif options.queue!="local":
        os.system('condor_submit submit_{i}.sub '.format(queue=options.queue,i=i))
    else:    
        os.system('sh submit_{i}.sh '.format(i=i))





