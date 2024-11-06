LIBRARY IEEE;

USE IEEE.std_logic_1164.ALL;
USE IEEE.math_real.ALL;

package device_config_pkg is

constant device_type: string := "ferro";
constant device_states: integer := 400;
constant dt: time := 0.0000002000 sec;
constant duty_cycle: real := 0.5;


end package device_config_pkg;

