""" 
devices.py contains the Motor and Sensor classes.
Each sensor type has its own class, derived from the base Sensor class.
Motor and sensor classes implement Direct Commands in a way that simplifies 
the interaction with the EV3 devices.

Author: Eduardo Nigro
    rev 0.0.3
    2021-12-17
"""
import numpy as np
import time

class Motor:
    """
    The class to represent the EV3 motor.
    
    Set up a motor on output port ``'B'``

        >>> from pyev3.brick import LegoEV3
        >>> from pyev3.devices import Motor
        >>> myev3 = LegoEV3(commtype='usb')
        >>> mymotor = Motor(myev3, port='B')

    Set up a motor on output port ``'A'`` of the first brick and port ``'B'``
    of the second brick

        >>> mymotor1 = Motor(myev3, layer=1, port='A')
        >>> mymotor2 = Motor(myev3, layer=2, port='B')

    :param ev3handle: ``LegoEV3`` instance representing the EV3 brick.
    :type ev3handle: object
    :param layer:
        The layer of the brick ``1`` or ``2`` in a daisy-chain
        configuration.
    :type layer: int
    :param port:
        The brick output port connected to the motor.
        Possible values are ``'A'``, ``'B'``, ``'C'``, or ``'D'``.
    :type port: str

    .. note::
        1. If EV3 bricks are connected in a daisy-chain configuration,
        set the input parameter `layer` to the appropriate number.

    """
    def __init__(self, ev3handle, layer=1, port='A'):
        """
        Class constructor.

        """
        # Assigning input attributes
        self._ev3handle = ev3handle
        self._layer = layer
        self._outputport = port
        # Assigning default attributes
        self._motorstopped = True
        self._outputmode = 'power'
        self._output = 0

    # GET/SET METHODS (PUBLIC PROPERTIES)
    @property
    def outputmode(self):
        """
        Contains the motor output mode.
        It can be either ``'speed'`` or ``'power'`` (`read/write`).
        The motor has to be stopped before switching modes.
        
        """
        return self._outputmode

    @outputmode.setter
    def outputmode(self, value):
        if self._motorstopped:
            if value.lower() == 'speed':
                self._outputmode = 'speed'
            elif value.lower() == 'power':
                self._outputmode = 'power'
            else:
                raise NameError('Invalid output type.')
        else:
            print('Stop motor to change output mode.')

    @property
    def output(self):
        """
        Contains the motor output level as a percentage.
        Values can be between ``-100`` or ``100`` (`read/write`).
        
        """
        return self._output

    @output.setter
    def output(self, value):
        # Limiting value or changing data type
        if value > 100:
            value = 100
        elif value < -100:
            value = -100
        else:
            value = np.int8(value)
        # Sending appropriate output level command to EV3 brick
        if self.outputmode == 'power':
            self._ev3handle._set_outputpower(
                layer=self._layer, port=self._outputport, power=value)
        elif self.outputmode == 'speed':
            self._ev3handle._set_outputspeed(
                layer=self._layer, port=self._outputport, speed=value)
        # Updating Output property
        self._output = value

    @property
    def angle(self):
        """
        Contains the angular position of the motor in degrees (`read only`).
        
        """
        return self._ev3handle._get_outputcount(
            layer=self._layer, port=self._outputport)

    @angle.setter
    def angle(self, _):
        print('"angle" is a read only property.')

    # MOTOR CONTROL METHODS
    def start(self):
        """
        Start the EV3 motor.

        >>> mymotor.start()

        """
        # Making sure current output mode is sent to EV3 brick
        if self.outputmode == 'power':
            self._ev3handle._set_outputpower(
                layer=self._layer, port=self._outputport, power=self.output)
        elif self.outputmode == 'speed':
            self._ev3handle._set_outputspeed(
                layer=self._layer, port=self._outputport, speed=self.output)
        # Changing motor stopped status flag
        self._motorstopped = False
        # Starting motor
        self._ev3handle._start_motor(
            layer=self._layer, port=self._outputport)

    def stop(self, brake='off'):
        """
        Stop the EV3 motor.

        :param brake:
            The brake option of the motor ``'on'`` or ``'off'``.
            Can be used to hold the motor position.
        :type brake: str

        >>> mymotor.stop(brake='on')

        """
        # Changing motor stopped status flag
        self._motorstopped = True
        # Stopping motor with appropriate brake option
        self._ev3handle._stop_motor(
            layer=self._layer, port=self._outputport, brake=brake)

    def reset_angle(self):
        """
        Reset the encoder output angle of the EV3 motor.

        >>> mymotor.reset_angle()

        """
        self._ev3handle._clear_outputcount(
            layer=self._layer, port=self._outputport)


