#!/bin/sh

fileName_In=$1
fileName_Out=$2
scriptOut=$3

#fileName_In='/home/sbhowmik/L1TauTrigger_NTuple/Performance_2018data_181128/NTuple_SingleMu_Run2018_total_forEfficiency_181128.root'
#fileName_Out='/home/sbhowmik/L1TauTrigger/L1TauStudy/L1TauStudy/L1TauPerformance/efficiencyPlot/results/fitOutput_Efficiency_vs_Eta_for_data_Run2018_20210715.root'
#scriptOut='parameter_file_Efficiency_Fitter_vs_Eta_for_data_Run2018_20210715.par'

varNameTag=("l1tPt30" "l1tPt34" "l1tPt38" "l1tPt120" "l1tPt30_Iso" "l1tPt34_Iso" "l1tPt38_Iso" "l1tPt120_Iso")

fileOut=${scriptOut}

echo "OutputFile: ${fileName_Out}" | cat >>$fileOut
echo "NCPU: 4" | cat >>$fileOut

echo "Turnon.N: 8" | cat >>$fileOut

for ((i_varName=0; i_varName<8; i_varName++))
do

    i_var=$((${i_varName}+1))

    echo "Turnon.${i_var}.Name: Stage2_Efficiency_${varNameTag[i_varName]}" | cat >>$fileOut
    echo "Turnon.${i_var}.File: ${fileName_In}" | cat >>$fileOut
    echo "Turnon.${i_var}.Tree: L1TauAnalyzer" | cat >>$fileOut
    echo "Turnon.${i_var}.XVar: tauEta" | cat >>$fileOut
    echo "Turnon.${i_var}.Cut: ${varNameTag[i_varName]}" | cat >>$fileOut
    echo "Turnon.${i_var}.WeightVar: bkgSubW" | cat >>$fileOut
    echo "Turnon.${i_var}.SelectionVars: tauPt" | cat >>$fileOut
    echo "Turnon.${i_var}.Selection: tauPt>40" | cat >>$fileOut
    echo "Turnon.${i_var}.Binning: -2.1 -1.8 -1.5 -1.2 -0.9 -0.6 -0.3 0 0.3 0.6 0.9 1.2 1.5 1.8 2.1" | cat >>$fileOut
    echo "Turnon.${i_var}.FitRange:-2.1 2.1" | cat >>$fileOut
    echo "Turnon.${i_var}.CB.Max: 1. 0.9 1." | cat >>$fileOut
    echo "Turnon.${i_var}.CB.Alpha: 3. 0.01 50." | cat >>$fileOut
    echo "Turnon.${i_var}.CB.N: 10. 1.001 100." | cat >>$fileOut
    echo "Turnon.${i_var}.CB.Mean: 30. 0. 120." | cat >>$fileOut
    echo "Turnon.${i_var}.CB.Sigma: 2. 0.01 10" | cat >>$fileOut

done
