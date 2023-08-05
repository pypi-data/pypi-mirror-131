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

#ifndef _app_framework_result_data_pybind_data_mps_hpp_
#define _app_framework_result_data_pybind_data_mps_hpp_

#include "framework/results/data/mixins/data_mps.hpp"
#include "framework/results/data/subtypes/pybind_data_map.hpp"

//------------------------------------------------------------------------------
// App C++ -> Python Conversion
//------------------------------------------------------------------------------

namespace AppToPy {

// Move mps_container_t to python object
template <> py::object to_python(APP::mps_container_t &&mps);

// Move an DataMPS container object to a new Python dict
py::object to_python(APP::DataMPS &&data);

// Move an DataMPS container object to an existing new Python dict
void add_to_python(py::dict &pydata, APP::DataMPS &&data);

} //end namespace AppToPy


//============================================================================
// Implementations
//============================================================================

template <> py::object AppToPy::to_python(APP::mps_container_t &&data) {
  py::list mats;
  for (auto& pair: data.first) {
    mats.append(py::make_tuple(AppToPy::to_python(std::move(pair.first)),
                               AppToPy::to_python(std::move(pair.second))));
  }
  py::list vecs;
  for (auto&& vec: data.second) {
    vecs.append(AppToPy::to_python(std::move(vec)));
  }
  return py::make_tuple(std::move(mats), std::move(vecs));
}

py::object AppToPy::to_python(APP::DataMPS &&data) {
  py::dict pydata;
  AppToPy::add_to_python(pydata, std::move(data));
  return std::move(pydata);
}

void AppToPy::add_to_python(py::dict &pydata, APP::DataMPS &&data) {
  AppToPy::add_to_python(pydata, static_cast<APP::DataMap<APP::SingleData, APP::mps_container_t, 1>&&>(data));
  AppToPy::add_to_python(pydata, static_cast<APP::DataMap<APP::SingleData, APP::mps_container_t, 2>&&>(data));
  AppToPy::add_to_python(pydata, static_cast<APP::DataMap<APP::ListData, APP::mps_container_t, 1>&&>(data));
  AppToPy::add_to_python(pydata, static_cast<APP::DataMap<APP::ListData, APP::mps_container_t, 2>&&>(data));
}

#endif
