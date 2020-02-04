#!/usr/bin/env python
# coding: utf-8

# # Test scripts for motor and servo components

# In[1]:


import time
import matplotlib.pyplot as plt
import numpy as np

from raceon import PWM


# ### Motor initialization and configuration
# 
# Motor speed range [0 - stop, 1 - full speed]

# In[2]:


# Enable servo
# object for servo
MOTOR_BRAKE = 1000000

motor = PWM(0)
motor.period = 20000000
motor.duty_cycle = MOTOR_BRAKE
motor.enable = True

#!! Wait for 3 seconds until the motor stops beeping


# # Upon start of device, motor speed must be set to 0 for at least 5 seconds 

# In[3]:


motor.duty_cycle = MOTOR_BRAKE + 120000 # Motor should run at low speed


# In[ ]:


motor.duty_cycle = MOTOR_BRAKE + 1000000 # Motor full speed


# In[4]:


motor.duty_cycle = MOTOR_BRAKE # stop motor


# ### Servo configuration and calibration
# 
# Servo angle range [-1 - full left, 0 - center, 1 - full right]
# 
# * Physical calibration of steering
# - Mount the motor on the vehicle
# - Mount the servo on the vehicle and while keeping the wheels straight. 
# - Calibrate the servo to zero angle (with the while 
# 

# In[1]:


# # Enable servo
# # object for servo
SERVO_MIDDLE = 1500000

servo = PWM(1)
servo.period = 20000000
servo.duty_cycle = SERVO_MIDDLE
servo.enable = True


# In[ ]:


servo.duty_cycle = SERVO_MIDDLE - 500000 # Full left


# In[ ]:


servo.duty_cycle = SERVO_MIDDLE + 500000 # Full right


# In[ ]:


servo.duty_cycle = SERVO_MIDDLE # Back to middle


# # Now mount the servo

# In[ ]:




