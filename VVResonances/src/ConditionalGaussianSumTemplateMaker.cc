#include "CMGTools/VVResonances/interface/ConditionalGaussianSumTemplateMaker.h"
#include "RooArgSet.h"

using namespace cmg;
ConditionalGaussianSumTemplateMaker::ConditionalGaussianSumTemplateMaker() {}
ConditionalGaussianSumTemplateMaker::~ConditionalGaussianSumTemplateMaker() {}

ConditionalGaussianSumTemplateMaker::ConditionalGaussianSumTemplateMaker(const RooDataSet* dataset,const char* varx, const char* vary,const char* varpt, TH1* hscalex,TH1* hresx,TH2* out,TH2* outUp,TH2* outDown, TH2* outUp2,TH2*outDown2,float reweigh ) {

  double genx,geny,x,scalex,resx,genpt;
  genx=0.0;
  geny=0.0;
  scalex=0.0;
  x=0.0;
  resx=0.0;
  genpt=0.0;

  

  //  int bin=0;
  unsigned int nevents = dataset->numEntries();
  for (unsigned int entry=0;entry<nevents;++entry) {

    if ((entry % 10000)==0) {
      printf("Processed %d out of %d entries\n",entry,nevents);
    }

    const RooArgSet *line  = dataset->get(entry);
    genx=line->getRealValue(varx);
    geny=line->getRealValue(vary);
    genpt=line->getRealValue(varpt);

    scalex=hscalex->Interpolate(genpt)*genx;
    resx=hresx->Interpolate(genpt)*genx;
    for (int i=1;i<out->GetNbinsX()+1;++i) {
      float weight = dataset->weight();
      x=out->GetXaxis()->GetBinCenter(i);
      weight=weight*(1.0+reweigh*genx);
      out->Fill(x,geny,weight*gaus(x,scalex,resx));
      outUp->Fill(x,geny,weight*(1+1.5e-3*(x-600))*gaus(x,scalex,resx));
      outDown->Fill(x,geny,weight*(1.0/(1+1.5e-3*(x-600)))*gaus(x,scalex,resx));
      outUp2->Fill(x,geny,weight*gaus(x,scalex*(std::max(1.0,1+0.005*(geny-80.))),resx));
      outDown2->Fill(x,geny,weight*gaus(x,scalex*(std::min(1.0,1-0.005*(geny-80))),resx));
    }
  }
}



double ConditionalGaussianSumTemplateMaker::gaus(double x,double genx,double resx) {
  return exp(-0.5*(x-genx)*(x-genx)/(resx*resx))/(2.5066*resx);

} 
