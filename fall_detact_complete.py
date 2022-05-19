import time
import board
import busio
import adafruit_adxl34x
import numpy as np
import matplotlib.pyplot as plt
import math
import openpyxl as op

#핀 정보 세텡
i2c = busio.I2C(board.SCL, board.SDA)
accelerometer = adafruit_adxl34x.ADXL345(i2c)

#시간 정보 초기화
SpentTime = 0


def ReadData():
    x = accelerometer.acceleration[0]
    y = accelerometer.acceleration[1]
    z = accelerometer.acceleration[2]
    global AccScala, AccVar
    AccScala = math.sqrt(x**2 + y**2 + z**2)
    AccVar = abs(AccScala - 9.8)


try:
    while True:
        ReadData()
        print(AccVar)
        if AccVar > 18.5:  #추락/낙상 판단 시작
            time.sleep(3)  #추락 시간을 고려해 3초간 딜레이
            StartTime = time.time()  #추락 시작 시간

            while SpentTime <= 15:  #15초간 움직임 감지
                ReadData()
                CurrentTime = time.time()
                SpentTime = CurrentTime - StartTime
                if AccVar > 1:  #15초 내 움직임이 있을 경우 무효
                    SpentTime = 0  #시간 초기화
                    break
            if SpentTime >= 15:  #움직임이 없는 상태로 15초가 흘렀을 경우 Emergency를 반복 출력
                while True:
                    print("Emergency")

except KeyboardInterrupt:
    exit(0)