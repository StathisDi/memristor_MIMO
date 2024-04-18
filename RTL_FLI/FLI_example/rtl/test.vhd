LIBRARY ieee, work;
USE ieee.std_logic_1164.ALL;
USE work.test_pkg.ALL;

ENTITY Testbench IS
END Testbench;

ARCHITECTURE Behavioral OF Testbench IS
  SIGNAL int_signal : INTEGER := 0;
  SIGNAL out_sig    : INTEGER := 0;
BEGIN

  -- Process to modify integer signal
  int_process : PROCESS
  BEGIN
    FOR i IN 0 TO 10 LOOP
      int_signal <= i;
      WAIT FOR 10 ns; -- Adjust timing as needed
    END LOOP;
    WAIT FOR 10 ns;
  END PROCESS;

  -- Call the foreign C++ function with the integer signal value
  call_pass_integer_to_python : PROCESS (int_signal)
    VARIABLE out_int : INTEGER := 0;
  BEGIN
    incr_py(int_signal, out_int);
    out_sig <= out_int;
  END PROCESS;

END Behavioral;