# L1TauStudy

go inside any $CMSSW_BASE/src/

cmsenv


# To make plots


git clone https://github.com/sandeepbhowmik1/L1TauStudy


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


