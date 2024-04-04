#include <Python.h>
// #include "mti.h"

#include <Python.h>
#include <iostream>

int call_increment_function(int input_value)
{
  Py_Initialize();

  // Import the Python module
  PyObject *pName = PyUnicode_FromString("increment");
  PyObject *pModule = PyImport_Import(pName);
  Py_DECREF(pName);

  if (pModule != nullptr)
  {
    // Get the increment_value function from the module
    PyObject *pFunc = PyObject_GetAttrString(pModule, "increment_value");
    if (pFunc && PyCallable_Check(pFunc))
    {
      // Prepare the argument for the function call
      PyObject *pArgs = PyTuple_New(1);
      PyObject *pValue = PyLong_FromLong(input_value);
      PyTuple_SetItem(pArgs, 0, pValue); // pValue reference stolen here

      // Call the function
      PyObject *pResult = PyObject_CallObject(pFunc, pArgs);
      Py_DECREF(pArgs);

      if (pResult != nullptr)
      {
        // Convert the result back to C++ int
        int result = PyLong_AsLong(pResult);
        Py_DECREF(pResult);
        Py_DECREF(pFunc);
        Py_DECREF(pModule);
        Py_Finalize();

        return result; // Return the result of the Python function
      }
      else
      {
        // Handle error: the function returned None
        Py_DECREF(pFunc);
        Py_DECREF(pModule);
        Py_Finalize();
        std::cerr << "Function call failed." << std::endl;
        return -1;
      }
    }
    else
    {
      // Handle error: the function was not found or is not callable
      if (PyErr_Occurred())
        PyErr_Print();
      Py_XDECREF(pFunc);
      Py_DECREF(pModule);
      Py_Finalize();
      std::cerr << "Function not callable or not found." << std::endl;
      return -1;
    }
  }
  else
  {
    // Handle error: the module was not found
    if (PyErr_Occurred())
      PyErr_Print();
    Py_Finalize();
    std::cerr << "Failed to load module." << std::endl;
    return -1;
  }
}

int main()
{
  int input_value = 5;
  int incremented_value = call_increment_function(input_value);
  std::cout << "Input value: " << input_value << ", Incremented value: " << incremented_value << std::endl;

  return 0;
}
