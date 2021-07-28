from ROOT import *
import numpy as n
import math
import sys
TH1.SetDefaultSumw2();
from array import array

#fileName_In = sys.argv[1]
#fileName_Out = sys.argv[2]

fileName_In = "/home/sbhowmik/L1TauTrigger_NTuple/Performance_2018data_181128/NTuple_SingleMu_Run2018_total_forResolution_181128.root"
#fileName_In = "/home/sbhowmik/RootTree/L1TauTrigger/Run3/rootTree_Signal_Resolution_for_data_Run2018_20210715.root"
fileName_Out = "/home/sbhowmik/L1TauTrigger/L1TauStudy/L1TauStudy/L1TauPerformance/resolutionPlot/results/hist_Et_Resolution_vs_Pt_Eta_Nvtx_for_data_Run2018_20210715.root"

fileIn = TFile.Open(fileName_In)
treeIn = fileIn.Get("L1TauAnalyzer")
fileOut = TFile (fileName_Out, 'recreate')

ptBinning  = [20, 23, 26, 30, 35, 40, 45, 50, 60, 70, 90, 110]
etaBinning = [0, 0.26, 0.52, 0.78, 1.04, 1.30, 1.48, 1.75, 2.0, 2.5]
nvtxBinning = [0, 10, 15, 20, 25, 30, 35, 40, 45, 50, 60, 70, 80]

hist_Et_Resolution_vs_Pt_for_All = TH1F ("hist_Et_Resolution_vs_Pt_for_All", "hist_Et_Resolution_vs_Pt_for_All", len(ptBinning)-1, array('d', ptBinning))
hist_Et_Resolution_vs_Pt_for_Barrel = TH1F ("hist_Et_Resolution_vs_Pt_for_Barrel", "hist_Et_Resolution_vs_Pt_for_Barrel", len(ptBinning)-1, array('d', ptBinning))
hist_Et_Resolution_vs_Pt_for_Endcap = TH1F ("hist_Et_Resolution_vs_Pt_for_Endcap", "hist_Et_Resolution_vs_Pt_for_Endcap", len(ptBinning)-1, array('d', ptBinning))
hist_Et_Resolution_vs_Eta_for_All = TH1F ("hist_Et_Resolution_vs_Eta_for_All", "hist_Et_Resolution_vs_Eta_for_All", len(etaBinning)-1, array('d', etaBinning))
hist_Et_Resolution_vs_Nvtx_for_All = TH1F ("hist_Et_Resolution_vs_Nvtx_for_All", "hist_Et_Resolution_vs_Nvtx_for_All", len(nvtxBinning)-1, array('d', nvtxBinning))

hist_2D_Et_Resolution_vs_Pt_for_All = TH2F ("hist_2D_Et_Resolution_vs_Pt_for_All", "hist_2D_Et_Resolution_vs_Pt_for_All", len(ptBinning)-1, array('d', ptBinning), 1000, 0, 3)
hist_2D_Et_Resolution_vs_Pt_for_Barrel = TH2F ("hist_2D_Et_Resolution_vs_Pt_for_Barrel", "hist_2D_Et_Resolution_vs_Pt_for_Barrel", len(ptBinning)-1, array('d', ptBinning), 1000, 0, 3)
hist_2D_Et_Resolution_vs_Pt_for_Endcap = TH2F ("hist_2D_Et_Resolution_vs_Pt_for_Endcap", "hist_2D_Et_Resolution_vs_Pt_for_Endcap", len(ptBinning)-1, array('d', ptBinning), 1000, 0, 3)
hist_2D_Et_Resolution_vs_Eta_for_All = TH2F ("hist_2D_Et_Resolution_vs_Eta_for_All", "hist_2D_Et_Resolution_vs_Eta_for_All", len(etaBinning)-1, array('d', etaBinning), 1000, 0, 3)
hist_2D_Et_Resolution_vs_Nvtx_for_All = TH2F ("hist_2D_Et_Resolution_vs_Nvtx_for_All", "hist_2D_Et_Resolution_vs_Nvtx_for_All", len(nvtxBinning)-1, array('d', nvtxBinning), 1000, 0, 3)


nentries = treeIn.GetEntries()
print "nentries ", nentries

for iEv in range (0, nentries):
    treeIn.GetEntry(iEv)
    if (iEv%10000 == 0) : print iEv, "/", nentries

    hist_2D_Et_Resolution_vs_Pt_for_All.Fill (treeIn.recoTauPt , treeIn.l1TauPt / treeIn.recoTauPt )
    if TMath.Abs(treeIn.recoTauEta) < 1.305:
        hist_2D_Et_Resolution_vs_Pt_for_Barrel.Fill (treeIn.recoTauPt , treeIn.l1TauPt / treeIn.recoTauPt )
    elif TMath.Abs(treeIn.recoTauEta) > 1.479:
        hist_2D_Et_Resolution_vs_Pt_for_Endcap.Fill (treeIn.recoTauPt , treeIn.l1TauPt / treeIn.recoTauPt )
    hist_2D_Et_Resolution_vs_Eta_for_All.Fill(TMath.Abs(treeIn.recoTauEta) , treeIn.l1TauPt / treeIn.recoTauPt )
    hist_2D_Et_Resolution_vs_Nvtx_for_All.Fill(TMath.Abs(treeIn.Nvtx) , treeIn.l1TauPt / treeIn.recoTauPt )


# put Et Resolution along Y axis of 2D histogram into 1D histogram  
def makeEtResolutionVsPtEtaNvtx (hist_2D, hist_1D):
    if hist_2D.GetNbinsX() != hist_1D.GetNbinsX():
        print "*** ERROR : not same binning"
        return False
    print "PROCESSING: " , hist_2D.GetName()
    for ixbin in range (1, hist_1D.GetNbinsX()+1):
        LowEdge = hist_1D.GetXaxis().GetBinCenter(ixbin) - hist_1D.GetXaxis().GetBinWidth(ixbin)/2
        hname = hist_1D.GetName()
        name = (str(hname) + "_" + str(LowEdge))
        histProjection = hist_2D.ProjectionY(name, ixbin, ixbin)
        hist_1D.SetBinContent(ixbin, histProjection.GetRMS() / histProjection.GetMean())
        error = histProjection.GetRMS() / (TMath.Sqrt(histProjection.Integral()))
        # hist_1D.SetBinError(ixbin, histProjection.GetRMSError()) 
        hist_1D.SetBinError(ixbin, error)

    return True

makeEtResolutionVsPtEtaNvtx( hist_2D_Et_Resolution_vs_Pt_for_All,  hist_Et_Resolution_vs_Pt_for_All )
makeEtResolutionVsPtEtaNvtx( hist_2D_Et_Resolution_vs_Pt_for_Barrel,  hist_Et_Resolution_vs_Pt_for_Barrel )
makeEtResolutionVsPtEtaNvtx( hist_2D_Et_Resolution_vs_Pt_for_Endcap,  hist_Et_Resolution_vs_Pt_for_Endcap )
makeEtResolutionVsPtEtaNvtx( hist_2D_Et_Resolution_vs_Eta_for_All,  hist_Et_Resolution_vs_Eta_for_All )
makeEtResolutionVsPtEtaNvtx( hist_2D_Et_Resolution_vs_Nvtx_for_All,  hist_Et_Resolution_vs_Nvtx_for_All )

fileOut.Write()
