# JSON API client generator

Table of contents:

[What is it?](#what_is_it)<br>
[How to use it?](#how_to_use_it)<br>
&emsp;[As a standalone repo](#as_a_standalone_repo)<br>
&emsp;[Integrating with CMake project](#integrating_woth_cmake_project)<br>
[API specification](#api_specification)<br>

## <a name="what_is_it"></a>What is it?

JACG (JSON API Client Generator) is a Python tool designed to save developers time when integrating JSON-based APIs into their Python applications. With JACG, you can effortlessly generate all the boilerplate code needed for clean architecture and proper abstraction layers, allowing you to focus on building your application logic. That boilerplate code includes:

* Python dataclasses reflecting API request structures
* Python dataclasses reflecting API response structures
* serialization code converting Python dataclasses to API request dictionaries
* deserialization code converting API response dictionaries into Python dataclasses
* API client class providing convenient methods to call all API commands

JACG generates all that code for you basing on the API specification and exposes a Python interface for interacting with the remote API:

<p align="center">
  <img src="https://github.com/pasparsw/jacg/blob/main/doc/general_idea.jpg" />
</p>

Target application uses that generated code to implement the business logic:

<p align="center">
  <img src="https://github.com/pasparsw/jacg/blob/main/doc/general_concept.jpg" />
</p>

The generated code is organized in the following way:

* _output_dir/api_client_ - main class containing Python interface for accessing all the available API commands
* _output_dir/enums_ - enums used in the requests/responses
* _output_dir/request_serializers_ - classes responsible for converting request dataclasses into dictionaries used by the API
* _output_dir/response_deserializers_ - classes responsible for converting response dictionaries into Python dataclasses
* _output_dir/structs_ - dataclasses used in the requests/responses

<p align="center">
  <img src="https://github.com/pasparsw/jacg/blob/main/doc/generated_api_client_design.jpg" />
</p>

> __Note:__ schema validator is not implemented yet.

## <a name="how_to_use_it"></a>How to use it?

### <a name="as_a_standalone_repo"></a>As a standalone repo

Clone this repository and run the installation script:

```bash
./scripts/instal.sh
```

After that, run JACG with the following options:

```bash
./scripts/run_jacg.sh run -spec <path_to_api_specificaition> -output <output_directory>
```

Where:
* `-spec`: path to the API specification JSON file
* `-output`: path to the directory where the generated code will be saved (ensure this directory is included in your Python paths)

Opionally, you can add `-log_level_` option to specify the logging level during the code generation. Now you can start using the generated code as shown in the example.

### <a name="integrating_woth_cmake_project"></a>Integrating with CMake project

If the application you're writing is just a part of a bigger project configured with CMake, you can easily integrate JACG using `FetchContent` and generate the code during the configuration stage.

```cmake
include(FetchContent)

FetchContent_Declare(
    Jacg
    GIT_REPOSITORY git@github.com:pasparsw/jacg.git
    GIT_TAG <version_tag>
)

FetchContent_MakeAvailable(Jacg)

set(GENERATE_XTB_API_CLIENT ${Jacg_SOURCE_DIR}/scripts/run_jacg.sh run
                            -spec /path/to/api/spec.json
                            -output /path/to/output/directory)

execute_process(
    COMMAND ${GENERATE_XTB_API_CLIENT}
    RESULT_VARIABLE generation_ret_code
)
```

## <a name="api_specification"></a>API specification

JSON file with the API specification must have the following schema:

```json
{
    "api_name": "ApiName",
    "hostname": "some.hostname.com",
    "port": 1234,
    "response_buffer_size": 1024,
    "timeout": 5,
    "ssl": true,
    "commands": {
        "CommandName": {
            "request": {
                "field_name": "field_type"
                ...
            },
            "response": {
                "field_name": "field_type"
                ...
            },
            "silent": false
        },
        ...
    },
    "enums": {
        "EnumName": {
            "field_name": field_value,
        },
        ...
    },
    "structs": {
        "StructName": {
            "field_name": "field_type",
            ...
        },
        ...
    }
}
```

* _api_name_ - is used in the name of the generated API client class
* _hostname_ - API hostname
* _port_ - API port number
* _response_buffer_size_ - size of the incoming data buffer
* _timeout_ - timeout in seconds for the API response to be received
* _ssl_ - if set to true, SSL will be used during the communication
* _commands_ - dictionary where keys are command names and values are dictionaries specifying:
  * request structure
  * response structure
  * _silent_ - if the request or response contains any secret data, you can set this field to _true_ to disable logging of the request/response payload when calling that specific command
* _enums_ - dictionary where keys are enum names and values are definitions of the enums used in the requests/responses
* _structs_ - dictionary where key are struct names and values are definitions of the structs used in the requests/responses

For more details, check the _example_ folder to see the implementation of the example API specification and application using the generated code (generate it by running `./scripts/run_example.sh`)
