import os, subprocess, sys


# ----------- *** Start Modification *** -------------------------------------

pathRootTree = '/home/sbhowmik/L1TauTrigger_NTuple/Performance_2018data_181128/'
#pathRootTree = '/home/sbhowmik/RootTree/L1TauTrigger/Run3/'

tagNTuple = '20210715'
tagRootTree = '20210715'
tagPlot = '20210715'

workingDir = os.getcwd()

pathPlot = os.path.join(workingDir, "plots")


#sampleType = ["data", "mc"]
sampleType = ["data"]

#dataType = ["Run2018", "Run2017", "Winter20"]
dataType = ["Run2018"]

objType=["Pt", "Eta", "Nvtx"]
#objType=["Pt"]

ratioWith = "RMS"  # "RMS", "FWHM"

# ------------ *** End Modification *** --------------------------------------



# ------------ Define command to execute -------------------------------------
def run_cmd(command):
  print "executing command = '%s'" % command
  p = subprocess.Popen(command, shell = True, stdout = subprocess.PIPE, stderr = subprocess.PIPE)
  stdout, stderr = p.communicate()
  return stdout


# -----------Convert root tree for efficiency plot ------------

for i in range (0, len(sampleType)):
  scriptFile = os.path.join(workingDir, "efficiencyPlot/macro", "convertTreeFor_EfficiencyPlot_"+sampleType[i]+".py")
  #fileName_In = os.path.join(pathRootTree, "rootTree_test_"+algoType[k]+"Analyzer_Signal_"+tagRootTree+".root")  
  fileName_In = os.path.join(pathRootTree, "NTuple_SingleMu_Run2018_total_181128.root")
  treeName_In = 'Ntuplizer/TagAndProbe'
  fileName_Out = os.path.join(pathRootTree, "NTuple_SingleMu_Run2018_total_forEfficiency_181128.root")
  run_cmd('python %s %s %s %s' % (scriptFile, fileName_In, treeName_In, fileName_Out))



# -------------- Plot efficiency vs Pt, Eta and Nvtx -------------------------------

scriptDir = os.path.join(workingDir, "efficiencyPlot/fitTurnon/run")
for i in range (0, len(objType)):
  scriptFile = os.path.join(scriptDir, "create_parameter_file_Efficiency_Fitter_vs_"+objType[i]+".sh")
  for j in range (0, len(sampleType)):
    for k in range (0, len(dataType)): 
      #fileName_In = os.path.join(pathRootTree, "rootTree_Signal_Efficiency_for_"+sampleType[j]+"_"+dataType[k]+"_"+tagPlot+".root")
      fileName_In = os.path.join(pathRootTree, "NTuple_SingleMu_Run2018_total_forEfficiency_181128.root")
      fileName_Out = os.path.join(workingDir, "efficiencyPlot/results", "fitOutput_Efficiency_vs_"+objType[i]+"_for_"+sampleType[j]+"_"+dataType[k]+"_"+tagPlot+".root")
      scriptOut = "parameter_file_Efficiency_Fitter_vs_"+objType[i]+"_for_"+sampleType[j]+"_"+dataType[k]+"_"+tagPlot+".par"
      run_cmd('bash %s %s %s %s' % (scriptFile, fileName_In, fileName_Out, scriptOut))
      run_cmd('mv %s %s' % (scriptOut, scriptDir))
      scriptFit = os.path.join(workingDir, "efficiencyPlot/fitTurnon", "fit.exe")
      parFile = os.path.join(scriptDir, scriptOut)
      run_cmd('%s %s' %(scriptFit, parFile))

      scriptPlot = os.path.join(workingDir, "efficiencyPlot/macro", "plot_Efficiency_vs_"+objType[i]+"_for_All_WorkingPoints.py")
      fileName_Out_Plot = os.path.join(workingDir, "efficiencyPlot/plots", "plot_Efficiency_vs_"+objType[i]+"_for_"+sampleType[j]+"_"+dataType[k]+"_"+tagPlot)
      run_cmd('python %s %s %s' % (scriptPlot, fileName_Out, fileName_Out_Plot))


# -------------- Plot efficiency vs Pt without fit ------------------------------- 

