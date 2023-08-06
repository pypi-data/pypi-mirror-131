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

#ifndef _app_framework_result_data_pybind_subtypes_hpp_
#define _app_framework_result_data_pybind_subtypes_hpp_

#include "framework/pybind_basics.hpp"
#include "framework/results/data/subtypes/single_data.hpp"
#include "framework/results/data/subtypes/accum_data.hpp"
#include "framework/results/data/subtypes/average_data.hpp"
#include "framework/results/data/subtypes/list_data.hpp"

namespace AppToPy {

// Move a SingleData object to python
template <typename T>
py::object to_python(APP::SingleData<T> &&src);

// Move an AccumData object to python
template <typename T>
py::object to_python(APP::AccumData<T> &&src);

// Move an AverageData object to python
template <typename T>
py::object to_python(APP::AverageData<T> &&src);

// Move an ListData object to python
template <typename T>
py::object to_python(APP::ListData<T> &&src);

} //end namespace AppToPy


//============================================================================
// Implementations
//============================================================================

template <typename T>
py::object AppToPy::to_python(APP::SingleData<T> &&src) {
  return AppToPy::to_python(std::move(src.value()));
}

template <typename T>
py::object AppToPy::to_python(APP::AccumData<T> &&src) {
  return AppToPy::to_python(std::move(src.value()));
}

template <typename T>
py::object AppToPy::to_python(APP::AverageData<T> &&src) {
  return AppToPy::to_python(std::move(src.value()));
}

template <typename T>
py::object AppToPy::to_python(APP::ListData<T> &&src) {
  return AppToPy::to_python(std::move(src.value()));
}

#endif
