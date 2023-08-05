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

#ifndef _app_framework_result_data_pybind_data_map_hpp_
#define _app_framework_result_data_pybind_data_map_hpp_

#include "framework/results/data/subtypes/pybind_subtypes.hpp"
#include "framework/results/data/subtypes/data_map.hpp"

namespace AppToPy {

// Move an DataMap object to python
template <template <class> class Data, class T, size_t N>
py::object to_python(APP::DataMap<Data, T, N> &&src);

// Move an DataMap object into an existing Python dict
template <template <class> class Data, class T, size_t N>
void add_to_python(py::dict &pydata, APP::DataMap<Data, T, N> &&src);

// Move an DataMap object into an existing Python dict
template <template <class> class Data, class T>
void add_to_python(py::dict &pydata, APP::DataMap<Data, T, 1> &&src);

} //end namespace AppToPy


//============================================================================
// Implementations
//============================================================================

template <template <class> class Data, class T, size_t N>
py::object AppToPy::to_python(APP::DataMap<Data, T, N> &&src) {
  py::dict pydata;
  if (src.enabled) {
    for (auto& elt : src.value()) {
      pydata[elt.first.data()] = AppToPy::to_python(std::move(elt.second));
    }
  }
  return std::move(pydata);
}

template <template <class> class Data, class T, size_t N>
void AppToPy::add_to_python(py::dict &pydata, APP::DataMap<Data, T, N> &&src) {
  if (src.enabled) {
    for (auto& elt : src.value()) {
      auto& key = elt.first;
      py::dict item = (pydata.contains(key.data())) 
        ? std::move(pydata[key.data()])
        : py::dict();
      AppToPy::add_to_python(item, std::move(elt.second));
      pydata[key.data()] = std::move(item);
    }
  }
}

template <template <class> class Data, class T>
void AppToPy::add_to_python(py::dict &pydata, APP::DataMap<Data, T, 1> &&src) {
  if (src.enabled) {
    for (auto& elt : src.value()) {
      pydata[elt.first.data()] = AppToPy::to_python(std::move(elt.second));
    }
  }
}

#endif
