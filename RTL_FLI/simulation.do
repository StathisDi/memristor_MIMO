# Example Tcl script for QuestaSim

# Set the source file path and the file name
set source_path "C:/Users/Dimitris/Documents/github/memristor_MIMO/RTL_FLI/FLI_MIMO/make"
set file_name "MTI_frontend.dll"
set top_name "work.MIMO_TB"

# Set the full source file path
set full_source_path "${source_path}/${file_name}"

if {[file exists $file_name]} {
    puts "Old file exists, deleting: $file_name"
    file delete -force $file_name
}

# Copy the file from the source path to the current working directory
file copy -force $full_source_path .

# Check if the file exists in the current directory after copying
if {[file exists $file_name]} {
    puts "File copied successfully: $file_name"
} else {
    puts "Failed to copy the file: $file_name"
    exit 1
}

vsim -gui ${top_name} -voptargs=+acc

add wave -position end  sim:/mimo_tb/front_end_mem_inst/clk
add wave -position end  sim:/mimo_tb/front_end_mem_inst/rst_n
add wave -position end  sim:/mimo_tb/front_end_mem_inst/instr
add wave -position end  sim:/mimo_tb/front_end_mem_inst/data_in_comp
add wave -position end  sim:/mimo_tb/front_end_mem_inst/data_in_prog
add wave -position end  sim:/mimo_tb/front_end_mem_inst/data_output
add wave -position end  sim:/mimo_tb/front_end_mem_inst/reading_prog
add wave -position end  sim:/mimo_tb/front_end_mem_inst/compute_cross
add wave -position end  sim:/mimo_tb/front_end_mem_inst/valid
add wave -position end  sim:/mimo_tb/front_end_mem_inst/program
add wave -position end  sim:/mimo_tb/front_end_mem_inst/compute
add wave -position end  sim:/mimo_tb/front_end_mem_inst/crossbar_input_prog
add wave -position end  sim:/mimo_tb/front_end_mem_inst/crossbar_input_comp
add wave -position end  sim:/mimo_tb/front_end_mem_inst/crossbar_output
add wave -position end  sim:/mimo_tb/front_end_mem_inst/crossbar_rdy

run -all