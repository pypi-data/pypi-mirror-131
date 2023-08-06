""" 
io.py contains the classes used to generate the Direct Commands for the EV3
brick. Direct Commands are grouped by Brick, Motor, and Sensor.

Author: Eduardo Nigro
    rev 0.0.3
    2021-12-17
"""
import struct
import numpy as np


class OpCode:

    """ Class containing EV3 op code definitions."""

    opUI_READ = 0x81
    opUI_WRITE = 0x82
    opSOUND = 0x94
    opINPUT_DEVICE_LIST = 0x98
    opINPUT_DEVICE = 0x99
    opOUTPUT_STOP = 0xA3
    opOUTPUT_POWER = 0xA4
    opOUTPUT_SPEED = 0xA5
    opOUTPUT_START = 0xA6
    opOUTPUT_READ = 0xA8
    opOUTPUT_CLR_COUNT = 0xB2
    opOUTPUT_GET_COUNT = 0xB3
    opCOM_GET = 0xD3
    opOUTPUT_STEP_POWER = 0xAC
    opOUTPUT_TIME_POWER = 0xAD
    opOUTPUT_STEP_SPEED = 0xAE
    opOUTPUT_TIME_SPEED = 0xAF


class SubCodeComGet:

    """ UIWriteSubCode - EV3 UI_WRITE subcode definition."""

    GET_PIN = 0x05
    GET_ID = 0x0C
    GET_BRICKNAME = 0x0D
    GET_NETWORK = 0x0E


class SubCodeInputDevice:

    """ OpCode - EV3 input subcode definition."""

    GET_FORMAT = 0x02
    GET_TYPEMODE = 0x05
    GET_SYMBOL = 0x06
    GET_NAME = 0x15
    GET_MODENAME = 0x16
    CLR_CHANGES = 0x1A
    READY_PCT = 0x1B
    READY_RAW = 0x1C
    READY_SI = 0x1D
    GET_MINMAX = 0x1E


class SubCodeUIRead:

    """ UIReadSubCode - EV3 UI_READ subcode definition. """

    GET_OS_VERS = 0x03
    GET_HW_VERS = 0x09
    GET_FW_VERS = 0x0A
    GET_FW_BUILD = 0x0B
    GET_OS_BUILD = 0x0C
    GET_LBATT = 0x12


class SubCodeUIWrite:

    """ UIWriteSubCode - EV3 UI_WRITE subcode definition. """

    LED = 0x1B


class DataFlag:

    """ DataFlag - EV3 DataFlag definition. """

    PRIMPAR_SHORT = 0x00
    PRIMPAR_LONG = 0x80
    PRIMPAR_CONST = 0x00
    PRIMPAR_VARIABLE = 0x40
    PRIMPAR_LOCAL = 0x00
    PRIMPAR_GLOBAL = 0x20
    PRIMPAR_HANDLE = 0x10
    PRIMPAR_ADD = 0x08
    PRIMPAR_INDEX = 0x1F
    PRIMPAR_CONST_SIGN = 0x20
    PRIMPAR_VALUE = 0x3F
    PRIMPAR_BYTES = 0x07
    PRIMPAR_STRING_OLD = 0
    PRIMPAR_1_BYTES = 1
    PRIMPAR_2_BYTES = 2
    PRIMPAR_4_BYTES = 3
    PRIMPAR_STRING = 4


class DeviceType:

    """ Device (sensor) type identifyer """

    TYPE_EV3_TOUCH = 16
    TYPE_EV3_COLOR = 29
    TYPE_EV3_ULTRASONIC = 30
    TYPE_EV3_GYRO = 32
    TYPE_EV3_IR = 33
    TYPE_THIRD_PARTY_START = 50
    TYPE_THIRD_PARTY_END = 99
    TYPE_IIC_UNKNOWN = 100
    TYPE_TERMINAL = 124
    TYPE_UNKNOWN = 125
    TYPE_NONE  = 126
    TYPE_ERROR = 127


