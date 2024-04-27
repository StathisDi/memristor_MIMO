#include <mti.h>
#include "util.h"
#include <Python.h>
#ifndef PY_PATH
#define PY_PATH "C:/Users/Dimitris/Documents/github/memristor_MIMO/RTL_FLI/FLI_MIMO/src_c"
#endif
#ifndef PY_NAME
#define PY_NAME ""
#endif

typedef struct
{
  mtiDelayT delay;
  // Signal IDs for inputs
  mtiSignalIdT clk_id;
  mtiSignalIdT rst_id;
  mtiSignalIdT program_id;
  mtiSignalIdT compute_id;
  mtiSignalIdT crossbar_input_prog_id;
  mtiSignalIdT crossbar_input_comp_id;

  // Signal IDs for outputs
  mtiSignalIdT crossbar_output_id;
  mtiSignalIdT crossbar_rdy_id;

  // Signal Drivers
  mtiDriverIdT crossbar_output_drv;
  mtiDriverIdT crossbar_rdy_drv;

  // Signal values
  mtiInt32T clk_vlu;
  mtiInt32T rst_vlu;
  mtiInt32T program_vlu;
  mtiInt32T compute_vlu;
  void *crossbar_input_prog_vlu;
  void *crossbar_input_comp_vlu;
  void *crossbar_output_vlu;
  mtiInt32T crossbar_rdy_vlu;

  // Array lengths
  mtiInt32T crossbar_input_prog_length;
  mtiInt32T crossbar_input_comp_length;
  mtiInt32T crossbar_output_length;

  // Python module
  PyObject *myModule;

} instanceInfoT;

/*
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
  printIntArray(inst->ret_array_id, mti_GetSignalType(inst->ret_array_id));
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
    int result = PyLong_AsLong(callPy(pFunc, pArgs));
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
    int result = PyLong_AsLong(callPy(pFunc, pArgs));
    return result;
  }
  else
  {
    mti_PrintFormatted("Python Module not found\n");
    mti_FatalError();
  }
}
*/
// Function sensitive to clock
static void clock_proc(void *param)
{
  instanceInfoT *inst = (instanceInfoT *)param;
  /* PyObject *myModule = inst->myModule;
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
 */
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
    inst->clk_vlu = to_std_logic(mti_GetSignalValue(inst->clk_id));
    if (to_std_logic(inst->clk_vlu) == STD_LOGIC_1)
    {
      mti_PrintFormatted("Time [%d,%d]:", mti_NowUpper(), mti_Now());
      printSignalInfo(inst->crossbar_input_prog_id);
      printSignalInfo(inst->crossbar_output_id);
      printSignalInfo(inst->crossbar_input_comp_id);
      printArrayLength(inst->crossbar_input_prog_id);
      printArrayLength(inst->crossbar_output_id);
      printArrayLength(inst->crossbar_input_comp_id);
      int i;
      void *array_val;
      array_val = GetSubArrayVal(inst->crossbar_input_prog_id);
      for (i = 0; i < inst->crossbar_input_prog_length; i++)
      {
        mti_GetSignalSubelements
      }

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
  // Create drivers for the output signals
  inst->crossbar_rdy_drv = mti_CreateDriver(inst->crossbar_rdy_id);
  inst->crossbar_output_drv = mti_CreateDriver(inst->crossbar_output_id);
  // Get lengths of arrays
  inst->crossbar_input_prog_length = mti_TickLength(mti_GetSignalType(inst->crossbar_input_prog_id));
  inst->crossbar_input_comp_length = mti_TickLength(mti_GetSignalType(inst->crossbar_input_comp_id));
  inst->crossbar_output_length = mti_TickLength(mti_GetSignalType(inst->crossbar_output_id));
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
  // Get id of the input signals
  inst->clk_id = mti_FindSignal("/MIMO_TOP/clk");
  inst->rst_id = mti_FindSignal("/MIMO_TOP/rst_n");
  inst->program_id = mti_FindSignal("/MIMO_TOP/program");
  inst->compute_id = mti_FindSignal("/MIMO_TOP/compute");
  inst->crossbar_input_prog_id = mti_FindSignal("/MIMO_TOP/crossbar_input_prog");
  inst->crossbar_input_comp_id = mti_FindSignal("/MIMO_TOP/crossbar_input_comp");

  // Get ids of output signals
  inst->crossbar_rdy_id = mti_FindSignal("/MIMO_TOP/crossbar_rdy");
  inst->crossbar_output_id = mti_FindSignal("/MIMO_TOP/crossbar_output");

  /*Py_Initialize();
  PyObject *sysPath = PySys_GetObject("path");
  PyList_Append(sysPath, PyUnicode_FromString(PY_PATH));
  PyObject *myModuleString = PyUnicode_FromString(PY_NAME);
  PyObject *myModule = PyImport_Import(myModuleString);
  inst->myModule = myModule;*/

  procid = mti_CreateProcess("clock_proc", clock_proc, inst);

  mti_Sensitize(procid, inst->clk_id, MTI_EVENT);

  mti_AddLoadDoneCB(loadDoneCallback, inst);
  mti_AddQuitCB(cleanupCallback, inst);
  mti_AddRestartCB(cleanupCallback, inst);
}