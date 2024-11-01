LIBRARY ieee, work;
USE ieee.std_logic_1164.ALL;
USE ieee.numeric_std.ALL;
USE work.data_types.ALL;
USE work.constants.ALL;

--! Control FSM for the memristor MIMO system.
ENTITY MIMO_Control_FSM IS
  PORT (
    clk                : IN STD_LOGIC;
    rst_n              : IN STD_LOGIC;
    instr              : IN INSTRUCTION;                                                              --! The instruction to be executed by the crossbar
    data_in_comp       : IN int_array_ty(crossbar_rows - 1 DOWNTO 0);                                 --! The data to be used computation, the data input comes in the form of 1D array equal to the number of rows in the crossbar (single column)
    data_in_prog       : IN int_array_ty(crossbar_cols - 1 DOWNTO 0);                                 --! The data to be used to program the array. The input comes in the form of 1D array equal to the number of columns (single row)
    crossbar_rdy       : IN STD_LOGIC;                                                                --! Asserted while the crossbar is ready for a new operation. When this signal is deasserted, the crossbar can not receive a new instruction 
    cross_compute_data : OUT int_array_ty(crossbar_rows - 1 DOWNTO 0);                                --! Data send to the crossbar for computation
    cross_program_data : OUT int_2d_array_ty(crossbar_rows - 1 DOWNTO 0, crossbar_cols - 1 DOWNTO 0); --! Data send to the crossbar for programming
    reading_prog       : OUT STD_LOGIC;                                                               --! Asserted while programming the crossbar. During this time it expects a new column of the crossbar in every cycle
    compute_cross      : OUT STD_LOGIC;                                                               --! Asserted while the computation is happening inside the crossbar, deasserted when it is done. During the computation time no new data should be sent to the crossbar
    program            : OUT STD_LOGIC;                                                               --! control signal to program the crossbar
    compute            : OUT STD_LOGIC;                                                               --! Control signal to compute using the crossbar
    valid              : OUT STD_LOGIC                                                                --! Asserted when the crossbar has completed the computation. It signals that the data is ready to be read
  );
END ENTITY;

--! This control FSM is used to program the crossbar and perform the computation.
--! It emulates the timing of the crossbar in terms of the delay needed to program or compute using the crossbar.
ARCHITECTURE FSM OF MIMO_Control_FSM IS
  TYPE STATE_ty IS (IDLE, PROG, COMP, DONE_ST, WAIT_RDY);
  SIGNAL state, state_reg, last_state       : STATE_ty;
  SIGNAL counter                            : INTEGER;
  SIGNAL assembled_prog, assembled_prog_reg : int_2d_array_ty(crossbar_rows - 1 DOWNTO 0, crossbar_cols - 1 DOWNTO 0); -- This signal is used when we want to program the crossbar
  SIGNAL assembled_comp, assembled_comp_reg : int_array_ty(crossbar_rows - 1 DOWNTO 0);                                -- This signal is used when we want to perform a computation
  SIGNAL row_counter                        : INTEGER;
  SIGNAL data_assebled                      : STD_LOGIC;
  SIGNAL compute_done                       : STD_LOGIC;
  SIGNAL start_comp_delay, cont_comp        : STD_LOGIC;
  SIGNAL start_prog_delay, cont_prog        : STD_LOGIC;
  SIGNAL count_en                           : STD_LOGIC;

