#define MTI 1
#include <Python.h>
#if MTI == 1
#include "mti.h"
#else
#include <iostream>
using namespace std;
#endif

#if MTI == 1
extern "C" void py_init(int x)
#else
void py_init(int x)
#endif
{
  Py_Initialize();
}

#if MTI == 1
extern "C" void py_fin(int x)
#else
void py_fin(int x)
#endif
{
  Py_Finalize();
}

int call_increment_function(int input_value, int x)
{
  // char *srcpath = strcat(getenv("USERPROFILE"), "/Documents/github/memristor_MIMO/RTL/FLI_example/src_c");
  // Py_Initialize();
  // Setup the path
  py_init(0);
  PyObject *sysPath = PySys_GetObject("path");
  PyList_Append(sysPath, PyUnicode_FromString("Define Path"));
  // exit(0);
  //  Setup the module
  PyObject *myModuleString = PyUnicode_FromString("process_integer");
  PyObject *myModule = PyImport_Import(myModuleString);
#if MTI != 1
  cout << "Starting call for python function. " << endl;
#endif
  if (myModule != NULL)
  {
    // Python module found, setup the function
    PyObject *pFunc = PyObject_GetAttrString(myModule, (char *)"process_integer");
    // Setup the parameters for the function
    PyObject *pArgs = PyTuple_New(2);
    PyObject *pValue0 = PyLong_FromLong(input_value);
    PyObject *pValue1 = PyLong_FromLong(x);
    PyTuple_SetItem(pArgs, 0, pValue0);
    PyTuple_SetItem(pArgs, 1, pValue1);

    // If function exists call the function
    if (pFunc != NULL)
    {
      PyObject *pResult = PyObject_CallObject(pFunc, pArgs);
      if (pResult != NULL)
      {
        // Convert the result back to C++ int
        int result = PyLong_AsLong(pResult);
        // Py_Finalize();
        py_fin(0);
#if MTI != 1
        cout << "return value " << result << endl;
#endif
        return result; // Return the result of the Python function
      }
      else
      {
#if MTI == 1
        mti_PrintFormatted("Function call failed.");
#else
        cout << "Function call failed." << endl;
#endif
        exit(-1);
      }
    }
    else
    {
#if MTI == 1
      mti_PrintFormatted("Couldn't find function\n");
#else
      cout << "Couldn't find function." << endl;
#endif
      exit(-1);
    }
  }
  else
  {
#if MTI == 1
    mti_PrintFormatted("Python Module not found\n");
#else
    cout << "Python Module not found." << endl;
#endif
    exit(-1);
  }
}

#if MTI == 1
extern "C" void incr_py(int vhdl_integer, int *out_int)
#else
void incr_py(int vhdl_integer, int *out_int)
#endif
{
  static int x = 0;
#if MTI == 1
  mti_PrintFormatted("The x is %d\n", x);
#else
  cout << "x is " << x << endl;
#endif
  x = call_increment_function(vhdl_integer, x);
  *out_int = x;
#if MTI == 1
  mti_PrintFormatted("The value of input is %d, the x is %d, the return value is %d\n", vhdl_integer, x, *out_int);
#else
  cout << "The value of the input is " << vhdl_integer << " the x is " << x << " the return value is " << *out_int << endl;
#endif
}

#if MTI != 1
int main()
{
  int input_value = 3;
  int out_int = -1;
  for (int i = 0; i < 5; i++)
  {
    cout << "calling start" << endl;
    incr_py(input_value, &out_int);
    cout << "Return Value is " << out_int << endl;
  }
  return 0;
}
#endif