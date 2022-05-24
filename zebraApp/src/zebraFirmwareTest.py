#!/bin/env dls-python
from zebraTool import zebraTool
import os, re, time, unittest, itertools

def make_classes(cls, suffixes):
    for i in suffixes:
        name = '%s%s' %(cls.__name__, i)
        yield type(name, (cls,), {'name': name, 'num': i})        

class Block(unittest.TestCase):

    def setUp(self):        
        self.zebra = zebraTool(portstr)
        for k, v in self.initial.items():
            self.zebra.writeReg(k % dict(name=self.name), v)

class AND(Block):
    initial = {
        "%(name)s_INV": 0,
        "%(name)s_ENA": 0,        
        "%(name)s_INP1": 0,                
        "%(name)s_INP2": 0,                
        "%(name)s_INP3": 0,                
        "%(name)s_INP4": 0,
        "SOFT_IN": 1,                                            
    }
    
    def nosignal(self):
        return 1
    
    def singleExpected(self, ena, inv, val):
        if ena:
            if inv:
                return not val
            else:
                return val
        else:
            return self.nosignal()
    
    def combExpected(self, inp1, inp2, inp3, inp4):
        return self.nosignal() and inp1 and inp2 and inp3 and inp4
    
    def setState(self, inp, val):
        if val:          
            self.zebra.writeReg("%s_INP%d" % (self.name, inp+1), "SOFT_IN1")
        else:
            self.zebra.writeReg("%s_INP%d" % (self.name, inp+1), "DISCONNECT")            
    
    def test_single(self):
        # now test single inputs
        for inp in range(4):
            for ena in (0, 1):
                self.zebra.writeReg("%s_ENA" % self.name, 2**inp * ena)
                for inv in (0, 1):
                    self.zebra.writeReg("%s_INV" % self.name, 2**inp * inv)
                    for val in (0, 1):
                        self.setState(inp, val)      
                        self.assertEqual(self.zebra.getStatus(self.name), self.singleExpected(ena, inv, val))
                        
    def test_combined(self):     
        # now test combined functions produce correct logical output
        permutations = itertools.product((0,1), (0,1), (0,1), (0,1)) 
        for perm in permutations:
            for i, v in enumerate(perm):
                self.setState(i, v)
            self.zebra.writeReg("%s_ENA" % self.name, 15)  
            self.zebra.writeReg("%s_INV" % self.name, 0) 
            self.assertEqual(self.zebra.getStatus(self.name), self.combExpected(*perm))

class OR(AND):
    def nosignal(self):
        return 0
    
    def combExpected(self, inp1, inp2, inp3, inp4):
        return self.nosignal() or inp1 or inp2 or inp3 or inp4

class GATE(Block):
    initial = {
        "POLARITY": 0,
        "%(name)s_INP1": "SOFT_IN1",                
        "%(name)s_INP2": "SOFT_IN2",                
        "SOFT_IN": 0,                                            
    }    
    
    def setState(self, state, inp1pol, inp2pol, inp1, inp2):
        # inpx: 0 = 0, 1 = 1, 2 = rising, 3 = falling
        # write polarity
        self.zebra.writeReg("POLARITY", 2 ** (self.num - 1) * inp1pol + 2 ** (self.num + 3) * inp2pol)        
        # write initial state
        soft1 = inp1 % 2
        soft2 = inp2 % 2
        self.zebra.writeReg("SOFT_IN", soft1 + soft2 * 2)
        # if state is wrong then toggle the appropriate input to get it right
        if self.zebra.getStatus(self.name) != state:
            if state:
                self.zebra.writeReg("SOFT_IN", (not soft1) + soft2 * 2)
            else:            
                self.zebra.writeReg("SOFT_IN", soft1 + (not soft2) * 2)
            self.zebra.writeReg("SOFT_IN", soft1 + soft2 * 2)              
        # now toggle inputs
        if inp1 / 2:
            soft1 = not (inp1 % 2)
        if inp2 / 2:
            soft2 = not (inp2 % 2)
        self.zebra.writeReg("SOFT_IN", soft1 + soft2 * 2)
        
    def expected(self, state, inp1pol, inp2pol, inp1, inp2):
        # calculate what we expect
        set_signal = (inp1pol == 0 and inp1 == 2 or inp1pol == 1 and inp1 == 3)
        reset_signal = (inp2pol == 0 and inp2 == 2 or inp2pol == 1 and inp2 == 3)        
        if reset_signal:
            return 0
        elif set_signal:
            return 1
        else:
            return state

    def test_reset(self):
        self.zebra.reset()
        # check the reset condition
        self.assertEqual(self.zebra.getStatus(self.name), 0)
    
    def test_perms(self):
        # test all permutations of input state, inp1 polarity, inp2 polarity, inp1, inp2
        permutations = itertools.product((0,1), (0,1), (0,1), (0,1,2,3), (0,1,2,3))      
        for perm in permutations:
            self.setState(*perm)
            self.assertEqual(self.zebra.getStatus(self.name), self.expected(*perm))

