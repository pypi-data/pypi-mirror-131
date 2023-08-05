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

#ifndef _app_framework_result_legacy_pybind_data_hpp_
#define _app_framework_result_legacy_pybind_data_hpp_

#include "framework/pybind_basics.hpp"
#include "framework/results/legacy/snapshot_data.hpp"

//------------------------------------------------------------------------------
// App C++ -> Python Conversion
//------------------------------------------------------------------------------

namespace AppToPy {

/**
 * Convert a LegacyAverageData to a python object
 * @param avg_data is an LegacyAverageData
 * @returns a py::dict
 */
template<typename T>
py::object from_avg_data(APP::LegacyAverageData<T> &&avg_data);
template<typename T>
py::object from_avg_data(APP::LegacyAverageData<T> &avg_data);

// JSON specialization
template<>
py::object from_avg_data(APP::LegacyAverageData<json_t> &&avg_data);

/**
 * Convert a LegacyAverageData to a python object
 * @param avg_data is an LegacyAverageData
 * @returns a py::dict
 */
template<typename T>
py::object from_avg_data(APP::LegacyAverageData<matrix<T>> &&avg_data);
template<typename T>
py::object from_avg_data(APP::LegacyAverageData<matrix<T>> &avg_data);


/**
 * Convert a LegacyAverageData to a python object
 * @param avg_data is an LegacyAverageData
 * @returns a py::dict
 */
template<typename T>
py::object from_avg_data(APP::LegacyAverageData<APP::Vector<T>> &&avg_data);
template<typename T>
py::object from_avg_data(APP::LegacyAverageData<APP::Vector<T>> &avg_data);

/**
 * Convert a LegacyAverageData to a python object
 * @param avg_data is an LegacyAverageData
 * @returns a py::dict
 */
template<typename T>
py::object from_avg_data(APP::LegacyAverageData<std::vector<T>> &&avg_data);
template<typename T>
py::object from_avg_data(APP::LegacyAverageData<std::vector<T>> &avg_data);

/**
 * Convert a AverageSnapshot to a python object
 * @param avg_snap is an AverageSnapshot
 * @returns a py::dict
 */
template<typename T>
py::object from_avg_snap(APP::AverageSnapshot<T> &&avg_snap);
template<typename T>
py::object from_avg_snap(APP::AverageSnapshot<T> &avg_snap);

/**
 * Convert a PershotSnapshot  to a python object
 * @param avg_snap is an PershotSnapshot 
 * @returns a py::dict
 */
template<typename T>
py::object from_pershot_snap(APP::PershotSnapshot<T> &&snap);
template<typename T>
py::object from_pershot_snap(APP::PershotSnapshot<T> &snap);

/**
 * Convert a PershotData to a python object
 * @param data is an PershotData
 * @returns a py::dict
 */
template<typename T>
py::object from_pershot_data(APP::PershotData<T> &&data);
template<typename T>
py::object from_pershot_data(APP::PershotData<T> &data);

// JSON specialization
template<>
py::object from_pershot_data(APP::PershotData<json_t> &&avg_data);

/**
 * Convert a PershotData to a python object
 * @param data is an PershotData
 * @returns a py::dict
 */
template<typename T>
py::object from_pershot_data(APP::PershotData<matrix<T>> &&data);
template<typename T>
py::object from_pershot_data(APP::PershotData<matrix<T>> &data);


/**
 * Convert a PershotData to a python object
 * @param data is an PershotData
 * @returns a py::dict
 */
template<typename T>
py::object from_pershot_data(APP::PershotData<APP::Vector<T>> &&data);
template<typename T>
py::object from_pershot_data(APP::PershotData<APP::Vector<T>> &data);

/**
 * Convert a PershotData to a python object
 * @param data is an PershotData
 * @returns a py::dict
 */
template<typename T>
py::object from_pershot_data(APP::PershotData<std::vector<T>> &&data);
template<typename T>
py::object from_pershot_data(APP::PershotData<std::vector<T>> &data);

/**
 * Convert an SnapshotData to a python object
 * @param result is an SnapshotData
 * @returns a py::dict
 */
py::dict from_snapshot(APP::SnapshotData &&result);
py::dict from_snapshot(APP::SnapshotData &result);

} //end namespace AppToPy


/*******************************************************************************
 *
 * Implementations
 *
 ******************************************************************************/

//============================================================================
// Pybind Conversion for Simulator types
//============================================================================

template<typename T> 
py::object AppToPy::from_avg_data(APP::LegacyAverageData<T> &avg_data) {
  return AppToPy::from_avg_data(std::move(avg_data));
}

template<typename T> 
py::object AppToPy::from_avg_data(APP::LegacyAverageData<T> &&avg_data) {
  py::dict d;
  d["value"] = std::move(avg_data.mean());
  if (avg_data.has_variance()) {
    d["variance"] = std::move(avg_data.variance());
  }
  return std::move(d);
}

