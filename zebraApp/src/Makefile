TOP=../..

include $(TOP)/configure/CONFIG

# -------------------------------
# Build an Diamond Support Module
# -------------------------------

LIBRARY_IOC += zebra

# xxxRecord.h will be created from xxxRecord.dbd
#DBDINC += xxx.h

# xxxRecord.dbd will be installed into <top>/dbd
DBD += zebraSupport.dbd
DBD += zebra_vdct.dbd
zebra_vdct_DBD += base.dbd
zebra_vdct_DBD += asyn.dbd
zebra_vdct_DBD += ADSupport.dbd
zebra_vdct_DBD += busySupport.dbd
zebra_vdct_DBD += motorSupport.dbd
zebra_vdct_DBD += devSoftMotor.dbd

# The following are compiled and added to the support library
zebra_SRCS += zebra.cpp
zebra_SRCS += ini.c

INCLUDE += zebraRegs.h

# We need to link against the EPICS Base libraries
#xxx_LIBS += $(EPICS_BASE_IOC_LIBS)

DATA += zebra_sim.py

include $(TOP)/configure/RULES

