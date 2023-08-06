""" 
comm.py contains the classes used to communicate with the EV3 brick.
Classes that support USB and TCP/IP communication are implemented.

Author: Eduardo Nigro
    rev 0.0.3
    2021-12-17
"""
import hid
import socket
import struct
import time
import numpy as np


class CommUSB:
    def __init__(self, deviceID):

        """ Class constructor """ 

        # Defining USB constants
        ID_VENDOR_LEGO = 0x0694
        ID_PRODUCT_EV3 = 0x0005
        # Connecting to EV3
        self.usbhandle = hid.device()
        if not deviceID:
            self.usbhandle.open(ID_VENDOR_LEGO, ID_PRODUCT_EV3)
        else:
            self.usbhandle.open(ID_VENDOR_LEGO, ID_PRODUCT_EV3, deviceID)
        # Assigning developer mode flag
        self._devmode = False

    def send(self, cmd):

        """ Send direct command data """

        # Padding command with zeros for 1024-byte package
        data = bytes(1) + cmd + bytes(1023-len(cmd))
        # Collecting developer mode data
        if self._devmode:
            self.cmd = cmd
            self.tstart = time.perf_counter_ns()
        # Sending direct command to EV3 brick
        self.usbhandle.write(data)

    def receive(self):

        """ Receive direct command reply data """

        # Getting 1024-byte data package
        data = self.usbhandle.read(1024)
        # Extracting actual number of bytes in the reply
        size = np.array(data[0:2], dtype=np.uint8).view(np.uint16)
        data = data[0:size[0]+2]
        # Collecting developer mode data and displaying info
        if self._devmode:
            self.tend = time.perf_counter_ns()-self.tstart
            self.reply = data
            display_stats(self.cmd, self.reply, self.tend)
        return data

    def close(self):

        """ Closes EV3 TCP client """

        self.usbhandle.close()

class CommTCPIP:
    def __init__(self, IPaddress, deviceID):

        """ Class constructor """ 

        # Defining TCP/IP parameters
        self.TCP_PORT = 5555
        self.BUFFER_SIZE = 1024
        self.TCP_IP = IPaddress
        self.deviceID = deviceID
        # Creating TCP/IP socket
        self.tcphandle = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.tcphandle.settimeout(5)
        self.tcphandle.connect((self.TCP_IP, self.TCP_PORT))
        # Connecting to EV3
        unlockstr = 'GET /target?sn=' + deviceID + ' VMTP1.0\nProtocol: EV3'
        self.tcphandle.send(unlockstr.encode())
        data = self.tcphandle.recv(self.BUFFER_SIZE)
        if data.decode('utf-8').find('Accept:EV340') < 0:
            raise NameError('Incorrect device.')
        # Assigning developer mode flag
        self._devmode = False
        # Setting socket as blocking
        self.tcphandle.settimeout(None)

    def send(self, cmd):

        """ Send direct command data """

        # Collecting developer mode data
        if self._devmode:
            self.cmd = cmd
            self.tstart = time.perf_counter_ns()
        # Sending direct command to EV3 brick
        self.tcphandle.send(cmd)

    def receive(self):

        """ Receive direct command reply data """

        # Getting 1024-byte data package
        data = self.tcphandle.recv(self.BUFFER_SIZE)
        # Collecting developer mode data and displaying info
        if self._devmode:
            self.tend = time.perf_counter_ns()-self.tstart
            self.reply = data
            display_stats(self.cmd, self.reply, self.tend)
        return data

    def close(self):

        """ Closes EV3 TCP client """

        self.tcphandle.shutdown(socket.SHUT_RDWR)
        self.tcphandle.close()

# HELPER FUNCTIONS
def display_stats(cmd, reply, t):

    """ Displays cmd/reply values and round-trip elapsed time. """

    print('____________________________________________________________')
    print('cmd:')
    print('  uint8 ' + str([byte[0]
            for byte in list(struct.iter_unpack('B', cmd))]))
    print('  0x|' + ':'.join('{:02X}'.format(byte) for byte in cmd) + '|')
    print('reply:')
    print('  uint8 ' + str(reply))
    print('  0x|' + ':'.join('{:02X}'.format(byte) for byte in reply) + '|')
    print("cmd/reply elapsed time (ms): {:3.3f}".format(1e-6*t))
    print('____________________________________________________________')
    print('')

def list_bricks():
    """
    Return a dictionary containing the names and corresponding ID of
    all the EV3 bricks that are currently connected to the USB port.
    
    Parameters
    ----------
    None.

    Returns
    -------
    brick : dicitonary containing brick names and IDs.

    Example
    -------
    >>> mybricks = list_bricks()

    """
    ID_VENDOR_LEGO = 0x0694
    brick = {
        'Name': [],
        'ID': []
    }
    for device_dict in hid.enumerate():
        if device_dict['vendor_id'] == ID_VENDOR_LEGO:
            brick['Name'].append(device_dict['product_string'])
            brick['ID'].append(device_dict['serial_number'])
    return brick