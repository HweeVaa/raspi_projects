import time
import board
import busio
import adafruit_adxl34x
import numpy as np
import matplotlib.pyplot as plt
import math

i2c = busio.I2C(board.SCL, board.SDA)
accelerometer = adafruit_adxl34x.ADXL345(i2c)

#그래프 데이터 초기화
t = 0
AccScala = 0

try:
    while True:
        # print("%f %f %f" % accelerometer.acceleration)
        x = accelerometer.acceleration[0]
        y = accelerometer.acceleration[1]
        z = accelerometer.acceleration[2]

        t += 0.01
        AccScala = math.sqrt(x**2 + y**2 + z**2)

        print(AccScala)

        # print(x, y, z)
        time.sleep(0.01)

except:
    KeyboardInterrupt()