# Example Tcl script for QuestaSim

# Set the source file path and the file name
set source_path "C:/Users/Dimitris/Documents/github/memristor_MIMO/RTL_FLI/FLI_example_array/src_c/make"
set file_name "array_signal.dll"
set top_name "work.top_array"

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