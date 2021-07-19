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
workingPointNames = ["l1tPt30", "l1tPt34", "l1tPt38", "l1tPt120"]


bkgSubW = n.zeros(1, dtype=float)
tauPt = n.zeros(1, dtype=float)
tauEta = n.zeros(1, dtype=float)
tauPhi = n.zeros(1, dtype=float)
l1tPt = n.zeros(1, dtype=float)
l1tEta = n.zeros(1, dtype=float)
l1tPhi = n.zeros(1, dtype=float)
Nvtx = n.zeros(1, dtype=float)
l1tPtIso = [n.zeros(1, dtype=int) for x in range (0, len(workingPoints))]
l1tPtNonIso = [n.zeros(1, dtype=int) for x in range (0, len(workingPoints))]

l1tNoCut = n.zeros(1, dtype=int)
l1tdZ = n.zeros(1, dtype=int)
l1tVLoose = n.zeros(1, dtype=int)
l1tLoose = n.zeros(1, dtype=int)
l1tMedium = n.zeros(1, dtype=int)
l1tTight = n.zeros(1, dtype=int)
Nvtx = n.zeros(1, dtype=float)

treeOut.Branch("bkgSubW", bkgSubW, "bkgSubW/D")
treeOut.Branch("tauPt", tauPt, "tauPt/D")
treeOut.Branch("tauEta", tauEta, "tauEta/D")
treeOut.Branch("tauPhi", tauPhi, "tauPhi/D")
treeOut.Branch("l1tPt", l1tPt, "l1tPt/D")
treeOut.Branch("l1tEta", l1tEta, "l1tEta/D")
treeOut.Branch("l1tPhi", l1tPhi, "l1tPhi/D")
treeOut.Branch("Nvtx", Nvtx, "Nvtx/D")
for i in range (0, len(workingPoints)):
    treeOut.Branch(workingPointNames[i], l1tPtNonIso[i], workingPointNames[i]+"/I")
    name = workingPointNames[i] + "_Iso"
    treeOut.Branch(name, l1tPtIso[i], name+"/I")

etaMin = 0
etaMax = 2.1
saveOnlyOS = False

nentries = treeIn.GetEntries()
print "nentries ", nentries

for ev in range (0, nentries):
    treeIn.GetEntry(ev)
    if (ev%10000 == 0) : print ev, "/", nentries
    if abs(treeIn.tauEta) < etaMin:
        continue
    if abs(treeIn.tauEta) > etaMax:
        continue
    if saveOnlyOS and not treeIn.isOS:
        continue
    bkgSubW[0] = 1. if treeIn.isOS else -1.
    Nvtx[0] = treeIn.Nvtx
    tauPt[0] = treeIn.tauPt
    tauEta[0] = treeIn.tauEta
    tauPhi[0] = treeIn.tauPhi
    l1tPt[0] = treeIn.l1tPt
    l1tEta[0] =treeIn.l1tEta
    l1tPhi[0] =treeIn.l1tPhi
    for j in range (0, len(workingPoints)):
        l1tPtIso[j][0] = 0
        l1tPtNonIso[j][0] = 0
        if treeIn.l1tPt > workingPoints[j]:
            l1tPtNonIso[j][0] = 1
            if treeIn.l1tIso:
                l1tPtIso[j][0] = 1

    treeOut.Fill()

treeOut.Write()
fileOut.Close()
