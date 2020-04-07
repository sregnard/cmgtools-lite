#include "CMGTools/VVResonances/interface/GaussianSumTemplateMaker.h"
#include "CMGTools/VVResonances/interface/ConditionalGaussianSumTemplateMaker.h"
#include "CMGTools/VVResonances/interface/PTWeightTemplateMaker.h"
#include "CMGTools/VVResonances/interface/GaussianSumTemplateMaker1D.h"
#include "CMGTools/VVResonances/interface/KDEProducer.h"
#include "CMGTools/VVResonances/interface/KDEProducer2D.h"
#include "CMGTools/VVResonances/interface/RooGaussianSumPdf.h"

namespace cmg{

  struct cmg_vvresonances_dictionary {
    cmg::GaussianSumTemplateMaker templateMaker;
    cmg::GaussianSumTemplateMaker1D templateMaker1D;
    cmg::ConditionalGaussianSumTemplateMaker templateMakerCond;
    cmg::PTWeightTemplateMaker ptTemplateMaker;
    KDEProducer kdeprod;
    KDEProducer2D kdeprod2d;
    RooGaussianSumPdf pdf;
  };
}
