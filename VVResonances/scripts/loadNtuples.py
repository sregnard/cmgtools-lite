import os
from CMGTools.VVResonances.plotting.TreePlotter import TreePlotter
from CMGTools.VVResonances.plotting.MergedPlotter import MergedPlotter




def loadNtuples(samples,sampleDir,isData=False):

    sampleTypes=samples.split(',')
    plotters=[]
    pcuts=[]
    filelist=[]

    #print os.listdir(sampleDir)
    #print [g for flist in [[(path+'/'+f) for f in os.listdir(sampleDir+'/'+path)] for path in os.listdir(sampleDir)] for g in flist]

    if sampleDir=='ntuples' or sampleDir=='ntuplesForData':
        filelist = [g for flist in [[(path+'/'+f) for f in os.listdir(sampleDir+'/'+path)] for path in os.listdir(sampleDir)] for g in flist]
    else:
        filelist = os.listdir(sampleDir)

    for filename in filelist:
        for sampleType in sampleTypes:
            if filename.find(sampleType)!=-1:
                fnameParts=filename.split('.')
                fname=fnameParts[0]
                ext=fnameParts[1]
                if ext.find("root") ==-1:
                    continue
                fpath=sampleDir+'/'+fname
                #print 'Adding file', fpath

                plotters.append(TreePlotter(fpath+'.root','tree'))

                ## Fix for cuts and weights for which the branches differ between years:
                if "ntuples2016" in fpath:
                    pcuts.append('(HLT_MU||HLT_ELE||HLT_ISOMU||HLT_ISOELE||HLT_MET||HLT_PHOTON)*L1PrefireWeight')
                elif "ntuples2017" in fpath:
                    pcuts.append('(HLT_MU||HLT_ELE||HLT_ISOMU||HLT_ISOELE||HLT_MET||HLT_PHOTON)*L1PrefireWeight')
                elif "ntuples2018" in fpath:
                    pcuts.append('(HLT_MU||HLT_ELE||HLT_ISOMU||HLT_ISOELE||HLT_MET)')
                else:
                    sys.exit("Year not found, aborting.")

                if not isData:
                    plotters[-1].setupFromFile(fpath+'.pck')
                    plotters[-1].addCorrectionFactor('xsec','tree')
                    plotters[-1].addCorrectionFactor('genWeight','tree')
                    plotters[-1].addCorrectionFactor('puWeight','tree')
                    plotters[-1].addCorrectionFactor('truth_genTop_weight','branch')
                    #plotters[-1].addCorrectionFactor('lnujj_sfWV','branch')
                    #plotters[-1].addCorrectionFactor('lnujj_btagWeight','branch')

                    ''' ## remove the Madgraph background NLO k-factors
                    if fname.find("WJetsToLNu_HT")!=-1:
                        wjetsAntiKFactor = 1./1.21
                        plotters[-1].addCorrectionFactor(wjetsAntiKFactor,'flat')
                        print '  reweighting '+fpath+' '+str(wjetsAntiKFactor)
                    elif fname.find("DYJetsToLL_M50_HT")!=-1:
                        dyAntiKFactor = 1./1.23
                        plotters[-1].addCorrectionFactor(dyAntiKFactor,'flat')
                        print '  reweighting '+fpath+' '+str(dyAntiKFactor)
                    #'''

                    #''' ## rescale the W+jets yields (the current factors were computed from 30 < mjet < 50 GeV, on top of the NLO k-factors)
                    if fname.find("WJetsToLNu_HT")!=-1: 
                        wjetsFactor=1.
                        if   "ntuples2016" in fpath:  wjetsFactor = 1.022
                        elif "ntuples2017" in fpath:  wjetsFactor = 0.926
                        elif "ntuples2018" in fpath:  wjetsFactor = 0.860
                        plotters[-1].addCorrectionFactor(wjetsFactor,'flat')
                        print '  reweighting '+fpath+' '+str(wjetsFactor)
                    #'''

    return MergedPlotter(plotters,pcuts)





def loadSignalNtuples(samples,sampleDir,minMX,maxMX,corr=1.):

    sampleTypes=samples.split(',')
    plotters={}
    pcuts={}
    filelist=[]

    if sampleDir=='ntuples':
        filelist = [g for flist in [[(path+'/'+f) for f in os.listdir(sampleDir+'/'+path)] for path in os.listdir(sampleDir)] for g in flist]
    else:
        filelist = os.listdir(sampleDir)

    for filename in filelist:
        for sampleType in sampleTypes:
            if filename.find(sampleType)!=-1:
                fnameParts=filename.split('.')
                fname=fnameParts[0]
                ext=fnameParts[1]
                if ext.find("root") ==-1:
                    continue
                fpath=sampleDir+'/'+fname

                mass = float(fname.split('_')[-1])

                if mass<minMX or mass>maxMX:
                    continue

                if not mass in plotters.keys():
                    plotters[mass] = []
                    pcuts[mass] = []

                plotters[mass].append(TreePlotter(fpath+'.root','tree'))

                ## Fix for cuts and weights for which the branches differ between years:
                if "ntuples2016" in fpath:
                    pcuts[mass].append('(HLT_MU||HLT_ELE||HLT_ISOMU||HLT_ISOELE||HLT_MET||HLT_PHOTON)*L1PrefireWeight')
                elif "ntuples2017" in fpath:
                    pcuts[mass].append('(HLT_MU||HLT_ELE||HLT_ISOMU||HLT_ISOELE||HLT_MET||HLT_PHOTON)*L1PrefireWeight')
                elif "ntuples2018" in fpath:
                    pcuts[mass].append('(HLT_MU||HLT_ELE||HLT_ISOMU||HLT_ISOELE||HLT_MET)')
                else:
                    sys.exit("Year not found, aborting.")

                plotters[mass][-1].setupFromFile(fpath+'.pck')
                plotters[mass][-1].addCorrectionFactor('xsec','tree')
                plotters[mass][-1].addCorrectionFactor('genWeight','tree')
                plotters[mass][-1].addCorrectionFactor('puWeight','tree')
                #plotters[mass][-1].addCorrectionFactor('lnujj_sfWV','branch')
                #plotters[mass][-1].addCorrectionFactor('lnujj_btagWeight','branch')
                plotters[mass][-1].addCorrectionFactor(corr,'flat')
                plotters[mass][-1].filename=fname

                print 'found', fpath, 'mass', str(mass)


    mergedplotters = {}

    for mass in sorted(plotters.keys()):

        if len(plotters[mass]) != (1,(3,2)['Wprime_VBF_Wh_Wlephinc_narrow' in samples])[sampleDir=='ntuples']: ##FIXME: rechange when 2017 VBFWH is ready
            continue

        mergedplotters[mass]=MergedPlotter(plotters[mass],pcuts[mass])

    return mergedplotters
