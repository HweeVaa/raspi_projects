import spidev
import time
spi=spidev.SpiDev()
spi.open(0,0)
spi.max_speed_hz = 500000


def read_spi_adc(adcChannel):
    adcValue = 0
    buff = spi.xfer2([1,(8+adcChannel)<<4,0])
    adcValue = ((buff[1]&3)<<8)+buff[2]
    return adcValue


count = 0


try:
    while True:
        adcChannel = 0
        adcValue = read_spi_adc(adcChannel)
        print("gas %d"%adcValue)
        time.sleep(0.2)

        if adcValue > 120 :  
            print("warning!! gas detected!!")
            count += 1
            if count >= 300:
                print("You need to stop working and escape!!!!")
        else:
            count = 0
            print("You are safe now.")


except KeyboardInterrupt:
    spi.close()
    