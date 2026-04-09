import RPi.GPIO as GPIO
import time

def dec2bin(value):
    return [int(element) for element in bin(value)[2:].zfill(8)]


GPIO.setmode(GPIO.BCM)

leds = [24, 22, 23, 27, 17, 25, 12, 16]
leds = leds[::-1]

GPIO.setup(leds, GPIO.OUT)

GPIO.output(leds, 0)

up = 9
down = 10
GPIO.setup(up, GPIO.IN)
GPIO.setup(down, GPIO.IN)

num = 0
sleep_time = 0.2

while True:
    if (GPIO.input(up)):
        time.sleep(0.05)
        if (GPIO.input(down)):
            num = 254
        num += 1

        if (num > 255):     num = 0     
        print(num, dec2bin(num))

        GPIO.output(leds, dec2bin(num))
        time.sleep(sleep_time)


    if (GPIO.input(down)):
        time.sleep(0.05)
        if (GPIO.input(up)):
                    num = 256

        num -= 1
        if (num < 0):       num = 0
        print(num, dec2bin(num))

        GPIO.output(leds, dec2bin(num))
        time.sleep(sleep_time)