class DIV(Block):
    initial = {
        "POLARITY": 0,
        "%(name)s_INP": "DISCONNECT",                
        "%(name)s_DIVLO": 0,
        "%(name)s_DIVHI": 0,        
        "DIV_FIRST": 0,  
        "SOFT_IN": 0,                                          
    }    

    def setState(self, div, state, inp1pol, inp1):
        # inpx: 0 = 0, 1 = 1, 2 = rising, 3 = falling
        # write polarity
        self.zebra.writeReg("POLARITY", 2 ** (self.num + 7) * inp1pol)        
        # write initial state
        soft1 = inp1 % 2
        self.zebra.writeReg("SOFT_IN", soft1)
        # if state is wrong then toggle the appropriate input to get it right
        current = self.zebra.getEnc(5 + self.num)
        for i in range((state + div - current) % div):
            self.zebra.writeReg("SOFT_IN", (not soft1))
            self.zebra.writeReg("SOFT_IN", soft1)              
        # now toggle inputs
        if inp1 / 2:
            soft1 = not (inp1 % 2)
            self.zebra.writeReg("SOFT_IN", soft1)         
        
    def expected(self, div, state, inp1pol, inp1):
        # calculate what we expect
        inc_state = (inp1pol == 0 and inp1 == 2 or inp1pol == 1 and inp1 == 3)
        inp_high = inp1 in (1,2)
        if inc_state:
            state = (state + 1) % div
        if state == 0:
            outd = inp_high
            outn = inp1pol
        else:
            outn = inp_high
            outd = inp1pol
        return state, outd, outn
    
    def test_reset(self):
        for div in (3, 2000, 2**30, 2**32-1):
            self.zebra.writeReg("%s_DIVLO" % self.name, div%2**16)
            self.zebra.writeReg("%s_DIVHI" % self.name, div/2**16)    
            for first in 0, 1:        
                self.zebra.writeReg("DIV_FIRST", 2 ** (self.num - 1)* first)
                self.zebra.reset()
                # check the reset condition
                self.assertEqual(self.zebra.getEnc(5 + self.num), (div - first) % div) 
                
    def test_3pos(self):
        # divisor is 3 to limit time taken
        div = 3
        self.zebra.writeReg("%s_DIVLO" % self.name, div)                          
        self.zebra.writeReg("%s_INP" % self.name, "SOFT_IN1")         
        # test all permutations of input state, inp polarity, inp1
        permutations = itertools.product((0,1,2), (0,1), (0,1,2,3))      
        for perm in permutations:
            self.setState(div, *perm)
            result = (self.zebra.getEnc(5 + self.num), 
                self.zebra.getStatus(self.name + "_OUTD"), 
                self.zebra.getStatus(self.name + "_OUTN"))   
            self.assertEqual(result, self.expected(div, *perm))

class QUAD(Block):
    initial = {
        "QUAD_STEP": "SOFT_IN1",                
        "QUAD_DIR": "SOFT_IN2",                
        "SOFT_IN": 0,                                            
    }    
    name = "QUAD"
    states = [(0, 0), (1, 0), (1, 1), (0, 1)]
    
    def setState(self, state, step, direction):
        # inpx: 0 = 0, 1 = 1, 2 = rising, 3 = falling
        # write initial state
        soft1 = step % 2
        soft2 = direction % 2
        self.zebra.writeReg("SOFT_IN", soft1 + soft2 * 2)
        # if state is wrong then toggle the appropriate input to get it right
        current = self.states.index((self.zebra.getStatus("QUAD_OUTA"), self.zebra.getStatus("QUAD_OUTB")))
        if soft2:
            ntoggles = (state + 4 - current) % 4
        else:
            ntoggles = (current - state + 4) % 4
        for i in range(ntoggles):
            self.zebra.writeReg("SOFT_IN", (not soft1) + soft2 * 2)
            self.zebra.writeReg("SOFT_IN", soft1 + soft2 * 2)  
        # now toggle inputs
        if step / 2:
            soft1 = not (step % 2)
        if direction / 2:
            soft2 = not (direction % 2)
        self.zebra.writeReg("SOFT_IN", soft1 + soft2 * 2)
        
    def expected(self, state, step, direction):
        # calculate what we expect
        if (step == 2):
            if (direction in (1, 2)):
                state = (state + 1) % 4
            else:
                state = (state + 3) % 4
        return state
    
    def test_perms(self):
        # test all permutations of input state, step, direction
        permutations = itertools.product((0,1,2,3), (0,1,2,3), (0,1,2,3))      
        for perm in permutations:
            self.setState(*perm)
            current = self.states.index((self.zebra.getStatus("QUAD_OUTA"), self.zebra.getStatus("QUAD_OUTB")))
            self.assertEqual(current, self.expected(*perm))

