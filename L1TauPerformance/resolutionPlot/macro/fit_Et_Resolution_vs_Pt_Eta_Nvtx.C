// double CB symmetric (two-sided tails)
double CrystalBall
(double* x, double* par){ 
  //http://en.wikipedia.org/wiki/Crystal_Ball_function 
  double xcur = x[0]; 
  double alpha = par[0]; 
  double n = par[1]; 
  double mu = par[2]; 
  double sigma = par[3]; 
  double N = par[4]; 
  TF1* exp = new TF1("exp","exp(x)",1e-20,1e20); 
  double A; double B; 
  if (alpha < 0){ 
    A = pow((n/(-1*alpha)),n)*exp->Eval((-1)*alpha*alpha/2); 
    B = n/(-1*alpha) + alpha;} 
  else { 
    A = pow((n/alpha),n)*exp->Eval((-1)*alpha*alpha/2); 
    B = n/alpha - alpha;} 
    double f; 
  if (TMath::Abs((xcur-mu)/sigma) < TMath::Abs(alpha) ) 
    f = N*exp->Eval((-1)*(xcur-mu)*(xcur-mu)/(2*sigma*sigma)); 
  else if (((xcur-mu)/sigma) < (-1.)*alpha )
    f = N*A*pow((B- (xcur-mu)/sigma),(-1*n)); // left tail
  else
    f = N*A*pow( (B- (mu-xcur)/sigma),(-1*n)); // right tail
  delete exp; 
  return f; 
} 

// double CB asymmetric
double DoubleCrystalBall
(double* x, double* par){ 
  //http://en.wikipedia.org/wiki/Crystal_Ball_function 
  double xcur = x[0]; 
  double alphaL = par[0]; 
  double nL = par[1]; 
  double alphaR = par[2]; 
  double nR = par[3]; 

  double mu = par[4]; 
  double sigma = par[5]; 
  double N = par[6]; 
 
  TF1* exp = new TF1("exp","exp(x)",1e-20,1e20); 
  double AL; double BL; double AR; double BR; 
 
  if (alphaL < 0){ 
    AL = pow((nL/(-1*alphaL)),nL)*exp->Eval((-1)*alphaL*alphaL/2); 
    BL = nL/(-1*alphaL) + alphaL;} 
  else { 
    AL = pow((nL/alphaL),nL)*exp->Eval((-1)*alphaL*alphaL/2); 
    BL = nL/alphaL - alphaL;} 

  if (alphaR < 0){ 
    AR = pow((nR/(-1*alphaR)),nR)*exp->Eval((-1)*alphaR*alphaR/2); 
    BR = nR/(-1*alphaR) + alphaR;} 
  else { 
    AR = pow((nR/alphaR),nR)*exp->Eval((-1)*alphaR*alphaR/2); 
    BR = nR/alphaR - alphaR;} 
   

    double f; 
  if ( ((xcur-mu)/sigma) > (-1.)*alphaL  && ((xcur-mu)/sigma) < (1.)*alphaR) 
    f = N*exp->Eval((-1)*(xcur-mu)*(xcur-mu)/(2*sigma*sigma)); 
  
  // left
  else if ( ((xcur-mu)/sigma) <= (-1.)*alphaL )
    f = N*AL*pow((BL- (xcur-mu)/sigma),(-1*nL)); // left tail
  //right
  else
    f = N*AR*pow( (BR- (mu-xcur)/sigma),(-1*nR)); // right tail
  delete exp; 
  return f; 
} 

double CompFWHM( TF1* FitFunc)
{
  double max = FitFunc->GetMaximum();
  double x_max = FitFunc->GetMaximumX();
  double x1_fwhm = 0;
  double x2_fwhm =0;
  double fwhm = 0;
  double xStep = 0.0003;
  for (int ix=0; ix<10000+1; ix++)
    {
      double x1 = ix*xStep;
      double x2 = (ix-1)*xStep;
      if (FitFunc->Eval(x1) > 0.5*max && FitFunc->Eval(x2) < 0.5*max)
	{
	  x1_fwhm = x1;
	}
      if (FitFunc->Eval(x1) < 0.5*max && FitFunc->Eval(x2) > 0.5*max)
	{
	  x2_fwhm= x1;
	}
    }
  fwhm = x2_fwhm - x1_fwhm;

  return fwhm;
}


