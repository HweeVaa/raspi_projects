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

sql = "INSERT INTO workerdata(Panic_Alert, time) VALUES(%s,%s)"
val = ("Emergency!!", time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))

count = 0


def main():
    while 1:
        if GPIO.input(button_pin) == GPIO.HIGH:
            count += 1
            if count >= 30:
                print("panic!!")
                cur.execute(sql, val)
                #commit to DB
                db.commit()

        else:
            count = 0

        time.sleep(0.1)


if __name__ == '__main__':
    try:
        with db.cursor() as cur:
            main()
        pass
    except KeyboardInterrupt:
        pass

GPIO.cleanup()