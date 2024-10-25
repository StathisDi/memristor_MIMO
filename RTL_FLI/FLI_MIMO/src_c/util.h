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
#ifndef UTIL_H
#define UTIL_H
#include <mti.h>
#include <Python.h>
#include <limits.h>
#include <vector>

// Function that normalize an integer to a symmetric range -1 to 1
// This maps the integer values from the VHDL to the programmed values in the crossbar.
double intToNormalizedReal(int x)
{
  if (x == INT_MIN)
  {
    return -1.0;
  }
  else
  {
    return x / (float)(INT_MAX) * 100000;
  }
}

// Define the STD logic to C
typedef enum
{
  STD_LOGIC_U,
  STD_LOGIC_X,
  STD_LOGIC_0,
  STD_LOGIC_1,
  STD_LOGIC_Z,
  STD_LOGIC_W,
  STD_LOGIC_L,
  STD_LOGIC_H,
  STD_LOGIC_D
} StdLogicType;

#define NS_EXPONENT -9

// Convert the value to NS
mtiDelayT convertToNS(mtiDelayT delay)
{
  int exp = NS_EXPONENT - mti_GetResolutionLimit();

  if (exp < 0)
  {
    /* Simulator resolution limit is coarser than ns.     */
    /* Cannot represent delay accurately, so truncate it. */
    while (exp++)
    {
      delay /= 10;
    }
  }
  else
  {
    /* Simulator resolution limit is finer than ns. */
    while (exp--)
    {
      delay *= 10;
    }
  }
  return delay;
}

static StdLogicType to_std_logic(mtiInt32T value)
{
  switch (value)
  {
  case STD_LOGIC_U:
    return STD_LOGIC_U;
  case STD_LOGIC_X:
    return STD_LOGIC_X;
  case STD_LOGIC_0:
    return STD_LOGIC_0;
  case STD_LOGIC_1:
    return STD_LOGIC_1;
  case STD_LOGIC_Z:
    return STD_LOGIC_Z;
  case STD_LOGIC_W:
    return STD_LOGIC_W;
  case STD_LOGIC_L:
    return STD_LOGIC_L;
  case STD_LOGIC_H:
    return STD_LOGIC_H;
  case STD_LOGIC_D:
    return STD_LOGIC_D;
  default:
    return STD_LOGIC_U;
  }
}

// Print the values of an int array signal
static void printIntArray(mtiSignalIdT sigid, mtiTypeIdT sigtype)
{
  int i;
  mtiInt32T num_elems;

  void *array_val;

  array_val = mti_GetArraySignalValue(sigid, 0);
  num_elems = mti_TickLength(sigtype);

  mtiInt32T *val = (mtiInt32T *)array_val;
  for (i = 0; i < num_elems; i++)
  {
    mti_PrintFormatted("  %d", val[i]);
  }
  mti_VsimFree(array_val);
}

// Print the values of an int array signal
static void printArrayLength(mtiSignalIdT sigid)
{
  int i;
  mtiInt32T num_elems;

  mtiTypeIdT sigtype;

  sigtype = mti_GetSignalType(sigid);
  num_elems = mti_TickLength(sigtype);

  mti_PrintFormatted("Array Size of %s is %d \n", mti_GetSignalName(sigid), num_elems);
}

// Print the type of the signal
static void printSignalInfo(mtiSignalIdT sigid)
{
  mtiTypeIdT sigtype;
  mti_PrintFormatted("Signal %s ", mti_GetSignalName(sigid));
  sigtype = mti_GetSignalType(sigid);
  switch (mti_GetTypeKind(sigtype))
  {
  case MTI_TYPE_SCALAR:
    mti_PrintFormatted("is of type INTEGER\n");
    break;
  case MTI_TYPE_ENUM:
    mti_PrintFormatted("is of type ENUMERATION\n");
    break;
  case MTI_TYPE_PHYSICAL:
    mti_PrintFormatted("is of type PHYSICAL\n");
    break;
  case MTI_TYPE_REAL:
    mti_PrintFormatted("is of type REAL\n");
    break;
  case MTI_TYPE_TIME:
    mti_PrintFormatted("is of type TIME\n");
    break;
  case MTI_TYPE_ARRAY:
    mti_PrintFormatted("is of type ARRAY\n");
    break;
  case MTI_TYPE_RECORD:
    mti_PrintFormatted("is of type RECORD\n");
    break;
  default:
    mti_PrintFormatted("is of type UNKNOWN\n");
    break;
  }
}

// Print the values of a 2D int array
static void print2DInt(mtiSignalIdT sigid, mtiInt32T signal_length)
{
  int i;
  mtiSignalIdT *elem_list;
  elem_list = mti_GetSignalSubelements(sigid, 0);
  mti_PrintFormatted("Signal 'i' length is %d\n", signal_length);
  for (i = 0; i < signal_length; i++)
  {
    int j = 0;
    mtiInt32T *array_val;
    mtiTypeIdT type;
    mtiInt32T siglen;
    array_val = (mtiInt32T *)mti_GetArraySignalValue(elem_list[i], 0);
    type = mti_GetSignalType(elem_list[i]);
    siglen = mti_TickLength(type);
    mti_PrintFormatted("Signal 'j' length is %d\n", siglen);
    for (j = 0; j < siglen; j++)
    {
      mti_PrintFormatted("\t\tSignal value of signal %s[%d,%d] = %d\n", mti_GetSignalName(sigid), i, j, array_val[j]);
    }
    mti_VsimFree(array_val);
  }
  mti_PrintFormatted("\n");
  // Free memory
  mti_VsimFree(elem_list);
}

