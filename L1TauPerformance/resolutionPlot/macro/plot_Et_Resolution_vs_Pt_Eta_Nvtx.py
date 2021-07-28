from ROOT import *
import ROOT
import operator
import array
ROOT.gSystem.Load('libRooFit')
import sys

#fileName_In = sys.argv[1]
#fileName_Out = sys.argv[2]
#ratioWith = sys.argv[3]

fileName_In = "/home/sbhowmik/L1TauTrigger/L1TauStudy/L1TauStudy/L1TauPerformance/resolutionPlot/results/hist_Et_Resolution_vs_Pt_Eta_Nvtx_for_data_Run2018_20210715.root"
#fileName_In = "/home/sbhowmik/L1TauTrigger/L1TauStudy/L1TauStudy/L1TauPerformance/resolutionPlot/results/fitted_Hist_Et_Resolution_vs_Pt_Eta_Nvtx_for_data_Run2018_20210715.root"
fileName_Out = "/home/sbhowmik/L1TauTrigger/L1TauStudy/L1TauStudy/L1TauPerformance/resolutionPlot/plots/plot_Et_Resolution_with_RMS_for_data_Run2018_20210715"
#fileName_Out = "/home/sbhowmik/L1TauTrigger/L1TauStudy/L1TauStudy/L1TauPerformance/resolutionPlot/plots/plot_Et_Resolution_with_FWHM_for_data_Run2018_20210715"
ratioWith = "RMS"  # "RMS", "FWHM" 


fileIn = TFile (fileName_In)

objTypes = ["Pt", "Eta", "Nvtx"]
titles = {"":""}
if(ratioWith=="RMS"):
    titles = {
        "Pt" : "; Offline #tau_{h} p_{T} [GeV]; RMS / <E_{T}^{#tau, L1}/p_{T}^{#tau, offline}>",
        "Eta" : "; Offline #tau_{h} #eta; RMS / <E_{T}^{#tau, L1}/p_{T}^{#tau, offline}>",
        "Nvtx" : "; Number of vertices; RMS / <E_{T}^{#tau, L1}/p_{T}^{#tau, offline}>",
    }
elif(ratioWith=="FWHM"):
    titles = {
        "Pt" : "; Offline #tau_{h} p_{T} [GeV]; FWHM / x-position-at-maximum",
        "Eta" : "; Offline #tau_{h} #eta; FWHM / x-position-at-maximum",
        "Nvtx" : "; Number of vertices; FWHM / x-position-at-maximum",
    }

xpos  = 0.11
ypos  = 0.91
cmsTextSize   = 0.03
CMSbox       = ROOT.TLatex  (xpos, ypos, "#scale[1.5]{CMS}                                   2018 data           13 TeV")
CMSbox.SetNDC()
CMSbox.SetTextSize(cmsTextSize)
xposText = 0.15
yposText = 0.85
extraTextSize   = 0.035
extraTextBox1 = ROOT.TLatex  (xposText, yposText, "")
extraTextBox1.SetNDC()
extraTextBox1.SetTextSize(extraTextSize)
extraTextBox2 = ROOT.TLatex  (xposText, yposText - 0.06, "")
extraTextBox2.SetNDC()
extraTextBox2.SetTextSize(extraTextSize)
extraTextBox3 = ROOT.TLatex  (xposText, yposText - 0.12, "")
extraTextBox3.SetNDC()
extraTextBox3.SetTextSize(extraTextSize)
extraTextBox4 = ROOT.TLatex  (xposText, yposText - 0.18, "")
extraTextBox4.SetNDC()
extraTextBox4.SetTextSize(extraTextSize)
extraTextBox5 = ROOT.TLatex  (xposText, yposText - 0.24, "")
extraTextBox5.SetNDC()
extraTextBox5.SetTextSize(extraTextSize)

for objType in objTypes:
    count=0
    ROOT.gStyle.SetPadLeftMargin(0.11)
    c1 = TCanvas ("c1", "c1", 800, 800)
    ROOT.gStyle.SetOptTitle(0)
    ROOT.gStyle.SetOptStat(000000)
    #ROOT.gStyle.SetStatX(0.9)
    #ROOT.gStyle.SetStatY(0.9)
    c1.SetGrid()
    legend = ROOT.TLegend(0.15, 0.680, 0.40, 0.780)
    legend.SetLineColor(0)
    legend.SetFillColor(0)
    legend.SetTextSize(extraTextSize)
    workingPointNames = [""]
    if(objType=="Pt"):
        workingPointNames = ["Barrel", "Endcap"]
    else:
        workingPointNames = ["All"]
    for i in range (0, len(workingPointNames)):
        count+=1
        hist_L1Tau = fileIn.Get("hist_Et_Resolution_vs_%s_for_%s" % (objType,workingPointNames[i]))
        if(objType=="Pt"):
            hist_L1Tau.SetAxisRange(0, 100)
        elif(objType=="Eta"):
            hist_L1Tau.SetAxisRange(0, 2.)
        elif(objType=="Nvtx"):
            hist_L1Tau.SetAxisRange(0, 70)
        if objType in titles:
            hist_L1Tau.SetTitle(titles[objType])
        hist_L1Tau.SetLineColor(count)
        hist_L1Tau.SetMarkerColor(count)
        hist_L1Tau.SetMarkerStyle(8)
        hist_L1Tau.SetMarkerSize(1.0)
        mm = hist_L1Tau.GetMaximum()
        hist_L1Tau.SetMaximum(1.55*mm)
        hist_L1Tau.SetMinimum(0)
        hist_L1Tau.GetXaxis().SetTitleOffset(0.9)
        hist_L1Tau.GetXaxis().SetTitleSize(0.05)
        hist_L1Tau.GetYaxis().SetTitleOffset(0.9)
        hist_L1Tau.GetYaxis().SetTitleSize(0.05)
        if (i==0):
            hist_L1Tau.Draw("p ")
        else:
            hist_L1Tau.Draw("p  same")
        if(objType=="Pt"):
            legend.AddEntry(hist_L1Tau,  "%s" % workingPointNames[i] ,  "lp")
        else:
            legend.AddEntry(hist_L1Tau,  ".",  "lp")
    legend.Draw()
    CMSbox.Draw()
    extraTextBox1.Draw()
    extraTextBox2.Draw()
    extraTextBox3.Draw()
    extraTextBox4.Draw()
    extraTextBox5.Draw()

    c1.Print(fileName_Out + "_" + objType + ".pdf", "pdf")
    c1.Print(fileName_Out + "_" + objType + ".png", "png")
    c1.Print(fileName_Out + "_" + objType + ".root", "root")