template <> 
py::object AppToPy::from_avg_data(APP::LegacyAverageData<json_t> &&avg_data) {
  py::dict d;
  py::object py_mean;
  from_json(avg_data.mean(), py_mean);
  d["value"] = std::move(py_mean);
  if (avg_data.has_variance()) {
    py::object py_var;
    from_json(avg_data.variance(), py_var);
    d["variance"] = std::move(py_var);
  }
  return std::move(d);
}

template<typename T> 
py::object AppToPy::from_avg_data(APP::LegacyAverageData<APP::Vector<T>> &avg_data) {
  return AppToPy::from_avg_data(std::move(avg_data));
}

template<typename T> 
py::object AppToPy::from_avg_data(APP::LegacyAverageData<APP::Vector<T>> &&avg_data) {
  py::dict d;
  d["value"] = AppToPy::to_numpy(std::move(avg_data.mean()));
  if (avg_data.has_variance()) {
    d["variance"] = AppToPy::to_numpy(std::move(avg_data.variance()));
  }
  return std::move(d);
}

template<typename T> 
py::object AppToPy::from_avg_data(APP::LegacyAverageData<matrix<T>> &avg_data) {
  return AppToPy::from_avg_data(std::move(avg_data));
}

template<typename T> 
py::object AppToPy::from_avg_data(APP::LegacyAverageData<matrix<T>> &&avg_data) {
  py::dict d;
  d["value"] = AppToPy::to_numpy(std::move(avg_data.mean()));
  if (avg_data.has_variance()) {
    d["variance"] = AppToPy::to_numpy(std::move(avg_data.variance()));
  }
  return std::move(d);
}

template<typename T> 
py::object AppToPy::from_avg_data(APP::LegacyAverageData<std::vector<T>> &avg_data) {
  return AppToPy::from_avg_data(std::move(avg_data));
}

template<typename T> 
py::object AppToPy::from_avg_data(APP::LegacyAverageData<std::vector<T>> &&avg_data) {
  py::dict d;
  d["value"] = AppToPy::to_numpy(std::move(avg_data.mean()));
  if (avg_data.has_variance()) {
    d["variance"] = AppToPy::to_numpy(std::move(avg_data.variance()));
  }
  return std::move(d);
}

template<typename T> 
py::object AppToPy::from_avg_snap(APP::AverageSnapshot<T> &avg_snap) {
  return AppToPy::from_avg_snap(std::move(avg_snap));
}

template<typename T> 
py::object AppToPy::from_avg_snap(APP::AverageSnapshot<T> &&avg_snap) {
  py::dict d;
  for (auto &outer_pair : avg_snap.data()) {
    py::list d1;
    for (auto &inner_pair : outer_pair.second) {
      // Store mean and variance for snapshot
      py::dict datum = AppToPy::from_avg_data(inner_pair.second);
      // Add memory key if there are classical registers
      auto memory = inner_pair.first;
      if ( ! memory.empty()) {
        datum["memory"] = inner_pair.first;
      }
      // Add to list of output
      d1.append(std::move(datum));
    }
    d[outer_pair.first.data()] = std::move(d1);
  }
  return std::move(d);
}

template<typename T> 
py::object AppToPy::from_pershot_snap(APP::PershotSnapshot<T> &snap) {
  return AppToPy::from_pershot_snap(std::move(snap));
}
template<typename T> 
py::object AppToPy::from_pershot_snap(APP::PershotSnapshot<T> &&snap) {
  py::dict d;
  // string PershotData
  for (auto &pair : snap.data())
    d[pair.first.data()] = AppToPy::from_pershot_data(pair.second);
  return std::move(d);
}

template<typename T>
py::object AppToPy::from_pershot_data(APP::PershotData<T> &&data) {
  return py::cast(data.data(), py::return_value_policy::move);
}

template<typename T>
py::object AppToPy::from_pershot_data(APP::PershotData<T> &data) {
  return AppToPy::from_pershot_data(std::move(data));
}

template<>
py::object AppToPy::from_pershot_data(APP::PershotData<json_t> &&data) {
  py::object tmp;
  from_json(data.data(), tmp);
  return tmp;
}

template<typename T>
py::object AppToPy::from_pershot_data(APP::PershotData<matrix<T>> &&data) {
  py::list l;
  for (auto &item : data.data()) {
    l.append(AppToPy::to_numpy(std::move(item)));
  }
  return std::move(l);
}

template<typename T>
py::object AppToPy::from_pershot_data(APP::PershotData<matrix<T>> &data) {
  return AppToPy::from_pershot_data(std::move(data));
}



template<typename T>
py::object AppToPy::from_pershot_data(APP::PershotData<APP::Vector<T>> &&data) {
  py::list l;
  for (auto &item : data.data()) {
    l.append(AppToPy::to_numpy(std::move(item)));
  }
  return std::move(l);
}