class PULSE(Block):
    initial = {
        "POLARITY": 0,
        "%(name)s_INP": "SOFT_IN1",                
        "%(name)s_DLY": 0,
        "%(name)s_WID": 1000,
        "%(name)s_PRE": 5000,
        "SOFT_IN": 0,                                          
    } 
       
    def test_polarity(self):
        # check that both polarities of trigger start a pulse
        self.zebra.writeReg("SOFT_IN", 1)
        self.assertEqual(self.zebra.getStatus(self.name), 1)
        time.sleep(0.1)
        self.assertEqual(self.zebra.getStatus(self.name), 0)       
        self.zebra.writeReg("POLARITY", 2 ** (self.num + 11)) 
        self.zebra.writeReg("SOFT_IN", 0)
        self.assertEqual(self.zebra.getStatus(self.name), 1)
        time.sleep(0.1)
        self.assertEqual(self.zebra.getStatus(self.name), 0)  
        
    def test_reset(self):
        # check a reset clears a pulse and error state
        self.zebra.writeReg("SOFT_IN", 1)
        self.zebra.writeReg("SOFT_IN", 0)
        self.zebra.writeReg("SOFT_IN", 1)
        self.zebra.writeReg("SOFT_IN", 0)
        self.assertEqual(self.zebra.getStatus(self.name), 1)        
        self.assertEqual(self.zebra.readReg("SYS_STATERR") >> (self.num - 1) & 1, 1)
        self.zebra.reset()
        self.assertEqual(self.zebra.getStatus(self.name), 0)        
        self.assertEqual(self.zebra.readReg("SYS_STATERR") >> (self.num - 1) & 1, 0)

    def test_dly(self):
        # check delay works as we expect
        self.zebra.writeReg("%s_DLY" % self.name, 1000)
        self.zebra.writeReg("SOFT_IN", 1)
        self.assertEqual(self.zebra.getStatus(self.name), 0)
        time.sleep(0.1)
        self.assertEqual(self.zebra.getStatus(self.name), 1)  
        time.sleep(0.1)
        self.assertEqual(self.zebra.getStatus(self.name), 0)       

class PC(Block):
    initial = {
        "PC_BIT_CAP": 0,
        "PC_ENC": 0,
        "PC_TSPRE": 50000,
        "PC_ARM_SEL": 0,
        "PC_GATE_SEL": 1,
        "PC_GATE_STARTLO": 0,
        "PC_GATE_STARTHI": 0,
        "PC_GATE_WIDLO": 0,
        "PC_GATE_WIDHI": 0,
        "PC_GATE_NGATELO": 1,
        "PC_GATE_NGATEHI": 0,
        "PC_GATE_STEPLO": 0,
        "PC_GATE_STEPHI": 0,
        "PC_PULSE_SEL": 1,
        "PC_PULSE_STARTLO": 0,
        "PC_PULSE_STARTHI": 0,
        "PC_PULSE_WIDLO": 0,
        "PC_PULSE_WIDHI": 0,
        "PC_PULSE_STEPLO": 0,
        "PC_PULSE_STEPHI": 0,
        "PC_PULSE_MAXLO": 0,
        "PC_PULSE_MAXHI": 0,
        "PC_DIR": 0,
        "PC_PULSE_DLYLO": 0,
        "PC_PULSE_DLYHI": 0,      
    } 
    name = "PC"
       
    def test_polling(self):    
        self.zebra.reset()     
        # produce data 10 times a second
        step_ms = 100
        self.zebra.writeReg("PC_PULSE_STEPLO", step_ms)
        # and run for 10s
        gate_ms = 10000
        self.zebra.writeReg("PC_GATE_WIDLO", gate_ms % 2**16)
        self.zebra.writeReg("PC_GATE_WIDHI", gate_ms / 2**16)        
        # gather 3 div values
        self.zebra.writeReg("PC_BIT_CAP", 2**6 + 2**7 + 2**8)
        # setup div values to look at 1MHz clock
        for div in ["DIV1", "DIV2", "DIV3"]:
            self.zebra.writeReg(div + "_INP", "CLOCK_1MHZ")
            self.zebra.writeReg(div + "_DIVLO", 0)
            self.zebra.writeReg(div + "_DIVHI", 0)                                    
        # start
        self.zebra.writeReg("PC_ARM", 1)        
        self.zebra.getExpected("PR")
        for i in range(gate_ms / step_ms):
            # now block waiting for positions
            self.zebra.getExpected("P")
            # check we can still poll
            for reg in self.initial:
                self.zebra.readReg(reg)            
        self.zebra.getExpected("PX")

###############################        

def main(pstr = "/dev/ttyUSB0"):
    global portstr
    portstr = pstr
    suite = unittest.TestSuite()
    classes = []
    classes += make_classes(AND, range(1, 5))
    classes += make_classes(OR, range(1, 5))    
    classes += make_classes(GATE, range(1, 5))
    classes += make_classes(DIV, range(1, 5))
    classes += [QUAD]
    classes += make_classes(PULSE, range(1, 5))
    classes += [PC]
    for cls in classes:
        suite.addTest(unittest.TestLoader().loadTestsFromTestCase(cls))        
    unittest.TextTestRunner(verbosity=5, failfast=0).run(suite)
    
if __name__ == '__main__':
    main()

