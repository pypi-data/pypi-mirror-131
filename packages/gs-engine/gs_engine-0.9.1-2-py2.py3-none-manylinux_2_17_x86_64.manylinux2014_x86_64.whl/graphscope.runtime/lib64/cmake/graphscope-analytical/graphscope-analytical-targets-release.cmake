#----------------------------------------------------------------
# Generated CMake target import file for configuration "Release".
#----------------------------------------------------------------

# Commands may need to know the format version.
set(CMAKE_IMPORT_FILE_VERSION 1)

# Import target "grape_engine" for configuration "Release"
set_property(TARGET grape_engine APPEND PROPERTY IMPORTED_CONFIGURATIONS RELEASE)
set_target_properties(grape_engine PROPERTIES
  IMPORTED_LOCATION_RELEASE "${_IMPORT_PREFIX}/bin/grape_engine"
  )

list(APPEND _IMPORT_CHECK_TARGETS grape_engine )
list(APPEND _IMPORT_CHECK_FILES_FOR_grape_engine "${_IMPORT_PREFIX}/bin/grape_engine" )

# Import target "gs_proto" for configuration "Release"
set_property(TARGET gs_proto APPEND PROPERTY IMPORTED_CONFIGURATIONS RELEASE)
set_target_properties(gs_proto PROPERTIES
  IMPORTED_LOCATION_RELEASE "${_IMPORT_PREFIX}/lib/libgs_proto.so"
  IMPORTED_SONAME_RELEASE "libgs_proto.so"
  )

list(APPEND _IMPORT_CHECK_TARGETS gs_proto )
list(APPEND _IMPORT_CHECK_FILES_FOR_gs_proto "${_IMPORT_PREFIX}/lib/libgs_proto.so" )

# Commands beyond this point should not need to know the version.
set(CMAKE_IMPORT_FILE_VERSION)
