#!/bin/env dls-python
from pkg_resources import require
require("pyserial")
from serial import Serial
import os, re
from ConfigParser import ConfigParser

class zebraRegs:
    bus_lookup = [
    "DISCONNECT",
    "IN1_TTL",
    "IN1_NIM",
    "IN1_LVDS",
    "IN2_TTL",
    "IN2_NIM",
    "IN2_LVDS",
    "IN3_TTL",
    "IN3_OC",
    "IN3_LVDS",
    "IN4_TTL",
    "IN4_CMP",
    "IN4_PECL",
    "IN5_ENCA",
    "IN5_ENCB",
    "IN5_ENCZ",
    "IN5_CONN",
    "IN6_ENCA",
    "IN6_ENCB",
    "IN6_ENCZ",
    "IN6_CONN",
    "IN7_ENCA",
    "IN7_ENCB",
    "IN7_ENCZ",
    "IN7_CONN",
    "IN8_ENCA",
    "IN8_ENCB",
    "IN8_ENCZ",
    "IN8_CONN",
    "PC_ARM",
    "PC_GATE",
    "PC_PULSE",
    "AND1",
    "AND2",
    "AND3",
    "AND4",
    "OR1",
    "OR2",
    "OR3",
    "OR4",
    "GATE1",
    "GATE2",
    "GATE3",
    "GATE4",
    "DIV1_OUTD",
    "DIV2_OUTD",
    "DIV3_OUTD",
    "DIV4_OUTD",
    "DIV1_OUTN",
    "DIV2_OUTN",
    "DIV3_OUTN",
    "DIV4_OUTN",
    "PULSE1",
    "PULSE2",
    "PULSE3",
    "PULSE4",
    "QUAD_OUTA",
    "QUAD_OUTB",
    "CLOCK_1KHZ",
    "CLOCK_1MHZ",
    "SOFT_IN1",
    "SOFT_IN2",
    "SOFT_IN3",
    "SOFT_IN4"]  
    
    def __init__(self):
        reg_lookup_str = open(os.path.realpath(os.path.join(__file__, "..", "zebraRegs.h"))).read()
        self.reg_lookup = {}
        self.name_lookup = {}
        self.reg_type = {}
        for line in re.sub(r"/\*(.|[\r\n])*?\*/", "", reg_lookup_str).splitlines():
            match = re.match(r'\s*\{\s*"([^"]*)"\s*,\s*(\w*),\s*(\w*)\s*\}', line) #,\s*(\w*)\w*}        
            if match:
                name, num, typ = match.groups()
                reg = int(num, 0)
                self.name_lookup[reg] = name
                self.reg_lookup[name] = reg
                self.reg_type[reg] = typ

    def regs(self):
        return self.name_lookup.keys()

    def reg(self, name):
        return self.reg_lookup[name]
                
    def names(self):
        return self.reg_lookup.keys()
    
    def name(self, reg):
        return self.name_lookup[reg]

    def type(self, reg):
        return self.reg_type[reg]

    def bus_index(self, name):
        return self.bus_lookup.index(name)

    def bus_name(self, index):
        return self.bus_lookup[index]

class zebraTool:
    # The serial port object
    port = None
    deftimeout = 10
    
    def __init__(self, portstr="/dev/ttyS0"):
        self.port = Serial(portstr, 115200, timeout=self.deftimeout)
        self.regs = zebraRegs()
    
    def getExpected(self, expected):
        response = self.port.readline().rstrip("\n")
        assert response, "Zebra timed out when expecting '%s'" % expected
        assert response.startswith(expected), "Zebra response '%s' should start with '%s'" %(response, expected)            
        return response
    
    def maybeGet(self, expected, timeout=0.1):
        self.port.timeout=0.1
        response = self.port.readline().rstrip("\n")
        self.port.timeout=self.deftimeout
        assert not response or response.startswith(expected), "Zebra response '%s' should start with '%s'" %(response, expected)            
        return response  
    
    def readReg(self, reg):
        """Takes reg and reads its values from zebra"""
        if reg.upper() in self.regs.names():
            reg = self.regs.reg(reg.upper())
        cmd = "R%02X" % reg
        self.port.write("%s\n" % cmd)        
        response = self.getExpected(cmd)
        out = int(response[len(cmd):], 16)
        if self.regs.type(reg) == "regMux":
            return self.regs.bus_name(out)
        return out
        
    def writeReg(self, reg, value, writecmd = True):
        """Takes reg in hex and writes its value to zebra"""
        if reg.upper() in self.regs.names():
            reg = self.regs.reg(reg.upper())        
        if not writecmd and self.regs.type(reg) not in ("regMux", "regRW"):
            return
        if self.regs.type(reg) == "regMux" and type(value) == str:
            value = self.regs.bus_index(value)
        self.port.write("W%02X%04X\n" % (reg, value))
        self.getExpected("W%02XOK" % reg)

    def systemBus(self):
        """A list of strings that represent items on the system bus"""
        return self.regs.bus_lookup

    def getStatus(self, name):
        """Get the status of a named element on the system bus"""
        i = self.regs.bus_index(name)
        stat_reg = "SYS_STAT" + (["1LO", "1HI", "2LO", "2HI"][i / 16])
        stat_off = i % 16
        return self.readReg(stat_reg) >> stat_off & 1          

    def writeCommand(self, cmd):
        """Write a command to zebra and return the result"""
        self.port.write("%s\n" % cmd)
        self.getExpected("%sOK" % cmd)        
        
    def uploadFile(self, fname):
        """Upload an ini file to a zebra"""
        assert os.path.isfile(fname), "File %s does not exist" % fname
        parser = ConfigParser()
        parser.read(fname)
        assert parser.has_section("regs"), "Cannot find reg section in %s" % fname
        for reg, value in parser.items("regs"):
            self.writeReg(reg, int(value), writecmd=False)
           
    def save(self):
        """Save the state of the zebra to flash"""
        self.writeCommand("S")

    def reset(self):
        """Reset zebra"""
        self.writeReg("SYS_RESET", 1)
    
    def getEnc(self, enc):
        """Uses position compare to get an encoder or div value"""
        self.writeReg("PC_DISARM", 1)
        self.writeReg("PC_BIT_CAP", 2 ** enc)
        # time gate
        self.writeReg("PC_GATE_SEL", 1)
        self.writeReg("PC_GATE_STARTLO", 0)
        self.writeReg("PC_GATE_STARTHI", 0)        
        self.writeReg("PC_GATE_WIDLO", 1)
        self.writeReg("PC_GATE_WIDHI", 0)                                                        
        self.writeReg("PC_GATE_NGATELO", 1)
        self.writeReg("PC_GATE_NGATEHI", 0)          
        # time pulse
        self.writeReg("PC_PULSE_SEL", 1)
        self.writeReg("PC_PULSE_STARTLO", 0)
        self.writeReg("PC_PULSE_STARTHI", 0)        
        self.writeReg("PC_PULSE_DLYLO", 0)
        self.writeReg("PC_PULSE_DLYHI", 0)                        
        # start acq
        self.writeReg("PC_ARM", 1)
        self.getExpected("PR")  
        P = self.getExpected("P")
        self.getExpected("PX") 
        return int(P[1:], 16) 
        
