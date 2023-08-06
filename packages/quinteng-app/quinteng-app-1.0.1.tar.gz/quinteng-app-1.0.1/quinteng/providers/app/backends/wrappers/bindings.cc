#include <iostream>

#ifdef APP_MPI
#include <mpi.h>
#endif

#include "misc/warnings.hpp"
DISABLE_WARNING_PUSH
#include <pybind11/pybind11.h>
DISABLE_WARNING_POP
#if defined(_MSC_VER)
    #undef snprintf
#endif

#include "framework/matrix.hpp"
#include "framework/python_parser.hpp"
#include "framework/pybind_casts.hpp"
#include "framework/types.hpp"
#include "framework/results/pybind_result.hpp"

#include "controllers/app_controller.hpp"
#include "controllers/controller_execute.hpp"

template<typename T>
class ControllerExecutor {
public:
    ControllerExecutor() = default;
    py::object operator()(const py::handle &qobj) {
#ifdef TEST_JSON // Convert input qobj to json to test standalone data reading
        return AppToPy::to_python(APP::controller_execute<T>(json_t(qobj)));
#else
        return AppToPy::to_python(APP::controller_execute<T>(qobj));
#endif
    }
};

PYBIND11_MODULE(controller_wrappers, m) {

#ifdef APP_MPI
  int prov;
  MPI_Init_thread(nullptr,nullptr,MPI_THREAD_MULTIPLE,&prov);
#endif

    py::class_<ControllerExecutor<APP::Controller> > app_ctrl (m, "app_controller_execute");
    app_ctrl.def(py::init<>());
    app_ctrl.def("__call__", &ControllerExecutor<APP::Controller>::operator());
    app_ctrl.def("__reduce__", [app_ctrl](const ControllerExecutor<APP::Controller> &self) {
        return py::make_tuple(app_ctrl, py::tuple());
    });
}
