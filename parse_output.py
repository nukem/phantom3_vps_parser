import struct
import binascii
import serial

ser = serial.Serial("COM3", 115200)

while True:
	data = ser.read()
	if data == b'\x55':
		data = ser.read()
		if data == b'\x0b':
			out = ser.read(3)
			out = ser.read(6)
			Height, ID, Count, Random = struct.unpack("<HBBh", out)
			# print(Height)
		elif data == b'\x57':
			out = ser.read(5)
			out = ser.read(6)
			X, Y, Z = struct.unpack("<hhH", out)
			print (X, Y)

