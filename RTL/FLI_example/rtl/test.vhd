LIBRARY ieee, work;
USE ieee.std_logic_1164.ALL;
USE work.test_pkg.ALL;

ENTITY Testbench IS
END Testbench;

ARCHITECTURE Behavioral OF Testbench IS
  SIGNAL int_signal : INTEGER := 0;
BEGIN
  -- Process to modify integer signal
  int_process : PROCESS
  BEGIN
    FOR i IN 0 TO 10 LOOP
      int_signal <= i;
      WAIT FOR 10 ns; -- Adjust timing as needed
    END LOOP;
    WAIT;
  END PROCESS;
  -- Call the foreign C++ function with the integer signal value
  call_pass_integer_to_python : PROCESS (int_signal)
  BEGIN
    print_param(int_signal);
  END PROCESS;
END Behavioral;