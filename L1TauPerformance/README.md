# L1TauStudy

go inside any $CMSSW_BASE/src/

cmsenv


# To make efficiency plots


cd L1TauStudy/L1TauPerformance/efficiencyPlot/fitTurnon

make clean

rm obj/*

make


cd L1TauStudy/L1TauPerformance/efficiencyPlot/macro

python convertTreeFor_EfficiencyPlot_data.py


cd L1TauStudy/L1TauPerformance/efficiencyPlot/fitTurnon

./fit.exe run/parameter_file_Efficiency_Fitter_vs_Pt_for_data_Run2018_20210715.par

./fit.exe run/parameter_file_Efficiency_Fitter_vs_Eta_for_data_Run2018_20210715.par

./fit.exe run/parameter_file_Efficiency_Fitter_vs_Nvtx_for_data_Run2018_20210715.par


cd L1TauStudy/L1TauPerformance/efficiencyPlot/macro

python plot_Efficiency_vs_Pt_for_All_WorkingPoints.py

see the plots in

cd L1TauStudy/L1TauPerformance/efficiencyPlot/plots



# To make resolution plots

cd L1TauStudy/L1TauPerformance/resolutionPlot/macro

python make_Resolution.py

root -l fit_Resolution.C

python plot_Resolution.py


python make_Et_Resolution_vs_Pt_Eta_Nvtx.py

python plot_Et_Resolution_vs_Pt_Eta_Nvtx.py

see the plots in

L1TauStudy/L1TauPerformance/resolutionPlot/plots