class Sensor:
    """
    The Sensor class implements common methods for all the different types
    of EV3 sensors. The following properties and methods are inherited by
    the derived sensor-specific classes.
    
    .. note::
        1. The sensor input mode can be changed at any time,
        even after its creation.

    """
    def __init__(self, ev3handle, layer=1, portnum=1):
        """
        Class constructor.

        :param ev3handle: ``LegoEV3`` instance representing the EV3 brick.
        :type ev3handle: object
        :param layer:
            The layer of the brick ``1`` or ``2`` in adaisy-chain
            configuration.
        :type layer: int
        :param portnum:
            The brick input port connected to the sensor.
            Possible values are ``1``, ``2``, ``3``, or ``4``.
        :type portnum: int

        """
        # Assigning input attributes
        self._ev3handle = ev3handle
        self._layer = layer
        self._inputport = portnum
        # Assigning sensor specific attributes
        self._sensortype, self.activemode = self._ev3handle._read_inputdevicetypemode(
            layer=self._layer, portnum=self._inputport)
        # Getting sensor info and separating name from mode
        nameaux = self._ev3handle._read_inputdevicename(
            layer=self._layer, portnum=self._inputport)
        indexaux = nameaux.find('-')
        # Assigning sensor name and active mode attributes
        if indexaux < 0:
            self._sensorname = 'TOUCH'
            self._activemodename = nameaux
        else:
            self._sensorname = nameaux[0:indexaux]
            self._activemodename = nameaux[indexaux+1::]
        # Creating default generic sensor attributes
        self._inputmode = None
        self._outputformat = None
        self._mode = None
        self._dataset = None
        # Creating sensor info dictionary
        self._info = {
            'TOUCH': ['Touch', ['touch', 'bump']],
            'COL': ['Color', ['reflected', 'ambient', 'color', 'rgb']],
            'RGB': ['Color', ['reflected', 'ambient', 'color', 'rgb']],
            'US': ['Ultrasonic', ['distance', 'listen']],
            'IR': ['Infrared', ['proximity', 'seeker', 'remote']],
            'GYRO': ['Gyro', ['angle', 'rate', 'angle&rate']]
        }

    # GET/SET METHOD INPUTMODE
    @property
    def inputmode(self):
        """
        Contains the sensor input mode.
        Use this to change the mode on the fly (`read/write`).
        
        """
        return self._inputmode

    @inputmode.setter
    def inputmode(self, value):
        if value in list(self.modepar.keys()):
            self._inputmode = value
            self._outputformat = self.modepar[value][0]
            self._mode = self.modepar[value][1]
            self._dataset = self.modepar[value][2]
            # Forcing mode change
            _ = self._read_output()
        else:
            nameaux = self._info[self._sensorname][0]
            raise NameError('Undefined input mode for ' + nameaux + ' sensor.')

    # SENSOR BASE CLASS METHODS
    def display_info(self):
        """
        Displays a summary with the sensor information.
        
        """
        print('____________________________________________________________')
        print('Sensor Name : ' + self._info[self._sensorname][0])
        print('Current Mode : ' + self.inputmode)
        print('Available Modes : ' + str(self._info[self._sensorname][1])[1:-1])
        print('Layer : ' + str(self._layer))
        print('Port Number : ' + str(self._inputport))
        print('____________________________________________________________')

    def _read_output(self):
        
        """ Read generic sensor output value. """

        # Assigning sensor output reader method
        if self._outputformat == 1:
            reader = self._ev3handle._read_inputdevicereadySI
        elif self._outputformat == 2:
            reader = self._ev3handle._read_inputdevicereadyPCT
        elif self._outputformat == 3:
            reader = self._ev3handle._read_inputdevicereadyRAW
        # Reading sensor output
        result = reader(
            layer=self._layer, portnum=self._inputport,
            mode=self._mode, dataset=self._dataset)
        while result is None:
            time.sleep(0.01)
            result = reader(
                layer=self._layer, portnum=self._inputport,
                mode=self._mode, dataset=self._dataset)
        return result

    def _clear_changes(self):
        self._ev3handle._clear_inputdevicechanges(
            layer=self._layer, portnum=self._inputport)


