#!/bin/env dls-python2.6

from pkg_resources import require
require("dls_serial_sim")
from dls_serial_sim import serial_device, CreateSimulation
import time, re, sys
from random import random

sys.path.append(os.path.join(__file__, "..", "..", "zebraApp", "src"))
from zebraTool import zebraRegs

class zebra(serial_device):

    InTerminator = "\n"
    OutTerminator = "\n"    
    ui = None
    #diagLevel = 4
    
    def __init__(self):    
        self.i = 0
        self.memory = dict((x, 0) for x in self.regs.names())
        self.schedule(self.poll,0.1)
        self.armed = 0
        self.regs = zebraRegs()           
    
    def poll(self):
        if self.armed:            
            ret = "P%08X" % (self.i*50)
            self.i+=1
            bits = self.memory[self.regs.reg("PC_BIT_CAP")]            
            for i in range(16):
                if (bits >> i) & 1:
                    ret += "%08X" % (random() * self.i)
            return ret

    def reply(self, command):
        command = command.strip("\r")
        if command == "S":
            time.sleep(0.1)
            return "SOK"            
        elif command.startswith("R") and len(command) == 3:
            addr = int(command[1:3], 16)
            if addr in self.memory:                
                return "R%02X%04X" % (addr, self.memory[addr])
            else:
                return "E1R%02X" % addr
        elif command.startswith("W") and len(command) == 7:
            addr = int(command[1:3], 16)
            value = int(command[3:7], 16)
            time.sleep(0.01)
            if addr in self.memory:
                self.memory[addr] = value
                ret = ""
                if self.regs.name(addr) == "PC_ARM":
                    self.armed = 1
                    ret = "PR\n"
                if self.regs.name(addr) == "PC_DISARM":
                    self.armed = 0
                    ret = "PX\n"
                return ret + "W%02XOK" % addr
            else:
                return "E1W%02X" % addr
        else:
            return "E0"

if __name__=="__main__":
    CreateSimulation(zebra)
    raw_input()
