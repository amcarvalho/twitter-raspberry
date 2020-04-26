import RPi.GPIO as GPIO
from time import sleep


def turn_gpio(gpio, action="on"):
    if action == "on":
        GPIO.output(gpio, GPIO.HIGH)
    else:
        GPIO.output(gpio, GPIO.LOW)


def blink_once(gpio):
    GPIO.setwarnings(False)
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(gpio, GPIO.OUT)
    turn_gpio(gpio, action="off")
    turn_gpio(gpio, action="on")
    sleep(0.2)
    turn_gpio(gpio, action="off")