scriptMake = os.path.join(workingDir, "efficiencyPlot/macro", "make_Hist_EfficiencyPlot_vs_Pt_for_All_WorkingPoints.py")
fileName_In = os.path.join(pathRootTree, "NTuple_SingleMu_Run2018_total_181128.root")
treeName_In = 'Ntuplizer/TagAndProbe' 
fileName_Out = os.path.join(workingDir, "efficiencyPlot/results", "hist_Efficiency_vs_Pt_for_data_Run2018_All_WorkingPoints_20210715.root")
run_cmd('python %s %s %s %s' % (scriptMake, fileName_In, treeName_In, fileName_Out))
scriptPlot = os.path.join(workingDir, "efficiencyPlot/macro", "plot_Hist_EfficiencyPlot_vs_Pt_for_All_WorkingPoints.py")
fileName_In = os.path.join(workingDir, "efficiencyPlot/results", "hist_Efficiency_vs_Pt_for_data_Run2018_All_WorkingPoints_20210715.root")
fileName_Out = os.path.join(workingDir, "efficiencyPlot/plots", "plot_Hist_Efficiency_vs_Pt_for_data_Run2018_All_WorkingPoints_20210715")
run_cmd('python %s %s %s' % (scriptPlot, fileName_In, fileName_Out))


# -----------Convert root tree for resolution plot ------------ 

for i in range (0, len(sampleType)):
  scriptFile = os.path.join(workingDir, "resolutionPlot/macro", "convertTreeFor_ResolutionPlot_"+sampleType[i]+".py")
  #fileName_In = os.path.join(pathRootTree, "rootTree_test_"+algoType[k]+"Analyzer_Signal_"+tagRootTree+".root")
  fileName_In = os.path.join(pathRootTree, "NTuple_SingleMu_Run2018_total_181128.root")
  treeName_In = 'Ntuplizer/TagAndProbe'
  fileName_Out = os.path.join(pathRootTree, "NTuple_SingleMu_Run2018_total_forResolution_181128.root")
  run_cmd('python %s %s %s %s' % (scriptFile, fileName_In, treeName_In, fileName_Out))


# -------------- Plot resolution turn-on vs Pt -------------------------------      

