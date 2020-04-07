#include "RooDataSet.h"
#include "TH2.h"
#include "TH1.h"
namespace cmg {

class ConditionalGaussianSumTemplateMaker {
 public:
  ConditionalGaussianSumTemplateMaker();
  ~ConditionalGaussianSumTemplateMaker();
  ConditionalGaussianSumTemplateMaker(const RooDataSet* dataset,const char* varx, const char* vary,const char* varpt, TH1* sx,TH1* resx,TH2* out,TH2* outUp,TH2* outDown, TH2* outUp2,TH2*outDown2,float reweigh );


 private:
  double gaus(double, double,double);
};


}
