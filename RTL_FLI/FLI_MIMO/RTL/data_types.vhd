LIBRARY ieee, work;
USE ieee.std_logic_1164.ALL;
USE ieee.math_real.ALL;

PACKAGE data_types IS
  TYPE int_array_ty IS ARRAY (NATURAL RANGE <>) OF INTEGER;
  TYPE real_array_ty IS ARRAY(NATURAL RANGE <>) OF real;
  TYPE int_2d_array_ty IS ARRAY (NATURAL RANGE <>, NATURAL RANGE <>) OF INTEGER;
END PACKAGE;