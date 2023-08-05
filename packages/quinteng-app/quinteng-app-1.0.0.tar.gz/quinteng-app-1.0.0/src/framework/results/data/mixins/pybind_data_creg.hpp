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

#ifndef _app_framework_result_data_pybind_data_creg_hpp_
#define _app_framework_result_data_pybind_data_creg_hpp_

#include "framework/results/data/mixins/data_creg.hpp"
#include "framework/results/data/subtypes/pybind_data_map.hpp"

//------------------------------------------------------------------------------
// App C++ -> Python Conversion
//------------------------------------------------------------------------------

namespace AppToPy {

// Move an DataCreg container object to a new Python dict
py::object to_python(APP::DataCreg &&data);

// Move an DataCreg container object to an existing new Python dict
void add_to_python(py::dict &pydata, APP::DataCreg &&data);

} //end namespace AppToPy


//============================================================================
// Implementations
//============================================================================

py::object AppToPy::to_python(APP::DataCreg &&data) {
  py::dict pydata;
  AppToPy::add_to_python(pydata, std::move(data));
  return std::move(pydata);
}

void AppToPy::add_to_python(py::dict &pydata, APP::DataCreg &&data) {
  AppToPy::add_to_python(pydata, static_cast<APP::DataMap<APP::ListData, std::string, 1>&&>(data));
  AppToPy::add_to_python(pydata, static_cast<APP::DataMap<APP::AccumData, APP::uint_t, 2>&&>(data));
}

#endif
