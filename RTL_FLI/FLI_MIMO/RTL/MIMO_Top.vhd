LIBRARY ieee, work;
USE ieee.std_logic_1164.ALL;
USE ieee.numeric_std.ALL;
USE work.data_types.ALL;
USE work.constants.ALL;
USE std.env.ALL;

ENTITY MIMO_TOP IS

END MIMO_TOP;

ARCHITECTURE sim OF MIMO_TOP IS

  SIGNAL clk                 : STD_LOGIC := '0';
  SIGNAL rst_n               : STD_LOGIC := '0';
  SIGNAL start               : STD_LOGIC := '0'; -- Start a single program and computer round
  SIGNAL crossbar_rdy        : STD_LOGIC;
  SIGNAL program             : STD_LOGIC;
  SIGNAL compute             : STD_LOGIC;
  SIGNAL done                : STD_LOGIC;
  SIGNAL crossbar_input_prog : int_2d_array_ty(crossbar_rows - 1 DOWNTO 0, crossbar_cols - 1 DOWNTO 0); -- This signal is used when we want to program the crossbar
  SIGNAL crossbar_input_comp : int_array_ty(crossbar_rows - 1 DOWNTO 0);                                -- This signal is used when we want to perform a computation
  SIGNAL crossbar_output     : real_array_ty(crossbar_cols - 1 DOWNTO 0);                               -- This signal is the output of the crossbar

  COMPONENT mti_front
  END COMPONENT;

  FOR ALL : mti_front USE ENTITY work.mti_front(arch_c);
BEGIN

  -- Instantiate the C defined architecture
  -- This essentially generates a process specified by the C function
  u_mti         : mti_front;

  u_control_fsm : ENTITY work.MIMO_Control_FSM
    PORT MAP(
      -- Inputs
      clk                 => clk,
      rst_n               => rst_n,
      start               => start,
      crossbar_rdy        => crossbar_rdy,
      -- Outputs
      program             => program,
      compute             => compute,
      done                => done,
      crossbar_input_prog => crossbar_input_prog,
      crossbar_input_comp => crossbar_input_comp
    );

  clk   <= NOT clk AFTER 5 ns;
  rst_n <= '1' AFTER 3 ns;
  start <= '1' AFTER 10 ns;
  P_reg : PROCESS (clk, rst_n)
  BEGIN
    IF rst_n = '0' THEN
    ELSIF rising_edge(clk) THEN
      IF (done = '1') THEN
        stop;
      END IF;
    END IF;
  END PROCESS;

END sim;