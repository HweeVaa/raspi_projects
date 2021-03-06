import RPi.GPIO as GPIO
import time
import pymysql
import math
import numpy as np
# change these as desired - they're the pins connected from the
# SPI port on the ADC to the Cobbler
SPICLK = 11
SPIMISO = 9
SPIMOSI = 10
SPICS = 8
mq2_dpin = 26
mq2_apin = 0

#db login
db = pymysql.connect(host="192.168.0.3",
                     user="gas",
                     password="gas",
                     db="gas_detact")


#port init
def init():
    GPIO.setwarnings(False)
    GPIO.cleanup()  #clean up at the end of your script
    GPIO.setmode(GPIO.BCM)  #to specify whilch pin numbering system
    # set up the SPI interface pins
    GPIO.setup(SPIMOSI, GPIO.OUT)
    GPIO.setup(SPIMISO, GPIO.IN)
    GPIO.setup(SPICLK, GPIO.OUT)
    GPIO.setup(SPICS, GPIO.OUT)
    GPIO.setup(mq2_dpin, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)


#read SPI data from MCP3008(or MCP3204) chip,8 possible adc's (0 thru 7)
def readadc(adcnum, clockpin, mosipin, misopin, cspin):
    if ((adcnum > 7) or (adcnum < 0)):
        return -1
    GPIO.output(cspin, True)

    GPIO.output(clockpin, False)  # start clock low
    GPIO.output(cspin, False)  # bring CS low

    commandout = adcnum
    commandout |= 0x18  # start bit + single-ended bit
    commandout <<= 3  # we only need to send 5 bits here
    for i in range(5):
        if (commandout & 0x80):
            GPIO.output(mosipin, True)
        else:
            GPIO.output(mosipin, False)
        commandout <<= 1
        GPIO.output(clockpin, True)
        GPIO.output(clockpin, False)

    adcout = 0
    # read in one empty bit, one null bit and 10 ADC bits
    for i in range(12):
        GPIO.output(clockpin, True)
        GPIO.output(clockpin, False)
        adcout <<= 1
        if (GPIO.input(misopin)):
            adcout |= 0x1

    GPIO.output(cspin, True)

    adcout >>= 1  # first bit is 'null' so drop it
    return adcout


#main ioop
def main():
    init()
    print("please wait...")
    time.sleep(5)
    while True:
        GASlevel = readadc(mq2_apin, SPICLK, SPIMOSI, SPIMISO,
                           SPICS)  #data from sensor
        sensorVoltage = (GASlevel / 1024.) * 3.3  #calculated voltage
        LPG = 26.572 * np.exp(1.2864 * sensorVoltage)  #calculated ppm of LPG
        CO = 3.027 * np.exp(1.0698 * sensorVoltage)  #calculated ppm of CO

        if GPIO.input(mq2_dpin):
            print("Gas not leak")
            time.sleep(0.5)
        else:
            print("Gas leakage")
            print("Current Gas AD vaule = " +
                  str("%.2f" % ((GASlevel / 1024.) * 3.3)) + " V")
            print("LPG: ", str("%.2f" % (LPG)), "ppm", "  CO: ",
                  str("%.2f" % (CO)), "ppm")

            alert = "WARNING!!"

            #sql sentence
            sql = "INSERT INTO MQ (time,gas_value,gas_alert,LPG,CO) VALUES(%s,%s,%s,%s,%s)"
            val = (time.strftime("%Y-%m-%d %H:%M:%S",
                                 time.localtime()), GASlevel, alert,
                   str("%.2f" % (LPG)), str("%.2f" % (CO)))

            cur.execute(sql, val)

            #commit to DB
            db.commit()
            time.sleep(1.0)


if __name__ == '__main__':
    try:
        with db.cursor() as cur:
            main()
        pass
    except KeyboardInterrupt:
        pass

GPIO.cleanup()