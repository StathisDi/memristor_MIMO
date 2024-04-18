PACKAGE test_pkg IS
  PROCEDURE py_init(x          : IN INTEGER);
  -- Foreign function declaration (to be linked with C++ function)
  ATTRIBUTE foreign OF py_init : PROCEDURE IS "py_init py_init.dll";

  PROCEDURE py_fin(x           : IN INTEGER);
  -- Foreign function declaration (to be linked with C++ function)
  ATTRIBUTE foreign OF py_fin  : PROCEDURE IS "py_fin py_fin.dll";

  PROCEDURE incr_py(vhdl_integer : IN INTEGER; out_int : OUT INTEGER);
  -- Foreign function declaration (to be linked with C++ function)
  ATTRIBUTE foreign OF incr_py : PROCEDURE IS "incr_py incr_py.dll";
END PACKAGE;

PACKAGE BODY test_pkg IS
  PROCEDURE incr_py (vhdl_integer : IN INTEGER; out_int : OUT INTEGER) IS
  BEGIN
    REPORT "Error";
  END PROCEDURE;
  PROCEDURE py_init (x : IN INTEGER) IS
  BEGIN
    REPORT "Error";
  END PROCEDURE;
  PROCEDURE py_fin (x : IN INTEGER) IS
  BEGIN
    REPORT "Error";
  END PROCEDURE;
END PACKAGE BODY;