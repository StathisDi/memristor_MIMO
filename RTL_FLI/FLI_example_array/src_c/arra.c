#include <mti.h>

typedef struct varInfoT_tag
{
  struct varInfoT_tag *next;
  char *name;
  mtiSignalIdT varid;
  mtiTypeIdT typeid;
} varInfoT;

typedef struct
{
  varInfoT *var_info; /* List of variables. */
  mtiProcessIdT proc; /* Test process id. */
} instanceInfoT;

static void printValue(mtiVariableIdT varid, mtiTypeIdT vartype, int indent)
{
  // Get the type of the variable to print
  switch (mti_GetTypeKind(vartype))
  {
  case MTI_TYPE_ENUM:     // Enumeration
  case MTI_TYPE_PHYSICAL: // Physical (not sure but I believe it has to do with physical units)
  case MTI_TYPE_SCALAR:   // Integer variable
  {
    mtiInt32T scalar_val;
    scalar_val = mti_GetVarValue(varid);      // Get value of the specific variable (of type integer)
    mti_PrintFormatted("  %d\n", scalar_val); // Print the value
  }
  break;
  case MTI_TYPE_ARRAY: // Array type
  {
    int i;
    mtiInt32T num_elems;
    mtiTypeIdT elem_type;
    mtiTypeKindT elem_typekind;
    void *array_val;

    /*

    mti_GetArrayVarValue() returns the value of an array-type VHDL variable.
    If the buffer parameter is NULL, then mti_GetArrayVarValue() returns a pointer to the value, which should be treated as read-only data. (Changing the value pointed to by this pointer actually changes the variable's value.) This pointer must not be freed.
    If the buffer parameter is not NULL, then mti_GetArrayVarValue() copies the value into the buffer parameter and also returns a pointer to it. The appropriate length of the buffer parameter can be determined by calling mti_TickLength() on the type of the array variable.
    The array value is interpreted as follows:

    For a subelement of type : The value should be cast to
    Enum                     : (char *) if <= 256 values
                               (mtiInt32T *) if > 256 values
    Physical                 : (mtiInt32T *)
    Real                     : (double *)
    Scalar (Integer)         : (mtiInt32T *)
    Time                     : (mtiTime64T *)

    */
    array_val = mti_GetArrayVarValue(varid, 0);   // returns pointer to the values since the second parameter is 0? Otherwise it copies the value of the variable to the buffer
    num_elems = mti_TickLength(vartype);          // Get the length of the array (length of the variable (type'HIGH - type'LOW + 1))
    elem_type = mti_GetArrayElementType(vartype); // returns a handle to the type ID for the subelements of the specified array type. If the array_type parameter is not a handle to an array type, then NULL is returned.
    elem_typekind = mti_GetTypeKind(elem_type);   // returns the kind of the specified VHDL or SystemC type. The returned value is one of the following:
    /*
    type_kind        : VHDL type
    MTI_TYPE_SCALAR  : Integer
    MTI_TYPE_ARRAY   : Array
    MTI_TYPE_RECORD  : Record
    MTI_TYPE_ENUM    : Enumeration
    MTI_TYPE_PHYSICAL: Physical
    MTI_TYPE_REAL    : Real
    MTI_TYPE_ACCESS  : Access
    MTI_TYPE_FILE    : File
    MTI_TYPE_TIME    : Time
    */
    switch (elem_typekind) // Select action based on the element type
    {
    case MTI_TYPE_ENUM:
    {
      char **enum_values;
      enum_values = mti_GetEnumValues(elem_type);
      if (mti_TickLength(elem_type) > 256)
      {
        mtiInt32T *val = array_val;
        for (i = 0; i < num_elems; i++)
        {
          mti_PrintFormatted("  %s", enum_values[val[i]]);
        }
      }
      else
      {
        char *val = array_val;
        for (i = 0; i < num_elems; i++)
        {
          mti_PrintFormatted("  %s", enum_values[val[i]]);
        }
      }
    }
    break;
    case MTI_TYPE_PHYSICAL:
    case MTI_TYPE_SCALAR:
    {
      mtiInt32T *val = array_val;
      for (i = 0; i < num_elems; i++)
      {
        mti_PrintFormatted("  %d", val[i]);
      }
    }
    break;
    case MTI_TYPE_ARRAY:
      mti_PrintMessage("  ARRAY");
      break;
    case MTI_TYPE_RECORD:
      mti_PrintMessage("  RECORD");
      break;
    case MTI_TYPE_REAL:
    {
      double *val = array_val;
      for (i = 0; i < num_elems; i++)
      {
        mti_PrintFormatted("  %g", val[i]);
      }
    }
    break;
    case MTI_TYPE_TIME:
    {
      mtiTime64T *val = array_val;
      for (i = 0; i < num_elems; i++)
      {
        mti_PrintFormatted("  [%d,%d]",
                           MTI_TIME64_HI32(val[i]),
                           MTI_TIME64_LO32(val[i]));
      }
    }
    break;
    default:
      break;
    }
    mti_PrintFormatted("\n");
  }
  break;
  case MTI_TYPE_RECORD: // Record type
  {
    int i;
    mtiVariableIdT *elem_list;
    mtiInt32T num_elems;
    /*
    mti_GetVarSubelements() returns an array containing the variable IDs of the subelements of the specified VHDL composite variable. If the buffer parameter is NULL, mti_GetVarSubelements() allocates memory for the array and returns a pointer to it. The caller is responsible for freeing this memory with mti_VsimFree(). If the buffer parameter is not NULL, then mti_GetVarSubelements() copies the subelement variable IDs into the buffer and also returns the buffer parameter. The length for the buffer parameter and the return value can be determined by calling mti_TickLength() on the type of the variable_id.
    mti_GetVarSubelements() returns NULL if the variable_id parameter is not a handle to a VHDL composite variable.
    The internal representation of multi-dimensional arrays is the same as arrays of arrays. For example, array a(x,y,z) is accessed in the same manner as a(x)(y)(z). In order to get to the scalar subelements of an array of arrays, you must use mti_GetVarSubelements() on each level of the array until reaching the scalar subelements.
    TODO Should this be used with multi-dimensional arrays or can we use the MTI_TYPE_ARRAY style?
    */
    elem_list = mti_GetVarSubelements(varid, 0);
    num_elems = mti_GetNumRecordElements(vartype); // returns the number of subelements in the specified VHDL record type.
    mti_PrintFormatted("\n");
    for (i = 0; i < num_elems; i++)
    {
      mti_PrintFormatted("%*c", indent, ' ');
      printValue(elem_list[i], mti_GetVarType(elem_list[i]),
                 indent + 2);
    }
    mti_VsimFree(elem_list);
  }
  break;
  case MTI_TYPE_REAL: // Real type
  {
    double real_val;
    /*
    mti_GetVarValueIndirect() returns the value of a variable of any type except record. mti_GetVarValueIndirect() must be used for scalar variables of type real and time.
    If the buffer parameter is NULL, mti_GetVarValueIndirect() returns a pointer to the value, which must be treated as read-only data and must not be freed.
    If the buffer parameter is not NULL, mti_GetVarValueIndirect() copies the value in the buffer parameter and also returns the buffer parameter.
    */
    mti_GetVarValueIndirect(varid, &real_val);
    mti_PrintFormatted("  %g\n", real_val);
  }
  break;
  case MTI_TYPE_TIME: // Time type
  {
    mtiTime64T time_val;
    mti_GetVarValueIndirect(varid, &time_val);
    mti_PrintFormatted("  [%d,%d]\n", MTI_TIME64_HI32(time_val), MTI_TIME64_LO32(time_val));
  }
  break;
  default:
    mti_PrintMessage("\n");
    break;
  }
}

