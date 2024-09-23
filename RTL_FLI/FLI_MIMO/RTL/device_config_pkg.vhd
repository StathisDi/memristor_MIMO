LIBRARY IEEE;

USE IEEE.std_logic_1164.ALL;
USE IEEE.math_real.ALL;

PACKAGE device_config_pkg IS

  CONSTANT device_states : INTEGER := 400;
  CONSTANT dt            : real    := 0.0000002000;
  CONSTANT duty_cycle    : real    := 0.5;

END PACKAGE device_config_pkg;