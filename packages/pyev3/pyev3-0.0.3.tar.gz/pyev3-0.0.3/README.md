# pyev3
**pyev3** can be used to interact with the **LEGO Mindstorms EV3**.

Send direct commands to the EVR from your PC (local host) using a USB or WiFi connection. **pyev3** is an alternative to [pybricks](https://pybricks.com/ev3-micropython/), which requires booting your EV3 brick from an SD card, and where micropython programs run in the EV3 memory. With **pyev3** you can run the EV3 as is. Just connect it to a USB port, or create a WiFi connection, and you're good to go!

## Classes
Interact with each one of the EV3 devices through simple methods and properties, implemented in the following classes:
* LegoEV3
* Motor
* Touch
* Color
* Ultrasonic
* Infrared
* Gyro

## Install
```
py -m pip install pyev3
```

## Documentation

Comprehensive documentation for **pyev3** is available [here](https://eduardonigro.github.io/pyev3/index.html#).

## Example Code
Start and stop a motor using the touch sensor. The motor speed is proportional to ambient light intensity.

```python
""" Example Code """
# Importing modules
import time
from pyev3.brick import LegoEV3
from pyev3.devices import Motor, Touch, Color
# Creating LEGO EV3 objects
ev3 = LegoEV3(commtype='usb')
motor = Motor(ev3, port='A')
touch = Touch(ev3, portnum=1, inputmode='bump')
color = Color(ev3, portnum=2, inputmode='ambient')
# Initializing system
motor.outputmode = 'speed'
motor.output = 0
motor.start()
touch.reset_count()

# Changing EV3 status light
ev3.set_statuslight(mode='pulsing')
# Running for 30 seconds
print('Running ...')
tcurr = 0
tstart = time.perf_counter()
while tcurr <= 30:
    # Getting current time (s)
    tcurr = time.perf_counter() - tstart
    # Checking for even/odd number of 'bumps'
    if (touch.output % 2) == 0:
        # Assigning ZERO speed output
        motor.output = 0
    else:
        # Assigning output proportional to ambient light
        motor.output = color.output

# Stopping motor and closing EV3 connection
motor.stop()
ev3.set_statuslight(mode='solid')
ev3.close()
print('Done.')
```

### Notes:
1. **pyev3** was developed and tested on MS Windows 10. It uses [cython-hidapi](https://github.com/trezor/cython-hidapi) for the USB communication interface.
2. It's very likely it will also work on Unix and macOS.