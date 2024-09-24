LIBRARY IEEE;

USE IEEE.std_logic_1164.ALL;
USE IEEE.math_real.ALL;

PACKAGE device_config_pkg IS

  CONSTANT device_type   : STRING  := "MF";
  CONSTANT device_states : INTEGER := 150;
  CONSTANT dt            : real    := 0.0200000000;
  CONSTANT duty_cycle    : real    := 0.5;
END PACKAGE device_config_pkg;