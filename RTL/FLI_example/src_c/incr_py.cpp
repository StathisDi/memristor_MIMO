#include <Python.h>
#include "mti.h"
#include <iostream>
#include <filesystem>
namespace fs = std::filesystem;
// TODO when executed in questasim, the python module is not found. Possible solution change the src path to hardcoded and remove the filesystem requirement, alternatively compile and call the executable

int call_increment_function(int input_value)
{
  char *srcpath = strcat(getenv("USERPROFILE"), "/Documents/github/memristor_MIMO/RTL/FLI_example/src_c");
  Py_Initialize();
  // Setup the path
  PyObject *sysPath = PySys_GetObject("path");
  PyList_Append(sysPath, PyUnicode_FromString(srcpath));
  // exit(0);
  //  Setup the module
  PyObject *myModuleString = PyUnicode_FromString("process_integer");
  PyObject *myModule = PyImport_Import(myModuleString);

  if (myModule != NULL)
  {
    // Python module found, setup the function
    PyObject *pFunc = PyObject_GetAttrString(myModule, (char *)"process_integer");
    // Setup the parameters for the function
    PyObject *pArgs = PyTuple_New(1);
    PyObject *pValue = PyLong_FromLong(input_value);
    PyTuple_SetItem(pArgs, 0, pValue);

    // If function exists call the function
    if (pFunc != NULL)
    {
      PyObject *pResult = PyObject_CallObject(pFunc, pArgs);
      if (pResult != NULL)
      {
        // Convert the result back to C++ int
        int result = PyLong_AsLong(pResult);
        Py_Finalize();
        return result; // Return the result of the Python function
      }
      else
      {
        mti_PrintFormatted("Function call failed.");
      }
    }
    else
    {
      mti_PrintFormatted("Couldn't find function\n");
    }
  }
  else
  {
    mti_PrintFormatted("Python Module not found\n");
    exit(-1);
  }
}

extern "C" void incr_py(int vhdl_integer, int *out_int)
{
  *out_int = call_increment_function(vhdl_integer);
  mti_PrintFormatted("The value of input is %d\n", vhdl_integer);
}