class ByteCode:

    """ ByteCode - EV3 byte code generation. """

    def __init__(self):
        self.numLocal = 0
        self.numGlobal = 0
        self.bCode = []

    # BRICK 
    def get_id(self, HARDWARE):
        """ opCOM_GET(GET_ID, (uint8)HARDWARE, (uint8)LENGTH, *(uint8)STRING) """
        self.numLocal = 4
        self.numGlobal = 0
        LENGTH = 16
        self.bCode = b''.join([
            OpCode.opCOM_GET.to_bytes(1, 'little'),
            SubCodeComGet.GET_ID.to_bytes(1, 'little'),
            HARDWARE.to_bytes(1, 'little'),
            struct.pack('<B', LENGTH),
            struct.pack('<B', 96)
        ])

    def get_brickname(self):
        """ opCOM_GET(GET_BRICKNAME, (uint8)LENGTH, *(uint8)NAME) """
        self.numLocal = 2
        self.numGlobal = 0
        LENGTH = 8
        self.bCode = b''.join([
            OpCode.opCOM_GET.to_bytes(1, 'little'),
            SubCodeComGet.GET_BRICKNAME.to_bytes(1, 'little'),
            struct.pack('<B', LENGTH),
            struct.pack('<B', 96)
        ])

    def read_osversion(self):
        """ opUI_READ(GET_OS_VERS, (uint8)LENGTH, *(uint8)DESTINATION) """
        self.numLocal = 4
        self.numGlobal = 0
        LENGTH = 16
        self.bCode = b''.join([
            OpCode.opUI_READ.to_bytes(1, 'little'),
            SubCodeUIRead.GET_OS_VERS.to_bytes(1, 'little'),
            struct.pack('<B', LENGTH),
            struct.pack('<B', 96)
        ])

    def read_hardwareversion(self):
        """ opUI_READ(GET_HW_VERS, (uint8)LENGTH, *(uint8)DESTINATION) """
        self.numLocal = 2
        self.numGlobal = 0
        LENGTH = 8
        self.bCode = b''.join([
            OpCode.opUI_READ.to_bytes(1, 'little'),
            SubCodeUIRead.GET_HW_VERS.to_bytes(1, 'little'),
            struct.pack('<B', LENGTH),
            struct.pack('<B', 96)
        ])

    def read_firmwareversion(self):
        """ opUI_READ(GET_FW_VERS, (uint8)LENGTH, *(uint8)DESTINATION) """
        self.numLocal = 2
        self.numGlobal = 0
        LENGTH = 8
        self.bCode = b''.join([
            OpCode.opUI_READ.to_bytes(1, 'little'),
            SubCodeUIRead.GET_FW_VERS.to_bytes(1, 'little'),
            struct.pack('<B', LENGTH),
            struct.pack('<B', 96)
        ])

    def read_firmwarebuild(self):
        """ opUI_READ(GET_FW_BUILD, (uint8)LENGTH, *(uint8)DESTINATION) """
        self.numLocal = 4
        self.numGlobal = 0
        LENGTH = 16
        self.bCode = b''.join([
            OpCode.opUI_READ.to_bytes(1, 'little'),
            SubCodeUIRead.GET_FW_BUILD.to_bytes(1, 'little'),
            struct.pack('<B', LENGTH),
            struct.pack('<B', 96)
        ])

    def read_osbuild(self):
        """ opUI_READ(GET_OS_BUILD, (uint8)LENGTH, *(uint8)DESTINATION) """
        self.numLocal = 4
        self.numGlobal = 0
        LENGTH = 16
        self.bCode = b''.join([
            OpCode.opUI_READ.to_bytes(1, 'little'),
            SubCodeUIRead.GET_OS_BUILD.to_bytes(1, 'little'),
            struct.pack('<B', LENGTH),
            struct.pack('<B', 96)
        ])

    def read_batterylevel(self):
        """ opUI_READ(GET_LBATT, *(uint8)PCT) """
        self.numLocal = 0
        self.numGlobal = 1
        self.bCode = b''.join([
            OpCode.opUI_READ.to_bytes(1, 'little'),
            SubCodeUIRead.GET_LBATT.to_bytes(1, 'little'),
            struct.pack('<B', 96)
        ])

    def write_LED(self, PATTERN):
        """ opUI_WRITE(LED, (uint8)PATTERN) """
        self.numLocal = 0
        self.numGlobal = 0
        self.bCode = b''.join([
            OpCode.opUI_WRITE.to_bytes(1, 'little'),
            SubCodeUIWrite.LED.to_bytes(1, 'little'),
            PATTERN.to_bytes(1, 'little')
        ])

    def play_tone(self, volume, frequency, duration):
        """ opSOUND(TONE, (uint8)VOLUME, (int16)FREQUENCY, (int16)DURATION) """
        self.numLocal = 0
        self.numGlobal = 0
        TONE = 1
        VOLUME = LC1(int(volume))
        FREQUENCY = LC2(int(frequency))
        DURATION = LC2(int(duration * 1000))
        duration = int(duration * 1000)
        self.bCode = b''.join([
            OpCode.opSOUND.to_bytes(1, 'little'),
            struct.pack('<B', TONE),
            VOLUME,
            FREQUENCY,
            DURATION
        ])

    # MOTOR INTERFACE
    def output_stop(self, layer, port, brake):
        """ opOUTPUT_STOP((uint8)LAYER, (uint8)NOS, (uint8)BRAKE) """
        self.numLocal = 0
        self.numGlobal = 0
        LAYER = layer - 1
        NOS = get_outputportid(port)
        BRAKE = get_outputbrakevalue(brake)
        self.bCode = b''.join([
            OpCode.opOUTPUT_STOP.to_bytes(1, 'little'),
            struct.pack('<B', LAYER),
            struct.pack('<B', NOS),
            struct.pack('<B', BRAKE)
        ])

    def output_power(self, layer, port, power):
        """ opOUTPUT_POWER((uint8)LAYER, (uint8)NOS, (uint8)POWER) """
        self.numLocal = 0
        self.numGlobal = 0
        LAYER = layer - 1
        NOS = get_outputportid(port)
        POWER = LC1(int(power))
        self.bCode = b''.join([
            OpCode.opOUTPUT_POWER.to_bytes(1, 'little'),
            struct.pack('<B', LAYER),
            struct.pack('<B', NOS),
            POWER
        ])

    def output_speed(self, layer, port, speed):
        """ opOUTPUT_SPEED((uint8)LAYER, (uint8)NOS, (uint8)SPEED) """
        self.numLocal = 0
        self.numGlobal = 0
        LAYER = layer - 1
        NOS = get_outputportid(port)
        SPEED = LC1(int(speed))
        self.bCode = b''.join([
            OpCode.opOUTPUT_SPEED.to_bytes(1, 'little'),
            struct.pack('<B', LAYER),
            struct.pack('<B', NOS),
            SPEED
        ])

    def output_start(self, layer, port):
        """ opOUTPUT_START((uint8)LAYER, (uint8)NOS) """
        self.numLocal = 0
        self.numGlobal = 0
        LAYER = layer - 1
        NOS = get_outputportid(port)
        self.bCode = b''.join([
            OpCode.opOUTPUT_START.to_bytes(1, 'little'),
            struct.pack('<B', LAYER),
            struct.pack('<B', NOS)
        ])

    def output_clearcount(self, layer, port):
        """ opOUTPUT_CLR_COUNT((uint8)LAYER, (uint8)NOS) """
        self.numLocal = 0
        self.numGlobal = 0
        LAYER = layer - 1
        NOS = get_outputportid(port)
        self.bCode = b''.join([
            OpCode.opOUTPUT_CLR_COUNT.to_bytes(1, 'little'),
            struct.pack('<B', LAYER),
            struct.pack('<B', NOS)
        ])

    def output_getcount(self, layer, port):
        """ opOUTPUT_GET_COUNT((uint8)LAYER, (uint8)NOS, *(int32)TACHO) """
        self.numLocal = 1
        self.numGlobal = 0
        LAYER = layer - 1
        NOS = get_outputportnum(port)
        self.bCode = b''.join([
            OpCode.opOUTPUT_GET_COUNT.to_bytes(1, 'little'),
            struct.pack('<B', LAYER),
            struct.pack('<B', NOS),
            struct.pack('<B', 96)
        ])

    # SENSOR INTERFACE
    def input_devicelist(self):
        """ opINPUT_DEVICE_LIST((uint8)LENGTH, *(uint8)ARRAY, *(uint8)CHANGED) """
        self.numLocal = 2
        self.numGlobal = 0
        LENGTH = 8
        self.bCode = b''.join([
            OpCode.opINPUT_DEVICE_LIST.to_bytes(1, 'little'),
            struct.pack('<B', LENGTH),
            struct.pack('<B', 96),
            struct.pack('<B', 100)
        ])

    def input_deviceformat(self, layer, nos):
        """ opINPUT_DEVICE(GET_FORMAT, (uint8)LAYER, (uint8)NOS, 
            *(uint8)DATASETS, *(uint8)FORMAT, *(uint8)MODES, *(uint8)VIEW) """
        self.numLocal = 1
        self.numGlobal = 0
        LAYER = layer - 1
        NOS = nos - 1
        self.bCode = b''.join([
            OpCode.opINPUT_DEVICE.to_bytes(1, 'little'),
            SubCodeInputDevice.GET_FORMAT.to_bytes(1, 'little'),
            struct.pack('<B', LAYER),
            struct.pack('<B', NOS),
            struct.pack('<B', 96),
            struct.pack('<B', 97),
            struct.pack('<B', 98),
            struct.pack('<B', 99)
        ])

    def input_devicetypemode(self, layer, nos):
        """ opINPUT_DEVICE(GET_TYPEMODE, (uint8)LAYER, (uint8)NOS, *(uint8)TYPE, *(uint8)MODE) """
        self.numLocal = 0
        self.numGlobal = 2
        LAYER = layer - 1
        NOS = nos - 1
        self.bCode = b''.join([
            OpCode.opINPUT_DEVICE.to_bytes(1, 'little'),
            SubCodeInputDevice.GET_TYPEMODE.to_bytes(1, 'little'),
            struct.pack('<B', LAYER),
            struct.pack('<B', NOS),
            struct.pack('<B', 96),
            struct.pack('<B', 97)
        ])

    def input_devicesymbol(self, layer, nos):
        """ opINPUT_DEVICE(GET_SYMBOL, (uint8)LAYER, (uint8)NOS, (uint8)LENGTH, *(uint8)DESTINATION) """
        self.numLocal = 4
        self.numGlobal = 0
        LENGTH = 16
        LAYER = layer - 1
        NOS = nos - 1
        self.bCode = b''.join([
            OpCode.opINPUT_DEVICE.to_bytes(1, 'little'),
            SubCodeInputDevice.GET_SYMBOL.to_bytes(1, 'little'),
            struct.pack('<B', LAYER),
            struct.pack('<B', NOS),
            struct.pack('<B', LENGTH),
            struct.pack('<B', 96)
        ])

    def input_devicename(self, layer, nos):
        """ opINPUT_DEVICE(GET_NAME, (uint8)LAYER, (uint8)NOS, (uint8)LENGTH, *(uint8)DESTINATION) """
        self.numLocal = 4
        self.numGlobal = 0
        LENGTH = 16
        LAYER = layer - 1
        NOS = nos - 1
        self.bCode = b''.join([
            OpCode.opINPUT_DEVICE.to_bytes(1, 'little'),
            SubCodeInputDevice.GET_NAME.to_bytes(1, 'little'),
            struct.pack('<B', LAYER),
            struct.pack('<B', NOS),
            struct.pack('<B', LENGTH),
            struct.pack('<B', 96)
        ])

    def input_devicemodename(self, layer, nos, mode):
        """ opINPUT_DEVICE(GET_MODENAME, (uint8)LAYER, (uint8)NOS, (uint8)MODE, (uint8)LENGTH, *(uint8)DESTINATION) """
        self.numLocal = 4
        self.numGlobal = 0
        LENGTH = 16
        LAYER = layer - 1
        NOS = nos - 1
        MODE = mode
        self.bCode = b''.join([
            OpCode.opINPUT_DEVICE.to_bytes(1, 'little'),
            SubCodeInputDevice.GET_MODENAME.to_bytes(1, 'little'),
            struct.pack('<B', LAYER),
            struct.pack('<B', NOS),
            struct.pack('<B', MODE),
            struct.pack('<B', LENGTH),
            struct.pack('<B', 96)
        ])

    def input_deviceclrchanges(self, layer, nos):
        """ opINPUT_DEVICE(CLR_CHANGES, (uint8)LAYER, (uint8)NOS) """
        self.numLocal = 0
        self.numGlobal = 0
        LAYER = layer - 1
        NOS = nos - 1
        self.bCode = b''.join([
            OpCode.opINPUT_DEVICE.to_bytes(1, 'little'),
            SubCodeInputDevice.CLR_CHANGES.to_bytes(1, 'little'),
            struct.pack('<B', LAYER),
            struct.pack('<B', NOS)
        ])

    def input_devicereadySI(self, layer, nos, mode, values):
        """ opINPUT_DEVICE(READY_SI, (uint8)LAYER, (uint8)NOS, (uint8)TYPE, 
                (uint8)MODE, (uint8)VALUES, *(single32)VALUE1) """
        self.numLocal = 4
        self.numGlobal = 0
        LAYER = layer - 1
        NOS = nos - 1
        TYPE = 0
        MODE = mode
        VALUES = values
        self.bCode = b''.join([
            OpCode.opINPUT_DEVICE.to_bytes(1, 'little'),
            SubCodeInputDevice.READY_SI.to_bytes(1, 'little'),
            struct.pack('<B', LAYER),
            struct.pack('<B', NOS),
            struct.pack('<B', TYPE),
            struct.pack('<B', MODE),
            struct.pack('<B', VALUES)
        ])
        for i in range(VALUES):
            self.bCode += struct.pack('<B', 96+i*4)

    def input_devicereadyRAW(self, layer, nos, mode, values):
        """ opINPUT_DEVICE(READY_RAW, (uint8)LAYER, (uint8)NOS, (uint8)TYPE,
                (uint8)MODE, (uint8)VALUES, *(int32)VALUE1) """
        self.numLocal = 4
        self.numGlobal = 0
        LAYER = layer - 1
        NOS = nos - 1
        TYPE = 0
        MODE = mode
        VALUES = values
        self.bCode = b''.join([
            OpCode.opINPUT_DEVICE.to_bytes(1, 'little'),
            SubCodeInputDevice.READY_RAW.to_bytes(1, 'little'),
            struct.pack('<B', LAYER),
            struct.pack('<B', NOS),
            struct.pack('<B', TYPE),
            struct.pack('<B', MODE),
            struct.pack('<B', VALUES)
        ])
        for i in range(VALUES):
            self.bCode += struct.pack('<B', 96+i*4)

    def input_devicereadyPCT(self, layer, nos, mode, values):
        """ opINPUT_DEVICE(READY_PCT, (uint8)LAYER, (uint8)NOS, (uint8)TYPE,
                (uint8)MODE, (uint8)VALUES, *(uint8)VALUE1) """
        self.numLocal = 1
        self.numGlobal = 0
        LAYER = layer - 1
        NOS = nos - 1
        TYPE = 0
        MODE = mode
        VALUES = values
        self.bCode = b''.join([
            OpCode.opINPUT_DEVICE.to_bytes(1, 'little'),
            SubCodeInputDevice.READY_PCT.to_bytes(1, 'little'),
            struct.pack('<B', LAYER),
            struct.pack('<B', NOS),
            struct.pack('<B', TYPE),
            struct.pack('<B', MODE),
            struct.pack('<B', VALUES)
        ])
        for i in range(VALUES):
            self.bCode += struct.pack('<B', 96+i)


