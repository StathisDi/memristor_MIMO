LIBRARY ieee, work;
USE ieee.std_logic_1164.ALL;
USE work.data_types.ALL;
USE work.constants.ALL;
USE work.function_pack.ALL;

--! This entity combines the control FSM and the memristive crossbar.
ENTITY front_end_mem IS
  PORT (
    clk           : IN STD_LOGIC;
    rst_n         : IN STD_LOGIC;
    --! The instruction to be executed by the crossbar
    instr         : IN INSTRUCTION;
    --! The data to be used computation, the data input comes in the form of 1D array equal to the number of rows in the crossbar (single column)
    data_in_comp  : IN int_array_ty(crossbar_rows - 1 DOWNTO 0);
    --! The data to be used to program the array. The input comes in the form of 1D array equal to the number of columns (single row)
    data_in_prog  : IN int_array_ty(crossbar_cols - 1 DOWNTO 0);
    --! When asserted new instructions can be sent to the crossbar
    data_output   : OUT int_array_ty(crossbar_cols - 1 DOWNTO 0);
    --! Asserted while programming the crossbar. During this time it expects a new column of the crossbar in every cycle
    reading_prog  : OUT STD_LOGIC;
    --! Asserted while the computation is happening inside the crossbar, deasserted when it is done. During the computation time no new data should be sent to the crossbar
    compute_cross : OUT STD_LOGIC;
    --! Asserted when the crossbar has completed the computation. It signals that the data is ready to be read
    valid         : OUT STD_LOGIC
  );
END ENTITY;

--! The design is meant to emulate the memristor crossbar and its digital front end.
--! It emulates the timing required to program the crossbar and perform the computation.
ARCHITECTURE sim OF front_end_mem IS
  SIGNAL program             : STD_LOGIC;
  SIGNAL compute             : STD_LOGIC;
  SIGNAL crossbar_input_prog : int_2d_array_ty(crossbar_rows - 1 DOWNTO 0, crossbar_cols - 1 DOWNTO 0);
  SIGNAL crossbar_input_comp : int_array_ty(crossbar_rows - 1 DOWNTO 0);
  SIGNAL crossbar_output     : real_array_ty(crossbar_cols - 1 DOWNTO 0);
  SIGNAL crossbar_rdy        : STD_LOGIC;

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
  u_mti : mti_front;
  u_FSM : ENTITY work.MIMO_Control_FSM
    PORT MAP(
      clk                => clk,                 -- Input
      rst_n              => rst_n,               -- Input
      instr              => instr,               -- Input
      data_in_comp       => data_in_comp,        -- Input
      data_in_prog       => data_in_prog,        -- Input
      crossbar_rdy       => crossbar_rdy,        -- To the output
      cross_compute_data => crossbar_input_comp, -- To the crossbar for computation
      cross_program_data => crossbar_input_prog, -- To the crossbar for programming
      reading_prog       => reading_prog,        -- To the output, crossbar is programming
      compute_cross      => compute_cross,       -- To the output, crossbar is computing
      program            => program,             -- To the crossbar to start programming
      compute            => compute,             -- To the crossbar to start computation
      valid              => valid                -- To the output Computation complete
    );

  -- Process that turns the output to integer
  P_comb : PROCESS (ALL)
  BEGIN
    -- The if function here is used to avoid errors when the simulation starts.
    -- Because the c emulation initializes the rea output of the crossbar to max_real we need to make sure that it is not passed to the function before it gets a usable value.
    IF rst_n = '1' THEN
      FOR i IN 0 TO crossbar_cols - 1 LOOP
        data_output(i) <= real_to_integer(crossbar_output(i));
      END LOOP;
    ELSE
      data_output <= (OTHERS => 0);
    END IF;
  END PROCESS;

END sim;