static void checkValues(void *inst_info)
{
  instanceInfoT *inst_data = (instanceInfoT *)inst_info;
  varInfoT *varinfo;

  // mti_NowUpper Gets the high order 32 bits of the 64-bit current simulation time.
  // mti_Now      Gets the low order 32 bits of the 64-bit current simulation time.
  // Returns mtiInt32T
  mti_PrintFormatted("Time [%d,%d]:\n", mti_NowUpper(), mti_Now());

  for (varinfo = inst_data->var_info; varinfo; varinfo = varinfo->next)
  {
    mti_PrintFormatted(" Variable %s:", varinfo->name);
    printValue(varinfo->varid, varinfo->typeid, 4);
  }

  mti_ScheduleWakeup(inst_data->proc, 5);
}

// This function creates a record for a variable based on its variable id.
static varInfoT *setupVariable(mtiVariableIdT varid)
{
  varInfoT *varinfo;

  varinfo = (varInfoT *)mti_Malloc(sizeof(varInfoT));
  varinfo->varid = varid;
  varinfo->name = mti_GetVarName(varid);
  varinfo->typeid = mti_GetVarType(varid);
  varinfo->next = 0;

  return (varinfo);
}

// This function initializes the instances and sets up the memory of the module in the simulator.
// It creates a process for the function "checkValues" which is the main function of the module.
static void initInstance(void *param)
{
  // Data for the instance
  instanceInfoT *inst_data;
  // Id of the procces
  mtiProcessIdT procid;
  // Id of the variable
  mtiVariableIdT varid;
  varInfoT *curr_info;
  // Values of the variables
  varInfoT *varinfo;

  /*
    mti_Malloc()
    Allocates simulator-managed memory

    memptr = mti_Malloc( size )
    Arguments
    size : unsigned long : The size in bytes of the memory to be allocated

    Return Values
    memptr : void * : A pointer to the allocated memory

    Description
    mti_Malloc() allocates a block of memory of the specified size from an internal simulator memory pool and returns a pointer to it. The simulator initializes the memory to zero, and automatically checkpoints memory allocated by mti_Malloc    (). On restore, this memory is guaranteed to be restored to the same location with the values it contained at the time of the checkpoint. You can free this memory only by mti_Free().
    mti_Malloc() automatically checks for a NULL pointer. In the case of an allocation error, mti_Malloc() issues the following error message and aborts the simulation:

  */
  inst_data = mti_Malloc(sizeof(instanceInfoT)); // Allocate memory for the module in the simulator

  // Set the variables info to 0
  inst_data->var_info = 0;

  // This for loop goes through all the processes in the VHDL design (top region) for as long as there are processes
  for (procid = mti_FirstProcess(mti_GetTopRegion()); procid; procid = mti_NextProcess())
  {
    // This loop goes through all the variables in each of the processes
    for (varid = mti_FirstVar(procid); varid; varid = mti_NextVar())
    {
      // if there is no variable record created, then create one.
      // in another case update the existing one (it updates the trace)
      varinfo = setupVariable(varid);
      if (inst_data->var_info == 0)
      {
        inst_data->var_info = varinfo;
      }
      else
      {
        curr_info->next = varinfo;
      }
      curr_info = varinfo;
    }
  }

  /*
  process_id = mti_CreateProcess( name, func, param )
  Arguments
  name : char * : The name of the new VHDL process; OPTIONAL - can be NULL
  func : mtiVoidFuncPtrT : A pointer to the function that will be executed as the body of the new process
  param : void * :A parameter to be passed to the function; OPTIONAL - can be NULL

  Return Values
  process_id : mtiProcessIdT : A handle to the new VHDL process or NULL if there is an error

  Description
  mti_CreateProcess() creates a new VHDL process with the specified name. If the name is non-NULL, then it appears in the Process window of the simulator; otherwise, it does not. The simulator calls the specified function along with its parameter whenever the process executes. The process executes either at the time specified in a call to mti_ScheduleWakeup() or whenever one of the signals to which it is sensitive changes (see mti_Sensitize()).

  If you create the process during elaboration from inside of a foreign architecture instance, then the simulator aumtomatically execugtes the process once at time zero after initializing all signals. If you create the process either after elaboration is complete or from any other context (such as from an initialization function that executes as a result of the loading of a foreign shared library by the -foreign option to vsim), then the simulation does not run the process automatically but must be scheduled or sensitized.

  mti_CreateProcess() allows you to create a process with an illegal HDL name. This is useful for integrators who provide shared libraries for use by end customers, as this is an easy way to avoid potential name conflicts with HDL processes. We recommend the following naming style:

  <PREFIX_name>

  where PREFIX is 3 or 4 characters that denote your software (to avoid name conflicts with other integration software) and name is the name of the process. Enclosing the entire name in angle brackets makes it an illegal HDL name. For example, <MTI_foreign_architecture>.

  We strongly recommend that you do not use characters in the name that will cause Tcl parsing problems. This includes spaces, the path separator (normally ’/’ or ’.’), square brackets ([]), and dollar signs ($). If you must use these characters, then create an escaped name by putting a backslash (\) at both ends of the name.
  */
  inst_data->proc = mti_CreateProcess("Test Process", checkValues,
                                      (void *)inst_data);
  /*
    mti_ScheduleWakeup64( process_id, delay )
    - process_id : mtiProcessIdT : A handle to a VHDL process
    - delay      : mtiTime64T    : The delay to be used in terms of the current simulator resolution limit
    Schedules a VHDL process to wake up at a specific time using a 64-bit delay.

    mti_ScheduleWakeup() schedules the specified process to be called after the specified 64-bit delay. A process can have no more than one pending wake-up call. A call to mti_ScheduleWakeup64() cancels a prior pending wake-up call for the specified process regardless of the delay values.
    The specified delay value is multiplied by the current simulator resolution limit. For example, if vsim was invoked with -t 10ns and the delay was specified as 5, then the actual delay would be 50 ns.
    The process_id must be a handle to a process that was created by mti_CreateProcess() or mti_CreateProcessWithPriority().
  */
  mti_ScheduleWakeup(inst_data->proc, 6);
}

