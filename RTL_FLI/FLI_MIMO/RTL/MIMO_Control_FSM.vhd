LIBRARY ieee, work;
USE ieee.std_logic_1164.ALL;
USE ieee.numeric_std.ALL;
USE work.data_types.ALL;
USE work.constants.ALL;

ENTITY MIMO_Control_FSM IS
  PORT (
    clk                 : IN STD_LOGIC;
    rst_n               : IN STD_LOGIC;
    start               : IN STD_LOGIC; -- Start a single program and computer round
    crossbar_rdy        : IN STD_LOGIC;
    program             : OUT STD_LOGIC;
    compute             : OUT STD_LOGIC;
    done                : OUT STD_LOGIC;
    crossbar_input_prog : OUT int_2d_array_ty(crossbar_rows - 1 DOWNTO 0, crossbar_cols - 1 DOWNTO 0); -- This signal is used when we want to program the crossbar
    crossbar_input_comp : OUT int_array_ty(crossbar_rows - 1 DOWNTO 0)                                 -- This signal is used when we want to perform a computation
  );
END ENTITY;

ARCHITECTURE FSM OF MIMO_Control_FSM IS
  TYPE STATE_ty IS (IDLE, PROG, COMP, DONE_ST, WAIT_RDY); --!
  SIGNAL state, last_state : STATE_ty;
  SIGNAL counter           : INTEGER;
BEGIN

  -- This process interfaces with the digital part.
  -- It reads and assembles the data to be send to the crossbar
  -- and sets the correct signals.
  P_reg : PROCESS (clk, rst_n)
  BEGIN
    IF rst_n = '0' THEN
      program             <= '0';
      crossbar_input_prog <= (OTHERS => (OTHERS => 0));
      crossbar_input_comp <= (OTHERS => 0);
      state               <= IDLE;
      counter             <= 0;
      compute             <= '0';
      done                <= '0';
      last_state          <= IDLE;
    ELSIF rising_edge(clk) THEN
      program             <= '0';
      crossbar_input_prog <= (OTHERS => (OTHERS => 0));
      crossbar_input_comp <= (OTHERS => 0);
      compute             <= '0';
      done                <= '0';
      CASE state IS
        WHEN IDLE =>
          last_state <= IDLE;
          IF (start = '1') THEN
            state <= WAIT_RDY;
          END IF;
        WHEN PROG =>
          last_state <= PROG;
          IF (counter = crossbar_rows - 1) THEN
            program             <= '0';
            counter             <= 0;
            state               <= COMP;
            crossbar_input_prog <= (OTHERS => (OTHERS => 0));
          ELSE
            IF counter = 0 THEN
              program <= '1';
            ELSE
              program <= '0';
            END IF;
            counter             <= counter + 1;
            crossbar_input_prog <= program_val;
          END IF;
        WHEN COMP =>
          last_state          <= COMP;
          compute             <= '1';
          crossbar_input_comp <= compute_val;
          IF crossbar_rdy = '1' THEN
            state <= DONE_ST;
          END IF;
        WHEN DONE_ST =>
          state <= IDLE;
          done  <= '1';
        WHEN WAIT_RDY =>
          IF (crossbar_rdy = '1') THEN
            IF (last_state = IDLE) THEN
              state <= PROG;
            ELSIF (last_state = PROG) THEN
              state <= COMP;
            END IF;
          ELSE
            state <= WAIT_RDY;
          END IF;
        WHEN OTHERS =>
          NULL;
      END CASE;
    END IF;
  END PROCESS;

  -- TODO This process is emulating the timing behavior of the crossbar It creates the proper delays and translates the data from signed -> int
  PROCESS
  BEGIN
    --TODO this process should have the appropriate delays introduced
  END PROCESS;

END ARCHITECTURE;