import sys
import glob
import struct
import binascii
import serial

ser = serial.Serial("/dev/tty.SLAB_USBtoUART", 115200)

def serial_ports():
    """ Lists serial port names

        :raises EnvironmentError:
            On unsupported or unknown platforms
        :returns:
            A list of the serial ports available on the system
    """
    if sys.platform.startswith('win'):
        ports = ['COM%s' % (i + 1) for i in range(256)]
    elif sys.platform.startswith('linux') or sys.platform.startswith('cygwin'):
        # this excludes your current terminal "/dev/tty"
        ports = glob.glob('/dev/tty[A-Za-z]*')
    elif sys.platform.startswith('darwin'):
        ports = glob.glob('/dev/tty.*')
    else:
        raise EnvironmentError('Unsupported platform')

    result = []
    for port in ports:
        try:
            s = serial.Serial(port)
            s.close()
            result.append(port)
        except (OSError, serial.SerialException):
            pass
    return result

# print(serial_ports())

while True:
	data = ser.read()
	if data == b'\x55':
		data = ser.read(4)
		#print (data)
		if data == bytearray(b'\x0B\x00\xF8\x03'):
			out = ser.read(6)
			Height, X, Y, X1, Y1 = struct.unpack("HBBBB", out)
			#print (str(Height) + "\t" + hex(X) + "\t" + hex(Y) + "\t" + str(X1) + "\t" + str(Y1))
		elif data == bytearray(b'\x57\x00\xC2\x02'):
			out = ser.read(2)
			out = ser.read(6)
			X, Y, Z = struct.unpack("hhh", out)
			print (str(X) + "\t" + str(Y) + "\t" + str(Z))