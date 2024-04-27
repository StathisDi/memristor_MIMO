#ifndef UTIL_H
#define UTIL_H
#include <mti.h>
#include <Python.h>
#include <limits.h>

// Function that normalize an integer to a symmetric range -1 to 1
double intToNormalizedRealSymmetric(int x)
{
  if (x == INT_MIN)
  {
    return -1.0;
  }
  else
  {
    return x / (double)(x < 0 ? -INT_MIN : INT_MAX);
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

// Get subarray of signal
static void *GetSubArrayVal(mtiSignalIdT sigid)
{
  void *array_val;
  array_val = mti_GetArraySignalValue(sigid, 0);
  return array_val;
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

#endif
