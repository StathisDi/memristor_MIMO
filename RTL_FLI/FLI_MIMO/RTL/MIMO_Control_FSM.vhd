LIBRARY ieee, work;
USE ieee.std_logic_1164.ALL;
USE ieee.numeric_std.ALL;
USE work.data_types.ALL;
USE work.constants.ALL;
USE work.function_pack.custom_delay;

ENTITY MIMO_Control_FSM IS
  PORT (
    clk          : IN STD_LOGIC;
    rst_n        : IN STD_LOGIC;
    instr        : IN INSTRUCTION;                              --! The instruction to be executed by the crossbar
    data_in      : IN int_array_ty(crossbar_rows - 1 DOWNTO 0); --! The data to be programmed or computed, the data input comes in the form of 1D array equal to the number of rows in the crossbar
    crossbar_rdy : IN STD_LOGIC;                                --! Asserted while the crossbar is ready for a new operation. When this signal is deasserted, the crossbar can not receive a new instruction 
    reading_prog : OUT STD_LOGIC;                               --! Asserted while programming the crossbar. During this time it expects a new column of the crossbar in every cycle
    compute      : OUT STD_LOGIC;                               --! Asserted while the computation is happening inside the crossbar, deasserted when it is done. During the computation time no new data should be sent to the crossbar
    valid        : OUT STD_LOGIC                                --! Asserted when the crossbar has completed the computation. It signals that the data is ready to be read
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
      counter     <= 0;
      row_counter <= 0;
    ELSIF rising_edge(clk) THEN
      -- TODO need control logic here for the counter
      counter <= counter + 1;
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
    VARIABLE prog_delay : TIME;
  BEGIN
    data_assebled <= '0';
    prog_delay := 500 ns; --TODO this should change to the proper delay based on the crossbar.
    IF (state_reg = PROG) THEN
      prog_delay := prog_delay - period; --! Reduce the delay that it takes to program the crossbar based on the period
      FOR i IN crossbar_rows - 1 DOWNTO 0 LOOP
        assembled_prog (row_counter, i) <= data_in(i);
      END LOOP;
      IF (row_counter = crossbar_cols - 1) THEN
        IF (prog_delay > 0 ns) THEN
          data_assebled <= custom_delay(prog_delay);
        ELSE
          data_assebled <= '1';
        END IF;
      END IF;
    END IF;
  END PROCESS;

  -- TODO This process is emulating the timing behavior of the crossbar It creates the proper delays and translates the data from signed -> int
  P_out : PROCESS (ALL)
  BEGIN
    --TODO this process should have the appropriate delays introduced
  END PROCESS;

END ARCHITECTURE;