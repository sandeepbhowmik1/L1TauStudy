from ROOT import *
import ROOT
import operator
import array
ROOT.gSystem.Load('libRooFit')
import sys

#fileName_In = sys.argv[1]
#fileName_Out = sys.argv[2]

fileName_In = "/home/sbhowmik/L1TauTrigger/L1TauStudy/L1TauStudy/L1TauPerformance/efficiencyPlot/results/hist_Efficiency_vs_Pt_for_data_Run2018_All_WorkingPoints_20210715.root"
fileName_Out = "/home/sbhowmik/L1TauTrigger/L1TauStudy/L1TauStudy/L1TauPerformance/efficiencyPlot/plots/plot_Hist_Efficiency_vs_Pt_for_data_Run2018_All_WorkingPoints_20210715"

fileIn = TFile (fileName_In)

isoTypes = ["nonIso", "Iso"]
plotRanges=[100, 500]
workingPoints = ["30", "34", "38"]
workingPointNames = ["l1tPt30", "l1tPt34", "l1tPt38"]
ROOT.gStyle.SetPadLeftMargin(0.11)
c1 = TCanvas ("c1", "c1", 800, 800)
ROOT.gStyle.SetOptTitle(0)
ROOT.gStyle.SetOptStat(000000)
c1.SetGrid()
#c1.SetLogy()

xpos  = 0.11
ypos  = 0.91
cmsTextSize   = 0.03
CMSbox       = ROOT.TLatex  (xpos, ypos, "#scale[1.5]{CMS}                                   2018 data           13 TeV")
CMSbox.SetNDC()
CMSbox.SetTextSize(cmsTextSize)
xposText = 0.50
yposText = 0.27
extraTextSize   = 0.035
extraTextBox1 = ROOT.TLatex  (xposText, yposText, "Level-1 #tau Trigger")
extraTextBox1.SetNDC()
extraTextBox1.SetTextSize(extraTextSize)
extraTextBox2 = ROOT.TLatex  (xposText, yposText - 0.06, "Level-1 #tau Trigger")
extraTextBox2.SetNDC()
extraTextBox2.SetTextSize(extraTextSize)
extraTextBox3 = ROOT.TLatex  (xposText, yposText - 0.06, "|#eta| < 2.1")
extraTextBox3.SetNDC()
extraTextBox3.SetTextSize(extraTextSize)
extraTextBox4 = ROOT.TLatex  (xposText, yposText - 0.18, "")
extraTextBox4.SetNDC()
extraTextBox4.SetTextSize(extraTextSize)
extraTextBox5 = ROOT.TLatex  (xposText, yposText - 0.24, "")
extraTextBox5.SetNDC()
extraTextBox5.SetTextSize(extraTextSize)

for isoType in isoTypes:
    for j in range (0, len(plotRanges)):
        legend = ROOT.TLegend(0.45, 0.35, 0.87, 0.5)
        legend.SetLineColor(0)
        legend.SetFillColor(0)
        legend.SetTextSize(extraTextSize)
        count=0
        for i in range (0, len(workingPointNames)):
            count+=1
            if(count==3):
                count+=1
            if (isoType == "nonIso"):
                hist_HLTTau = fileIn.Get("RecoTau_Pt_Efficiency_%s" % (workingPointNames[i]))
            elif (isoType == "Iso"):
                hist_HLTTau = fileIn.Get("RecoTau_Pt_Efficiency_%s_Iso" % (workingPointNames[i]))
            hist_HLTTau.SetLineColor(count)
            hist_HLTTau.SetMarkerColor(count)
            hist_HLTTau.SetMarkerSize(1.0)
            hist_HLTTau.SetMarkerStyle(8)
            hist_HLTTau.SetMinimum(0)
            hist_HLTTau.SetMaximum(1.11)
            hist_HLTTau.SetAxisRange(0, plotRanges[j]+1)
            hist_HLTTau.SetTitle(";Offline #tau_{h} p_{T} [GeV]; Efficiency")
            hist_HLTTau.GetXaxis().SetTitleOffset(0.9)
            hist_HLTTau.GetXaxis().SetTitleSize(0.05)
            hist_HLTTau.GetYaxis().SetTitleOffset(0.9)
            hist_HLTTau.GetYaxis().SetTitleSize(0.05)
            if (i==0):
                #hist_HLTTau.Draw("p e")
                hist_HLTTau.Draw("p ")
            else:
                #hist_HLTTau.Draw("p e same")
                hist_HLTTau.Draw("p  same")
            if (isoType == "nonIso"):
                legend.AddEntry(hist_HLTTau,  "Inclusive, E_{T}^{#tau, L1} > " + workingPoints[i] + " GeV",  "lp")
            elif (isoType == "Iso"):
                legend.AddEntry(hist_HLTTau,  "Isolated, E_{T}^{#tau, L1} > " + workingPoints[i] + " GeV",  "lp") 
        legend.Draw()

        CMSbox.Draw()
        extraTextBox1.Draw()
        #extraTextBox2.Draw()
        #extraTextBox3.Draw()
        #extraTextBox4.Draw()
        #extraTextBox5.Draw()
        if (isoType == "nonIso"):
            c1.Print(fileName_Out + "_Inclusive" + "_" + str(plotRanges[j]) + ".pdf", "pdf")
            c1.Print(fileName_Out + "_Inclusive" + "_" + str(plotRanges[j]) + ".png", "png")
            c1.Print(fileName_Out + "_Inclusive" + "_" + str(plotRanges[j]) + ".root", "root")
        elif(isoType == "Iso"):
            c1.Print(fileName_Out + "_Isolated" + "_" + str(plotRanges[j]) + ".pdf", "pdf")
            c1.Print(fileName_Out + "_Isolated" + "_" + str(plotRanges[j]) + ".png", "png")
            c1.Print(fileName_Out + "_Isolated" + "_" + str(plotRanges[j]) + ".root", "root")




