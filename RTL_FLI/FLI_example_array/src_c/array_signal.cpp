#include <mti.h>

typedef struct varInfoT_tag
{
  struct varInfoT_tag *next;
  char *name;
  mtiSignalIdT varid;
  mtiTypeIdT type_id; // renamed to type_id to be compatible with c++
} varInfoT;

typedef struct
{
  mtiDelayT delay;
  // Signal IDs
  mtiSignalIdT clk_id;
  mtiSignalIdT rst_id;
  mtiSignalIdT int_array_id;
  mtiSignalIdT ret_array_id;
  // Signal Drivers
  mtiDriverIdT clk_drv;
  mtiDriverIdT rst_drv;
  mtiDriverIdT int_array_drv;
  mtiDriverIdT ret_array_drv;

  // Signal values
  mtiInt32T clk_value;
  mtiInt32T rst_value;
  void *int_array_value;
  void *ret_array_value;

  // Array lengths
  mtiInt32T int_value_length;
  mtiInt32T ret_value_length;

} instanceInfoT;

#define NS_EXPONENT -9

mtiDelayT convertToNS(mtiDelayT delay)
{
  int exp = NS_EXPONENT - mti_GetResolutionLimit();

  if (exp < 0)
  {
    /* Simulator resolution limit is coarser than ns.     */
    /* Cannot represent delay accurately, so truncate it. */
    while (exp++)
    {
      delay /= 10;
    }
  }
  else
  {
    /* Simulator resolution limit is finer than ns. */
    while (exp--)
    {
      delay *= 10;
    }
  }
  return delay;
}

static void print_array(mtiSignalIdT sigid, mtiTypeIdT sigtype)
{
  int i;
  mtiInt32T num_elems;

  void *array_val;

  array_val = mti_GetArraySignalValue(sigid, 0);
  num_elems = mti_TickLength(sigtype);

  mtiInt32T *val = (mtiInt32T *)array_val;
  for (i = 0; i < num_elems; i++)
  {
    mti_PrintFormatted("  %d", val[i]);
  }
  mti_VsimFree(array_val);
}

static void printSignalInfo(mtiSignalIdT sigid)
{
  mtiTypeIdT sigtype;
  sigtype = mti_GetSignalType(sigid);
  switch (mti_GetTypeKind(sigtype))
  {
  case MTI_TYPE_SCALAR:
    mti_PrintFormatted("is of type INTEGER\n");
    break;
  case MTI_TYPE_ENUM:
    mti_PrintFormatted("is of type ENUMERATION\n");
    break;
  case MTI_TYPE_PHYSICAL:
    mti_PrintFormatted("is of type PHYSICAL\n");
    break;
  case MTI_TYPE_REAL:
    mti_PrintFormatted("is of type REAL\n");
    break;
  case MTI_TYPE_TIME:
    mti_PrintFormatted("is of type TIME\n");
    break;
  case MTI_TYPE_ARRAY:
    mti_PrintFormatted("is of type ARRAY\n");
    break;
  case MTI_TYPE_RECORD:
    mti_PrintFormatted("is of type RECORD\n");
    break;
  default:
    mti_PrintFormatted("is of type UNKNOWN\n");
    break;
  }
}

// Function sensitive to clock
static void clock_proc(void *param)
{
  instanceInfoT *inst = (instanceInfoT *)param;
  // check for the reset value
  mti_PrintFormatted("Function called in [%d,%d]  %s = %s\n", mti_NowUpper(), mti_Now(), mti_GetSignalName(inst->rst_id), mti_SignalImage(inst->rst_id));
  mtiInt32T scalar_val;
  scalar_val = mti_GetSignalValue(inst->rst_id);
  if (scalar_val == 2)
  {
    mti_PrintFormatted("Function called in (rst0) [%d,%d]  %s = %s\n", mti_NowUpper(), mti_Now(), mti_GetSignalName(inst->rst_id), mti_SignalImage(inst->rst_id));
  }
  else
  {
    mtiInt32T clk_val;
    clk_val = mti_GetSignalValue(inst->clk_id);
    if (clk_val == 3)
    {
      mti_PrintFormatted("Time [%d,%d]:", mti_NowUpper(), mti_Now());
      print_array(inst->int_array_id, mti_GetSignalType(inst->int_array_id));
      mti_PrintFormatted("\n");
    }
  }
}

// Clean up function
void cleanupCallback(void *param)
{
  mti_PrintMessage("Cleaning up...\n");
  mti_Free(param);
}

/*

  If we require to work with signals:

  static void initInstance( void * param )
{
  mtiSignalIdT sigid;
  mtiTypeIdT   typeid;

  mti_PrintMessage( "Design Signals:\n" );
  for ( sigid = mti_FirstSignal( mti_GetTopRegion() );
        sigid; sigid = mti_NextSignal() ) {
    typeid = mti_GetSignalType( sigid );
    mti_PrintFormatted( "%14s: type %-12s; length = %d\n",
                       mti_GetSignalName( sigid ), getTypeStr( typeid ),
                       mti_TickLength( typeid ));
  }
}


*/

// Main function that links to an architecture
extern "C" void initForeign(
    mtiRegionIdT region,         /* The ID of the region in which this     */
                                 /* foreign architecture is instantiated.  */
    char *param,                 /* The last part of the string in the     */
                                 /* foreign attribute.                     */
    mtiInterfaceListT *generics, /* A list of generics for the foreign model.*/
    mtiInterfaceListT *ports     /* A list of ports for the foreign model.   */
)
{

  instanceInfoT *inst;
  mtiProcessIdT procid;

  inst = (instanceInfoT *)mti_Malloc(sizeof(instanceInfoT));

  // Get id of the signals
  inst->clk_id = mti_FindSignal("/top_array/clk");
  inst->rst_id = mti_FindSignal("/top_array/rst");
  inst->int_array_id = mti_FindSignal("/top_array/int_array");
  inst->ret_array_id = mti_FindSignal("/top_array/ret_array");

  procid = mti_CreateProcess("clock_proc", clock_proc, inst);
  mti_Sensitize(procid, inst->clk_id, MTI_EVENT);

  mti_AddQuitCB(cleanupCallback, inst);
  mti_AddRestartCB(cleanupCallback, inst);
}