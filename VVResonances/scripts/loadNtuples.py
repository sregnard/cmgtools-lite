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
                #print 'Adding file', fname

                plotters.append(TreePlotter(sampleDir+'/'+fname+'.root','tree'))

                ## Temporary fix for HLT flags and MET flags:
                if "ntuples2016" in fname:
                    pcuts.append('(HLT_MU||HLT_ELE||HLT_ISOMU||HLT_ISOELE||HLT_MET||HLT_PHOTON)*Flag_BadMuonFilter*Flag_globalSuperTightHalo2016Filter')
                else:
                    pcuts.append('(HLT_MU||HLT_ELE||HLT_ISOMU||HLT_ISOELE||HLT_MET120)*Flag_BadPFMuonFilter*Flag_globalTightHalo2016Filter')

                if not isData:
                    plotters[-1].setupFromFile(sampleDir+'/'+fname+'.pck')
                    plotters[-1].addCorrectionFactor('xsec','tree')
                    plotters[-1].addCorrectionFactor('genWeight','tree')
                    plotters[-1].addCorrectionFactor('puWeight','tree')
                    plotters[-1].addCorrectionFactor('truth_genTop_weight','branch')
                    #plotters[-1].addCorrectionFactor('lnujj_sfWV','branch')
                    #plotters[-1].addCorrectionFactor('lnujj_btagWeight','branch')

                    #''' ## rescale the W+jets yield from low-mjet sideband:
                    if fname.find("WJetsToLNu_HT")!=-1: 
                        renormWJets2016=0.8727054353
                        renormWJets2017=0.699592444047
                        renormWJets2018=0.728005348312
                        renormWJetsRun2=0.760376974966
                        wjetsfactor=renormWJets2016 if fname.find("2016")!=-1 else renormWJets2017 if fname.find("2017")!=-1 else renormWJets2018 if fname.find("2018")!=-1 else 1.
                        plotters[-1].addCorrectionFactor(wjetsfactor,'flat')
                        if wjetsfactor!=1.:
                            print 'reweighting '+fname+' '+str(wjetsfactor)
                    #'''
                    ''' ## alternatively, remove the background k-factors (still to be tested with the templates and statistical analysis):
                    if fname.find("WJetsToLNu_HT")!=-1:
                        wjetsAntiKfactor=1./1.21
                        plotters[-1].addCorrectionFactor(wjetsAntiKfactor,'flat')
                        print 'reweighting '+fname+' '+str(wjetsAntiKfactor)
                    elif fname.find("DYJetsToLL_M50_HT")!=-1:
                        dyAntiKfactor=1./1.23
                        plotters[-1].addCorrectionFactor(dyAntiKfactor,'flat')
                        print 'reweighting '+fname+' '+str(dyAntiKfactor)
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

                mass = float(fname.split('_')[-1])

                if mass<minMX or mass>maxMX:
                    continue

                if not mass in plotters.keys():
                    plotters[mass] = []
                    pcuts[mass] = []

                plotters[mass].append(TreePlotter(sampleDir+'/'+fname+'.root','tree'))

                ## Temporary fix for HLT flags and MET flags:
                if "ntuples2016" in fname:
                    pcuts[mass].append('(HLT_MU||HLT_ELE||HLT_ISOMU||HLT_ISOELE||HLT_MET||HLT_PHOTON)*Flag_BadMuonFilter*Flag_globalSuperTightHalo2016Filter')
                else:
                    pcuts[mass].append('(HLT_MU||HLT_ELE||HLT_ISOMU||HLT_ISOELE||HLT_MET120)*Flag_BadPFMuonFilter*Flag_globalTightHalo2016Filter')

                plotters[mass][-1].setupFromFile(sampleDir+'/'+fname+'.pck')
                plotters[mass][-1].addCorrectionFactor('xsec','tree')
                plotters[mass][-1].addCorrectionFactor('genWeight','tree')
                plotters[mass][-1].addCorrectionFactor('puWeight','tree')
                #plotters[mass][-1].addCorrectionFactor('lnujj_sfWV','branch')
                #plotters[mass][-1].addCorrectionFactor('lnujj_btagWeight','branch')
                plotters[mass][-1].addCorrectionFactor(corr,'flat')
                plotters[mass][-1].filename=fname

                print 'found',filename,'mass',str(mass)


    mergedplotters = {}

    for mass in sorted(plotters.keys()):

        if len(plotters[mass]) != (1,3)[sampleDir=='ntuples']:
            continue

        mergedplotters[mass]=MergedPlotter(plotters[mass],pcuts[mass])

    return mergedplotters
