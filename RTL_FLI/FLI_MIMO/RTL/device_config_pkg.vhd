LIBRARY IEEE;

USE IEEE.std_logic_1164.ALL;
USE IEEE.math_real.ALL;

PACKAGE device_config_pkg IS

  CONSTANT device_type   : STRING  := "ideal";
  CONSTANT device_states : INTEGER := 50;
  CONSTANT dt            : TIME    := 0.0020000000 sec;
  CONSTANT duty_cycle    : real    := 0.5;

END PACKAGE device_config_pkg;