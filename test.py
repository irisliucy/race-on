import pygame

# Enable servo
SERVO_MIDDLE = 1500000
# servo = PWM(1)
# servo.period = 20000000
# servo.duty_cycle = SERVO_MIDDLE
# servo.enable = True

# Enable servo
MOTOR_BRAKE = 1000000
# motor = PWM(0)
# motor.period = 20000000
# motor.duty_cycle = MOTOR_BRAKE
# motor.enable = True

pygame.init()
clock = pygame.time.Clock()
pygame.joystick.init()
joystick_count = pygame.joystick.get_count()
joystick = pygame.joystick.Joystick(0)
joystick.init()
axes = joystick.get_numaxes()

quitTest = False
while not quitTest:
    for event in pygame.event.get(): # User did something.
        if event.type == pygame.JOYBUTTONDOWN:
            print("Joystick button pressed.")
        elif event.type == pygame.JOYBUTTONUP:
            print("Joystick button released.")

    steering = joystick.get_axis(0)  # left stick x axis
    print("steering: "+str(steering))
    DUTY_CYCLE = SERVO_MIDDLE + 500000 * steering
    if DUTY_CYCLE > 2000000:
        DUTY_CYCLE = 2000000
    if DUTY_CYCLE < 1000000:
        DUTY_CYCLE = 1000000
        # servo.duty_cycle =  DUTY_CYCLE

    gas = (joystick.get_axis(5) + 1) / 2  # right trigger, normalize from (-1, 1) to (0, 1)
    print("gas: "+str(gas))
    # motor.duty_cycle = MOTOR_BRAKE + (120000 - MOTOR_BRAKE) * gas

    if joystick.get_button(2):  # "x" button
        quitTest = True

    clock.tick(20)

pygame.quit()