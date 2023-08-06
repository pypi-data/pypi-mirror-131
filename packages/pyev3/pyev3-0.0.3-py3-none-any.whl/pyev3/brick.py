"""
Creates a class for interacting with the LEGO EV3 brick using direct commands.
LEGO original documentation on direct commands can be found in:
    - LEGO MINDSTORMS EV3 Firmware Developer Kit.pdf
    - LEGO MINDSTORMS EV3 Communication Developer Kit.pdf

Essential commands for motors and all commands for sensors are implemented.
File I/O and LCD commands are left for those with a brave spirit.

Note: Use code folding at the method level to improve readability.

Author: Eduardo Nigro
    rev 0.0.3
    2021-12-17
"""
import time
import numpy as np
from pyev3 import io
from pyev3 import comm


class LegoEV3:
    """
    The class to represent the LEGO EV3 brick.
    You can use LegoEV3 to interact with the EV3 brick.

    Set up USB connection between host and EV3 brick.

        >>> from pyev3.brick import LegoEV3
        >>> myev3 = LegoEV3(commtype='usb')
        >>> myev3.display_info()
        >>> myev3.close()

    Set up WiFi connection between host and EV3 brick

        >>> myev3 = LegoEV3(commtype='wifi', IPaddress='192.168.0.19', deviceID='001653470e58')
        >>> myev3.display_info()
        >>> myev3.close()

    :param commtype: The type of communication with the brick. ``'usb'`` or ``'wifi'``.
    :type commtype: str
    :param IPaddress: The IP address assigned to the EV3 brick.
    :type IPaddress: str
    :param deviceID:
        The individual device ID of the EV3 brick.
        Connect to the brick using `commtype='usb'` and use the
        `display_info()` method to retrieve the ID of the brick.
    :type deviceID: str

    .. note::
        1. Always use the `close()` method before opening a new connection.
        2. Try a USB connection first. It's easier to set up and faster.

    """
    def __init__(self, commtype='usb', IPaddress=None, deviceID=None):
        """
        Class constructor.

        """
        # Assigning private property developer mode flag
        self._devmode = False
        # Assigning EV3 hardware number
        self.HARDWARE = 0x02
        # Assigning LED attributes
        self.LEDcolorlist = ['green', 'red', 'orange']
        self.LEDmodelist = ['solid', 'pulsing', 'off']
        self.LEDpattern = {
            'off': 0,
            'solidgreen': 1,
            'solidred': 2,
            'solidorange': 3,
            'pulsinggreen': 7,
            'pulsingred': 8,
            'pulsingorange': 9
        }
        # Assigning list of device (sensor) types
        self.devicetypes = {
            io.DeviceType.TYPE_EV3_TOUCH: 'EV3 Touch',
            io.DeviceType.TYPE_EV3_COLOR: 'EV3 Color',
            io.DeviceType.TYPE_EV3_ULTRASONIC: 'EV3 Ultrasonic',
            io.DeviceType.TYPE_EV3_GYRO: 'EV3 Gyro',
            io.DeviceType.TYPE_EV3_IR: 'EV3 Infrared',
            io.DeviceType.TYPE_THIRD_PARTY_START: 'Third Party Start',
            io.DeviceType.TYPE_THIRD_PARTY_END: 'Third Party End',
            io.DeviceType.TYPE_IIC_UNKNOWN: 'IIC Unknown',
            io.DeviceType.TYPE_TERMINAL: 'Terminal',
            io.DeviceType.TYPE_UNKNOWN: 'Unknown',
            io.DeviceType.TYPE_NONE: ' ',
            io.DeviceType.TYPE_ERROR: 'Error'
        }
        # Creating communication connection
        if commtype.lower() == 'usb':
            self._commtype = 'USB'
            self._commhandle = comm.CommUSB(deviceID)
        elif commtype.lower() == 'wifi':
            self._commtype = 'WiFi'
            self._commhandle = comm.CommTCPIP(IPaddress, deviceID)
        else:
            raise NameError('Unknown communication type.')
        # Getting EV3 properties
        self._brickname = self._get_brickname()
        self._brickID = self._get_brickid(self.HARDWARE)
        self._hardwareversion = self._read_hardwareversion()
        self._firmware = (
            'Version: ' + self._read_firmwareversion() +
            ' / Build: ' + self._read_firmwarebuild())
        self._os = (
            'Version: ' + self._read_osversion() +
            ' / Build: ' + self._read_osbuild())

    # GET/SET METHODS (PUBLIC PROPERTIES)
    @property
    def devmode(self):
        """
        Contains a developer mode flag. Default is ``False``. 
        When ``True``, communication info is displayed after
        each direct command (`read/write`).
        
        """
        # Getting private value
        return self._devmode

    @devmode.setter
    def devmode(self, value):
        # Setting private vlaue
        self._devmode = value
        # Updating developer mode in communication object
        self._commhandle._devmode = self._devmode

    @property
    def batterylevel(self):
        """
        Contains the EV3 battery level in `%` (`read only`).
        
        """
        return self._read_batterylevel()

    @batterylevel.setter
    def batterylevel(self, _):
        print('"batterylevel" is a read only attribute.')

    @property
    def connectedsensors(self):
        """
        Contains a list with the sensors connected to the EV3 (`read only`).
        
        """
        return self._read_inputdevicelist()

    @connectedsensors.setter
    def connectedsensors(self, _):
        print('"connectedsensors" is a read only attribute.')

    # BRICK PUBLIC METHODS
    def close(self):
        """
        Close the EV3 brick connection.

        >>> myev3.close()

        """
        self._commhandle.close()

    def display_info(self):
        """
        Displays a summary with the brick information.
        
        """
        print('____________________________________________________________')
        print('Brick Name : ' + self._brickname)
        print('Brick ID : ' + self._brickID)
        print('Communication Type : ' + self._commtype)
        print('Hardware Version : ' + self._hardwareversion)
        print('Firmware : ' + self._firmware)
        print('OS : ' + self._os)
        print('Battery Level : ' + str(self.batterylevel))
        print('Connected Sensors : ' + str(self.connectedsensors))
        print('____________________________________________________________')

    def set_statuslight(self, mode='solid', color='green'):
        """
        Set the status light of the EV3 brick.

        :param mode: The light mode: ``'solid'``, ``'pulsing'``, ``'off'``
        :type mode: str
        :param color: The light color: ``'green'``, ``'orange'``, ``'red'``
        :type color: str

        >>> myev3.set_statuslight(mode='pulsing', color='orange')

        """
        pattern = self._get_LEDpattern(mode, color)
        cmd = io.DirectCommand.write_LED(pattern)
        self._commhandle.send(cmd)
        self._receive_reply()

    def play_tone(self, volume=10, frequency=440, duration=1):
        """
        Play a tone on the EV3 brick.

        :param volume: The volume of the played tone: ``0`` to ``100``
        :type volume: int
        :param frequency: The frequency (Hz) of the played tone: ``0`` to ``10000``
        :type frequency: int
        :param duration: The duration (s) of the played tone: ``0`` to ``5``
        :type duration: float

        >>> myev3.play_tone(volume=5, frequency=880, duration=0.5)

        """
        cmd = io.DirectCommand.play_tone(volume, frequency, duration)
        self._commhandle.send(cmd)
        self._receive_reply()

    # BRICK PRIVATE METHODS
    def _get_brickid(self, hardware):
        # opCOM_GET, GET_ID
        cmd = io.DirectCommand.get_brickid(hardware)
        self._commhandle.send(cmd)
        return self._receive_reply(type='char')

    def _get_brickname(self):
        # opCOM_GET, GET_BRICKNAME
        cmd = io.DirectCommand.get_brickname()
        self._commhandle.send(cmd)
        return self._receive_reply(type='char')

    def _read_osversion(self):
        # opCOM_GET, GET_OS_VERS
        cmd = io.DirectCommand.read_osversion()
        self._commhandle.send(cmd)
        return self._receive_reply(type='char')

    def _read_hardwareversion(self):
        # opCOM_GET, GET_HW_VERS
        cmd = io.DirectCommand.read_hardwareversion()
        self._commhandle.send(cmd)
        return self._receive_reply(type='char')

    def _read_firmwareversion(self):
        # opCOM_GET, GET_FW_VERS
        cmd = io.DirectCommand.read_firmwareversion()
        self._commhandle.send(cmd)
        return self._receive_reply(type='char')

    def _read_firmwarebuild(self):
        # opCOM_GET, GET_FW_BUILD
        cmd = io.DirectCommand.read_firmwarebuild()
        self._commhandle.send(cmd)
        return self._receive_reply(type='char')

    def _read_osbuild(self):
        # opCOM_GET, GET_FW_BUILD
        cmd = io.DirectCommand.read_osbuild()
        self._commhandle.send(cmd)
        return self._receive_reply(type='char')

    def _read_batterylevel(self):
        # opCOM_GET, GET_FW_BUILD
        cmd = io.DirectCommand.read_batterylevel()
        self._commhandle.send(cmd)
        return self._receive_reply(type='int8')

    # MOTOR PRIVATE METHODS
    def _stop_motor(self, layer=1, port='A', brake='off'):
        # opOUTPUT_STOP
        cmd = io.DirectCommand.stop_motor(layer, port, brake)
        self._commhandle.send(cmd)
        self._receive_reply()

    def _set_outputpower(self, layer=1, port='A', power=10):
        # opOUTPUT_SET_TYPE (POWER)
        cmd = io.DirectCommand.set_outputpower(layer, port, power)
        self._commhandle.send(cmd)
        self._receive_reply()

    def _set_outputspeed(self, layer=1, port='A', speed=10):
        # opOUTPUT_SET_TYPE (SPEED)
        cmd = io.DirectCommand.set_outputspeed(layer, port, speed)
        self._commhandle.send(cmd)
        self._receive_reply()

    def _start_motor(self, layer=1, port='A'):
        # opOUTPUT_STOP
        cmd = io.DirectCommand.start_motor(layer, port)
        self._commhandle.send(cmd)
        self._receive_reply()

    def _clear_outputcount(self, layer=1, port='A'):
        # opOUTPUT_CLR_COUNT
        cmd = io.DirectCommand.clear_outputcount(layer, port)
        self._commhandle.send(cmd)
        self._receive_reply()

    def _get_outputcount(self, layer=1, port='A'):
        # opOUTPUT_GET_COUNT
        cmd = io.DirectCommand.get_outputcount(layer, port)
        self._commhandle.send(cmd)
        return self._receive_reply(type='int32')

    # SENSOR PRIVATE METHODS
    def _read_inputdevicelist(self):
        # opINPUT_DEVICE_LIST
        cmd = io.DirectCommand.read_inputdevicelist()
        data = self._send_cmd_receive_reply(cmd)
        return self._get_devciceinfo(data)

    def _read_inputdeviceformat(self, layer=1, portnum=1):
        # opINPUT_DEVICE, GET_FORMAT
        # [dataset, format, modes, view]
        cmd = io.DirectCommand.read_inputdeviceformat(layer, portnum)
        data = self._send_cmd_receive_reply(cmd)
        dataset = data[0]
        format = data[1]
        modes = data[2]
        view = data[3]
        return dataset, format, modes, view

    def _read_inputdevicetypemode(self, layer=1, portnum=1):
        # opINPUT_DEVICE, GET_TYPEMODE
        cmd = io.DirectCommand.read_inputdevicetypemode(layer, portnum)
        data = self._send_cmd_receive_reply(cmd, externalflag='type')
        type = data[0]
        mode = data[1]
        return type, mode

    def _read_inputdevicesymbol(self, layer=1, portnum=1):
        # opINPUT_DEVICE, GET_SYMBOL
        cmd = io.DirectCommand.read_inputdevicesymbol(layer, portnum)
        symbol = self._send_cmd_receive_reply(cmd, externalflag='string')
        return symbol

    def _read_inputdevicename(self, layer=1, portnum=1):
        # opINPUT_DEVICE, GET_NAME
        cmd = io.DirectCommand.read_inputdevicename(layer, portnum)
        name = self._send_cmd_receive_reply(cmd, externalflag='string')
        return name

    def _read_inputdevicemodename(self, layer=1, portnum=1, mode=0):
        # opINPUT_DEVICE, GET_MODENAME
        cmd = io.DirectCommand.read_inputdevicemodename(layer, portnum, mode)
        modename = self._send_cmd_receive_reply(cmd, externalflag='string')
        return modename

    def _clear_inputdevicechanges(self, layer=1, portnum=1):
        # opINPUT_DEVICE, CLR_CHANGES
        cmd = io.DirectCommand.clear_inputdevicechanges(layer, portnum)
        self._send_cmd_receive_reply(cmd)

    def _read_inputdevicereadySI(self, layer=1, portnum=1, mode=0, dataset=1):
        # opINPUT_DEVICE, READY_SI - Read sensor input in SI format
        cmd = io.DirectCommand.read_inputdevicereadySI(layer, portnum, mode, dataset)
        self._commhandle.send(cmd)
        data = self._receive_reply(type='other')
        return self._get_deviceoutput(data, dataset, type='SI')

    def _read_inputdevicereadyPCT(self, layer=1, portnum=1, mode=0, dataset=1):
        # opINPUT_DEVICE, READY_SI - Read sensor input in percent format
        cmd = io.DirectCommand.read_inputdevicereadyPCT(layer, portnum, mode, dataset)
        self._commhandle.send(cmd)
        data = self._receive_reply(type='other')
        return self._get_deviceoutput(data, dataset, type='PCT')

    def _read_inputdevicereadyRAW(self, layer=1, portnum=1, mode=0, dataset=1):
        # opINPUT_DEVICE, READY_SI - Read sensor input in raw format
        cmd = io.DirectCommand.read_inputdevicereadyRAW(layer, portnum, mode, dataset)
        self._commhandle.send(cmd)
        data = self._receive_reply(type='other')
        return self._get_deviceoutput(data, dataset, type='RAW')

    # HELPER METHODS
    def _receive_reply(self, type=None):
        #
        result = None
        data = self._commhandle.receive()
        # Checking for successful receive status
        if data[4] == 2:
            if type == 'char':
                result = "".join(map(chr, data[5:data.index(0, 5)]))
            elif type == 'int8':
                result = int(data[5])
            elif type == 'int32':
                if self._commtype == 'USB':
                    result = int(np.array(data[5:9], dtype=np.int8).view(np.int32))
                else:
                    result = int(np.array(data[5:9]).view(np.int32))
            elif type == 'other':
                result = data[5::]
            return result
        else:
            raise NameError('Get brick reply failed.')

    def _send_cmd_receive_reply(self, cmd, externalflag=None):
        attempt = 0
        dataflag = False
        while (attempt < 5) and not dataflag:
            time.sleep(0.1)
            self._commhandle.send(cmd)
            data = self._commhandle.receive()
            if data[4] == 2:
                if externalflag is None:
                    dataflag = True
                    result = data[5::]
                elif externalflag == 'type':
                    dataflag = self._is_validdevicetype(data)
                    result = data[5::]
                elif externalflag == 'string':
                    dataflag = self._is_validdevicestring(data)
                    result = "".join(map(chr, data[5:data.index(0, 5)])).strip()
            attempt += 1
        if dataflag:
            return result
        else:
            raise NameError('Get brick reply failed.')

    def _get_LEDpattern(self, mode, color):
        #
        if mode not in self.LEDmodelist:
            raise NameError('Invalid LED mode argument.')
        if color not in self.LEDcolorlist:
            raise NameError('Invalid LED color argument.')
        if mode == 'off':
            color = ''
        return self.LEDpattern[mode+color]

    def _get_devciceinfo(self, data):
        #
        info = []
        for type in data:
            info.append(self.devicetypes[type])
        return info

    def _get_deviceoutput(self, data, dataset, type='SI'):
        #
        result = []
        for i in range(dataset):
            if type == 'SI':
                if self._commtype == 'USB':
                    result.append(np.array(data[i*4:i*4+4], dtype=np.int8).view(np.float32)[0])
                else:
                    result.append(np.array(data[i*4:i*4+4]).view(np.float32))
            elif type == 'RAW':
                if self._commtype == 'USB':
                    result.append(np.array(data[i*4:i*4+4], dtype=np.int8).view(np.int32)[0])
                else:
                    result.append(np.array(data[i*4:i*4+4]).view(np.int32))
            elif type == 'PCT':
                result.append(data[i])
        return result

    def _is_validdevicetype(self, data):
        #
        type = data[5]
        if type in list(self.devicetypes.keys()):
            validtype = True
        else:
            validtype = False
        return validtype

    def _is_validdevicestring(self, data):
        #
        string = "".join(map(chr, data[0:data.index(0)])).strip()
        if len(string) > 0:
            validstring = True
        else:
            validstring = False
        return validstring
