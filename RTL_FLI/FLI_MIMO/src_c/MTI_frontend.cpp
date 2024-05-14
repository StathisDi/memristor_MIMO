/*
MIT License

Copyright (c) 2024 Dimitrios Stathis

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
*/
#include <mti.h>
#include "util.h"
#include <Python.h>

#ifndef PY_PATH
#define PY_PATH "C:/Users/Dimitris/Documents/github/memristor_MIMO/modules/MemMIMO/examples/MIMO"
#endif
#ifndef PY_NAME
#define PY_NAME "wrapper"
#endif

#ifndef CRB_COL
#define CRB_COL 2
#endif

#ifndef CRB_ROW
#define CRB_ROW 3
#endif

typedef struct
{
  mtiDelayT delay;
  // Drive process id
  mtiProcessIdT procid;
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

// Program the crossbar
static void program(void *param)
{
  instanceInfoT *inst = (instanceInfoT *)param;
  mti_PrintFormatted("[Program]\tCrossbar is programmed with the following values: \n");
  print2DInt(inst->crossbar_input_prog_id, inst->crossbar_input_prog_length);
  PyObject *myModule = inst->myModule;
  int **prog_values = read2DArray(inst->crossbar_input_prog_id, inst->crossbar_input_prog_length);
  mti_PrintFormatted("[Program]\t\t Values read from RTL are:\n");
  for (int i = 0; i < CRB_ROW; ++i)
  {
    for (int j = 0; j < CRB_COL; ++j)
    {
      mti_PrintFormatted("\t\t\t%d ", prog_values[i][j]);
    }
    mti_PrintFormatted("\n ");
  }
  double **float_values = intToFloat2D(prog_values, CRB_ROW, CRB_COL);
  // Sett the python arguments and function call
  mti_PrintFormatted("Call py\n");
  // Get the function from the module
  PyObject *pFunc = PyObject_GetAttrString(myModule, (char *)"mem_program");
  if (pFunc == NULL)
  {
    mti_PrintFormatted("Function not found \n");
  }
  // Create a 2D array in C and convert it to a Python list of lists
  PyObject *pArray = pyList2D(float_values, CRB_ROW, CRB_COL);
  PyObject *pArgs = PyTuple_New(1);
  PyTuple_SetItem(pArgs, 0, pArray);
  PyObject *pResults;
  mti_PrintFormatted("Ready to program the crossbar!\n");
  pResults = callPy(pFunc, pArgs);
  // Py_DECREF(pArgs);
  if (pResults != NULL)
  {
    mti_PrintFormatted("Program Py function returned: %d\n", PyLong_AsLong(pResults));
  }
  else
  {
    mti_PrintFormatted("Program function did not return\n");
    mti_FatalError();
  }
  // Py_DECREF(pResults);
  // Py_DECREF(pFunc);

  delete2DArray(prog_values, inst->crossbar_input_prog_length);
  delete2DArray(float_values, CRB_ROW);
}

// Compute using the crossbar
static void compute(void *param)
{
  instanceInfoT *inst = (instanceInfoT *)param;
  mti_PrintFormatted("[Compute]\tCrossbar is computing with the following values: \n");
  print1DInt(inst->crossbar_input_comp_id);

  PyObject *myModule = inst->myModule;
  int *comp_values = read1DArray(inst->crossbar_input_comp_id);
  mti_PrintFormatted("[Compute]\t\t Values read from RTL are:\n");
  for (int i = 0; i < CRB_ROW; ++i)
  {
    mti_PrintFormatted("\t\t\t%d ", comp_values[i]);
    mti_PrintFormatted("\n ");
  }
  double *float_values = intToFloat1D(comp_values, CRB_ROW);
  // Sett the python arguments and function call
  mti_PrintFormatted("Call Compute function!\n");
  // Get the function from the module
  PyObject *pFunc = PyObject_GetAttrString(myModule, (char *)"mem_compute");
  if (pFunc == NULL)
  {
    mti_PrintFormatted("Function not found \n");
  }
  // Create a 1D array in C and convert it to a Python list of lists
  PyObject *pArray = pyList1D(float_values, CRB_ROW);
  PyObject *pArgs = PyTuple_New(1);
  PyTuple_SetItem(pArgs, 0, pArray);

  PyObject *pResult = NULL;
  double temp[CRB_COL];
  // If function exists call the function
  if (pFunc != NULL)
  {
    mti_PrintFormatted("\t\t Calling Py Function with args.\n");
    pResult = PyObject_CallObject(pFunc, pArgs);
    if (pResult != NULL)
    {
      // Convert the result back to C++ int
      // int result = PyLong_AsLong(pResult);
      PyObject *ptemp;
      for (int i = 0; i < CRB_COL; i++)
      {
        ptemp = PyList_GetItem(pResult, i);
        temp[i] = PyFloat_AS_DOUBLE(ptemp);
        mti_PrintFormatted("Results %d: %G \n", i, temp[i]);
      }
    }
    else
    {
      mti_PrintFormatted("Function call failed.\n");
      mti_FatalError();
    }
  }
  else
  {
    mti_PrintFormatted("Couldn't find function\n");
    mti_FatalError();
  }
  comp_values = NULL;
  float_values = NULL;
  delete float_values;
  delete comp_values;
  mti_PrintFormatted("Computation done\n");
  driveSig(inst->crossbar_output_drv, (void *)temp);
}

// Function sensitive to clock
static void clock_proc(void *param)
{
  instanceInfoT *inst = (instanceInfoT *)param;
  // check for the reset value
  mti_PrintFormatted("Function called in [%d,%d]  %s = %s\n", mti_NowUpper(), mti_Now(), mti_GetSignalName(inst->rst_id), mti_SignalImage(inst->rst_id));
  mtiInt32T scalar_val;
  scalar_val = mti_GetSignalValue(inst->rst_id);
  if (scalar_val == STD_LOGIC_0)
  {
    mti_PrintFormatted("Function called in (rst0) [%d,%d]  %s = %s\n", mti_NowUpper(), mti_Now(), mti_GetSignalName(inst->rst_id), mti_SignalImage(inst->rst_id));
    mtiInt32T rdy = STD_LOGIC_1;
    mti_ScheduleDriver(inst->crossbar_rdy_drv, rdy, convertToNS(0), MTI_TRANSPORT);
  }
  else
  {
    inst->clk_vlu = to_std_logic(mti_GetSignalValue(inst->clk_id));
    if (to_std_logic(inst->clk_vlu) == STD_LOGIC_1)
    {
      mti_PrintFormatted("Time [%d,%d] Proccess is triggered!\n", mti_NowUpper(), mti_Now());
      inst->crossbar_rdy_vlu = STD_LOGIC_1;
      inst->program_vlu = mti_GetSignalValue(inst->program_id);
      inst->compute_vlu = mti_GetSignalValue(inst->compute_id);
      if (inst->compute_vlu == STD_LOGIC_1)
      {
        if (inst->program_vlu == STD_LOGIC_1)
        {
          mti_PrintFormatted("\t\t!ERROR! Both program and compute signals active at the same time!\n");
          mti_FatalError();
        }
        inst->crossbar_rdy_vlu = STD_LOGIC_0;
        compute(inst);
      }
      else
      {
        if (inst->program_vlu == STD_LOGIC_1)
        {
          program(inst);
          inst->crossbar_rdy_vlu = STD_LOGIC_0;
        }
        else
        {
          inst->crossbar_rdy_vlu = STD_LOGIC_1;
        }
      }
      mti_ScheduleDriver(inst->crossbar_rdy_drv, inst->crossbar_rdy_vlu, convertToNS(0), MTI_TRANSPORT);
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
  mti_SetDriverOwner(inst->crossbar_rdy_drv, inst->procid);
  inst->crossbar_output_drv = mti_CreateDriver(inst->crossbar_output_id);
  mti_SetDriverOwner(inst->crossbar_output_drv, inst->procid);
  mtiInt32T *val;
  mtiInt32T tmp_val[CRB_COL];
  int i;
  for (i = 0; i < CRB_COL; i++)
  {
    tmp_val[i] = 0;
  }
  val = tmp_val;
  driveSig(inst->crossbar_output_drv, (void *)val);
  mtiInt32T rdy = STD_LOGIC_0;
  mti_ScheduleDriver(inst->crossbar_rdy_drv, rdy, convertToNS(0), MTI_TRANSPORT);
  //  Get lengths of arrays
  inst->crossbar_input_prog_length = mti_TickLength(mti_GetSignalType(inst->crossbar_input_prog_id));
  inst->crossbar_input_comp_length = mti_TickLength(mti_GetSignalType(inst->crossbar_input_comp_id));
  inst->crossbar_output_length = mti_TickLength(mti_GetSignalType(inst->crossbar_output_id));
  val = NULL;
  delete val;
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

  Py_Initialize();
  PyObject *sysPath = PySys_GetObject("path");
  PyList_Append(sysPath, PyUnicode_FromString(PY_PATH));
  PyObject *myModuleString = PyUnicode_FromString(PY_NAME);
  PyObject *myModule = PyImport_Import(myModuleString);
  if (myModule != NULL)
  {
    inst->myModule = myModule;
    mti_PrintFormatted("Py Module Loaded\n");
  }
  else
  {
    mti_PrintFormatted("Python module not found\n");
    mti_FatalError();
  }
  procid = mti_CreateProcess("clock_proc", clock_proc, inst);
  inst->procid = procid;
  mti_Sensitize(procid, inst->clk_id, MTI_EVENT);

  mti_AddLoadDoneCB(loadDoneCallback, inst);
  mti_AddQuitCB(cleanupCallback, inst);
  mti_AddRestartCB(cleanupCallback, inst);
}