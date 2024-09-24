LIBRARY ieee, work;
USE ieee.std_logic_1164.ALL;
USE work.data_types.ALL;
USE work.constants.ALL;

ENTITY front_end_mem IS
  PORT (
    clk         : IN STD_LOGIC;
    rst_n       : IN STD_LOGIC;
    reset       : IN STD_LOGIC;
    instruction : IN INSTRUCTION;
    DATA_IN     : IN STD_LOGIC_VECTOR(BITWIDTH - 1 DOWNTO 0);
    DATA_OUT    : OUT STD_LOGIC_VECTOR(BITWIDTH - 1 DOWNTO 0);
    ready       : OUT STD_LOGIC
  );
END ENTITY;

ARCHITECTURE sim OF front_end_mem IS

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

  -- TODO An output should be added (signed) and the real value output should be translated to int and then signed. The input is computed as return x / (float)(INT_MAX) * 100000; so the reversed should be used to go for real to int
END sim;