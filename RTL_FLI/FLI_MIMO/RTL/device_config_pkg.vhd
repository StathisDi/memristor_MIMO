LIBRARY IEEE;

USE IEEE.std_logic_1164.ALL;
USE IEEE.math_real.ALL;

package device_config_pkg is

constant device_type: string := "MF";
constant device_states: integer := 150;
constant dt: time := 0.0200000000 sec;
constant duty_cycle: real := 0.5;


end package device_config_pkg;

