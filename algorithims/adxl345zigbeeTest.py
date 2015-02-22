import serial
import time

def adxl345Test():
	startTime = time.time()
	currTime = startTime
	print(startTime)
	print(currTime)
	ser = serial.Serial('/dev/ttyAMA0', 9600)
	while(currTime - startTime < 50):
		currTime = time.time()
		reading = ser.readline()
		print(reading[:len(reading)-2] + "," + str(currTime) + "\n")
	ser.close()
if(__name__ == "__main__"):
	adxl345Test()
