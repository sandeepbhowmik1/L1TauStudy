from ROOT import *
import numpy as n
import math
import sys

#fileName_In = sys.argv[1]
#treeName_In = sys.argv[2]
#fileName_Out = sys.argv[3]

fileName_In = "/home/sbhowmik/L1TauTrigger_NTuple/Performance_2018data_181128/NTuple_SingleMu_Run2018_total_181128.root"
treeName_In = "Ntuplizer/TagAndProbe"
fileName_Out = "/home/sbhowmik/L1TauTrigger/L1TauStudy/L1TauStudy/L1TauPerformance/efficiencyPlot/results/hist_Efficiency_vs_Pt_for_data_Run2018_All_WorkingPoints_20210715.root"

fileIn = TFile.Open(fileName_In)
treeIn = fileIn.Get(treeName_In)
fileOut = TFile (fileName_Out, 'recreate')
treeOut = TTree("L1TauAnalyzer", "L1TauAnalyzer")

etaMin = 0
etaMax = 2.1
saveOnlyOS = False

workingPoints = ["30", "34", "38"]
workingPointNames = ["l1TauPt30", "l1TauPt34", "l1TauPt38"]

hist_RecoTau_Pt_Denominator = TH1F ("RecoTau_Pt_Denominator", "RecoTau_Pt_Denominator", 200, 0., 1000.)

hist_RecoTau_Pt_Numerator_l1tPt30 = TH1F ("RecoTau_Pt_Numerator_l1tPt30", "RecoTau_Pt_Numerator_l1tPt30", 200, 0., 1000.)
hist_RecoTau_Pt_Numerator_l1tPt34 = TH1F ("RecoTau_Pt_Numerator_l1tPt34", "RecoTau_Pt_Numerator_l1tPt34", 200, 0., 1000.)
hist_RecoTau_Pt_Numerator_l1tPt38 = TH1F ("RecoTau_Pt_Numerator_l1tPt38", "RecoTau_Pt_Numerator_l1tPt38", 200, 0., 1000.)

hist_RecoTau_Pt_Numerator_l1tPt30_Iso = TH1F ("RecoTau_Pt_Numerator_l1tPt30_Iso", "RecoTau_Pt_Numerator_l1tPt30_Iso", 200, 0., 1000.)
hist_RecoTau_Pt_Numerator_l1tPt34_Iso = TH1F ("RecoTau_Pt_Numerator_l1tPt34_Iso", "RecoTau_Pt_Numerator_l1tPt34_Iso", 200, 0., 1000.)
hist_RecoTau_Pt_Numerator_l1tPt38_Iso = TH1F ("RecoTau_Pt_Numerator_l1tPt38_Iso", "RecoTau_Pt_Numerator_l1tPt38_Iso", 200, 0., 1000.)

hist_RecoTau_Pt_Efficiency_l1tPt30 = TH1F ("RecoTau_Pt_Efficiency_l1tPt30", "RecoTau_Pt_Efficiency_l1tPt30", 200, 0., 1000.)
hist_RecoTau_Pt_Efficiency_l1tPt34 = TH1F ("RecoTau_Pt_Efficiency_l1tPt34", "RecoTau_Pt_Efficiency_l1tPt34", 200, 0., 1000.)
hist_RecoTau_Pt_Efficiency_l1tPt38 = TH1F ("RecoTau_Pt_Efficiency_l1tPt38", "RecoTau_Pt_Efficiency_l1tPt38", 200, 0., 1000.)

hist_RecoTau_Pt_Efficiency_l1tPt30_Iso = TH1F ("RecoTau_Pt_Efficiency_l1tPt30_Iso", "RecoTau_Pt_Efficiency_l1tPt30_Iso", 200, 0., 1000.)
hist_RecoTau_Pt_Efficiency_l1tPt34_Iso = TH1F ("RecoTau_Pt_Efficiency_l1tPt34_Iso", "RecoTau_Pt_Efficiency_l1tPt34_Iso", 200, 0., 1000.)
hist_RecoTau_Pt_Efficiency_l1tPt38_Iso = TH1F ("RecoTau_Pt_Efficiency_l1tPt38_Iso", "RecoTau_Pt_Efficiency_l1tPt38_Iso", 200, 0., 1000.)

nentries = treeIn.GetEntries()
for ev in range (0, nentries):
    treeIn.GetEntry(ev)
    if (ev%10000 == 0) : print ev, "/", nentries
    if abs(treeIn.tauEta) < etaMin:
        continue
    if abs(treeIn.tauEta) > etaMax:
        continue
    if saveOnlyOS and not treeIn.isOS:
        continue

    hist_RecoTau_Pt_Denominator.Fill(treeIn.tauPt)
    if treeIn.l1tPt > 30 :
        hist_RecoTau_Pt_Numerator_l1tPt30.Fill(treeIn.tauPt)
        if treeIn.l1tIso:
            hist_RecoTau_Pt_Numerator_l1tPt30_Iso.Fill(treeIn.tauPt)
    if treeIn.l1tPt > 34 :
        hist_RecoTau_Pt_Numerator_l1tPt34.Fill(treeIn.tauPt)
        if treeIn.l1tIso:
            hist_RecoTau_Pt_Numerator_l1tPt34_Iso.Fill(treeIn.tauPt)
    if treeIn.l1tPt > 38 :
        hist_RecoTau_Pt_Numerator_l1tPt38.Fill(treeIn.tauPt)
        if treeIn.l1tIso:
            hist_RecoTau_Pt_Numerator_l1tPt38_Iso.Fill(treeIn.tauPt)

hist_RecoTau_Pt_Efficiency_l1tPt30.Divide(hist_RecoTau_Pt_Numerator_l1tPt30, hist_RecoTau_Pt_Denominator)
hist_RecoTau_Pt_Efficiency_l1tPt34.Divide(hist_RecoTau_Pt_Numerator_l1tPt34, hist_RecoTau_Pt_Denominator)
hist_RecoTau_Pt_Efficiency_l1tPt38.Divide(hist_RecoTau_Pt_Numerator_l1tPt38, hist_RecoTau_Pt_Denominator)

hist_RecoTau_Pt_Efficiency_l1tPt30_Iso.Divide(hist_RecoTau_Pt_Numerator_l1tPt30_Iso, hist_RecoTau_Pt_Denominator)
hist_RecoTau_Pt_Efficiency_l1tPt34_Iso.Divide(hist_RecoTau_Pt_Numerator_l1tPt34_Iso, hist_RecoTau_Pt_Denominator)
hist_RecoTau_Pt_Efficiency_l1tPt38_Iso.Divide(hist_RecoTau_Pt_Numerator_l1tPt38_Iso, hist_RecoTau_Pt_Denominator)


fileOut.Write()
fileOut.Close()
