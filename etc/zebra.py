class DataBus:
    def __init__(self):
        self.index = self.instances.add(self)
        self.databus = self.index + self.base

class Instances:
    all_instances = []

    def __init__(self, max_count):
        self.instances = []
        self.all_instances.append(self)
        self.max_count = max_count

    def add(self, instance):
        assert len(self.instances) < self.max_count
        self.instances.append(instance)
        return len(self.instances) - 1

    @classmethod
    def emit(self):
        for instances in self.all_instances:
            for instance in instances.instances:
                instance.emit()


class Input(DataBus):
    instances = Instances(12)
    base = 0

    invert = False

    def __init__(self):
        DataBus.__init__(self)

    def emit(self):
        pass

class Not:
    invert = True

    def __init__(self, input):
        assert isinstance(input, Input)
        self.index = input.index
        self.input = input


class AndOr(DataBus):
    def __init__(self, *inputs):
        DataBus.__init__(self)
        for i in inputs:
            assert isinstance(i, (Input, Not))
        self.inputs = inputs

    def emit(self):
        input_mask = 0
        invert_mask = 0
        for inp in self.inputs:
            input_mask |= 1 << inp.index
            if inp.invert:
                invert_mask |= 1 << inp.index
        print '%s: %03x %03x' % (self.name, input_mask, invert_mask)

class And(AndOr):
    instances = Instances(8)
    base = 16
    name = 'And'

class Or(AndOr):
    instances = Instances(8)
    base = 24
    name = 'Or'

class Pulsegen(DataBus):
    instances = Instances(4)
    base = 32

    def __init__(self, trigger, delay, width, prescale):
        DataBus.__init__(self)
        assert isinstance(trigger, DataBus)
        assert isinstance(delay, int)
        assert isinstance(width, int)
        assert isinstance(prescale, int)
        self.trigger = trigger
        self.delay = delay
        self.width = width
        self.prescale = prescale

    def emit(self):
        print 'Pulsegen: %d %d %d %d' % (
            self.trigger.databus, self.delay, self.width, self.prescale)

class Gategen(DataBus):
    instances = Instances(4)
    base = 36

    def __init__(self, trig0, trig1):
        DataBus.__init__(self)
        assert isinstance(trig0, DataBus)
        assert isinstance(trig1, DataBus)
        self.trig0 = trig0
        self.trig1 = trig1

    def emit(self):
        print 'Gategen: %d %d' % (self.trig0.databus, self.trig1.databus)


class Divgen(DataBus):
    instances = Instances(4)
    base = 40

    def __init__(self, trigger, divisor):
        DataBus.__init__(self)
        assert isinstance(trigger, DataBus)
        assert isinstance(divisor, int)
        self.trigger = trigger
        self.divisor = divisor

    def emit(self):
        print 'Divgen: %d %d' % (self.trigger.databus, self.divisor)


class Output:
    instances = Instances(12)

    def __init__(self, output, value):
        assert isinstance(value, DataBus)
        self.output = output
        self.value = value
        self.instances.add(self)

    def emit(self):
        print 'OutMux %d: %d' % (self.output, self.value.databus)

for n in range(12):
    globals()['I%d' % (n + 1)] = Input()


Output(1, And(I1, Not(I2)))
Output(2, Pulsegen(Or(I1, I12), 10, 10, 1))

Instances.emit()
