#include <Python.h>
// #include "mti.h"
#include <iostream>

int call_increment_function(int input_value)
{
  Py_Initialize();
  // Setup the path
  PyObject *sysPath = PySys_GetObject("path");
  PyList_Append(sysPath, PyUnicode_FromString("C:/Users/Dimitris/Documents/github/memristor_MIMO/RTL/FLI_example/src_c"));
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
        std::cerr << "Function call failed." << std::endl;
      }
    }
    else
    {
      std::cout << "Couldn't find function\n";
    }
  }
  else
  {
    std::cout << "Python Module not found\n";
    exit(-1);
  }
}

int main()
{
  int input_value = 5;
  int incremented_value = call_increment_function(input_value);
  std::cout << "Input value: " << input_value << ", Incremented value: " << incremented_value << std::endl;

  return 0;
}