class DirectCommand:

    """ DirectCommand - EV3 direct command definition """

    # BRICK
    def get_brickid(hardware):
        BCode = ByteCode()
        BCode.get_id(hardware)
        cmd = constructCommand('Reply', BCode)
        return cmd

    def get_brickname():
        BCode = ByteCode()
        BCode.get_brickname()
        cmd = constructCommand('Reply', BCode)
        return cmd

    def read_osversion():
        BCode = ByteCode()
        BCode.read_osversion()
        cmd = constructCommand('Reply', BCode)
        return cmd

    def read_hardwareversion():
        BCode = ByteCode()
        BCode.read_hardwareversion()
        cmd = constructCommand('Reply', BCode)
        return cmd

    def read_firmwareversion():
        BCode = ByteCode()
        BCode.read_firmwareversion()
        cmd = constructCommand('Reply', BCode)
        return cmd

    def read_firmwarebuild():
        BCode = ByteCode()
        BCode.read_firmwarebuild()
        cmd = constructCommand('Reply', BCode)
        return cmd

    def read_osbuild():
        BCode = ByteCode()
        BCode.read_osbuild()
        cmd = constructCommand('Reply', BCode)
        return cmd

    def read_batterylevel():
        BCode = ByteCode()
        BCode.read_batterylevel()
        cmd = constructCommand('Reply', BCode)
        return cmd

    def write_LED(pattern):
        BCode = ByteCode()
        BCode.write_LED(pattern)
        cmd = constructCommand('Reply', BCode)
        return cmd

    def play_tone(volume, frequency, duration):
        BCode = ByteCode()
        BCode.play_tone(volume, frequency, duration)
        cmd = constructCommand('Reply', BCode)
        return cmd

    # MOTORS
    def stop_motor(layer, port, brake):
        BCode = ByteCode()
        BCode.output_stop(layer, port, brake)
        cmd = constructCommand('Reply', BCode)
        return cmd

    def set_outputpower(layer, port, power):
        BCode = ByteCode()
        BCode.output_power(layer, port, power)
        cmd = constructCommand('Reply', BCode)
        return cmd

    def set_outputspeed(layer, port, speed):
        BCode = ByteCode()
        BCode.output_speed(layer, port, speed)
        cmd = constructCommand('Reply', BCode)
        return cmd

    def start_motor(layer, port):
        BCode = ByteCode()
        BCode.output_start(layer, port)
        cmd = constructCommand('Reply', BCode)
        return cmd

    def clear_outputcount(layer, port):
        BCode = ByteCode()
        BCode.output_clearcount(layer, port)
        cmd = constructCommand('Reply', BCode)
        return cmd

    def get_outputcount(layer, port):
        BCode = ByteCode()
        BCode.output_getcount(layer, port)
        cmd = constructCommand('Reply', BCode)
        return cmd

    # SENSORS
    def read_inputdevicelist():
        BCode = ByteCode()
        BCode.input_devicelist()
        cmd = constructCommand('Reply', BCode)
        return cmd

    def read_inputdeviceformat(layer, portnum):
        BCode = ByteCode()
        BCode.input_deviceformat(layer, portnum)
        cmd = constructCommand('Reply', BCode)
        return cmd

    def read_inputdevicetypemode(layer, portnum):
        BCode = ByteCode()
        BCode.input_devicetypemode(layer, portnum)
        cmd = constructCommand('Reply', BCode)
        return cmd

    def read_inputdevicesymbol(layer, portnum):
        BCode = ByteCode()
        BCode.input_devicesymbol(layer, portnum)
        cmd = constructCommand('Reply', BCode)
        return cmd

    def read_inputdevicename(layer, portnum):
        BCode = ByteCode()
        BCode.input_devicename(layer, portnum)
        cmd = constructCommand('Reply', BCode)
        return cmd

    def read_inputdevicemodename(layer, portnum, mode):
        BCode = ByteCode()
        BCode.input_devicemodename(layer, portnum, mode)
        cmd = constructCommand('Reply', BCode)
        return cmd

    def clear_inputdevicechanges(layer, portnum):
        BCode = ByteCode()
        BCode.input_deviceclrchanges(layer, portnum)
        cmd = constructCommand('Reply', BCode)
        return cmd

    def read_inputdevicereadySI(layer, portnum, mode, dataset):
        BCode = ByteCode()
        BCode.input_devicereadySI(layer, portnum, mode, dataset)
        cmd = constructCommand('Reply', BCode)
        return cmd

    def read_inputdevicereadyRAW(layer, portnum, mode, dataset):
        BCode = ByteCode()
        BCode.input_devicereadyRAW(layer, portnum, mode, dataset)
        cmd = constructCommand('Reply', BCode)
        return cmd

    def read_inputdevicereadyPCT(layer, portnum, mode, dataset):
        BCode = ByteCode()
        BCode.input_devicereadyPCT(layer, portnum, mode, dataset)
        cmd = constructCommand('Reply', BCode)
        return cmd


