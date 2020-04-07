#include "CMGTools/VVResonances/interface/GaussianSumTemplateMaker1D.h"
#include "RooArgSet.h"

using namespace cmg;
GaussianSumTemplateMaker1D::GaussianSumTemplateMaker1D() {}
GaussianSumTemplateMaker1D::~GaussianSumTemplateMaker1D() {}

GaussianSumTemplateMaker1D::GaussianSumTemplateMaker1D(const RooDataSet* dataset, const char* varx,const char* varpt,TH1* hscalex,TH1* hresx,TH1* output,TH1* outputScaleUp,TH1* outputScaleDown,TH1* outputResUp,TH1* outputResDown,const char* varw,TH1* weightH) {

  double genx,x,scalex,resx,genpt,reweight,genw;
  genx=0.0;
  scalex=0.0;
  x=0.0;
  resx=0.0;
  genpt=0.0;
  reweight=1.0;
  genw=0.0;
  


  int binw=0;
  unsigned int nevents = dataset->numEntries();
  for (unsigned int entry=0;entry<nevents;++entry) {

    if ((entry % 10000)==0) {
      printf("Processed %d out of %d entries\n",entry,nevents);
    }

    const RooArgSet *line  = dataset->get(entry);
    genx=line->getRealValue(varx);
    genpt=line->getRealValue(varpt);
    if (weightH!=0) {
      genw=line->getRealValue(varw);
      binw=weightH->GetXaxis()->FindBin(genw);
      reweight=weightH->GetBinContent(binw);
    }
      
    scalex=hscalex->Interpolate(genpt)*genx;
    resx=hresx->Interpolate(genpt)*genx;
    for (int i=1;i<output->GetNbinsX()+1;++i) {
      x=output->GetXaxis()->GetBinCenter(i);
      output->Fill(x,reweight*dataset->weight()*gaus(x,scalex,resx));
      outputScaleUp->Fill(x,reweight*dataset->weight()*gaus(x,1.15*scalex,resx));
      outputScaleDown->Fill(x,reweight*dataset->weight()*gaus(x,0.85*scalex,resx));
      outputResUp->Fill(x,reweight*dataset->weight()*gaus(x,scalex,1.25*resx));
      outputResDown->Fill(x,reweight*dataset->weight()*gaus(x,scalex,0.75*resx));

    }
  }
}



double GaussianSumTemplateMaker1D::gaus(double x,double genx,double resx) {
  return exp(-0.5*(x-genx)*(x-genx)/(resx*resx))/(2.5066*resx);
} 
