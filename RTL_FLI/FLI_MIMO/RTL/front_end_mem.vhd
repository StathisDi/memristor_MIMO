LIBRARY ieee, work;

USE work.data_types.ALL;
USE work.constants.ALL;

ENTITY front_end_mem IS
  PORT (
    clk   : IN STD_LOGIC;
    reset : IN STD_LOGIC;

  );
END ENTITY;