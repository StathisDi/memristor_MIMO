LIBRARY ieee, work;
USE ieee.std_logic_1164.ALL;
USE work.data_types.ALL;
USE work.constants.ALL;

--! This entity combines the control FSM and the memristive crossbar.
ENTITY front_end_mem IS
  PORT (
    clk           : IN STD_LOGIC;
    rst_n         : IN STD_LOGIC;
    instr         : IN INSTRUCTION;                              --! The instruction to be executed by the crossbar (IDLE, PROGRAM, COMPUTE)
    data_in_comp  : IN int_array_ty(crossbar_rows - 1 DOWNTO 0); --! The data to be used computation, the data input comes in the form of 1D array equal to the number of rows in the crossbar (single column)
    data_in_prog  : IN int_array_ty(crossbar_cols - 1 DOWNTO 0); --! The data to be used to program the array. The input comes in the form of 1D array equal to the number of columns (single row)
    crossbar_rdy  : IN STD_LOGIC;                                --! Asserted while the crossbar is ready for a new operation. When this signal is deasserted, the crossbar can not receive a new instruction 

    reading_prog  : OUT STD_LOGIC;                               --! Asserted while programming the crossbar. During this time it expects a new column of the crossbar in every cycle
    compute_cross : OUT STD_LOGIC;                               --! Asserted while the computation is happening inside the crossbar, deasserted when it is done. During the computation time no new data should be sent to the crossbar
    valid         : OUT STD_LOGIC                                --! Asserted when the crossbar has completed the computation. It signals that the data is ready to be read
  );
END ENTITY;

--! The design is meant to emulate the memristor crossbar and its digital front end.
--! It emulates the timing required to program the crossbar and perform the computation.
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
    --------------------------------------------------------------------------------
    -- Inptus:
    --    * inst->clk_id = mti_FindSignal("/../clk");
    --    * inst->rst_id = mti_FindSignal("/../rst_n");
    --    * inst->program_id = mti_FindSignal("/../program");
    --    * inst->compute_id = mti_FindSignal("/../compute");
    --    * inst->crossbar_input_prog_id = mti_FindSignal("/../crossbar_input_prog");
    --    * inst->crossbar_input_comp_id = mti_FindSignal("/../crossbar_input_comp");
    -- Outputs:
    --    * inst->crossbar_rdy_id    = mti_FindSignal("/../crossbar_rdy");
    --    * inst->crossbar_output_id = mti_FindSignal("/../crossbar_output");
    --------------------------------------------------------------------------------
  END COMPONENT;

  FOR ALL : mti_front USE ENTITY work.mti_front(arch_c);
BEGIN

  -- Instantiate the C defined architecture
  -- This essentially generates a process specified by the C function
  u_mti                 : mti_front;

  MIMO_Control_FSM_inst : ENTITY work.MIMO_Control_FSM
    PORT MAP(
      clk           => clk,
      rst_n         => rst_n,
      instr         => instr,
      data_in_comp  => data_in_comp,
      data_in_prog  => data_in_prog,
      crossbar_rdy  => crossbar_rdy,
      reading_prog  => reading_prog,
      compute_cross => compute_cross,
      valid         => valid
    );

  -- TODO An output should be added (signed) and the real value output should be translated to int and then signed. The input is computed as return x / (float)(INT_MAX) * 100000; so the reversed should be used to go for real to int
END sim;