template<typename T>
py::object AppToPy::from_pershot_data(APP::PershotData<APP::Vector<T>> &data) {
  return AppToPy::from_pershot_data(std::move(data));
}



template<typename T>
py::object AppToPy::from_pershot_data(APP::PershotData<std::vector<T>> &&data) {
  py::list l;
  for (auto &item : data.data()) {
    l.append(AppToPy::to_numpy(std::move(item)));
  }
  return std::move(l);
}

template<typename T>
py::object AppToPy::from_pershot_data(APP::PershotData<std::vector<T>> &data) {
  return AppToPy::from_pershot_data(std::move(data));
}


py::dict AppToPy::from_snapshot(APP::SnapshotData &datum) {
  return AppToPy::from_snapshot(std::move(datum));
}

py::dict AppToPy::from_snapshot(APP::SnapshotData &&datum) {
  py::dict snapshots;

  // Snapshot data
  if (datum.return_snapshots_) {

    // Average snapshots
    for (auto &pair : datum.average_snapshots<json_t>()) {
      snapshots[pair.first.data()] = AppToPy::from_avg_snap(pair.second);
    }
    for (auto &pair : datum.average_snapshots<std::complex<double>>()) {
      snapshots[pair.first.data()] = AppToPy::from_avg_snap(pair.second);
    }
    for (auto &pair : datum.average_snapshots<std::vector<std::complex<float>>>()) {
      snapshots[pair.first.data()] = AppToPy::from_avg_snap(pair.second);
    }
    for (auto &pair : datum.average_snapshots<std::vector<std::complex<double>>>()) {
      snapshots[pair.first.data()] = AppToPy::from_avg_snap(pair.second);
    }
    for (auto &pair : datum.average_snapshots<APP::Vector<std::complex<float>>>()) {
      snapshots[pair.first.data()] = AppToPy::from_avg_snap(pair.second);
    }
    for (auto &pair : datum.average_snapshots<APP::Vector<std::complex<double>>>()) {
      snapshots[pair.first.data()] = AppToPy::from_avg_snap(pair.second);
    }
    for (auto &pair : datum.average_snapshots<matrix<std::complex<float>>>()) {
      snapshots[pair.first.data()] = AppToPy::from_avg_snap(pair.second);
    }
    for (auto &pair : datum.average_snapshots<matrix<std::complex<double>>>()) {
      snapshots[pair.first.data()] = AppToPy::from_avg_snap(pair.second);
    }
    for (auto &pair : datum.average_snapshots<std::map<std::string, std::complex<double>>>()) {
      snapshots[pair.first.data()] = AppToPy::from_avg_snap(pair.second);
    }
    for (auto &pair : datum.average_snapshots<std::map<std::string, double>>()) {
      snapshots[pair.first.data()] = AppToPy::from_avg_snap(pair.second);
    }
    // Singleshot snapshot data
    // Note these will override the average snapshots
    // if they share the same type string
    
    for (auto &pair : datum.pershot_snapshots<json_t>()) {
      snapshots[pair.first.data()] = AppToPy::from_pershot_snap(pair.second);
    }
    for (auto &pair : datum.pershot_snapshots<std::complex<double>>()) {
      snapshots[pair.first.data()] = AppToPy::from_pershot_snap(pair.second);
    }
    for (auto &pair : datum.pershot_snapshots<std::vector<std::complex<float>>>()) {
      snapshots[pair.first.data()] = AppToPy::from_pershot_snap(pair.second);
    }
    for (auto &pair : datum.pershot_snapshots<std::vector<std::complex<double>>>()) {
      snapshots[pair.first.data()] = AppToPy::from_pershot_snap(pair.second);
    }
    for (auto &pair : datum.pershot_snapshots<APP::Vector<std::complex<float>>>()) {
      snapshots[pair.first.data()] = AppToPy::from_pershot_snap(pair.second);
    }
    for (auto &pair : datum.pershot_snapshots<APP::Vector<std::complex<double>>>()) {
      snapshots[pair.first.data()] = AppToPy::from_pershot_snap(pair.second);
    }
    for (auto &pair : datum.pershot_snapshots<matrix<std::complex<float>>>()) {
      snapshots[pair.first.data()] = AppToPy::from_pershot_snap(pair.second);
    }
    for (auto &pair : datum.pershot_snapshots<matrix<std::complex<double>>>()) {
      snapshots[pair.first.data()] = AppToPy::from_pershot_snap(pair.second);
    }
    for (auto &pair : datum.pershot_snapshots<std::map<std::string, std::complex<double>>>()) {
      snapshots[pair.first.data()] = AppToPy::from_pershot_snap(pair.second);
    }
    for (auto &pair : datum.pershot_snapshots<std::map<std::string, double>>()) {
      snapshots[pair.first.data()] = AppToPy::from_pershot_snap(pair.second);
    }
  }
  return snapshots;
}

#endif