/*

  If we require to work with signals:

  static void initInstance( void * param )
{
  mtiSignalIdT sigid;
  mtiTypeIdT   typeid;

  mti_PrintMessage( "Design Signals:\n" );
  for ( sigid = mti_FirstSignal( mti_GetTopRegion() );
        sigid; sigid = mti_NextSignal() ) {
    typeid = mti_GetSignalType( sigid );
    mti_PrintFormatted( "%14s: type %-12s; length = %d\n",
                       mti_GetSignalName( sigid ), getTypeStr( typeid ),
                       mti_TickLength( typeid ));
  }
}


*/

// Main function that links to an architecture
void initForeign(
    mtiRegionIdT region,         /* The ID of the region in which this     */
                                 /* foreign architecture is instantiated.  */
    char *param,                 /* The last part of the string in the     */
                                 /* foreign attribute.                     */
    mtiInterfaceListT *generics, /* A list of generics for the foreign model.*/
    mtiInterfaceListT *ports     /* A list of ports for the foreign model.   */
)
{
  /*
    mti_AddLoadDoneCB( func, param );
    - func  : mtiVoidFuncPtrT : A pointer to a function to be called at the end of elaboration
    - param : void *          : A parameter to be passed to the function; OPTIONAL - can be NULL

    Description
    mti_AddLoadDoneCB() adds the specified function to the elaboration done callback list. You can add the same function multiple times, with possibly a different parameter each time. At the end of elaboration, all callbacks in the list are called with their respective parameters. These callbacks are also called at the end of a restart or a cold restore (vsim ‑restore).
    You must call mti_AddLoadDoneCB() from a foreign initialization function in order for the callback to take effect. You specify a foreign initialization function either in the foreign attribute string of a foreign architecture or in the -foreign string option of a vsim command.
  */
  mti_AddLoadDoneCB(initInstance, 0);
}