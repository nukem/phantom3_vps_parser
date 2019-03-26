import struct
import binascii
import serial

ser = serial.Serial("COM3", 115200)

while True:
	data = ser.read()
	if data == b'\x55':
		data = ser.read(4)
		if data == bytearray(b'\x0B\x00\xF8\x03'):
			out = ser.read(6)
			Height, Count, Random = struct.unpack("<HHH", out)
			print(Height + "\t" + "\t" + Count + "\t" + Random)
		elif data == bytearray(b'\x57\x00\xC2\x02'):
			#out = ser.read(6)
			#X, Y, Z = struct.unpack("<hhH", out)
			#print (X, Y)
			print("YYYY")
