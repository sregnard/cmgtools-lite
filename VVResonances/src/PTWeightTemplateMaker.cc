#include "CMGTools/VVResonances/interface/PTWeightTemplateMaker.h"
#include "RooArgSet.h"

using namespace cmg;
PTWeightTemplateMaker::PTWeightTemplateMaker() {}
PTWeightTemplateMaker::~PTWeightTemplateMaker() {}

PTWeightTemplateMaker::PTWeightTemplateMaker(const RooDataSet* dataset, const char* varx,const char* varpt,TH1* source,TH1* target,TH2* output,int biny) {

  double x=0.0;
  double pt=0.0;
  int binpt=0;
  int binx=0;
  double scaling=0.0;
  int bin=0;
  unsigned int nevents = dataset->numEntries();
  source->Scale(1.0/source->Integral());
  target->Scale(1.0/target->Integral());

  double targetVal=0.0;
  double sourceVal=0.0;

  for (unsigned int entry=0;entry<nevents;++entry) {

    const RooArgSet *line  = dataset->get(entry);
    x=line->getRealValue(varx);
    pt=line->getRealValue(varpt);
    binx=output->GetXaxis()->FindBin(x);
    binpt=source->GetXaxis()->FindBin(pt);
    targetVal = target->GetBinContent(binpt);
    sourceVal = source->GetBinContent(binpt);
    scaling=targetVal/sourceVal;

    if (sourceVal==0.0||scaling>5.0)
      continue;
    
    bin=output->GetBin(binx,biny);
    output->SetBinContent(bin,output->GetBinContent(bin)+dataset->weight()*scaling);
  }

}


