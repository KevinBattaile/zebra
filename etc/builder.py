from iocbuilder import AutoSubstitution, Device
from iocbuilder.modules.asyn import Asyn, AsynPort, _AsynOctetInterface
from iocbuilder.modules.ADCore import ADCore, ADBaseTemplate, makeTemplateInstance, includesTemplates
from iocbuilder.modules.busy import Busy
from iocbuilder.modules.motor import MotorLib
from iocbuilder.arginfo import *

@includesTemplates(ADBaseTemplate)
class _zebraTemplate(AutoSubstitution):
    ## Parse this template file for macros
    TemplateFile = 'zebra.template'

class zebra(AsynPort):
    '''Controls the zebra signal converter box'''
    DbdFileList = ["zebraSupport"]
    LibFileList = ["zebra"]
    UniqueName = "PORT"
    Dependencies = (ADCore, MotorLib)

    def __init__(self, PORT, serialPort, NELM=100000, MAXBUF=5, MAXMEM=0,
                 **args):
        # Init the superclass (AsynPort)
        self.__super.__init__(PORT)
        # Update the attributes of self from the commandline args
        self.__dict__.update(locals())
        # Make an instance of our template
        R = args["Q"] + ":"
        makeTemplateInstance(_zebraTemplate, locals(), args)

    def Initialise(self):
        print '#zebraConfig(Port, SerialPort, MaxPosCompPoints, MaxBuffers, MaxMemory)'
        print 'zebraConfig("%(PORT)s", "%(serialPort)s", %(NELM)s, %(MAXBUF)d, %(MAXMEM)d)' % self.__dict__

    ArgInfo = ADBaseTemplate.ArgInfo.filtered(without = ["R"]) + \
        _zebraTemplate.ArgInfo.filtered(without=["EMPTY", "R"]) + \
        makeArgInfo(
            __init__,
            PORT = Simple("Driver port name"),
            serialPort = Ident ("Serial port name", _AsynOctetInterface),
            NELM = Simple("Number of elements in position capture arrays", int),
            MAXBUF = Simple("Maximum number of buffers (areaDetector)", int),
            MAXMEM = Simple("Maximum memory (areaDetector)", int))

class zebraLastDivDiff(AutoSubstitution):
    '''Makes a record pointing to DIV$(DIV) that will display the difference
    between the last two DIV readings in position compare mode'''
    TemplateFile = 'zebraLastDivDiff.template'
