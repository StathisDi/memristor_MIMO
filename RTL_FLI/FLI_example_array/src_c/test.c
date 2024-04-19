#include <mti.h>

typedef struct signalInfoT_tag
{
  struct signalInfoT_tag *next;
  char *name;
  mtiSignalIdT sigid;
  mtiTypeIdT typeid;
} signalInfoT;

typedef struct
{
  signalInfoT *sig_info; /* List of signals. */
  mtiProcessIdT proc;    /* Test process id. */
} instanceInfoT;

static void printValue(mtiSignalIdT sigid, mtiTypeIdT sigtype, int indent)
{
  switch (mti_GetTypeKind(sigtype))
  {
  case MTI_TYPE_ENUM:
  {
    char **enum_values;
    mtiInt32T scalar_val;
    scalar_val = mti_GetSignalValue(sigid);
    enum_values = mti_GetEnumValues(sigtype);
    mti_PrintFormatted("  %s\n", enum_values[scalar_val]);
  }
  break;
  case MTI_TYPE_PHYSICAL:
  case MTI_TYPE_SCALAR:
  {
    mtiInt32T scalar_val;
    scalar_val = mti_GetSignalValue(sigid);
    mti_PrintFormatted("  %d\n", scalar_val);
  }
  break;
  case MTI_TYPE_ARRAY:
  {
    int i;
    mtiInt32T num_elems;
    mtiTypeIdT elem_type;
    mtiTypeKindT elem_typekind;
    void *array_val;

    array_val = mti_GetArraySignalValue(sigid, 0);
    num_elems = mti_TickLength(sigtype);
    elem_type = mti_GetArrayElementType(sigtype);
    elem_typekind = mti_GetTypeKind(elem_type);
    switch (elem_typekind)
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
    mti_VsimFree(array_val);
  }
  break;
  case MTI_TYPE_RECORD:
  {
    int i;
    mtiSignalIdT *elem_list;
    mtiInt32T num_elems;
    elem_list = mti_GetSignalSubelements(sigid, 0);
    num_elems = mti_GetNumRecordElements(sigtype);
    mti_PrintFormatted("\n");
    for (i = 0; i < num_elems; i++)
    {
      mti_PrintFormatted("%*c", indent, ' ');
      printValue(elem_list[i], mti_GetSignalType(elem_list[i]),
                 indent + 2);
    }
    mti_VsimFree(elem_list);
  }
  break;
  case MTI_TYPE_REAL:
  {
    double real_val;
    mti_GetSignalValueIndirect(sigid, &real_val);
    mti_PrintFormatted("  %g\n", real_val);
  }
  break;
  case MTI_TYPE_TIME:
  {
    mtiTime64T time_val;
    mti_GetSignalValueIndirect(sigid, &time_val);
    mti_PrintFormatted("  [%d,%d]\n",
                       MTI_TIME64_HI32(time_val),
                       MTI_TIME64_LO32(time_val));
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
  signalInfoT *siginfo;

  mti_PrintFormatted("Time [%d,%d]:\n", mti_NowUpper(), mti_Now());

  for (siginfo = inst_data->sig_info; siginfo; siginfo = siginfo->next)
  {
    mti_PrintFormatted("  Signal %s:", siginfo->name);
    printValue(siginfo->sigid, siginfo->typeid, 4);
  }

  mti_ScheduleWakeup(inst_data->proc, 5);
}

static signalInfoT *setupSignal(mtiSignalIdT sigid)
{
  signalInfoT *siginfo;

  siginfo = (signalInfoT *)mti_Malloc(sizeof(signalInfoT));
  siginfo->sigid = sigid;
  siginfo->name = mti_GetSignalNameIndirect(sigid, 0, 0);
  siginfo->typeid = mti_GetSignalType(sigid);
  siginfo->next = 0;

  return (siginfo);
}

static void initInstance(void *param)
{
  instanceInfoT *inst_data;
  mtiSignalIdT sigid;
  signalInfoT *curr_info;
  signalInfoT *siginfo;

  inst_data = mti_Malloc(sizeof(instanceInfoT));
  inst_data->sig_info = 0;

  for (sigid = mti_FirstSignal(mti_GetTopRegion());
       sigid; sigid = mti_NextSignal())
  {
    siginfo = setupSignal(sigid);
    if (inst_data->sig_info == 0)
    {
      inst_data->sig_info = siginfo;
    }
    else
    {
      curr_info->next = siginfo;
    }
    curr_info = siginfo;
  }

  inst_data->proc = mti_CreateProcess("Test Process", checkValues,
                                      (void *)inst_data);
  mti_ScheduleWakeup(inst_data->proc, 6);
}

void initForeign(
    mtiRegionIdT region,         /* The ID of the region in which this     */
                                 /* foreign architecture is instantiated.  */
    char *param,                 /* The last part of the string in the     */
                                 /* foreign attribute.                     */
    mtiInterfaceListT *generics, /* A list of generics for the foreign model.*/
    mtiInterfaceListT *ports     /* A list of ports for the foreign model.   */
)
{
  mti_AddLoadDoneCB(initInstance, 0);
}