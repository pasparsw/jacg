cmake_minimum_required(VERSION 3.28)
project(Jacg)

find_package(Python3 REQUIRED COMPONENTS Interpreter)

set(REQUIREMENTS_PATH ${CMAKE_CURRENT_SOURCE_DIR}/requirements.txt)
set(VENV_DIR ${CMAKE_CURRENT_SOURCE_DIR}/venv)

if(NOT EXISTS VENV_DIR)
    if(NOT EXISTS ${REQUIREMENTS_PATH})
        message(FATAL_ERROR "Requirements file not found in ${REQUIREMENTS_PATH}")
    endif()

    execute_process(
        COMMAND ${Python3_EXECUTABLE} -m venv ${VENV_DIR}
        RESULT_VARIABLE venv_creation_ret_code
    )

    if(venv_creation_ret_code)
        message(FATAL_ERROR "Failed to create virtual environment in ${VENV_DIR}!")
    endif()

    execute_process(
        COMMAND ${VENV_DIR}/bin/pip install -r ${REQUIREMENTS_PATH}
        RESULT_VARIABLE pip_install_ret_code
    )

    if(pip_install_ret_code)
        message(FATAL_ERROR "Failed to install dependencies from ${REQUIREMENTS_PATH}!")
    endif()
endif()

message(STATUS "Virtual environment setup done at ${VENV_DIR} with dependencies from ${REQUIREMENTS_PATH}")
