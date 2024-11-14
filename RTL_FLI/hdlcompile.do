# Read or set the path to the source files'
# If the source_path variable is not set, the default path is "./"
if {![info exists source_path]} {
  set source_path "./"
}

set library_file_list {
  work {
    "/RTL/data_types.vhd"
    "/RTL/device_config_pkg.vhd"
    "/RTL/constants.vhd"
    "/RTL/function_pack.vhd"
    "/RTL/mti_front.vhd"
    "/RTL/MIMO_Control_FSM.vhd"
    "/RTL/front_end_mem.vhd"
    "/test/MIMO_Top.vhd"
    "/test/control_fsm_tb.vhd"
  }
}


foreach {library file_list} $library_file_list {
  vlib $library
  vmap work $library
  foreach file $file_list {
    echo "$source_path$file"
    if [regexp {.vhdl?$} "$source_path$file"] {
      echo "Compiling $source_path$file"
      vcom -work work -2008 -explicit -vopt -stats=none "$source_path$file"
    } else {
      vlog $file
    }
  }
}