# HELPER FUNCTIONS
def constructCommand(cmdtype, bcode):

    """ Assembles direct command using input byte code"""

    # Getting command type
    if cmdtype.lower() == 'reply':
        type = 0x00
    else:
        type = 0x80
    # Assigning comand pieces
    size = len(bcode.bCode)
    nl = bcode.numLocal
    nr = bcode.numGlobal
    nl = nl << 2
    nr1 = nr & 3
    nr2 = nr >> 2
    # Assembling direct command
    cmd = b''.join([
        struct.pack('<H', size + 5),
        struct.pack('<H', 0),
        type.to_bytes(1, 'little'),
        struct.pack('<B', nl + nr1),
        struct.pack('<B', nr2),
        bcode.bCode
    ])
    return cmd

def LC1(v):

    """ Parameter encoding - one byte to follow """

    b1 = DataFlag.PRIMPAR_LONG
    b2 = DataFlag.PRIMPAR_CONST
    b3 = DataFlag.PRIMPAR_1_BYTES
    result = b''.join([
        struct.pack('<B', ((b1 | b2) | b3)), 
        struct.pack('<B', np.array(v, dtype=np.int8).view(np.uint8))
        ])
    return result

def LC2(v):

    """ Parameter encoding - two bytes to follow """

    b1 = DataFlag.PRIMPAR_LONG
    b2 = DataFlag.PRIMPAR_CONST
    b3 = DataFlag.PRIMPAR_2_BYTES
    result = b''.join([
        struct.pack('<B', ((b1 | b2) | b3)), 
        struct.pack('<H', np.array(v, dtype=np.int16).view(np.uint16))
        ])
    return result

