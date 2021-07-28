from ROOT import *
import numpy as n
import math
import sys
TH1.SetDefaultSumw2();

#fileName_In = sys.argv[1]
#fileName_Out = sys.argv[2]

fileName_In = "/home/sbhowmik/L1TauTrigger_NTuple/Performance_2018data_181128/NTuple_SingleMu_Run2018_total_forResolution_181128.root"
#fileName_In = "/home/sbhowmik/RootTree/L1TauTrigger/Run3/rootTree_Signal_Resolution_for_data_Run2018_20210715.root"
fileName_Out = "/home/sbhowmik/L1TauTrigger/L1TauStudy/L1TauStudy/L1TauPerformance/resolutionPlot/results/hist_Resolution_for_data_Run2018_20210715.root"

fileIn = TFile.Open(fileName_In)
treeIn = fileIn.Get("L1TauAnalyzer")
fileOut = TFile (fileName_Out, 'recreate')

workingPointNames = ["All", "Barrel", "Endcap"]

hist_Et_Resolution_for_All = TH1F ("hist_Et_Resolution_for_All", "hist_Et_Resolution_for_All", 60, 0, 3)
hist_Eta_Resolution_for_All = TH1F ("hist_Eta_Resolution_for_All", "hist_Eta_Resolution_for_All", 50, -0.3, 0.3)
hist_Phi_Resolution_for_All = TH1F ("hist_Phi_Resolution_for_All", "hist_Phi_Resolution_for_All", 50, -0.3, 0.3)

hist_Et_Resolution_for_Barrel = TH1F ("hist_Et_Resolution_for_Barrel", "hist_Et_Resolution_for_Barrel", 60, 0, 3)
hist_Eta_Resolution_for_Barrel = TH1F ("hist_Eta_Resolution_for_Barrel", "hist_Eta_Resolution_for_Barrel", 50, -0.3, 0.3)
hist_Phi_Resolution_for_Barrel = TH1F ("hist_Phi_Resolution_for_Barrel", "hist_Phi_Resolution_for_Barrel", 50, -0.3, 0.3)

hist_Et_Resolution_for_Endcap = TH1F ("hist_Et_Resolution_for_Endcap", "hist_Et_Resolution_for_Endcap", 60, 0, 3)
hist_Eta_Resolution_for_Endcap = TH1F ("hist_Eta_Resolution_for_Endcap", "hist_Eta_Resolution_for_Endcap", 50, -0.3, 0.3)
hist_Phi_Resolution_for_Endcap = TH1F ("hist_Phi_Resolution_for_Endcap", "hist_Phi_Resolution_for_Endcap", 50, -0.3, 0.3)

for i in range (0, len(workingPointNames)):
    hist_Name_Et_Resolution = "hist_Et_Resolution_for_%s" % workingPointNames[i]
    hist_Name_Eta_Resolution = "hist_Eta_Resolution_for_%s" % workingPointNames[i]
    hist_Name_Phi_Resolution = "hist_Phi_Resolution_for_%s" % workingPointNames[i]
    cut = ""
    if(workingPointNames[i]=="All"):
        cut = "abs(recoTauEta) < 2.1 && recoTauPt > 20"
    if(workingPointNames[i]=="Barrel"):
        cut = "abs(recoTauEta) < 1.305 && recoTauPt > 20"
    if(workingPointNames[i]=="Endcap"):
        cut = "abs(recoTauEta) > 1.479 && recoTauPt > 20"

    treeIn.Draw("l1TauPt / recoTauPt >> %s" % hist_Name_Et_Resolution, "%s" % cut)
    treeIn.Draw("l1TauEta - recoTauEta >> %s" % hist_Name_Eta_Resolution, "%s" % cut)
    treeIn.Draw("l1TauPhi - recoTauPhi >> %s" % hist_Name_Phi_Resolution, "%s" % cut)



fileOut.Write()
fileOut.Close()
