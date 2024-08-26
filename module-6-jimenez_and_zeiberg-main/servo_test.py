import RPi.GPIO as GPIO
import time
GPIO.setmode(GPIO.BOARD)
GPIO.setwarnings(False) 

# Define pin, frequency and duty cycle
PWM_pin   = 11
freq      = 50

# Configure pin for output
GPIO.setup(PWM_pin, GPIO.OUT)

# Create PWM instance for pin w freqency
pwm = GPIO.PWM(PWM_pin, freq)

while True:
  dutyCycleLow = float(input('Set low duty cycle: '))
  dutyCycleHigh = float(input('Set high duty cycle: '))
  
  # Start the PWM object
  pwm.start(dutyCycleLow)
  time.sleep(1)           # let it sit for a second
  
  # Change the duty cycle
  pwm.ChangeDutyCycle(dutyCycleHigh)
  time.sleep(0.1)         # give it time to move 

# Stop the output for the PWM pin 
pwm.stop()
GPIO.cleanup()