void fit_Et_Resolution_vs_Pt_Eta_Nvtx() // for FWHM
{
  TString fileName_In = "../results/hist_Et_Resolution_vs_Pt_Eta_Nvtx_for_data_Run2018_20210715.root"; 
  TString fileName_Out = "../results/fitted_Hist_Et_Resolution_vs_Pt_Eta_Nvtx_for_data_Run2018_20210715.root"
  //void fit_Et_Resolution_vs_Pt_Eta_Nvtx(TString fileName_In, TString fileName_Out)
    //{

  TFile* fileIn = new TFile(fileName_In);
  TFile* fileOut = new TFile(fileName_Out, "RECREATE");
  const int netabin = 9;
  const int nptbin = 11;
  const int nvtxbin = 12;
  float etaBinning[netabin+1] = {0, 0.26, 0.52, 0.78, 1.04, 1.30, 1.48, 1.75, 2.0, 2.5};
  float ptBinning[nptbin+1]  = {20, 23, 26, 30, 35, 40, 45, 50, 60, 70, 90, 110};
  float nvtxBinning[nvtxbin+1] = {0, 10, 15, 20, 25, 30, 35, 40, 45, 50, 60, 70, 80};
  TH1F *hist_Et_Resolution_vs_Eta_for_All = new TH1F ("hist_Et_Resolution_vs_Eta_for_All", "hist_Et_Resolution_vs_Eta_for_All", netabin,  etaBinning);
  TH1F *hist_Et_Resolution_vs_Pt_for_All = new TH1F ("hist_Et_Resolution_vs_Pt_for_All", "hist_Et_Resolution_vs_Pt_for_All", nptbin, ptBinning);
  TH1F *hist_Et_Resolution_vs_Pt_for_Barrel = new TH1F ("hist_Et_Resolution_vs_Pt_for_Barrel", "hist_Et_Resolution_vs_Pt_for_Barrel", nptbin, ptBinning);
  TH1F *hist_Et_Resolution_vs_Pt_for_Endcap = new TH1F ("hist_Et_Resolution_vs_Pt_for_Endcap", "hist_Et_Resolution_vs_Pt_for_Endcap", nptbin, ptBinning);
  TH1F *hist_Et_Resolution_vs_Nvtx_for_All = new TH1F ("hist_Et_Resolution_vs_Nvtx_for_All", "hist_Et_Resolution_vs_Nvtx_for_All",  nvtxbin, nvtxBinning);

  vector<TString> fitDoubleCB_eta = {"hist_Et_Resolution_vs_Eta_for_All_0.0", "hist_Et_Resolution_vs_Eta_for_All_0.26", "hist_Et_Resolution_vs_Eta_for_All_0.52", "hist_Et_Resolution_vs_Eta_for_All_0.78", "hist_Et_Resolution_vs_Eta_for_All_1.04", "hist_Et_Resolution_vs_Eta_for_All_1.3", "hist_Et_Resolution_vs_Eta_for_All_1.48", "hist_Et_Resolution_vs_Eta_for_All_1.75", "hist_Et_Resolution_vs_Eta_for_All_2.0"};
  vector<TString> fitDoubleCB_pt = {"hist_Et_Resolution_vs_Pt_for_All_20.0", "hist_Et_Resolution_vs_Pt_for_All_23.0", "hist_Et_Resolution_vs_Pt_for_All_26.0", "hist_Et_Resolution_vs_Pt_for_All_30.0", "hist_Et_Resolution_vs_Pt_for_All_35.0", "hist_Et_Resolution_vs_Pt_for_All_40.0", "hist_Et_Resolution_vs_Pt_for_All_45.0", "hist_Et_Resolution_vs_Pt_for_All_50.0", "hist_Et_Resolution_vs_Pt_for_All_60.0", "hist_Et_Resolution_vs_Pt_for_All_70.0", "hist_Et_Resolution_vs_Pt_for_All_90.0"};
  vector<TString> fitDoubleCB_pt_barrel = {"hist_Et_Resolution_vs_Pt_for_Barrel_20.0", "hist_Et_Resolution_vs_Pt_for_Barrel_23.0", "hist_Et_Resolution_vs_Pt_for_Barrel_26.0", "hist_Et_Resolution_vs_Pt_for_Barrel_30.0", "hist_Et_Resolution_vs_Pt_for_Barrel_35.0", "hist_Et_Resolution_vs_Pt_for_Barrel_40.0", "hist_Et_Resolution_vs_Pt_for_Barrel_45.0", "hist_Et_Resolution_vs_Pt_for_Barrel_50.0", "hist_Et_Resolution_vs_Pt_for_Barrel_60.0", "hist_Et_Resolution_vs_Pt_for_Barrel_70.0", "hist_Et_Resolution_vs_Pt_for_Barrel_90.0"};
  vector<TString> fitDoubleCB_pt_endcap = {"hist_Et_Resolution_vs_Pt_for_Endcap_20.0", "hist_Et_Resolution_vs_Pt_for_Endcap_23.0", "hist_Et_Resolution_vs_Pt_for_Endcap_26.0", "hist_Et_Resolution_vs_Pt_for_Endcap_30.0", "hist_Et_Resolution_vs_Pt_for_Endcap_35.0", "hist_Et_Resolution_vs_Pt_for_Endcap_40.0", "hist_Et_Resolution_vs_Pt_for_Endcap_45.0", "hist_Et_Resolution_vs_Pt_for_Endcap_50.0", "hist_Et_Resolution_vs_Pt_for_Endcap_60.0", "hist_Et_Resolution_vs_Pt_for_Endcap_70.0", "hist_Et_Resolution_vs_Pt_for_Endcap_90.0"};
  vector<TString> fitDoubleCB_nvtx = {"hist_Et_Resolution_vs_Nvtx_for_All_0.0", "hist_Et_Resolution_vs_Nvtx_for_All_10.0", "hist_Et_Resolution_vs_Nvtx_for_All_15.0", "hist_Et_Resolution_vs_Nvtx_for_All_20.0", "hist_Et_Resolution_vs_Nvtx_for_All_25.0", "hist_Et_Resolution_vs_Nvtx_for_All_30.0", "hist_Et_Resolution_vs_Nvtx_for_All_35.0", "hist_Et_Resolution_vs_Nvtx_for_All_40.0", "hist_Et_Resolution_vs_Nvtx_for_All_45.0", "hist_Et_Resolution_vs_Nvtx_for_All_50.0", "hist_Et_Resolution_vs_Nvtx_for_All_60.0", "hist_Et_Resolution_vs_Nvtx_for_All_70.0"};
  /*
  vector<TString> fitDoubleCB_eta = {"hist_Et_Resolution_vs_Eta_for_All_0.0"};
  vector<TString> fitDoubleCB_pt = {"hist_Et_Resolution_vs_Pt_for_All_20.0"};
  vector<TString> fitDoubleCB_nvtx = {"hist_Et_Resolution_vs_Nvtx_for_All_0.0"};
  */
  TH1::SetDefaultSumw2();

  TF1* CBFuncAsymm = new TF1("CBFuncAsymm",&DoubleCrystalBall,0.,3.,7);

  int i_ptbin = 0;
  for (TString name : fitDoubleCB_pt)
    {
      i_ptbin++;
      cout << "... fitting: " << name << endl;
      TH1F* h = (TH1F*) fileIn->Get(name);
      h->Scale(1./h->Integral());
      CBFuncAsymm->SetParameters(0.9, 4.3, 1.3, 4.3, h->GetMean(), h->GetRMS(), 1.);
      h->Fit("CBFuncAsymm");

      //double fwhm_ = CompFWHM(CBFuncAsymm);
      //cout << " fwhm_ " << fwhm_ << endl;

      double max = CBFuncAsymm->GetMaximum();
      double x_max = CBFuncAsymm->GetMaximumX();
      int nbin = h->GetNbinsX();
      double x1_fwhm = 0;
      double x2_fwhm =0;
      double fwhm = 0;
      double xStep = 0.0003;
      for (int ix=0; ix<10000+1; ix++)
	{
	  double x1 = ix*xStep;
	  double x2 = (ix-1)*xStep;
	  if (CBFuncAsymm->Eval(x1) > 0.5*max && CBFuncAsymm->Eval(x2) < 0.5*max)
	    {
	      x1_fwhm = x1;
	    }
	  if (CBFuncAsymm->Eval(x1) < 0.5*max && CBFuncAsymm->Eval(x2) > 0.5*max)
	    { 
	      x2_fwhm= x1;
	    }
	}
      fwhm = x2_fwhm - x1_fwhm;
      //cout << " ibin " << i_ptbin << " fwhm " << fwhm << " x_max " << x_max << " fwhm/x_max " << fwhm/x_max << endl;


      
      hist_Et_Resolution_vs_Pt_for_All->SetBinContent(i_ptbin, fwhm/x_max);
      //hist_Et_Resolution_vs_Pt_for_All->SetBinError(i_ptbin, 0.0);

      fileOut->cd();
      h->Write();
    }
  hist_Et_Resolution_vs_Pt_for_All->Write();

  int i_ptbin_barrel = 0;
  for (TString name : fitDoubleCB_pt_barrel)
    {
      i_ptbin_barrel++;
      cout << "... fitting: " << name << endl;
      TH1F* h = (TH1F*) fileIn->Get(name);
      h->Scale(1./h->Integral());
      CBFuncAsymm->SetParameters(0.9, 4.3, 1.3, 4.3, h->GetMean(), h->GetRMS(), 1.);
      h->Fit("CBFuncAsymm");
      
      double max = CBFuncAsymm->GetMaximum();
      double x_max = CBFuncAsymm->GetMaximumX();
      int nbin = h->GetNbinsX();
      double x1_fwhm = 0;
      double x2_fwhm =0;
      double fwhm = 0;
      double xStep = 0.0003;
      for (int ix=0; ix<10000+1; ix++)
	{
	  double x1 = ix*xStep;
	  double x2 = (ix-1)*xStep;
	  if (CBFuncAsymm->Eval(x1) > 0.5*max && CBFuncAsymm->Eval(x2) < 0.5*max)
	    { 
	      x1_fwhm= x1;
	    }
	  if (CBFuncAsymm->Eval(x1) < 0.5*max && CBFuncAsymm->Eval(x2) > 0.5*max)
	    {
	      x2_fwhm= x1;
              }
	}
      fwhm = x2_fwhm - x1_fwhm;
      cout << "fwhm " << fwhm << endl;
      
      hist_Et_Resolution_vs_Pt_for_Barrel->SetBinContent(i_ptbin_barrel, fwhm/x_max);
      //hist_Et_Resolution_vs_Pt_for_Barrel->SetBinError(i_ptbin_barrel, 0.0);
      
      fileOut->cd();
      h->Write();
    }
  hist_Et_Resolution_vs_Pt_for_Barrel->Write();
  
  int i_ptbin_endcap = 0;
  for (TString name : fitDoubleCB_pt_endcap)
    {
      i_ptbin_endcap++;
      cout << "... fitting: " << name << endl;
      TH1F* h = (TH1F*) fileIn->Get(name);
      h->Scale(1./h->Integral());
      CBFuncAsymm->SetParameters(0.9, 4.3, 1.3, 4.3, h->GetMean(), h->GetRMS(), 1.);
      h->Fit("CBFuncAsymm");
      
      double max = CBFuncAsymm->GetMaximum();
      double x_max = CBFuncAsymm->GetMaximumX();
      int nbin = h->GetNbinsX();
      double x1_fwhm = 0;
      double x2_fwhm =0;
      double fwhm = 0;
      double xStep = 0.0003;
      for (int ix=0; ix<10000+1; ix++)
	{
	  double x1 = ix*xStep;
	  double x2 = (ix-1)*xStep;
	  if (CBFuncAsymm->Eval(x1) > 0.5*max && CBFuncAsymm->Eval(x2) < 0.5*max)
	    { 
	      x1_fwhm= x1;
	    }
	  if (CBFuncAsymm->Eval(x1) < 0.5*max && CBFuncAsymm->Eval(x2) > 0.5*max)
	    {
	      x2_fwhm= x1;
	    }
	}
      fwhm = x2_fwhm - x1_fwhm;
      cout << "fwhm " << fwhm << endl;
      
      hist_Et_Resolution_vs_Pt_for_Endcap->SetBinContent(i_ptbin_endcap, fwhm/x_max);
      //hist_Et_Resolution_vs_Pt_for_Endcap->SetBinError(i_ptbin_endcap, 0.0);
      
      fileOut->cd();
      h->Write();
    }
  hist_Et_Resolution_vs_Pt_for_Endcap->SetBinContent(nptbin, 0); // forsed as this bin could't fit 
  //hist_Et_Resolution_vs_Pt_for_Endcap->SetBinError(nptbin, 0.0);
  hist_Et_Resolution_vs_Pt_for_Endcap->Write();

  int i_ptbin_eta = 0;
  for (TString name : fitDoubleCB_eta)
    {
      i_ptbin_eta++;
      cout << "... fitting: " << name << endl;
      TH1F* h = (TH1F*) fileIn->Get(name);
      h->Scale(1./h->Integral());
      CBFuncAsymm->SetParameters(0.9, 4.3, 1.3, 4.3, h->GetMean(), h->GetRMS(), 1.);
      h->Fit("CBFuncAsymm");
      
      double max = CBFuncAsymm->GetMaximum();
      double x_max = CBFuncAsymm->GetMaximumX();
      int nbin = h->GetNbinsX();
      double x1_fwhm = 0;
      double x2_fwhm =0;
      double fwhm = 0;
      double xStep = 0.0003;
      for (int ix=0; ix<10000+1; ix++)
	{
	  double x1 = ix*xStep;
	  double x2 = (ix-1)*xStep;
	  if (CBFuncAsymm->Eval(x1) > 0.5*max && CBFuncAsymm->Eval(x2) < 0.5*max)
	    { 
	      x1_fwhm= x1;
	    }
            if (CBFuncAsymm->Eval(x1) < 0.5*max && CBFuncAsymm->Eval(x2) > 0.5*max)
              {
                x2_fwhm= x1;
              }
          }
      fwhm = x2_fwhm - x1_fwhm;
      cout << "fwhm " << fwhm << endl;
      
      hist_Et_Resolution_vs_Eta_for_All->SetBinContent(i_ptbin_eta, fwhm/x_max);
      //hist_Et_Resolution_vs_Eta_for_All->SetBinError(i_ptbin_eta, 0.0);
      
      fileOut->cd();
      h->Write();
    }
  hist_Et_Resolution_vs_Eta_for_All->Write();
  
  int i_ptbin_nvtx = 0;
  for (TString name : fitDoubleCB_nvtx)
    {
      i_ptbin_nvtx++;
      cout << "... fitting: " << name << endl;
      TH1F* h = (TH1F*) fileIn->Get(name);
      h->Scale(1./h->Integral());
      CBFuncAsymm->SetParameters(0.9, 4.3, 1.3, 4.3, h->GetMean(), h->GetRMS(), 1.);
      h->Fit("CBFuncAsymm");
      
      double max = CBFuncAsymm->GetMaximum();
      double x_max = CBFuncAsymm->GetMaximumX();
      int nbin = h->GetNbinsX();
      double x1_fwhm = 0;
      double x2_fwhm =0;
      double fwhm = 0;
      double xStep = 0.0003;
      for (int ix=0; ix<10000+1; ix++)
	{
	  double x1 = ix*xStep;
	  double x2 = (ix-1)*xStep;
	  if (CBFuncAsymm->Eval(x1) > 0.5*max && CBFuncAsymm->Eval(x2) < 0.5*max)
	    { 
	      x1_fwhm= x1;
	    }
	  if (CBFuncAsymm->Eval(x1) < 0.5*max && CBFuncAsymm->Eval(x2) > 0.5*max)
	    {
	      x2_fwhm= x1;
	    }
	}
      fwhm = x2_fwhm - x1_fwhm;
      cout << "fwhm " << fwhm << endl;
      
      hist_Et_Resolution_vs_Nvtx_for_All->SetBinContent(i_ptbin_nvtx, fwhm/x_max);
      //hist_Et_Resolution_vs_Nvtx_for_All->SetBinError(i_ptbin_nvtx, 0.0);
      
      fileOut->cd();
      h->Write();
    }
  hist_Et_Resolution_vs_Nvtx_for_All->Write();

  fileOut->Close();
}
