import machine
import time

# Rui Santos & Sara Santos - Random Nerd Tutorials
# Complete project details at https://RandomNerdTutorials.com/raspberry-pi-pico-stepper-motor-micropython/
# Forked from: https://github.com/larsks/micropython-stepper-motor/blob/master/motor.py

class Motor:
    stepms = 10

    # Do be defined by subclasses
    maxpos = 0
    states = []

    def __init__(self, p1 : machine.Pin, p2 : machine.Pin, p3 : machine.Pin, p4 : machine.Pin, stepms : int =None):
        '''
        Create an object that supports a stepper motor with 4 phases.  This code
        is specific to drive a 28BYJ-48 motor attached to a ULN2003 driver.
        
        Note:
        
        All pins must be derrived from machine.Pin, and have an output mode.
        
        Parameters:
            p1 - Pin for First phase
            p2 - Pin for Second phase
            p3 - Pin for third phase
            p4 - Pin for fourth phase
            stepsms - Time needed for steps in Milliseconds
        ''' 
        self.pins = [p1, p2, p3, p4]
        
        # make absolutely sure machine.Pin objects were passed in!
        for pin in self.pins:
            if not isinstance( pin, machine.Pin ):
                raise TypeError( "Pins are not of type Machine.Pin" )

        if stepms is not None:
            self.stepms = stepms

        self._state = 0
        self._pos = 0

    def __repr__(self):
        '''
        Display information about the stepper motor and its current position.
        
        Returns
            A string representing the class name, and position of the stepper motor
        '''
        return '<{} @ {}>'.format(
            self.__class__.__name__,
            self.pos,
        )

    @property
    def pos(self):
        '''
        Create property that allows us to obtain the position of the stepper
        motor
        
        Returns:
            The current position of the stepper motor, in steps since the last
            zero
        '''
        return self._pos

    @classmethod
    def frompins(cls, *pins, **kwargs):
        '''
        Create a class method to allow use to generate a instance of the
        derrived class.
        
        Returns:
            The derived class
        '''
        return cls(*[machine.Pin(pin, machine.Pin.OUT) for pin in pins],
                   **kwargs)

    def zero(self):
        '''
        This member function sets the current position of the stepper motor as
        the new zero.  Once this function is called all relative movements
        relate to the current position.
        
        '''
        self._pos = 0

    def _step(self, dir : int ):
        '''
        Stepper motors require setting the state of each phase and allowing them
        the time to perform that action.  This routine is called to set the
        proper state for each phase so the movement will occur for a single
        step
        
        Parameters:
            dir - 1 for forward, -1 for reverse.
        
        '''
        state = self.states[self._state]

        for i, val in enumerate(state):
            self.pins[i].value(val)

        self._state = (self._state + dir) % len(self.states)
        self._pos = (self._pos + dir) % self.maxpos

    def step(self, steps : int):
        '''
        This member function performs multiple steps of the stepper motoer one
        at a time, allowing for proper amount if time between requests so the
        stepper moves appropriately.
        
        Parameter:
            steps - The number of steps the stepper should be moved
        
        '''
        dir = 1 if steps >= 0 else -1
        steps = abs(steps)

        for _ in range(steps):
            t_start = time.ticks_ms()

            self._step(dir)

            t_end = time.ticks_ms()
            t_delta = time.ticks_diff(t_end, t_start)
            time.sleep_ms(self.stepms - t_delta)

    def step_until(self, target : int , dir : int = None):
        '''
        Move the stepper motor until we the specified number of
        steps has been reached.  Note that the target value must be positive
        and the direction set to -1 to reverse the stepper.
        
        If the target is less than zero,m or we have already reached the
        max position, a value error will be raised.
        
        If no direction is provided, this code will automastically set the
        direction to move the stepper in the closest way... note set the
        direction if you wish to override.
        
        Parameters:
            target - The locaton relative to zero we wish to reach
            dir    - The direction to move it.  If not provided, the direction
                     will be set toe shortest distance from were the stepper
                     is to where we want it to be.
        '''
        if target < 0 or target > self.maxpos:
            raise ValueError(target)

        if dir is None:
            dir = 1 if target > self._pos else -1
            if abs(target - self._pos) > self.maxpos/2:
                dir = -dir

        while True:
            if self._pos == target:
                break
            self.step(dir)

    def step_until_angle(self, angle : int , dir : int = None):
        '''
        Move from current position by the specifified angle, relatively from
        the current position of the motor,
        
        Parameters:
            angle    - The angle from 1 -> 359
            dir      - Direction to move in
            
        Note:  If you so not specify a direction, a direction will be choses
               that will result in the least amount of movement.  To override
               this behavior, set a direction.
        '''
        if angle < 0 or angle > 360:
            raise ValueError(angle)

        target = int(angle / 360 * self.maxpos)
        self.step_until(target, dir=dir)
        
    def step_degrees(self, degrees : int):
        '''
        Move the stepper the specified number of degrees from the current
        position.
        
        Parameter:
            degrees - The number of degrees to move
            
        '''
        if degrees < 0 or degrees > 360:
            raise ValueError("Degrees should be between 0 and 360")

        steps_to_take = int(degrees / 360 * self.maxpos)

        self.zero()  # Ignore the current position, start from zero
        self.step(steps_to_take)

class FullStepMotor(Motor):
    '''
    Create a full move stepper motor, i.e. the motor will move one complete step
    at a time.
    
    Returns:
        A stepper motor object
    '''
    stepms = 5
    maxpos = 2048
    states = [
        [1, 1, 0, 0],
        [0, 1, 1, 0],
        [0, 0, 1, 1],
        [1, 0, 0, 1],
    ]


class HalfStepMotor(Motor):
    '''
    Create a half step motor object. The motor is moved at 1/2 a step at a time.
    
    Returns:
        A stepper motor object
    '''
    stepms = 3
    maxpos = 4096
    states = [
        [1, 0, 0, 0],
        [1, 1, 0, 0],
        [0, 1, 0, 0],
        [0, 1, 1, 0],
        [0, 0, 1, 0],
        [0, 0, 1, 1],
        [0, 0, 0, 1],
        [1, 0, 0, 1],
    ]

if __name__ == "__main__":
    def moveTest( obj ):
        obj.zero()
        print( obj )
        obj.step( 10 )
        print( obj )
        if obj.pos != 10:
            raise ValueError( "Bad move" )
        
        obj.step_until( 30 )
        print( obj )
        if obj.pos != 30:
            raise ValueError( "Bad move" )
        
        obj.step_until_angle( 30 )
        print( obj )
        obj.step_degrees( 20 )
        print( obj )
        
    #  Make sure it fail if we initialize it incorrectly
    try:
        test = Motor( 1, 2, 3, 4, 5 )
    except TypeError as e:
        print( f"Received the expected type error : {e}" )
    except:
        print( "Total failure" )
        
    try:
        test = FullStepMotor.frompins( 5,4,3,2 )
        moveTest( test )
    except:
        print( "Full step failue!" )
        
    try:
        test = HalfStepMotor.frompins( 5,4,3,2 )
        moveTest( test )
    except:
        print( "Half Step failure!" )
        
        
