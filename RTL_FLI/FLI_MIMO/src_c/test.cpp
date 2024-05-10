#include <Python.h>
#include <iostream>

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
int main(int argc, char **argv)
{
  Py_Initialize();

  // First set in path where to find your custom python module.
  // You have to tell the path otherwise the next line will try to load
  // your module from the path where Python's system modules/packages are
  // found.
  Py_Initialize();
  printf("Starting ... \n");
  PyObject *sysPath = PySys_GetObject("path");
  PyList_Append(sysPath, PyUnicode_FromString(PY_PATH));
  PyObject *myModuleString = PyUnicode_FromString(PY_NAME);
  PyObject *myModule = PyImport_Import(myModuleString);
  PyObject_SetAttrString(myModule, "CRB_ROW", PyLong_FromLong(CRB_ROW));
  PyObject_SetAttrString(myModule, "CRB_COL", PyLong_FromLong(CRB_COL));
  if (myModule != NULL)
  {
    printf("Loaded\n");
  }
  else
  {
    printf("Python module not found\n");
    exit(-1);
  }
  PyObject *pFunc = PyObject_GetAttrString(myModule, (char *)"mem_program");
  PyObject *pArgs = PyTuple_New(1);
  int input_value = 1;
  PyObject *pArray = PyList_New(CRB_ROW);
  for (int i = 0; i < CRB_ROW; i++)
  {
    PyObject *pRow = PyList_New(CRB_COL);
    for (int j = 0; j < CRB_COL; j++)
    {
      PyList_SetItem(pRow, j, PyLong_FromLong(input_value));
    }
    PyList_SetItem(pArray, i, pRow);
  }
  // PyObject *pValue0 = PyLong_FromLong(input_value);
  PyTuple_SetItem(pArgs, 0, pArray);
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

  pFunc = PyObject_GetAttrString(myModule, (char *)"mem_compute");
  pArgs = PyTuple_New(1);
  float inp = 0.5;
  pArray = PyList_New(CRB_ROW);
  for (int i = 0; i < CRB_ROW; i++)
  {
    PyList_SetItem(pArray, i, PyFloat_FromDouble(inp));
  }
  PyTuple_SetItem(pArgs, 0, pArray);
  pResult = NULL;
  // If function exists call the function
  if (pFunc != NULL)
  {
    printf("\t\t Calling Py Function with args.\n");
    pResult = PyObject_CallObject(pFunc, pArgs);
    if (pResult != NULL)
    {
      // Convert the result back to C++ int
      // int result = PyLong_AsLong(pResult);
      double temp[CRB_COL];
      PyObject *ptemp;
      for (int i = 0; i < CRB_COL; i++)
      {
        ptemp = PyList_GetItem(pResult, i);
        temp[i] = PyFloat_AS_DOUBLE(ptemp);
        printf("Good %d: %f \n", i, temp[i]);
      }
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
  Py_Finalize();
  return 0;
}