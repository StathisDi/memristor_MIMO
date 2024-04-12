PACKAGE test_pkg IS
  PROCEDURE incr_py(vhdl_integer : IN INTEGER; out_int : OUT INTEGER);
  -- Foreign function declaration (to be linked with C++ function)
  ATTRIBUTE foreign OF incr_py : PROCEDURE IS "incr_py incr_py.dll";
END PACKAGE;

PACKAGE BODY test_pkg IS
  PROCEDURE incr_py (vhdl_integer : IN INTEGER; out_int : OUT INTEGER) IS
  BEGIN
    REPORT "Error";
  END PROCEDURE;
END PACKAGE BODY;