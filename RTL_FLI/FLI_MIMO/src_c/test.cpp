#include <Python.h>
#include <iostream>
#ifndef PY_PATH
#define PY_PATH "<set your path to the python script>"
#endif
#ifndef PY_NAME
#define PY_NAME "my_test"
#endif
int main(int argc, char **argv)
{
  Py_Initialize();

  // First set in path where to find your custom python module.
  // You have to tell the path otherwise the next line will try to load
  // your module from the path where Python's system modules/packages are
  // found.
  Py_Initialize();
  printf("Starting ...");
  PyObject *sysPath = PySys_GetObject("path");
  PyList_Append(sysPath, PyUnicode_FromString("C:/Users/Dimitris/Documents/github/memristor_MIMO/RTL_FLI/FLI_MIMO/src_c"));
  PyObject *myModuleString = PyUnicode_FromString(PY_NAME);
  PyObject *myModule = PyImport_Import(myModuleString);

  if (myModule != NULL)
  {
    printf("Loaded\n");
  }
  else
  {
    printf("Python module not found\n");
    exit(-1);
  }
  PyObject *pFunc = PyObject_GetAttrString(myModule, (char *)"py_set");
  PyObject *pArgs = PyTuple_New(1);
  int input_value = 1;
  PyObject *pValue0 = PyLong_FromLong(input_value);
  PyTuple_SetItem(pArgs, 0, pValue0);
  PyObject *pResult = NULL;
  // If function exists call the function
  if (pFunc != NULL)
  {
    printf("\t\t Calling Py Function with args.\n");
    pResult = PyObject_CallObject(pFunc, pArgs);
    if (pResult != NULL)
    {
      // Convert the result back to C++ int
      // int result = PyLong_AsLong(pResult);
      printf("Good %d\n", PyLong_AsLong(pResult)); // Return the result of the Python function
    }
    else
    {
      printf("Function call failed.\n");
      exit(-1);
    }
  }
  else
  {
    printf("Couldn't find function\n");
    exit(-1);
  }
  return 0;
}