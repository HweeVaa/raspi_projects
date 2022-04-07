import RPi.GPIO as GPIO
import time
import pymysql

button_pin = 15

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
GPIO.setup(button_pin, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

db = pymysql.connect(host="localhost",
                     user="root",
                     password="root",
                     db="worker")

count = 0

while 1:
    if GPIO.input(button_pin) == GPIO.HIGH:
        count += 1
        if count >= 30:
            print("panic!!")

    else:
        count = 0

    time.sleep(0.1)

GPIO.cleanup()