class Touch(Sensor):
    """
    The class to represent the EV3 touch sensor.
    
    Set up a touch sensor on port number 1

        >>> from pyev3.brick import LegoEV3
        >>> from pyev3.devices import Touch
        >>> myev3 = LegoEV3(commtype='usb')
        >>> mysensor = Touch(myev3, portnum=1, inputmode='bump')

    :param ev3handle: ``LegoEV3`` instance representing the EV3 brick.
    :type ev3handle: object
    :param layer:
        The layer of the brick ``1`` or ``2`` in a daisy-chain
        configuration.
    :type layer: int
    :param portnum:
        The brick input port connected to the sensor.
        Possible values are ``1``, ``2``, ``3``, or ``4``.
    :type portnum: int
    :param inputmode:
        * ``'touch'`` to check the button state (`pressed or released`)
        * ``'bump'`` to count the number of press/release events
    :type inputmode: str

    """
    def __init__(self, ev3handle, layer=1, portnum=1, inputmode='touch'):
        """
        Class constructor.

        """
        # Defining touch sensor mode parameters
        # [outputformat, mode, dataset]
        self.modepar = {
            'touch': [1, 0, 1],
            'bump': [1, 1, 1]
        }
        # Instantiating base class Sensor
        super(Touch, self).__init__(ev3handle, layer=layer, portnum=portnum)
        # Checking for valid sensor
        if self._info[self._sensorname][0] != 'Touch':
            raise NameError('Incorrect sensor type on port : ' + str(portnum))
        # Assining sensor specific attributes
        self.inputmode = inputmode

    @property
    def output(self):
        """
        Contains the sensor output based on the `inputmode` (`read only`).

            * ``1`` or ``0``  (`inputmode='touch'`)
            * ``int`` (`inputmode='bump'`)
        
        """
        data = self._read_output()
        result = int(data[0])
        return result

    @output.setter
    def output(self, _):
        print('"output" is a read only property.')

    def reset_count(self):
        """
        Reset the touch sensor event counter.

        >>> mysensor.reset_count()

        """
        return self._clear_changes()


class Color(Sensor):
    """
    The class to represent the EV3 color sensor.

    Set up a color sensor on port number 2

        >>> from pyev3.brick import LegoEV3
        >>> from pyev3.devices import Color
        >>> myev3 = LegoEV3(commtype='usb')
        >>> mysensor = Color(myev3, portnum=2, inputmode='rgb')

    :param ev3handle: ``LegoEV3`` instance representing the EV3 brick.
    :type ev3handle: object
    :param layer:
        The layer of the brick ``1`` or ``2`` in a daisy-chain
        configuration.
    :type layer: int
    :param portnum:
        The brick input port connected to the sensor.
        Possible values are ``1``, ``2``, ``3``, or ``4``.
    :type portnum: int
    :param inputmode:
        * ``'ambient'`` ambient light intensity
        * ``'reflected'`` reflected light intensity
        * ``'color'`` surface color
        * ``'rgb'`` surface color RGB components
    :type inputmode: str

    """
    def __init__(self, ev3handle, layer=1, portnum=1, inputmode='ambient'):
        """
        Class constructor.

        """
        # Defining color sensor mode parameters
        # [outputformat, mode, dataset]
        self.modepar = {
            'reflected': [2, 0, 1],
            'ambient': [2, 1, 1],
            'color': [1, 2, 1],
            'rgb': [3, 4, 3]
        }
        # Instantiating base class Sensor
        super(Color, self).__init__(ev3handle, layer=layer, portnum=portnum)
        # Checking for valid sensor
        if self._info[self._sensorname][0] != 'Color':
            raise NameError('Incorrect sensor type on port : ' + str(portnum))
        # Assining sensor specific attributes
        self.inputmode = inputmode
        # Defining color list
        self._color = [
            'unknown',
            'black',
            'blue',
            'green',
            'yellow',
            'red',
            'white',
            'brown'
        ]

    @property
    def output(self):
        """
        Contains the sensor output based on the `inputmode` (`read only`).

            * ``0`` to ``100`` (`inputmode='ambient'`)
            * ``0`` to ``100`` (`inputmode='reflected'`)
            * ``'blue'``, ``'green'``, ``'yellow'``, ``'red'``, ``'white'``, ``'brown'``, ``'unknown'`` (`inputmode='color'`)
            * tuple of integers (``0`` to ``255``, ``0`` to ``255``, ``0`` to ``255``) (`inputmode='rgb'`)
        
        """
        data = self._read_output()
        if self._inputmode == 'reflected':
            result = int(data[0])
        elif self._inputmode == 'ambient':
            result = int(data[0])
        elif self._inputmode == 'color':
            result = self._color[int(data[0])]
        elif self._inputmode == 'rgb':
            result = tuple([min(255, int(value)) for value in data])
        return result

    @output.setter
    def output(self, _):
        print('"output" is a read only property.')