BEGIN
  program            <= data_assebled;
  cross_compute_data <= assembled_comp_reg;
  -- This process interfaces with the digital part.
  -- It reads and assembles the data to be send to the crossbar
  -- and sets the correct signals.
  P_reg : PROCESS (clk, rst_n)
  BEGIN
    IF rst_n = '0' THEN
      compute            <= '0';
      assembled_prog_reg <= (OTHERS => (OTHERS => 0));
      assembled_comp_reg <= (OTHERS => 0);
      state_reg          <= IDLE;
      last_state         <= IDLE;
      valid              <= '0';
    ELSIF rising_edge(clk) THEN
      assembled_comp_reg <= assembled_comp;
      assembled_prog_reg <= assembled_prog;
      state_reg          <= state;
      valid              <= compute_done;
      compute            <= compute_done;
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
      IF state = PROG THEN
        IF count_en = '1' THEN
          row_counter <= row_counter + 1;
        END IF;
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
        IF instr = PROGRAM_INST THEN
          state <= PROG;
        ELSIF instr = COMPUTE_INST THEN
          REPORT "Entering COMPUTE state.";
          state <= COMP;
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
    start_prog_delay   <= '0';
    data_assebled      <= '0';
    count_en           <= '0';
    cross_program_data <= (OTHERS => (OTHERS => 0));
    IF (state_reg = PROG) THEN
      assembled_prog <= assembled_prog_reg;
      reading_prog   <= '1';
      -- Wait until all rows have been assembled
      IF (row_counter >= crossbar_rows) THEN
        REPORT "All rows have been assembled. Programming the crossbar.";
        IF (cont_prog = '1') THEN -- delay to program the crossbar
          REPORT "Programming delay completed.";
          -- Send the data out to the crossbar
          cross_program_data <= assembled_prog_reg;
          data_assebled      <= '1';
          start_prog_delay   <= '0';
        ELSE -- If the delay is negative, we do not need to wait (i.e. the crossbar can program the data in every clock cycle)
          REPORT "Programming delay not completed.";
          data_assebled    <= '0';
          start_prog_delay <= '1';
        END IF;
      ELSE
        count_en <= '1';
        -- If not all rows have been assembled then keep building
        -- Build a single row of the crossbar.
        REPORT "Assembling row: " & INTEGER'image(row_counter);
        cross_program_data <= (OTHERS => (OTHERS => 0));
        FOR i IN crossbar_cols - 1 DOWNTO 0 LOOP
          assembled_prog (row_counter, i) <= data_in_prog(i);
        END LOOP;
      END IF;
    ELSE
      cross_program_data <= (OTHERS => (OTHERS => 0));
      data_assebled      <= '0';
      reading_prog       <= '0';
      assembled_prog     <= (OTHERS => (OTHERS => 0));
    END IF;
  END PROCESS;

  P_prog_delay : PROCESS
  BEGIN
    cont_prog <= '0';
    WAIT UNTIL start_prog_delay = '1';
    IF (prog_delay > 0 ns) THEN
      WAIT FOR prog_delay;
    END IF;
    WAIT UNTIL rising_edge(clk); -- Sync with the clock
    cont_prog <= '1';            -- Keep active for 1 clk
    WAIT UNTIL rising_edge(clk);
  END PROCESS;

  P_comp_delay : PROCESS
  BEGIN
    cont_comp <= '0';
    WAIT UNTIL start_comp_delay = '1';
    IF (comp_delay > 0 ns) THEN
      WAIT FOR comp_delay;
    END IF;
    WAIT UNTIL rising_edge(clk); -- Sync with the clock
    cont_comp <= '1';            -- Keep active for 1 clk
    WAIT UNTIL rising_edge(clk);
  END PROCESS;

  --! This process send the data for computation to the crossbar and performs the matrix-vector multiplication
  P_comp : PROCESS (ALL)
  BEGIN
    compute_cross    <= '0';
    assembled_comp   <= (OTHERS => 0);
    start_comp_delay <= '0';
    compute_done     <= '0';
    IF (state_reg = COMP) THEN
      compute_cross <= '1';
      IF cont_comp = '1' THEN
        assembled_comp   <= data_in_comp;
        compute_done     <= '1';
        start_comp_delay <= '0';
      ELSE
        compute_done     <= '0';
        start_comp_delay <= '1';
      END IF;
    END IF;
  END PROCESS;

END ARCHITECTURE;