for j in range (0, len(sampleType)):
  for k in range (0, len(dataType)):
    scriptMake = os.path.join(workingDir, "resolutionPlot/macro", "make_Resolution.py")
    #fileName_In = os.path.join(pathRootTree, "rootTree_Signal_Resolution_for_"+sampleType[j]+"_"+dataType[k]+"_"+tagPlot+".root")
    fileName_In = os.path.join(pathRootTree, "NTuple_SingleMu_Run2018_total_forResolution_181128.root")
    fileName_Out = os.path.join(workingDir, "resolutionPlot/results", "hist_Resolution_for_"+sampleType[j]+"_"+dataType[k]+"_"+tagPlot+".root")
    run_cmd('python %s %s %s' % (scriptMake, fileName_In, fileName_Out))
    scriptFit = os.path.join(workingDir, "resolutionPlot/macro", "fit_Resolution.C")
    fileName_In = os.path.join(workingDir, "resolutionPlot/results", "hist_Resolution_for_"+sampleType[j]+"_"+dataType[k]+"_"+tagPlot+".root")
    fileName_Out = os.path.join(workingDir, "resolutionPlot/results", "fitted_Hist_Resolution_for_"+sampleType[j]+"_"+dataType[k]+"_"+tagPlot+".root")
    run_cmd('root -b -n -q -l \'%s(\"%s\", \"%s\")\'' % (scriptFit, fileName_In, fileName_Out)) 
    scriptPlot = os.path.join(workingDir, "resolutionPlot/macro", "plot_Resolution.py")
    fileName_In = os.path.join(workingDir, "resolutionPlot/results", "fitted_Hist_Resolution_for_"+sampleType[j]+"_"+dataType[k]+"_"+tagPlot+".root")
    fileName_Out = os.path.join(workingDir, "resolutionPlot/plots", "plot_Resolution_for_"+sampleType[j]+"_"+dataType[k]+"_"+tagPlot)
    run_cmd('python %s %s %s' % (scriptPlot, fileName_In, fileName_Out))

    scriptMake = os.path.join(workingDir, "resolutionPlot/macro", "make_Et_Resolution_vs_Pt_Eta_Nvtx.py")
    #fileName_In = os.path.join(pathRootTree, "rootTree_Signal_Resolution_for_"+sampleType[j]+"_"+dataType[k]+"_"+tagPlot+".root") 
    fileName_In = os.path.join(pathRootTree, "NTuple_SingleMu_Run2018_total_forResolution_181128.root")
    fileName_Out = os.path.join(workingDir, "resolutionPlot/results", "hist_Et_Resolution_vs_Pt_Eta_Nvtx_for_"+sampleType[j]+"_"+dataType[k]+"_"+tagPlot+".root")
    run_cmd('python %s %s %s' % (scriptMake, fileName_In, fileName_Out))
    if(ratioWith=="FWHM"):
      scriptFit = os.path.join(workingDir, "resolutionPlot/macro", "fit_Et_Resolution_vs_Pt_Eta_Nvtx.C")
      fileName_In = os.path.join(workingDir, "resolutionPlot/results", "hist_Et_Resolution_vs_Pt_Eta_Nvtx_for_"+sampleType[j]+"_"+dataType[k]+"_"+tagPlot+".root")
      fileName_Out = os.path.join(workingDir, "resolutionPlot/results", "fitted_Hist_Et_Resolution_vs_Pt_Eta_Nvtx_for_"+sampleType[j]+"_"+dataType[k]+"_"+tagPlot+".root")
      run_cmd('root -b -n -q -l \'%s(\"%s\", \"%s\")\'' % (scriptFit, fileName_In, fileName_Out)) 
    scriptPlot = os.path.join(workingDir, "resolutionPlot/macro", "plot_Et_Resolution_vs_Pt_Eta_Nvtx.py")
    if(ratioWith=="FWHM"):
      fileName_In = os.path.join(workingDir, "resolutionPlot/results", "fitted_Hist_Et_Resolution_vs_Pt_Eta_Nvtx_for_"+sampleType[j]+"_"+dataType[k]+"_"+tagPlot+".root")
      fileName_Out = os.path.join(workingDir, "resolutionPlot/results", "plot_Et_Resolution_with_FWHM_for_"+sampleType[j]+"_"+dataType[k]+"_"+tagPlot)
    else:
      fileName_In = os.path.join(workingDir, "resolutionPlot/results", "hist_Et_Resolution_vs_Pt_Eta_Nvtx_for_"+sampleType[j]+"_"+dataType[k]+"_"+tagPlot+".root")
      fileName_Out = os.path.join(workingDir, "resolutionPlot/plots", "plot_Et_Resolution_with_RMS_for_"+sampleType[j]+"_"+dataType[k]+"_"+tagPlot)
    run_cmd('python %s %s %s %s' % (scriptPlot, fileName_In, fileName_Out, ratioWith))






# ---------------- Keep relavant plots to plot directory ------------------
'''
run_cmd('rm %s/*png' % pathPlot)
run_cmd('rm %s/*txt' % pathPlot)  
run_cmd('cp %s %s' % (workingDir+"/ratePlot/plots/"+"*"+tagPlot+"*.png", pathPlot))
run_cmd('cp %s %s' % (workingDir+"/efficiencyPlot/results/"+"*"+tagPlot+"*.txt", pathPlot)) 
run_cmd('cp %s %s' % (workingDir+"/efficiencyPlot/plots/"+"*"+tagPlot+"*.png", pathPlot))
run_cmd('cp %s %s' % (workingDir+"/resolutionPlot/plots/"+"*"+tagPlot+"*.png", pathPlot))
'''
# ----------------- Clean all directory for results --------------------
'''
run_cmd('rm %s/*' % (os.path.join(workingDir, "plots")))
run_cmd('rm %s/*' % (os.path.join(workingDir, "ratePlot/results")))
run_cmd('rm %s/*' % (os.path.join(workingDir, "ratePlot/plots")))
run_cmd('rm %s/*' % (os.path.join(workingDir, "efficiencyPlot/results")))
run_cmd('rm %s/*' % (os.path.join(workingDir, "efficiencyPlot/plots")))
run_cmd('rm %s/*.par' % (os.path.join(workingDir, "efficiencyPlot/fitTurnon/run")))
run_cmd('rm %s/*' % (os.path.join(workingDir, "resolutionPlot/results")))
run_cmd('rm %s/*' % (os.path.join(workingDir, "resolutionPlot/plots")))
'''