class Ultrasonic(Sensor):
    """
    The class to represent the EV3 ultrasonic sensor.
    
    Set up an ultrasonic sensor on port number 3

        >>> from pyev3.brick import LegoEV3
        >>> from pyev3.devices import Ultrasonic
        >>> myev3 = LegoEV3(commtype='usb')
        >>> mysensor = Ultrasonic(myev3, portnum=3, inputmode='distance')

    :param ev3handle: ``LegoEV3`` instance representing the EV3 brick.
    :type ev3handle: object
    :param layer:
        The layer of the brick ``1`` or ``2`` in a daisy-chain
        configuration.
    :type layer: int
    :param portnum:
        The brick input port connected to the sensor.
        Possible values are ``1``, ``2``, ``3``, or ``4``.
    :type portnum: int
    :param inputmode:
        * ``'distance'`` measure distance to an object in cm
        * ``'listen'`` presence of other ultrasound source
    :type inputmode: str

    """
    def __init__(self, ev3handle, layer=1, portnum=1, inputmode=None):
        """
        Class constructor.

        """
        # Defining ultrasonic sensor mode parameters
        # [outputformat, mode, dataset]
        self.modepar = {
            'distance': [1, 0, 1],
            'listen': [1, 2, 1]
        }
        # Instantiating base class Sensor
        super(Ultrasonic, self).__init__(ev3handle, layer=layer, portnum=portnum)
        # Checking for valid sensor
        if self._info[self._sensorname][0] != 'Ultrasonic':
            raise NameError('Incorrect sensor type on port : ' + str(portnum))
        # Assining sensor specific attributes
        self.inputmode = inputmode

    @property
    def output(self):
        """
        Contains the sensor output based on the `inputmode` (`read only`).

            * ``0`` to ``250`` (`inputmode='distance'`)
            * ``0`` or ``1`` (`inputmode='listen'`)
        
        """
        data = self._read_output()
        if self._inputmode == 'distance':
            result = np.float32(data[0])
        elif self._inputmode == 'listen':
            result = int(data[0])
        return result

    @output.setter
    def output(self, _):
        print('"output" is a read only property.')


