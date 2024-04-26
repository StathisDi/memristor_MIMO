#include <mti.h>
#include "util.h"
#include <Python.h>

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
  mtiDriverIdT ret_array_drv;

  // Signal values
  mtiInt32T clk_value;
  mtiInt32T rst_value;
  void *int_array_value;
  void *ret_array_value;

  // Array lengths
  mtiInt32T int_value_length;
  mtiInt32T ret_value_length;

  // Python module
  PyObject *myModule;

} instanceInfoT;

static void compute_out_value(void *param)
{
  instanceInfoT *inst = (instanceInfoT *)param;
  int i;
  mtiInt32T num_elems;

  inst->int_array_value = mti_GetArraySignalValue(inst->int_array_id, 0);
  num_elems = inst->int_value_length;
  mti_PrintFormatted("\nEdit function ");
  mtiInt32T *val;
  val = (mtiInt32T *)inst->int_array_value;
  mtiInt32T *ret;
  ret = (mtiInt32T *)inst->ret_array_value;
  for (i = 0; i < num_elems; i++)
  {
    ret[i] = val[i] + 5;
  }
  print_int_array(inst->ret_array_id, mti_GetSignalType(inst->ret_array_id));
  mti_ScheduleDriver(inst->ret_array_drv, (long)inst->ret_array_value, convertToNS(0), MTI_INERTIAL);
  mti_PrintFormatted("Signals are updated \n ");
}

static int inc_py(PyObject *myModule)
{
  mti_PrintFormatted("\t\t !!!! Calling python Function !!!! [%d,%d] \n", mti_NowUpper(), mti_Now());
  if (myModule != NULL)
  {
    // Python module found, setup the function
    PyObject *pFunc = PyObject_GetAttrString(myModule, (char *)"accumulate");
    // Setup the parameters for the function
    PyObject *pArgs = PyTuple_New(1);
    int input_value = 1;
    PyObject *pValue0 = PyLong_FromLong(input_value);
    PyTuple_SetItem(pArgs, 0, pValue0);
    // Convert the result back to C++ int
    int result = PyLong_AsLong(call_py(pFunc, pArgs));
    return result;
  }
  else
  {
    mti_PrintFormatted("Python Module not found\n");
    mti_FatalError();
  }
}

static int dec_py(PyObject *myModule)
{
  mti_PrintFormatted("\t\t !!!! Calling python Function !!!! [%d,%d] \n", mti_NowUpper(), mti_Now());
  if (myModule != NULL)
  {
    // Python module found, setup the function
    PyObject *pFunc = PyObject_GetAttrString(myModule, (char *)"redact");
    // Setup the parameters for the function
    PyObject *pArgs = PyTuple_New(1);
    int input_value = 1;
    PyObject *pValue0 = PyLong_FromLong(input_value);
    PyTuple_SetItem(pArgs, 0, pValue0);
    // Convert the result back to C++ int
    int result = PyLong_AsLong(call_py(pFunc, pArgs));
    return result;
  }
  else
  {
    mti_PrintFormatted("Python Module not found\n");
    mti_FatalError();
  }
}

// Function sensitive to clock
static void clock_proc(void *param)
{
  instanceInfoT *inst = (instanceInfoT *)param;
  PyObject *myModule = inst->myModule;
  int x = -1;
  void *array_val;
  array_val = mti_GetArraySignalValue(inst->int_array_id, 0);
  mtiInt32T *val = (mtiInt32T *)array_val;
  if (val[0] > 5)
  {
    x = dec_py(myModule);
  }
  else
  {
    x = inc_py(myModule);
  }
  mti_PrintFormatted("\t\t !!!! Python returned %d !!!! [%d,%d] \n", x, mti_NowUpper(), mti_Now());

  // check for the reset value
  mti_PrintFormatted("Function called in [%d,%d]  %s = %s\n", mti_NowUpper(), mti_Now(), mti_GetSignalName(inst->rst_id), mti_SignalImage(inst->rst_id));
  mtiInt32T scalar_val;
  scalar_val = mti_GetSignalValue(inst->rst_id);
  if (scalar_val == STD_LOGIC_0)
  {
    mti_PrintFormatted("Function called in (rst0) [%d,%d]  %s = %s\n", mti_NowUpper(), mti_Now(), mti_GetSignalName(inst->rst_id), mti_SignalImage(inst->rst_id));
  }
  else
  {
    // mtiInt32T clk_val;
    // clk_val = mti_GetSignalValue(inst->clk_id);
    inst->clk_value = to_std_logic(mti_GetSignalValue(inst->clk_id));
    if (to_std_logic(inst->clk_value) == STD_LOGIC_1)
    {
      mti_PrintFormatted("Time [%d,%d]:", mti_NowUpper(), mti_Now());
      print_int_array(inst->int_array_id, mti_GetSignalType(inst->int_array_id));
      compute_out_value(inst);
      mti_PrintFormatted("\n");
    }
  }
}

// Clean up function
void cleanupCallback(void *param)
{
  mti_PrintMessage("Cleaning up...\n");
  Py_Finalize();
  mti_Free(param);
}

void loadDoneCallback(void *param)
{
  instanceInfoT *inst = (instanceInfoT *)param;

  inst->clk_value = mti_GetSignalValue(inst->clk_id);
  inst->rst_value = mti_GetSignalValue(inst->rst_id);
  inst->int_array_value = mti_GetArraySignalValue(inst->int_array_id, 0);
  inst->ret_array_value = mti_GetArraySignalValue(inst->ret_array_id, 0);
  inst->int_value_length = mti_TickLength(mti_GetSignalType(inst->int_array_id));
  inst->ret_value_length = mti_TickLength(mti_GetSignalType(inst->ret_array_id));
}

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

  inst->ret_array_drv = mti_CreateDriver(inst->ret_array_id);
  Py_Initialize();
  PyObject *sysPath = PySys_GetObject("path");
  PyList_Append(sysPath, PyUnicode_FromString("C:/Users/Dimitris/Documents/github/memristor_MIMO/RTL_FLI/FLI_example_array/src_c"));

  PyObject *myModuleString = PyUnicode_FromString("accumulate");
  PyObject *myModule = PyImport_Import(myModuleString);
  inst->myModule = myModule;
  procid = mti_CreateProcess("clock_proc", clock_proc, inst);

  mti_Sensitize(procid, inst->clk_id, MTI_EVENT);

  mti_AddLoadDoneCB(loadDoneCallback, inst);
  mti_AddQuitCB(cleanupCallback, inst);
  mti_AddRestartCB(cleanupCallback, inst);
}