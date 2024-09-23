class VHDLFunction:
    def __init__(self, name):
        self.name = name
        self.parameters = []  # List of tuples (name, data_type)
        self.return_type = None
        self.body = []  # Lines of code in the function body
        self.code_definition = ""  # Function declaration/signature
        self.code_body = ""  # Function implementation/body

    def add_parameter(self, name, data_type):
        """Add an input/output parameter to the function."""
        self.parameters.append((name, data_type))
        self._update_code()

    def set_return_type(self, data_type):
        """Set the return type of the function."""
        self.return_type = data_type
        self._update_code()

    def add_code_line(self, code):
        """Add a line of code to the function body."""
        self.body.append(code)
        self._update_code()

    def _update_code(self):
        """Update the function declaration (code_definition) and body (code_body)."""
        param_str = '; '.join([f"{name}: {data_type}" for name, data_type in self.parameters])
        return_type_str = f" return {self.return_type}" if self.return_type else ""

        # Construct the function header (declaration)
        self.code_definition = f"function {self.name}({param_str}){return_type_str};"

        # Construct the function body
        function_body = f"function {self.name}({param_str}){return_type_str} is\n"
        function_body += "begin\n"
        for line in self.body:
            function_body += f"    {line}\n"
        function_body += "end function;\n"

        self.code_body = function_body

    def __str__(self):
        """Return the full function body for debugging or printing."""
        return self.code_body

class VHDLPackage:
    def __init__(self, package_name):
        self.package_name = package_name
        self.library_declarations = []  # Holds library declarations like "LIBRARY IEEE;"
        self.use_clauses = []  # Holds specific package usage like "USE IEEE.std_logic_1164.ALL;"
        self.constants = []
        self.data_types = []
        self.functions_definitions = []  # Function signatures for the package
        self.code = ""  # Full package code

    def add_library(self, library_name):
        """Add a library declaration."""
        self.library_declarations.append(f"LIBRARY {library_name};")

    def add_use_clause(self, use_clause):
        """Add a use clause for a specific library."""
        self.use_clauses.append(f"USE {use_clause};")

    def add_constant(self, name, value, data_type):
        """Add a constant with a specific type."""
        constant_str = f"constant {name}: {data_type} := {value};"
        self.constants.append(constant_str)
        self._update_code()

    def add_data_type(self, custom_type):
        """Add a custom data type."""
        self.data_types.append(custom_type)
        self._update_code()

    def add_function_definition(self, function_definition):
        """Add the function definition (signature) to the package."""
        self.functions_definitions.append(function_definition)
        self._update_code()

    def _update_code(self):
        """Update the VHDL package code."""
        package_str = ""
        # Add libraries
        for lib in self.library_declarations:
            package_str += f"{lib}\n"
        package_str += "\n"

        for use in self.use_clauses:
            package_str += f"{use}\n"
        package_str += "\n"
        # Create the VHDL package header
        package_str += f"package {self.package_name} is\n\n"
        
        # Add constants
        for const in self.constants:
            package_str += f"{const}\n"
        package_str += "\n"
        
        # Add custom data types
        for dtype in self.data_types:
            package_str += f"{dtype}\n"
        package_str += "\n"
        
        # Add function definitions (signatures only)
        for function_def in self.functions_definitions:
            package_str += f"{function_def}\n"
        
        # End the package
        package_str += f"end package {self.package_name};"

        # Update the code attribute
        self.code = package_str

    def __str__(self):
        """Return the VHDL package as a string."""
        return self.code

class VHDLPackageBody:
    def __init__(self, package_name):
        self.package_name = package_name
        self.function_bodies = []  # Function bodies for the package body
        self.code = ""  # Full package body code

    def add_function_body(self, function_body):
        """Add the function body to the package body."""
        self.function_bodies.append(function_body)
        self._update_code()

    def _update_code(self):
        """Update the VHDL package body code."""
        # Create the VHDL package body header
        package_body_str = f"package body {self.package_name} is\n\n"
        
        # Add function bodies
        for function_body in self.function_bodies:
            package_body_str += f"{function_body}\n"
        
        # End the package body
        package_body_str += f"end package body {self.package_name};"

        # Update the code attribute
        self.code = package_body_str

    def __str__(self):
        """Return the VHDL package body as a string."""
        return self.code


class VHDLCodeGen:
    def __init__(self):
        self.code = ""  # To hold the complete VHDL code

    def add_package(self, vhdl_package):
        """Add the generated VHDL package code."""
        self.code += vhdl_package.code
        self.code += "\n\n"  # Separate different packages by two new lines

    def add_package_body(self, vhdl_package_body):
        """Add the generated VHDL package body code."""
        if vhdl_package_body.code.strip():  # Only add if there is a body
            self.code += vhdl_package_body.code
            self.code += "\n\n"

    def write_to_file(self, filename):
        """Write the VHDL code to a file."""
        with open(filename, 'w') as file:
            file.write(self.code)

    def __str__(self):
        """Return the complete VHDL code as a string."""
        return self.code

def example():
    # Example Usage
    # Create a VHDL package
    pkg = VHDLPackage("MyPackage")

    # Add libraries
    pkg.add_library("IEEE")
    pkg.add_use_clause("IEEE.std_logic_1164.ALL")
    pkg.add_use_clause("IEEE.std_logic_arith.ALL")

    # Add constants
    pkg.add_constant("MY_CONSTANT", "10", "integer")

    # Add custom data types
    pkg.add_data_type("type my_type is array (0 to 7) of std_logic;")

    # Create a function
    func = VHDLFunction("my_function")
    func.add_parameter("a", "std_logic")
    func.add_parameter("b", "integer")
    func.set_return_type("std_logic")
    func.add_code_line("if a = '1' then")
    func.add_code_line("return '0';")
    func.add_code_line("else")
    func.add_code_line("return '1';")
    func.add_code_line("end if;")

    # Add the function signature (declaration) to the package
    pkg.add_function_definition(func.code_definition)

    # Create a VHDL package body
    pkg_body = VHDLPackageBody("MyPackage")

    # Add the function body to the package body
    pkg_body.add_function_body(func.code_body)

    # Create the VHDL code generator
    code_gen = VHDLCodeGen()

    # Add the package to the VHDL code generator
    code_gen.add_package(pkg)

    # Add the package body (if functions are defined)
    code_gen.add_package_body(pkg_body)

    # Print the generated VHDL code
    print(code_gen)

    # Write the package and body to a VHDL file
    code_gen.write_to_file("mypackage.vhd")
