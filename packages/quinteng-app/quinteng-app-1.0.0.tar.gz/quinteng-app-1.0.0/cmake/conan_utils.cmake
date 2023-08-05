include(conan)

macro(_rename_conan_lib package)
    add_library(APP_DEPENDENCY_PKG::${package} INTERFACE IMPORTED)
    target_link_libraries(APP_DEPENDENCY_PKG::${package} PUBLIC INTERFACE CONAN_PKG::${package})
endmacro()

macro(setup_conan)

    # Right now every dependency shall be static
    set(CONAN_OPTIONS ${CONAN_OPTIONS} "*:shared=False")

    set(REQUIREMENTS nlohmann_json/3.1.1 spdlog/1.5.0)
    list(APPEND APP_CONAN_LIBS nlohmann_json spdlog)
    if(APPLE AND CMAKE_CXX_COMPILER_ID MATCHES "Clang")
        set(REQUIREMENTS ${REQUIREMENTS} llvm-openmp/12.0.1)
        list(APPEND APP_CONAN_LIBS llvm-openmp)
        if(SKBUILD)
            set(CONAN_OPTIONS ${CONAN_OPTIONS} "llvm-openmp:shared=True")
        endif()
    endif()

    if(SKBUILD)
        set(REQUIREMENTS ${REQUIREMENTS} muparserx/4.0.8)
        list(APPEND APP_CONAN_LIBS muparserx)
        if(NOT MSVC)
            set(CONAN_OPTIONS ${CONAN_OPTIONS} "muparserx:fPIC=True")
        endif()
    endif()

    if(APP_THRUST_BACKEND AND NOT APP_THRUST_BACKEND STREQUAL "CUDA")
        set(REQUIREMENTS ${REQUIREMENTS} thrust/1.9.5)
        list(APPEND APP_CONAN_LIBS thrust)
        string(TOLOWER ${APP_THRUST_BACKEND} THRUST_BACKEND)
        set(CONAN_OPTIONS ${CONAN_OPTIONS} "thrust:device_system=${THRUST_BACKEND}")
        if(THRUST_BACKEND MATCHES "tbb")
            list(APPEND APP_CONAN_LIBS tbb)
        endif()
    endif()

    if(BUILD_TESTS)
        set(REQUIREMENTS ${REQUIREMENTS} catch2/2.13.6)
        list(APPEND APP_CONAN_LIBS catch2)
    endif()

    conan_cmake_run(REQUIRES ${REQUIREMENTS}
                    OPTIONS ${CONAN_OPTIONS}
                    ENV CONAN_CMAKE_PROGRAM=${CMAKE_COMMAND}
                    BASIC_SETUP
                    CMAKE_TARGETS
                    KEEP_RPATHS
                    BUILD missing)

    # Headers includes
    if(APP_THRUST_BACKEND AND NOT APP_THRUST_BACKEND STREQUAL "CUDA")
        set(APP_SIMULATOR_CPP_EXTERNAL_LIBS ${APP_SIMULATOR_CPP_EXTERNAL_LIBS} ${CONAN_INCLUDE_DIRS_THRUST})
    endif()

    # Reassign targets from CONAN_PKG to APP_DEPENDENCY_PKG
    foreach(CONAN_LIB ${APP_CONAN_LIBS})
        _rename_conan_lib(${CONAN_LIB})
    endforeach()

    if(APPLE)
        set(OPENMP_FOUND TRUE)
        if(NOT SKBUILD)
            set(APP_LIBRARIES ${APP_LIBRARIES} APP_DEPENDENCY_PKG::llvm-openmp)
        else()
            set(CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} ${CONAN_CXX_FLAGS_LLVM-OPENMP}")
            set(APP_SIMULATOR_CPP_EXTERNAL_LIBS ${APP_SIMULATOR_CPP_EXTERNAL_LIBS} ${CONAN_INCLUDE_DIRS_LLVM-OPENMP})
            set(BACKEND_REDIST_DEPS ${BACKEND_REDIST_DEPS} "${CONAN_LIB_DIRS_LLVM-OPENMP}/libomp.dylib")
        endif()
    endif()
endmacro()
