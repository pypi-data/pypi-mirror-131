/**
 * This code is part of Quinteng.
 *
 * (C) Copyright IBM 2021.
 *
 * This code is licensed under the Apache License, Version 2.0. You may
 * obtain a copy of this license in the LICENSE.txt file in the root directory
 * of this source tree or at http://www.apache.org/licenses/LICENSE-2.0.
 *
 * Any modifications or derivative works of this code must retain this
 * copyright notice, and modified files need to carry a notice indicating
 * that they have been altered from the originals.
 */

#ifndef _app_framework_result_data_pybind_data_rvalue_hpp_
#define _app_framework_result_data_pybind_data_rvalue_hpp_

#include "framework/results/data/mixins/data_rvalue.hpp"
#include "framework/results/data/subtypes/pybind_data_map.hpp"

//------------------------------------------------------------------------------
// App C++ -> Python Conversion
//------------------------------------------------------------------------------

namespace AppToPy {

// Move an DataRValue container object to a new Python dict
py::object to_python(APP::DataRValue &&data);

// Move an DataRValue container object to an existing new Python dict
void add_to_python(py::dict &pydata, APP::DataRValue &&data);

} //end namespace AppToPy


//============================================================================
// Implementations
//============================================================================

py::object AppToPy::to_python(APP::DataRValue &&data) {
  py::dict pydata;
  AppToPy::add_to_python(pydata, std::move(data));
  return std::move(pydata);
}

void AppToPy::add_to_python(py::dict &pydata, APP::DataRValue &&data) {
  AppToPy::add_to_python(pydata, static_cast<APP::DataMap<APP::ListData, double, 1>&&>(data));
  AppToPy::add_to_python(pydata, static_cast<APP::DataMap<APP::ListData, double, 2>&&>(data));
  AppToPy::add_to_python(pydata, static_cast<APP::DataMap<APP::AccumData, double, 1>&&>(data));
  AppToPy::add_to_python(pydata, static_cast<APP::DataMap<APP::AccumData, double, 2>&&>(data));
  AppToPy::add_to_python(pydata, static_cast<APP::DataMap<APP::AverageData, double, 1>&&>(data));
  AppToPy::add_to_python(pydata, static_cast<APP::DataMap<APP::AverageData, double, 2>&&>(data));
}

#endif
