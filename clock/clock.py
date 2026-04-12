import stepper
import time

# Define the stepper motor pins
IN1 = 5
IN2 = 4
IN3 = 3
IN4 = 2

STEPS_PER_MINUTE = 512
SECONDS_BETWEEN_MOVES = 60
MS_BETWEEN_MOVES = SECONDS_BETWEEN_MOVES * 1000

# Initialize the stepper motor
stepper_motor = stepper.HalfStepMotor.frompins(IN1, IN2, IN3, IN4)

# Set the current position as position 0
stepper_motor.zero()

try:
    while True:
        
        #Move STEPS_PER_MINUTE steps in counter clockwise direction
        start = time.ticks_ms()
        stepper_motor.step(STEPS_PER_MINUTE)
        stop = time.ticks_ms()
        delta = time.ticks_diff(time.ticks_ms(),start)
        
        time.sleep_ms( MS_BETWEEN_MOVES - delta )
except KeyboardInterrupt:
    print( "Terminated" )
