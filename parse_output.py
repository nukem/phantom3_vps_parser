import sys
import glob
import struct
import binascii
import serial
import tkinter
from tkinter import font

class KalmanFilter(object):

    def __init__(self, process_variance, estimated_measurement_variance):
        self.process_variance = process_variance
        self.estimated_measurement_variance = estimated_measurement_variance
        self.posteri_estimate = 0.0
        self.posteri_error_estimate = 1.0

    def input_latest_noisy_measurement(self, measurement):
        priori_estimate = self.posteri_estimate
        priori_error_estimate = self.posteri_error_estimate + self.process_variance
        KalmanGain = priori_error_estimate / ( priori_error_estimate + self.estimated_measurement_variance )
        print(KalmanGain)
        self.posteri_estimate = priori_estimate + KalmanGain * ( measurement - priori_estimate )
        self.posteri_error_estimate = (  1 - KalmanGain ) * priori_error_estimate
        return self.posteri_estimate

    def get_latest_estimated_measurement(self):
        return self.posteri_estimate

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


measurement_standard_deviation = 0.5
process_variance = 1e-3
estimated_measurement_variance = measurement_standard_deviation ** 2
kalman_filter = KalmanFilter(process_variance, estimated_measurement_variance)
xflow_kf = KalmanFilter(1e-4, 0.001)
yflow_kf = KalmanFilter(1e-4, 0.001)

window = tkinter.Tk()
bold_font = font.Font(family="Arial", size=12, weight="bold")
canvas = tkinter.Canvas(window, width = 640, height = 480)
height_rect = canvas.create_rectangle( 0, 480, 50, 460, fill = "green" )
height_text = canvas.create_text( 50, 100, text = "0", font = bold_font)

xflow_rect = canvas.create_rectangle(300, 240, 300, 190, fill = "red")
xflow_text = canvas.create_text(420, 240, text = "0", font = bold_font)
yflow_rect = canvas.create_rectangle(275, 240, 300, 240, fill = "yellow")
yflow_text = canvas.create_text(320, 240, text = "0", font = bold_font)

canvas.pack()

ser = serial.Serial("COM3", 115200)

Old_Height = 0

while True:
    window.update()
    data = ser.read()
    if data == b'\x55':
        data = ser.read(4)
		#print (data)
        if data == bytearray(b'\x0B\x00\xF8\x03'):
            out = ser.read(6)
            Height, X, Y, X1, Y1 = struct.unpack("HBBBB", out)
			#print (str(Height) + "\t" + hex(X) + "\t" + hex(Y) + "\t" + str(X1) + "\t" + str(Y1))
            #print ( Height )
            if Height > 3000:
                Height = Old_Height
            else:
                Old_Height = Height


            KF_Height = kalman_filter.input_latest_noisy_measurement(Height)
            #print( KF_Height, Height)
            _y = 480 * (1 - (KF_Height / 3000))
            canvas.coords(height_rect, 0, 480, 50, _y)
            canvas.itemconfigure(height_text, text = str(int(KF_Height)))

        elif data == bytearray(b'\x57\x00\xC2\x02'):
            out = ser.read(2)
            out = ser.read(4)
            X, Y = struct.unpack("hh", out)
            KF_X = xflow_kf.input_latest_noisy_measurement(X)
            KF_Y = yflow_kf.input_latest_noisy_measurement(Y)
            canvas.itemconfigure(xflow_text, text = str(X))
            canvas.coords(xflow_rect, 300, 240, 300 + KF_X, 190)
            canvas.itemconfigure(yflow_text, text = str(Y))
            canvas.coords(yflow_rect, 275, 240, 325, 240 + Y)