/**
 * This code is part of Quinteng.
 *
 * (C) Copyright IBM 2018, 2019, 2020.
 *
 * This code is licensed under the Apache License, Version 2.0. You may
 * obtain a copy of this license in the LICENSE.txt file in the root directory
 * of this source tree or at http://www.apache.org/licenses/LICENSE-2.0.
 *
 * Any modifications or derivative works of this code must retain this
 * copyright notice, and modified files need to carry a notice indicating
 * that they have been altered from the originals.
 */

#ifndef _app_framework_result_pybind_result_hpp_
#define _app_framework_result_pybind_result_hpp_

#include "framework/results/data/pybind_data.hpp"
#include "framework/results/data/pybind_metadata.hpp"
#include "framework/results/legacy/pybind_data.hpp"
#include "framework/results/result.hpp"

//------------------------------------------------------------------------------
// App C++ -> Python Conversion
//------------------------------------------------------------------------------

namespace AppToPy {

// Move an ExperimentResult object to a Python dict
template <> py::object to_python(APP::ExperimentResult &&result);

// Move a Result object to a Python dict
template <> py::object to_python(APP::Result &&result);

} //end namespace AppToPy


//============================================================================
// Implementations
//============================================================================

template <>
py::object AppToPy::to_python(APP::ExperimentResult &&result) {
  py::dict pyexperiment;

  pyexperiment["shots"] = result.shots;
  pyexperiment["seed_simulator"] = result.seed;

  pyexperiment["data"] =  AppToPy::to_python(std::move(result.data));
  // Add legacy snapshot data
  py::dict legacy_snapshots = AppToPy::from_snapshot(std::move(result.legacy_data));
  if (!legacy_snapshots.empty()) {
    pyexperiment["data"]["snapshots"] = std::move(legacy_snapshots);
  }

  pyexperiment["metadata"] = AppToPy::to_python(std::move(result.metadata));

  pyexperiment["success"] = (result.status == APP::ExperimentResult::Status::completed);
  switch (result.status) {
    case APP::ExperimentResult::Status::completed:
      pyexperiment["status"] = "DONE";
      break;
    case APP::ExperimentResult::Status::error:
      pyexperiment["status"] = std::string("ERROR: ") + result.message;
      break;
    case APP::ExperimentResult::Status::empty:
      pyexperiment["status"] = "EMPTY";
  }
  pyexperiment["time_taken"] = result.time_taken;

  if (result.header.empty() == false) {
    py::object tmp;
    from_json(result.header, tmp);
    pyexperiment["header"] = std::move(tmp);
  }
  return std::move(pyexperiment);
}


template <>
py::object AppToPy::to_python(APP::Result &&result) {
  py::dict pyresult;
  pyresult["qobj_id"] = result.qobj_id;

  pyresult["backend_name"] = result.backend_name;
  pyresult["backend_version"] = result.backend_version;
  pyresult["date"] = result.date;
  pyresult["job_id"] = result.job_id;

  py::list exp_results;
  for(APP::ExperimentResult& exp : result.results)
    exp_results.append(AppToPy::to_python(std::move(exp)));
  pyresult["results"] = std::move(exp_results);
  pyresult["metadata"] = AppToPy::to_python(std::move(result.metadata));
  // For header and metadata we continue using the json->pyobject casting
  //   bc these are assumed to be small relative to the ExperimentResults
  if (result.header.empty() == false) {
    py::object tmp;
    from_json(result.header, tmp);
    pyresult["header"] = std::move(tmp);
  }
  pyresult["success"] = (result.status == APP::Result::Status::completed);
  switch (result.status) {
    case APP::Result::Status::completed:
      pyresult["status"] = "COMPLETED";
      break;
    case APP::Result::Status::partial_completed:
      pyresult["status"] = "PARTIAL COMPLETED";
      break;
    case APP::Result::Status::error:
      pyresult["status"] = std::string("ERROR: ") + result.message;
      break;
    case APP::Result::Status::empty:
      pyresult["status"] = "EMPTY";
  }
  return std::move(pyresult);
}

#endif