def LC4(v):

    """ Parameter encoding - four bytes to follow """

    b1 = DataFlag.PRIMPAR_LONG
    b2 = DataFlag.PRIMPAR_CONST
    b3 = DataFlag.PRIMPAR_4_BYTES
    result = b''.join([
        struct.pack('<B', ((b1 | b2) | b3)), 
        struct.pack('<I', np.array(v, dtype=np.int32).view(np.uint32))
        ])
    print([byte[0] for byte in list(struct.iter_unpack('B', result))])
    return result

def get_outputportid(port):

    """ Get the output port ID corresponding to the port letter """

    portid = {
        'a': 1,
        'b': 2,
        'c': 4,
        'd': 8
    }
    port = port.lower()
    if type(port) is not str:
        raise NameError('Invalid output port.')
    if port not in list(portid.keys()):
        raise NameError('Invalid output port.')
    return portid[port]

def get_outputportnum(port):

    """ Get the output port number corresponding to the port letter """

    portnum = {
        'a': 0,
        'b': 1,
        'c': 2,
        'd': 3
    }
    port = port.lower()
    if type(port) is not str:
        raise NameError('Invalid output port.')
    if port not in list(portnum.keys()):
        raise NameError('Invalid output port.')
    return portnum[port]

def get_outputbrakevalue(brake):

    """ Get the output brake value correposnding to the setting word """

    brakevalue = {
        'off': 0,
        'on': 1
    }
    brake = brake.lower()
    if type(brake) is not str:
        raise NameError('Invalid brake value.')
    if brake not in list(brakevalue.keys()):
        raise NameError('Invalid brake value.')
    return brakevalue[brake]
