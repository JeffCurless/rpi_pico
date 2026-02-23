# Clock — Stepper Motor Clock

Advances a clock hand exactly one minute tick every 60 seconds using a 28BYJ-48 stepper motor and ULN2003 driver board.

## Files

### stepper.py

Motor driver classes for the 28BYJ-48 stepper:

- **`Motor`** — base class with shared step logic
- **`FullStepMotor`** — drives the motor in full-step mode
- **`HalfStepMotor`** — drives the motor in half-step mode (smoother, more torque)

**Key methods:**

| Method | Description |
|---|---|
| `frompins(p1, p2, p3, p4)` | Class method — create an instance from four GPIO pin numbers |
| `step(n)` | Advance the motor `n` steps |
| `step_until(pos)` | Step until the motor reaches an absolute position |
| `step_until_angle(deg)` | Step until the motor reaches a given angle |
| `step_degrees(deg)` | Step the motor by a relative angle in degrees |

### clock.py

- Wires `HalfStepMotor` to GPIO pins 2, 3, 4, 5
- Steps 512 half-steps (one full revolution of the output shaft geared to one minute-hand tick) every 60 seconds
- Uses `time.ticks_ms()` to subtract the time spent stepping, so the 60-second interval stays accurate

## Wiring

Connect the ULN2003 driver board IN1–IN4 pins to Pico GPIO 2–5. Power the driver from 5 V (VBUS) for best torque.

## Parent

See the [project root](../README.md) for an overview of all projects.
