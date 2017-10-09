import RPi.GPIO as GPIO
from time import sleep

GPIO.setmode(GPIO.BOARD)

Motor1A = 16
Motor1B = 18
Motor1E = 22

Motor2A = 12
Motor2B = 10
Motor2E = 8

Motor3A = 19
Motor3B = 21
Motor3E = 23

GPIO.setup(Motor2A,GPIO.OUT)
GPIO.setup(Motor2B,GPIO.OUT)
GPIO.setup(Motor2E,GPIO.OUT)

GPIO.setup(Motor1A,GPIO.OUT)
GPIO.setup(Motor1B,GPIO.OUT)
GPIO.setup(Motor1E,GPIO.OUT)

GPIO.setup(Motor3A,GPIO.OUT)
GPIO.setup(Motor3B,GPIO.OUT)
GPIO.setup(Motor3E,GPIO.OUT)

pwm1=GPIO.PWM(22,100)
pwm2=GPIO.PWM(8,100)
pwm3=GPIO.PWM(23,100)
def testDC():

    pwm3.start(0)

    i = 10 
    while(i < 71):
        pwm3.ChangeDutyCycle(i)
        print(i)
        sleep(4)
        i = i + 10

def up():	
	
	pwm1.start(50)	
	pwm3.start(50)
	pwm2.start(100)	

	    GPIO.output(Motor1A,GPIO.LOW)
        GPIO.output(Motor1B,GPIO.HIGH)
        GPIO.output(Motor1E,GPIO.HIGH)

        GPIO.output(Motor3A,GPIO.LOW)
        GPIO.output(Motor3B,GPIO.HIGH)
        GPIO.output(Motor3E,GPIO.HIGH)

        GPIO.output(Motor2A,GPIO.HIGH)
        GPIO.output(Motor2B,GPIO.LOW)
        GPIO.output(Motor2E,GPIO.HIGH)

def down():
	
##      pwm1.start(50)
##      pwm3.start(50)
##      pwm2.start(100)

##      GPIO.output(Motor1A,GPIO.HIGH)
##      GPIO.output(Motor1B,GPIO.LOW)
##      GPIO.output(Motor1E,GPIO.HIGH)

##      GPIO.output(Motor3A,GPIO.HIGH)
##      GPIO.output(Motor3B,GPIO.LOW)
##      GPIO.output(Motor3E,GPIO.HIGH)

##      GPIO.output(Motor2A,GPIO.LOW)
##      GPIO.output(Motor2B,GPIO.HIGH)
##      GPIO.output(Motor2E,GPIO.HIGH)


def right():

	GPIO.output(Motor1A,GPIO.HIGH)
	GPIO.output(Motor1B,GPIO.LOW)
	GPIO.output(Motor1E,GPIO.HIGH)

	GPIO.output(Motor3A,GPIO.LOW)
	GPIO.output(Motor3B,GPIO.HIGH)
	GPIO.output(Motor3E,GPIO.HIGH)

	GPIO.output(Motor2A,GPIO.LOW)
	GPIO.output(Motor2B,GPIO.LOW)
	GPIO.output(Motor2E,GPIO.LOW)


def left():
        GPIO.output(Motor1A,GPIO.LOW)
        GPIO.output(Motor1B,GPIO.HIGH)
        GPIO.output(Motor1E,GPIO.HIGH)

        GPIO.output(Motor3A,GPIO.HIGH)
        GPIO.output(Motor3B,GPIO.LOW)
        GPIO.output(Motor3E,GPIO.HIGH)

        GPIO.output(Motor2A,GPIO.LOW)
        GPIO.output(Motor2B,GPIO.LOW)
        GPIO.output(Motor2E,GPIO.LOW)

print "Turning motor on"
sleep(2)
up()
sleep(2)
#down()
#sleep(2)
#left()
#sleep(2)
#right()
#sleep(2)

print "Stopping motor"
GPIO.output(Motor1E,GPIO.LOW)
GPIO.output(Motor2E,GPIO.LOW)
GPIO.output(Motor3E,GPIO.LOW)
pwm1.stop()
GPIO.cleanup()
