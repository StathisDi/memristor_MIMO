#include <stdio.h>
#include <mti.h>
extern "C" void incrementor(int vhdl_integer, int *out_int)
{
  *out_int = vhdl_integer + 1;
  mti_PrintFormatted("The value of input is %d\n", vhdl_integer);
}
