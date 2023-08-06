/**
 * This code is part of Quinteng.
 *
 * (C) Copyright IBM 2020.
 *
 * This code is licensed under the Apache License, Version 2.0. You may
 * obtain a copy of this license in the LICENSE.txt file in the root directory
 * of this source tree or at http://www.apache.org/licenses/LICENSE-2.0.
 *
 * Any modifications or derivative works of this code must retain this
 * copyright notice, and modified files need to carry a notice indicating
 * that they have been altered from the originals.
 */

#ifndef _app_framework_result_data_pybind_data_hpp_
#define _app_framework_result_data_pybind_data_hpp_

#include "framework/results/data/data.hpp"
#include "framework/results/data/mixins/pybind_data_creg.hpp"
#include "framework/results/data/mixins/pybind_data_rdict.hpp"
#include "framework/results/data/mixins/pybind_data_rvalue.hpp"
#include "framework/results/data/mixins/pybind_data_rvector.hpp"
#include "framework/results/data/mixins/pybind_data_cmatrix.hpp"
#include "framework/results/data/mixins/pybind_data_cvector.hpp"
#include "framework/results/data/mixins/pybind_data_cdict.hpp"
#include "framework/results/data/mixins/pybind_data_json.hpp"
#include "framework/results/data/mixins/pybind_data_mps.hpp"

namespace AppToPy {

// Move an ExperimentResult data object to a Python dict
template <> py::object to_python(APP::Data &&data);

} //end namespace AppToPy


//============================================================================
// Implementations
//============================================================================

template <>
py::object AppToPy::to_python(APP::Data &&data) {
  py::dict pydata;
  AppToPy::add_to_python(pydata, static_cast<APP::DataRValue&&>(data));
  AppToPy::add_to_python(pydata, static_cast<APP::DataRVector&&>(data));
  AppToPy::add_to_python(pydata, static_cast<APP::DataRDict&&>(data));
  AppToPy::add_to_python(pydata, static_cast<APP::DataCVector&&>(data));
  AppToPy::add_to_python(pydata, static_cast<APP::DataCMatrix&&>(data));
  AppToPy::add_to_python(pydata, static_cast<APP::DataCDict&&>(data));
  AppToPy::add_to_python(pydata, static_cast<APP::DataJSON&&>(data));
  AppToPy::add_to_python(pydata, static_cast<APP::DataMPS&&>(data));
  AppToPy::add_to_python(pydata, static_cast<APP::DataCreg&&>(data));
  return std::move(pydata);
}

#endif
