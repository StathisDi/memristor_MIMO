LIBRARY IEEE;
USE IEEE.STD_LOGIC_1164.ALL;
USE IEEE.STD_LOGIC_ARITH.ALL;
USE IEEE.STD_LOGIC_UNSIGNED.ALL;

--! This package contains the functions used in the design.
PACKAGE function_pack IS
  --! This function will pause the VHDL simulation to emulate
  --! the delay in the crossbar.
  FUNCTION custom_delay(delay_time : TIME) RETURN STD_LOGIC;
END PACKAGE function_pack;

PACKAGE BODY function_pack IS

  FUNCTION custom_delay(delay_time : TIME) RETURN STD_LOGIC IS
  BEGIN
    WAIT FOR delay_time;
    RETURN '1';
  END FUNCTION custom_delay;

END PACKAGE BODY function_pack;