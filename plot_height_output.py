import collections
import numpy as np
from matplotlib import pyplot as plt
from matplotlib import animation
from threading import Thread,Event

import sys
import glob
import struct
import binascii
import serial


x = np.linspace(0, 255, 300)
y = collections.deque( [0] * 300, maxlen=300 )


def in_background():
	global y
	ser = serial.Serial("COM3", 115200, timeout=0.5)

	while True:
		data = ser.read()
		if data == b'\x55':
			data = ser.read(4)
			#print (data)
			if data == bytearray(b'\x0B\x00\xF8\x03'):
				out = ser.read(6)
				Height, X, Y, X1, Y1 = struct.unpack("HBBBB", out)
				#print (str(Height) + "\t" + hex(X) + "\t" + hex(Y) + "\t" + str(X1) + "\t" + str(Y1))
				#y.append(Height)
				# x.append(Y)
				y.append(Height)

	serialport.close()

thread = Thread(target = in_background)
thread.daemon = True
thread.start()



fig = plt.figure()
ax = fig.add_subplot(111)

# fig, ax = plt.subplots()
line, = ax.plot([], [], 'k-')

ax.set_xlim(0, 300)
ax.set_ylim(0, 3000)

def update(i):
	#line.set_xdata(x)
	line.set_data(x, y)
	return line,

anim = animation.FuncAnimation(fig, update, interval=0, blit=True)
plt.show()