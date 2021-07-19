import ROOT
import Efficiency_plot_macro as EfficiencyPlot
import sys

#fileName_In = sys.argv[1]
#fileName_Out = sys.argv[2]
fileName_In = "/home/sbhowmik/L1TauTrigger/L1TauStudy/L1TauStudy/L1TauPerformance/efficiencyPlot/results/fitOutput_Efficiency_vs_Pt_for_data_Run2018_20210715.root"
fileName_Out = "/home/sbhowmik/L1TauTrigger/L1TauStudy/L1TauStudy/L1TauPerformance/efficiencyPlot/plots/plot_Efficiency_vs_Pt_for_data_Run2018_All_WorkingPoints_20210715"

fileIn_L1Tau = ROOT.TFile.Open(fileName_In)

hist_L1Tau = []
fit_L1Tau = []
efficiency_L1Tau = []
plots = []

isoTypes = ["nonIso", "Iso"]
plotRanges=[100, 500]
workingPoints = ["30", "34", "38"]
workingPointNames = ["l1tPt30", "l1tPt34", "l1tPt38"]

for i in range (0, len(isoTypes)):
    for j in range (0, len(plotRanges)):
        count=0
        plots.append(EfficiencyPlot.EfficiencyPlot())
        for k in range (0, len(workingPointNames)):
            count+=1
            if(count==3):
                count+=1
            if(i==0):
                hist_L1Tau.append(fileIn_L1Tau.Get("histo_Stage2_Efficiency_"+workingPointNames[k]))
                hist_L1Tau[-1].__class__ = ROOT.RooHist
                fit_L1Tau.append(fileIn_L1Tau.Get("fit_Stage2_Efficiency_"+workingPointNames[k]))
                fit_L1Tau[-1].__class__ = ROOT.RooCurve
                efficiency_L1Tau.append(EfficiencyPlot.Efficiency(Name="L1Tau", Histo=hist_L1Tau[-1], Fit=fit_L1Tau[-1],
                                                                    MarkerColor=(count), MarkerStyle=20, LineColor=(count),LineStyle=1,
                                                                    Legend=("Inclusive, E_{T}^{#tau, L1} > " + workingPoints[k] + " GeV")))
            else:
                hist_L1Tau.append(fileIn_L1Tau.Get("histo_Stage2_Efficiency_"+workingPointNames[k]+"_Iso"))
                hist_L1Tau[-1].__class__ = ROOT.RooHist
                fit_L1Tau.append(fileIn_L1Tau.Get("fit_Stage2_Efficiency_"+workingPointNames[k]+"_Iso"))
                fit_L1Tau[-1].__class__ = ROOT.RooCurve
                efficiency_L1Tau.append(EfficiencyPlot.Efficiency(Name="L1Tau", Histo=hist_L1Tau[-1], Fit=fit_L1Tau[-1],
                                                                    MarkerColor=(count), MarkerStyle=20, LineColor=(count),LineStyle=1,
                                                                    Legend=("Isolated, E_{T}^{#tau, L1} > " + workingPoints[k] + " GeV")))

            plots[-1].addEfficiency(efficiency_L1Tau[-1])
            plots[-1].xposText =0.50
            plots[-1].yposText =0.270
            plots[-1].extraText1 = "|#eta| < 2.1" 
            plots[-1].extraText2 = ""
            plots[-1].extraText3 = ""
            plots[-1].extraText4 = ""
            plots[-1].extraText5 = ""
            if(i==0):
                plots[-1].name = fileName_Out + "_Inclusive" + "_" + str(plotRanges[j])
            else:
                plots[-1].name = fileName_Out + "_Isolated" + "_" + str(plotRanges[j])
            plots[-1].xRange = (0, plotRanges[j]+1)
            #plots[-1].xTitle = "p_{T}^{#tau, offline} [GeV]"
            plots[-1].xTitle = "Offline #tau_{h} p_{T} [GeV]"
            plots[-1].legendPosition = (0.45, 0.35, 0.87, 0.5)

canvas = []
for plot in plots:
    canvas.append(plot.plot())

fileIn_L1Tau.Close()


