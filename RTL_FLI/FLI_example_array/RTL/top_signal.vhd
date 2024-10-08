ENTITY c_comp IS
END c_comp;

ARCHITECTURE arch_c OF c_comp IS
  ATTRIBUTE foreign OF arch_c : ARCHITECTURE IS "initForeign array_signal.dll;";
BEGIN
END arch_c;

LIBRARY ieee;
USE ieee.std_logic_1164.ALL;

ENTITY top_array IS

  TYPE intarray IS ARRAY(NATURAL RANGE <>) OF INTEGER;

END top_array;

ARCHITECTURE a OF top_array IS

  SIGNAL clk, rst  : STD_LOGIC := '0';
  SIGNAL int_array : intarray(3 DOWNTO 0);
  SIGNAL ret_array : intarray(3 DOWNTO 0);

  COMPONENT c_comp
  END COMPONENT;

  FOR ALL : c_comp USE ENTITY work.c_comp(arch_c);

BEGIN

  -- Instantiate the C defined architecture
  -- This essentially generates a process specified by the C function
  inst1 : c_comp;
  clk <= NOT clk AFTER 5 ns;
  rst <= '1' AFTER 3 ns;
  P_reg : PROCESS (clk, rst)
  BEGIN
    IF rst = '0' THEN
      int_array <= (OTHERS => 0);
    ELSIF rising_edge(clk) THEN
      int_array(0) <= int_array(0) + 1;
      int_array(1) <= int_array(0) + 2;
      int_array(2) <= int_array(0) + 3;
      int_array(3) <= int_array(0) + 4;
    END IF;
  END PROCESS;
END a;