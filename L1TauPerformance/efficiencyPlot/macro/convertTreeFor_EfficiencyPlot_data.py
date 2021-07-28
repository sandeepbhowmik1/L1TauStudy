from ROOT import *
import numpy as n
import math
import sys

#fileName_In = sys.argv[1]
#treeName_In = sys.argv[2]
#fileName_Out = sys.argv[3]

fileName_In = "/home/sbhowmik/L1TauTrigger_NTuple/Performance_2018data_181128/NTuple_SingleMu_Run2018_total_181128.root"
treeName_In = "Ntuplizer/TagAndProbe"
fileName_Out = "/home/sbhowmik/L1TauTrigger_NTuple/Performance_2018data_181128/NTuple_SingleMu_Run2018_total_forEfficiency_181128.root"

fileIn = TFile.Open(fileName_In)
treeIn = fileIn.Get(treeName_In)
fileOut = TFile (fileName_Out, 'recreate')
treeOut = TTree("L1TauAnalyzer", "L1TauAnalyzer")

workingPoints = [30, 34, 38, 120]
workingPointNames = ["l1TauPt30", "l1TauPt34", "l1TauPt38", "l1TauPt120"]


bkgSubW = n.zeros(1, dtype=float)
recoTauPt = n.zeros(1, dtype=float)
recoTauEta = n.zeros(1, dtype=float)
recoTauPhi = n.zeros(1, dtype=float)
l1TauPt = n.zeros(1, dtype=float)
l1TauEta = n.zeros(1, dtype=float)
l1TauPhi = n.zeros(1, dtype=float)
Nvtx = n.zeros(1, dtype=float)
l1TauPtIso = [n.zeros(1, dtype=int) for x in range (0, len(workingPoints))]
l1TauPtNonIso = [n.zeros(1, dtype=int) for x in range (0, len(workingPoints))]

treeOut.Branch("bkgSubW", bkgSubW, "bkgSubW/D")
treeOut.Branch("recoTauPt", recoTauPt, "recoTauPt/D")
treeOut.Branch("recoTauEta", recoTauEta, "recoTauEta/D")
treeOut.Branch("recoTauPhi", recoTauPhi, "recoTauPhi/D")
treeOut.Branch("l1TauPt", l1TauPt, "l1TauPt/D")
treeOut.Branch("l1TauEta", l1TauEta, "l1TauEta/D")
treeOut.Branch("l1TauPhi", l1TauPhi, "l1TauPhi/D")
treeOut.Branch("Nvtx", Nvtx, "Nvtx/D")
for i in range (0, len(workingPoints)):
    treeOut.Branch(workingPointNames[i], l1TauPtNonIso[i], workingPointNames[i]+"/I")
    name = workingPointNames[i] + "_Iso"
    treeOut.Branch(name, l1TauPtIso[i], name+"/I")

etaMin = 0
etaMax = 2.1
saveOnlyOS = False

nentries = treeIn.GetEntries()
print "nentries ", nentries

for ev in range (0, nentries):
    treeIn.GetEntry(ev)
    if (ev%10000 == 0) : print ev, "/", nentries
    if abs(treeIn.tauEta) < etaMin:
    #if abs(treeIn.recoTauEta) < etaMin:
        continue
    if abs(treeIn.tauEta) > etaMax:
    #if abs(treeIn.recoTauEta) > etaMax:
        continue
    if saveOnlyOS and not treeIn.isOS:
        continue
    bkgSubW[0] = 1. if treeIn.isOS else -1.
    Nvtx[0] = treeIn.Nvtx
    recoTauPt[0] = treeIn.tauPt
    #recoTauPt[0] = treeIn.recoTauPt
    recoTauEta[0] = treeIn.tauEta
    #recoTauEta[0] = treeIn.recoTauEta
    recoTauPhi[0] = treeIn.tauPhi
    #recoTauPhi[0] = treeIn.recoTauPhi
    l1TauPt[0] = treeIn.l1tPt
    #l1TauPt[0] = treeIn.l1TauPt
    l1TauEta[0] =treeIn.l1tEta
    #l1TauEta[0] =treeIn.l1TauEta
    l1TauPhi[0] =treeIn.l1tPhi
    #l1TauPhi[0] =treeIn.l1TauPhi
    for j in range (0, len(workingPoints)):
        l1TauPtIso[j][0] = 0
        l1TauPtNonIso[j][0] = 0
        if treeIn.l1tPt > workingPoints[j]:
        #if treeIn.l1TauPt > workingPoints[j]:
            l1TauPtNonIso[j][0] = 1
            if treeIn.l1tIso:
            #if treeIn.l1TauIso:
                l1TauPtIso[j][0] = 1

    treeOut.Fill()

treeOut.Write()
fileOut.Close()
