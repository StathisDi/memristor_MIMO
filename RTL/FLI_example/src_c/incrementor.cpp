#include <stdio.h>
#include <mti.h>
extern "C" void incrementor(int vhdl_integer)
{
  mti_PrintFormatted("The value of input is %d\n", vhdl_integer);
}
