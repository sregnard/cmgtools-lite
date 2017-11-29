#!/usr/bin/env python

## Script that creates a graph of local p-value vs. mass,
## to be then used as input to the leeFromUpcrossings.py script.

import os
import ROOT

import optparse
parser = optparse.OptionParser(usage="usage: %prog [options] treeFromCombine.root")
parser.add_option("-v","--verbose",action="store_true",dest="verbose",help="print graph values",default=False)
parser.add_option("-x","--minX",dest="minX",type=float,help="lower bound of mass range",default=1000.0)
parser.add_option("-X","--maxX",dest="maxX",type=float,help="upper bound of mass range",default=4400.0)
parser.add_option("-o","--output",dest="outputFile",metavar="FILE",help="write the graph to FILE",default='graphForLEE.root')
parser.add_option("-g","--graph",dest="graphName",help="graph name",default='pvalueVsMass')
(options,args) = parser.parse_args()



fIn = ROOT.TFile(args[0])
tree = fIn.Get("limit")
    
data = {}
gOut = ROOT.TGraph()
gOut.SetName(options.graphName)
N=0

for entry in tree:
    if float(entry.mh)<options.minX or float(entry.mh)>options.maxX:
        continue

    if not entry.quantileExpected<0:
        print 'WARNING: Found quantileExpected>=0: please check that the input file is correct.'
        continue

    if entry.mh in data.keys():
        print 'WARNING: Found more than one entry for mass', entry.mh, ': please check that the input file is correct.'
        continue

    if options.verbose:
        print 'Mass', entry.mh, ', p-value', entry.limit
    data[entry.mh]=entry.limit
    gOut.SetPoint(N,entry.mh,entry.limit)

    N=N+1

gOut.Sort()

fIn.Close()


fOut=ROOT.TFile(options.outputFile,"RECREATE")
fOut.cd()
gOut.Write()
fOut.Close()



