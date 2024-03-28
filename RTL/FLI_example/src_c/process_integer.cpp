#include <Python.h>
#include "mti.h"

extern "C" void process_integer(int value)
{
  // Initialize Python interpreter and ensure thread safety
  Py_Initialize();
  PyGILState_STATE gil_state = PyGILState_Ensure();

  // Import the Python module and function
  PyObject *pName = PyUnicode_FromString("integer_processor");
  PyObject *pModule = PyImport_Import(pName);
  Py_DECREF(pName);

  if (pModule != nullptr)
  {
    PyObject *pFunc = PyObject_GetAttrString(pModule, "process_integer");
    if (pFunc && PyCallable_Check(pFunc))
    {
      PyObject *pValue = PyLong_FromLong(value);
      PyObject *pArgs = PyTuple_New(1);
      PyTuple_SetItem(pArgs, 0, pValue);
      PyObject_CallObject(pFunc, pArgs);
      Py_DECREF(pArgs);
    }
    else
    {
      PyErr_Print();
    }
    Py_XDECREF(pFunc);
    Py_DECREF(pModule);
  }
  else
  {
    PyErr_Print();
  }

  // Cleanup
  PyGILState_Release(gil_state);
  Py_Finalize();
}
