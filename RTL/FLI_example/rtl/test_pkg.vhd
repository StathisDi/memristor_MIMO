PACKAGE test_pkg IS
  PROCEDURE print_param(vhdl_integer : IN INTEGER);
  -- Foreign function declaration (to be linked with C++ function)
  ATTRIBUTE foreign OF print_param   : PROCEDURE IS "print_param print_param.dll";
END PACKAGE;

PACKAGE BODY test_pkg IS
  PROCEDURE print_param (vhdl_integer : IN INTEGER) IS
  BEGIN
    REPORT "Error";
  END PROCEDURE;
END PACKAGE BODY;