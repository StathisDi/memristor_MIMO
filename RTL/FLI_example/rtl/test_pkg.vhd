PACKAGE test_pkg IS
  PROCEDURE incrementor(vhdl_integer : IN INTEGER);
  -- Foreign function declaration (to be linked with C++ function)
  ATTRIBUTE foreign OF incrementor   : PROCEDURE IS "incrementor incrementor.dll";
END PACKAGE;

PACKAGE BODY test_pkg IS
  PROCEDURE incrementor (vhdl_integer : IN INTEGER) IS
  BEGIN
    REPORT "Error";
  END PROCEDURE;
END PACKAGE BODY;