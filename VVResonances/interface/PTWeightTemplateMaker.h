#include "RooDataSet.h"
#include "TH2.h"
#include "TH1.h"
namespace cmg {

class PTWeightTemplateMaker {
 public:
  PTWeightTemplateMaker();
  ~PTWeightTemplateMaker();
  PTWeightTemplateMaker(const RooDataSet*,const char*, const char*, TH1*,TH1*,TH2*,int );


 private:

};


}
