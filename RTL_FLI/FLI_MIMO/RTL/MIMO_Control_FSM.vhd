LIBRARY ieee, work;
USE ieee.std_logic_1164.ALL;
USE ieee.numeric_std.ALL;
USE work.data_types.ALL;
USE work.constants.ALL;
USE work.function_pack.custom_delay;

ENTITY MIMO_Control_FSM IS
  PORT (
    clk           : IN STD_LOGIC;
    rst_n         : IN STD_LOGIC;
    instr         : IN INSTRUCTION;                              --! The instruction to be executed by the crossbar
    data_in_comp  : IN int_array_ty(crossbar_rows - 1 DOWNTO 0); --! The data to be used computation, the data input comes in the form of 1D array equal to the number of rows in the crossbar (single column)
    data_in_prog  : IN int_array_ty(crossbar_cols - 1 DOWNTO 0); --! The data to be used to program the array. The input comes in the form of 1D array equal to the number of columns (single row)
    crossbar_rdy  : IN STD_LOGIC;                                --! Asserted while the crossbar is ready for a new operation. When this signal is deasserted, the crossbar can not receive a new instruction 
    reading_prog  : OUT STD_LOGIC;                               --! Asserted while programming the crossbar. During this time it expects a new column of the crossbar in every cycle
    compute_cross : OUT STD_LOGIC;                               --! Asserted while the computation is happening inside the crossbar, deasserted when it is done. During the computation time no new data should be sent to the crossbar
    valid         : OUT STD_LOGIC                                --! Asserted when the crossbar has completed the computation. It signals that the data is ready to be read
  );
END ENTITY;

ARCHITECTURE FSM OF MIMO_Control_FSM IS
  TYPE STATE_ty IS (IDLE, PROG, COMP, DONE_ST, WAIT_RDY);
  SIGNAL state, state_reg, last_state       : STATE_ty;
  SIGNAL counter                            : INTEGER;
  SIGNAL assembled_prog, assembled_prog_reg : int_2d_array_ty(crossbar_rows - 1 DOWNTO 0, crossbar_cols - 1 DOWNTO 0); -- This signal is used when we want to program the crossbar
  SIGNAL assembled_comp, assembled_comp_reg : int_array_ty(crossbar_rows - 1 DOWNTO 0);                                -- This signal is used when we want to perform a computation
  SIGNAL row_counter                        : INTEGER;
  SIGNAL data_assebled                      : STD_LOGIC;
  SIGNAL compute_done                       : STD_LOGIC;

BEGIN
  -- This process interfaces with the digital part.
  -- It reads and assembles the data to be send to the crossbar
  -- and sets the correct signals.
  P_reg : PROCESS (clk, rst_n)
  BEGIN
    IF rst_n = '0' THEN
      assembled_prog_reg <= (OTHERS => (OTHERS => 0));
      assembled_comp_reg <= (OTHERS => 0);
      state_reg          <= IDLE;
      last_state         <= IDLE;
    ELSIF rising_edge(clk) THEN
      assembled_comp_reg <= assembled_comp;
      assembled_prog_reg <= assembled_prog;
      state_reg          <= state;
      last_state         <= state_reg;
    END IF;
  END PROCESS;

  P_count : PROCESS (clk, rst_n)
  BEGIN
    IF rst_n = '0' THEN
      row_counter <= 0;
    ELSIF rising_edge(clk) THEN
      -- Row counter is used to count the number of rows
      -- assembled during the programming phase
      IF state_reg = PROG THEN
        row_counter <= row_counter + 1;
      ELSE -- row counter 0 to any other state
        row_counter <= 0;
      END IF;
    END IF;
  END PROCESS;

  P_state : PROCESS (ALL)
  BEGIN
    state <= state_reg;
    CASE state_reg IS
      WHEN IDLE =>
        IF instr = PROGRAM THEN
          state <= PROG;
        ELSIF instr = COMPUTE THEN
          state <= PROG;
        END IF;

      WHEN PROG =>
        IF data_assebled = '1' THEN
          state <= IDLE;
        END IF;

      WHEN COMP =>
        IF compute_done = '1' THEN
          state <= IDLE;
        END IF;

      WHEN OTHERS =>
        state <= IDLE;
    END CASE;
  END PROCESS;

  --! This process compiles the computation array and programs the crossbar
  P_prog : PROCESS (ALL)
  BEGIN
    IF (state_reg = PROG) THEN
      assembled_prog <= assembled_prog_reg;
      reading_prog   <= '1';
      -- Build a single row of the crossbar.
      FOR i IN crossbar_cols - 1 DOWNTO 0 LOOP
        assembled_prog (row_counter, i) <= data_in_prog(i);
      END LOOP;
      -- Wait until all rows have been assembled
      IF (row_counter = crossbar_rows - 1) THEN
        IF (prog_delay > 0 ns) THEN -- delay to program the crossbar
          data_assebled <= custom_delay(prog_delay);
        ELSE -- If the delay is negative, we do not need to wait (i.e. the crossbar can program the data in every clock cycle)
          data_assebled <= '1';
        END IF;
      END IF;
    ELSE
      data_assebled  <= '0';
      reading_prog   <= '0';
      assembled_prog <= (OTHERS => (OTHERS => 0));
    END IF;
  END PROCESS;

  --! This process send the data for computation to the crossbar and performs the matrix-vector multiplication
  P_comp : PROCESS (ALL)
  BEGIN
    valid          <= '0';
    compute_cross  <= '0';
    assembled_comp <= (OTHERS => 0);
    IF (state = COMP) THEN
      assembled_comp <= data_in_comp;
      compute_cross  <= '1';
      IF (comp_delay > 0 ns) THEN
        compute_done <= custom_delay(comp_delay);
      ELSE
        compute_done <= '1';
      END IF;
    END IF;
  END PROCESS;

END ARCHITECTURE;