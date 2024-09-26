LIBRARY ieee, work;
USE ieee.std_logic_1164.ALL;
USE ieee.numeric_std.ALL;
USE work.data_types.ALL;
USE work.constants.ALL;

ENTITY MIMO_Control_FSM IS
  PORT (
    clk          : IN STD_LOGIC;
    rst_n        : IN STD_LOGIC;
    instr        : IN INSTRUCTION;
    crossbar_rdy : IN STD_LOGIC;
    program      : OUT STD_LOGIC;
    compute      : OUT STD_LOGIC;
    done         : OUT STD_LOGIC
  );
END ENTITY;

ARCHITECTURE FSM OF MIMO_Control_FSM IS
  TYPE STATE_ty IS (IDLE, PROG, COMP, DONE_ST, WAIT_RDY);
  SIGNAL state, state_reg, last_state       : STATE_ty;
  SIGNAL counter                            : INTEGER;
  SIGNAL assembled_prog, assembled_prog_reg : int_2d_array_ty(crossbar_rows - 1 DOWNTO 0, crossbar_cols - 1 DOWNTO 0); -- This signal is used when we want to program the crossbar
  SIGNAL assembled_comp, assembled_comp_reg : int_array_ty(crossbar_rows - 1 DOWNTO 0);                                -- This signal is used when we want to perform a computation
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
      counter <= 0;
    ELSIF rising_edge(clk) THEN
      -- TODO need control logic here for the counter
      counter <= counter + 1;
    END IF;
  END PROCESS;

  P_state : PROCESS (ALL)
  BEGIN
    -- TODO this should control the state
    state <= state_reg;
    CASE state_reg IS
      WHEN IDLE =>
        state <= PROG;

      WHEN PROG =>
        state <= COMP;

      WHEN OTHERS =>
        NULL;
    END CASE;
  END PROCESS;

  -- TODO This process is emulating the timing behavior of the crossbar It creates the proper delays and translates the data from signed -> int
  P_out : PROCESS (ALL)
  BEGIN
    --TODO this process should have the appropriate delays introduced
  END PROCESS;

END ARCHITECTURE;