int **read2DArray(mtiSignalIdT sigid, mtiInt32T signal_length)
{
  // Allocate an array of pointers to represent rows
  mtiInt32T **array = new mtiInt32T *[signal_length];
  mtiSignalIdT *elem_list;
  elem_list = mti_GetSignalSubelements(sigid, 0);
  mti_PrintFormatted("Reading values for signal %s\n", mti_GetSignalName(sigid));
  mti_PrintFormatted("\tSignal has %d rows.\n", signal_length);
  for (int i = 0; i < signal_length; ++i)
  {
    mtiInt32T *array_val;
    mtiTypeIdT type;
    mtiInt32T siglen;
    type = mti_GetSignalType(elem_list[i]);
    siglen = mti_TickLength(type);
    // Allocate an array for each row and initialize with the initial value
    array[i] = new int[siglen];
    array_val = (mtiInt32T *)mti_GetArraySignalValue(elem_list[i], 0);
    mti_PrintFormatted("Signal 'j' length is %d\n", siglen);
    for (int j = 0; j < siglen; ++j)
    {
      array[i][j] = array_val[j];
    }
  }
  return array;
}

// Function to deallocate the 2D array
static void delete2DArray(int **array, int rows)
{
  for (int i = 0; i < rows; ++i)
  {
    delete[] array[i];
  }
  delete[] array;
}

// Function to deallocate the 2D array
static void delete2DArray(double **array, int rows)
{
  for (int i = 0; i < rows; ++i)
  {
    delete[] array[i];
  }
  delete[] array;
}

// Print the values of a 1D int array
static void print1DInt(mtiSignalIdT sigid)
{
  int i;
  mtiInt32T *array_val;
  mtiTypeIdT type;
  mtiInt32T siglen;
  array_val = (mtiInt32T *)mti_GetArraySignalValue(sigid, 0);
  type = mti_GetSignalType(sigid);
  siglen = mti_TickLength(type);
  mti_PrintFormatted("Signal 'i' length is %d\n", siglen);
  for (i = 0; i < siglen; i++)
  {
    mti_PrintFormatted("\t\tSignal value of signal %s[%d] = %d\n", mti_GetSignalName(sigid), i, array_val[i]);
  }
  mti_VsimFree(array_val);
  mti_PrintFormatted("\n");
}

static mtiInt32T *read1DArray(mtiSignalIdT sigid)
{
  mtiInt32T *array_val;
  array_val = (mtiInt32T *)mti_GetArraySignalValue(sigid, 0);
  return array_val;
}

// Assign values in up to 1D VHDL array
static void driveSig(mtiDriverIdT sigid, void *val)
{
  mti_ScheduleDriver(sigid, (mtiLongT)val, convertToNS(0), MTI_TRANSPORT);
}

// Calling a python function *pFunc with arguments *pArgs
// returns PyObject *
static PyObject *callPy(PyObject *pFunc, PyObject *pArgs)
{
  PyObject *pResult = NULL;
  // If function exists call the function
  if (pFunc != NULL)
  {
    mti_PrintFormatted("\t\t Calling Py Function with args.\n");
    pResult = PyObject_CallObject(pFunc, pArgs);
    if (pResult != NULL)
    {
      // Convert the result back to C++ int
      // int result = PyLong_AsLong(pResult);
      return pResult; // Return the result of the Python function
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
  return pResult;
}

// Create and return a 2D python list of float numbers
static PyObject *pyList2D(double **values, int row, int cols)
{
  PyObject *pArray = PyList_New(row);
  for (int i = 0; i < row; i++)
  {
    PyObject *pRow = PyList_New(cols);
    for (int j = 0; j < cols; j++)
    {
      PyList_SetItem(pRow, j, PyFloat_FromDouble(values[i][j]));
    }
    PyList_SetItem(pArray, i, pRow);
  }
  return pArray;
}

// Create and return a 1D python list of float numbers
static PyObject *pyList1D(double *values, int row)
{
  PyObject *pArray = PyList_New(row);
  for (int i = 0; i < row; i++)
  {

    PyList_SetItem(pArray, i, PyFloat_FromDouble(values[i]));
  }
  return pArray;
}

// Turn an integer 2D array to double 2D array between 0 and 1
// This function changes the integer values to float, the integer values from the VHDL
// has to be normalized to a range between -1 and 1 to be programmed in the crossbar.
// If the mapping need to change, the function intToNormalizedReal has to be modified.
static double **intToFloat2D(int **values, int row, int cols)
{
  mti_PrintFormatted("\t\tCalculating 2D float array: \n");
  double **float_array = new double *[row];
  for (int i = 0; i < row; ++i)
  {
    float_array[i] = new double[cols];
    for (int j = 0; j < cols; ++j)
    {
      float_array[i][j] = intToNormalizedReal(values[i][j]);
      mti_PrintFormatted("\t\t\t%G ", float_array[i][j]);
    }
    mti_PrintFormatted("\n ");
  }
  return float_array;
}

// Turn an integer 1D array to double 1D array between 0 and 1
static double *intToFloat1D(int *values, int row)
{
  double *float_array = new double[row];
  mti_PrintFormatted("\t\tCalculating 1D float array: \n");
  for (int i = 0; i < row; ++i)
  {
    float_array[i] = intToNormalizedReal(values[i]);
    mti_PrintFormatted("\t\t\t%G \n", float_array[i]);
  }
  return float_array;
}
#endif
