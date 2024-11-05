LIBRARY IEEE;
USE IEEE.STD_LOGIC_1164.ALL;
USE IEEE.STD_LOGIC_ARITH.ALL;
USE IEEE.STD_LOGIC_UNSIGNED.ALL;
USE ieee.MATH_REAL.ALL;
--! This package contains the functions used in the design.
PACKAGE function_pack IS

  FUNCTION real_to_integer (input_real : REAL) RETURN INTEGER;

END PACKAGE function_pack;

PACKAGE BODY function_pack IS
  -- This function converts a real number to an integer.
  -- This is the inverse mapping that is used in the MTI 
  -- that turns the integer to real based on the following
  -- formula: x / (float)(INT_MAX) * 100000;
  FUNCTION real_to_integer (input_real : REAL) RETURN INTEGER IS
    CONSTANT INT_MAX                     : real := 2147483647.0;
    VARIABLE result                      : INTEGER;
    VARIABLE temp_real                   : REAL;
  BEGIN
    temp_real := input_real / 100000.0;
    temp_real := temp_real * INT_MAX;
    result    := INTEGER(temp_real);
    RETURN result;
  END FUNCTION real_to_integer;
END PACKAGE BODY function_pack;