class Infrared(Sensor):
    """
    The class to represent the EV3 infrared sensor.
    
    Set up an infrared sensor on port number 4

        >>> from pyev3.brick import LegoEV3
        >>> from pyev3.devices import Infrared
        >>> myev3 = LegoEV3(commtype='usb')
        >>> mysensor = Infrared(myev3, portnum=4, inputmode='remote')

    :param ev3handle: ``LegoEV3`` instance representing the EV3 brick.
    :type ev3handle: object
    :param layer:
        The layer of the brick ``1`` or ``2`` in a daisy-chain
        configuration.
    :type layer: int
    :param portnum:
        The brick input port connected to the sensor.
        Possible values are ``1``, ``2``, ``3``, or ``4``.
    :type portnum: int
    :param inputmode:
        * ``'proximity'`` detect proximity to an object
        * ``'seeker'`` searches beacon (`requires channel 1 and beacon on`)
        * ``'remote'`` takes remote control input
    :type inputmode: str

    """
    def __init__(self, ev3handle, layer=1, portnum=1, inputmode='proximity'):
        """
        Class constructor.

        """
        # Defining infrared sensor mode parameters
        # [outputformat, mode, dataset]
        self.modepar = {
            'proximity': [1, 0, 1],
            'seeker': [1, 1, 2],
            'remote': [1, 2, 4]
        }
        # Instantiating base class Sensor
        super(Infrared, self).__init__(ev3handle, layer=layer, portnum=portnum)
        # Checking for valid sensor
        if self._info[self._sensorname][0] != 'Infrared':
            raise NameError('Incorrect sensor type on port : ' + str(portnum))
        # Assining sensor specific attributes
        self.inputmode = inputmode

    @property
    def output(self):
        """
        Contains the sensor output based on the `inputmode` (`read only`).

            * ``0`` to ``100`` (`inputmode='proximity'`)
            * tuple of integers (``azymuth``, ``proximity``) (`inputmode='seeker'`)
            * tuple of integers (``channel``, ``buttoncode``) (`inputmode='remote'`)
            
                * channel ``1``, ``2``, ``3``, ``4``
                * buttoncode

                    * ``0``  = No button
                    * ``1``  = Button 1
                    * ``2``  = Button 2
                    * ``3``  = Button 3
                    * ``4``  = Button 4
                    * ``5``  = Buttons 1 and 3
                    * ``6``  = Buttons 1 and 4
                    * ``7``  = Buttons 2 and 3
                    * ``8``  = Buttons 2 and 4
                    * ``9``  = Beacon Mode is on
                    * ``10`` = Buttons 1 and 2
                    * ``11`` = Buttons 3 and 4

        """
        data = self._read_output()
        if self._inputmode == 'proximity':
            result = int(data[0])
        elif self._inputmode == 'seeker':
            if not np.isnan(data[1]):
                result = (int(data[0]), int(data[1]))
            else:
                raise NameError('Incorrect remote channel or beacon is off.')
        elif self._inputmode == 'remote':
            index = np.nonzero(data)[0]
            if len(index) > 0:
                channel = index[0]+1
                button = int(data[index[0]])
                result = (channel, button)
            else:
                result = (0, 0)
        return result

    @output.setter
    def output(self, _):
        print('"output" is a read only property.')


class Gyro(Sensor):
    """
    The class to represent the EV3 gyro sensor.
    
    Set up a gyro sensor on port number 1

        >>> from pyev3.brick import LegoEV3
        >>> from pyev3.devices import Gyro
        >>> myev3 = LegoEV3(commtype='usb')
        >>> mysensor = Gyro(myev3, portnum=1, inputmode='rate')

    :param ev3handle: ``LegoEV3`` instance representing the EV3 brick.
    :type ev3handle: object
    :param layer:
        The layer of the brick ``1`` or ``2`` in a daisy-chain
        configuration.
    :type layer: int
    :param portnum:
        The brick input port connected to the sensor.
        Possible values are ``1``, ``2``, ``3``, or ``4``.
    :type portnum: int
    :param inputmode:
        * ``'angle'`` angular position in deg
        * ``'rate'`` angular speed up to 440 deg/s
        * ``'angle&rate'`` angular position and rate
    :type inputmode: str

    """
    def __init__(self, ev3handle, layer=1, portnum=1, inputmode='angle'):
        """
        Class constructor.

        """
        # Defining gyro sensor mode parameters
        # [outputformat, mode, dataset]
        self.modepar = {
            'angle': [1, 0, 1],
            'rate': [1, 1, 1],
            'angle&rate': [1, 3, 2]
        }
        # Instantiating base class Sensor
        super(Gyro, self).__init__(ev3handle, layer=layer, portnum=portnum)
        # Checking for valid sensor
        if self._info[self._sensorname][0] != 'Gyro':
            raise NameError('Incorrect sensor type on port : ' + str(portnum))
        # Assining sensor specific attributes
        self.inputmode = inputmode

    @property
    def output(self):
        """
        Contains the sensor output based on the `inputmode` (`read only`).

            * integer ``angle`` (`inputmode='angle'`)
            * integer ``rate`` (`inputmode='rate'`)
            * tuple of integers (``angle``, ``rate``) (`inputmode='angle&rate'`)
        
        """
        data = self._read_output()
        if self._inputmode == 'angle':
            result = int(data[0])
        elif self._inputmode == 'rate':
            result = int(data[0])
        elif self._inputmode == 'angle&rate':
            result = (int(data[0]), int(data[1]))
        return result

    @output.setter
    def output(self, _):
        print('"output" is a read only property.')
