#!/bin/env dls-python
from zebraTool import zebraTool
import zebraFirmwareTest
import os, re, time

def doHardwareTest(zebra, mismatch="BAD", match="OK", sleep=0.2):
    errors = 0
    version = zebra.readReg("SYS_VER")                    
    assert version >= 0x20, "Can only hardware test zebras with 0x20 firmware or higher"

    # first disconnect all the outputs
    for name in zebra.regs.names():
        if name.startswith("OUT"):
            zebra.writeReg(name, "DISCONNECT")   
    
    # now do the front panel inputs
    for i, signal in enumerate(zebra.systemBus()):
        # test inputs against outputs in system bus
        m = re.match(r"IN(\d)", signal)
        if m and int(m.group(1)) < 5:
            # find corresponding output
            if signal == "IN4_CMP":
                out = "OUT4_NIM"
            else:
                out = signal.replace("IN", "OUT")
            print "%40s"%("Testing %s and %s..." % (signal, out)),
            # set output to soft input
            zebra.writeReg(out, "SOFT_IN1")
            ret = match
            for expected in (1, 0):
                # check if we get the input on the system bus                                    
                # special for PECL
                if signal == "IN4_PECL":
                    # Latch the PECL inputs
                    zebra.writeReg("GATE1_INP1", signal)
                    # Reset on SOFT_IN2
                    zebra.writeReg("GATE1_INP2", "SOFT_IN2")
                    # Reset gate                        
                    zebra.writeReg("SOFT_IN", 2)                        
                    # Send pulse
                    zebra.writeReg("SOFT_IN", expected)
                    # Get pulse
                    if (zebra.getStatus("GATE1") != expected):
                        ret = mismatch                                            
                else:
                    zebra.writeReg("SOFT_IN", expected)                    
                    if (zebra.getStatus(signal) != expected):
                        ret = mismatch
                # slow it down so we can see it
                time.sleep(sleep)    
            zebra.writeReg(out, "DISCONNECT")
            if ret == "BAD":        
                errors += 1
            print ret

    # now do the encoder inputs
    for i in range(5,9):
        # enable with soft in 2
        zebra.writeReg("OUT%d_CONN" % i, "SOFT_IN2")
        for suff in "ABZ":
            signal = "IN%d_ENC%s" % (i, suff)
            out = "OUT%d_ENC%s" % (i, suff)                
            print "%40s"%("Testing %s and %s..." % (signal, out)),
            zebra.writeReg(out, "SOFT_IN1")
            ret = match
            for conn in (1,0):
                for expected in (0,1):
                    # bit mask, conn is soft2, input is soft1
                    if conn == 0:
                        expected = 1
                    zebra.writeReg("SOFT_IN", 2*conn+expected)
                    if (zebra.getStatus(signal) != expected):
                        ret = mismatch  
                time.sleep(sleep) 
            zebra.writeReg(out, "DISCONNECT")         
            if ret == "BAD":        
                errors += 1                             
            print ret
        zebra.writeReg("OUT%d_CONN" % i, "DISCONNECT")
            
    return errors


def twoTests(zebra):
    print "Downloading defaults..."
    zebra.uploadFile(os.path.realpath(os.path.join(__file__, "..", "configs", "defaults.ini")))
    zebra.save()        
    toterrors = 0
    for test, mismatch, match in (("unplugged", "OK", "BAD"),
                                  ("plugged in", "BAD", "OK")):  
        raw_input("Ensure signal cables are %s and press return to run hardware tests." % test)
        repeat = "y"
        while repeat.lower() == "y":        
            print "Doing hardware test with cables %s..." % test
            errors = doHardwareTest(zebra, mismatch=mismatch, match=match)
            repeat = raw_input("Repeat 'cable %s' test? (y/n): " % test)
        toterrors += errors
    print "Hardware test complete: %d Errors" % toterrors
    
if __name__=="__main__":
    repeat = "y"
    portstr = "/dev/ttyUSB0"
    tool = zebraTool(portstr)
    while repeat.lower() == "y":
        version = tool.readReg("SYS_VER") 
        print "Zebra connected with firmware version 0x%X" % version
        if raw_input("Would you like to test firmware? (y/n): ").lower() == "y":
            print "Testing firmware..."         
            zebraFirmwareTest.main(portstr)
        twoTests(tool)
        repeat = raw_input("Test another zebra? (y/n): ")   
