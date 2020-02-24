#!/usr/bin/env python
# coding: utf-8

# In[1]:


from picamera.array import PiYUVArray, PiRGBArray
from picamera import PiCamera

from scipy.signal import find_peaks, butter, filtfilt

import time
import matplotlib.pyplot as plt
import skimage as ski
import numpy as np

# Camera resolution
res = (640, 480)

CAMERA_CENTER = res[0] // 2
       
from raceon import PWM

import pygame


# ## Setup servo and motor PWM signal to control the steering angle and the speed.
# 
# The values specified period and duty cycle ar in nanoseconds.
# 
# Servo and motor controlled follow the following protocol:
#   1. Control signal is read 50 times per second by each device (servo and speed controller). Thus period is 20 ms => 20000000 ns
#   2. To send the minimum value (full left for servo and break for motor) the duty cycle should be 1 ms => 1000000 ns
#   3. Maximum value corresponds to a duty cycle of 2 ms => 2000000 ns
#   
# However, these devices are not perfect and you can set a duty cycle outside this range and still get a response. I would recoment to play with it and find are the limits in your case. Pay attention that servo is limited by the mechanical construction how much it can turn the wheels. Do not set these limits to a value which servo cannot execute as it will try to do that and eventually burn.

# In[2]:


# Setup joystick
pygame.init()
clock = pygame.time.Clock()
pygame.joystick.init()
joystick_count = pygame.joystick.get_count()
joystick = pygame.joystick.Joystick(0)
joystick.init()
axes = joystick.get_numaxes()


# In[2]:


# Enable servo
SERVO_MIDDLE = 1500000

servo = PWM(1)
servo.period = 20000000
servo.duty_cycle = SERVO_MIDDLE
servo.enable = True


# In[3]:


# Enable servo
MOTOR_BRAKE = 1000000

motor = PWM(0)
motor.period = 20000000
motor.duty_cycle = MOTOR_BRAKE
motor.enable = True


# In[4]:


motor.duty_cycle = MOTOR_BRAKE 


# ## The self driving code
# 
# Quick explanation on how this algorithm works:
#   1. Initialize the camera, use a frame rate of 10 to 20 fps
#   2. Get the coefficients of the butterworth filter of order 3 and cut-off frequency of 0.1 (change cut of frequency if the peak functions is not working)
#   3. For each frame captured from the camera:
#     1. Get the blak and white part of the image
#     2. Select line 195 to use for lane detection (this number depends on your camera angle)
#     3. Filter the line and find the peaks that are greater than 160. White parts of the image have higher values than the black. The threshold of 160 depends on the ambient light, lower if the room is darker
#     4. Find the peaks left and right of the camera center, these peaks should corresponds to the white lines delimiting the track,
#     5. Compute the center point between these lines. This is where we want our car
#     6. Compute the error by substracting the center point from camera middle and multiply by 5000. 5000 is our P gain.
#     7. Adjust the duty cycle of the servo such that the

# In[5]:


# Run a track detection algorithm on a single horizontal line.
# Uses YUV420 image format as the Y component corresponds to image intensity (gray image)
# and thus there is no need to convert from RGB to BW

RUN_TIMER = 10 # seconds
history=[]

camera = PiCamera()
        
# Check the link below for the combinations between mode and resolution
# https://picamera.readthedocs.io/en/release-1.13/fov.html#sensor-modes
camera.sensor_mode = 7
camera.resolution = res
camera.framerate = 10

# Initialize the buffer and start capturing
rawCapture = PiYUVArray(camera, size=res)
stream = camera.capture_continuous(rawCapture, format="yuv", use_video_port=True)

# Measure the time needed to process 300 images to estimate the FPS
t = time.time()

# To filter the noise in the image we use a 3rd order Butterworth filter

# Wn = 0.02, the cut-off frequency, acceptable values are from 0 to 1
b, a = butter(3, 0.1)

line_pos    = CAMERA_CENTER
first_frame = True

# start car
motor.duty_cycle = MOTOR_BRAKE + 180000

for f in stream:
    if first_frame:
        first_frame = False
        # Reset the buffer for the next image
        rawCapture.truncate(0)
        continue
    
    # Stop after RUN_TIMER seconds
    if (time.time() - t) > RUN_TIMER:
        break
        
    # Get the intensity component of the image (a trick to get black and white images)
    I = f.array[:, :, 0]
    
    # Reset the buffer for the next image
    rawCapture.truncate(0)
    
    # Select a horizontal line in the middle of the image
    L = I[270, :]

    # Smooth the transitions so we can detect the peaks 
    Lf = filtfilt(b, a, L)
    history.append(Lf)

    # Find peaks which are higher than 0.5
    p = find_peaks(Lf, height=160)   
    
    peaks = p[0]
    
    line_left   = None
    line_right  = None
    peaks_left  = peaks[peaks < CAMERA_CENTER]
    peaks_right = peaks[peaks > CAMERA_CENTER]

    if peaks_left.size:
        line_left = peaks_left.max()

    if peaks_right.size:
        line_right = peaks_right.min()
        
    if line_left and line_right:
        line_pos    = (line_left + line_right ) // 2
        track_width = line_right - line_left
        
    elif line_left and not line_right:
        line_pos    = line_left + int(track_width / 2)
        
    elif not line_left and line_right:
        line_pos    = line_right - int(track_width / 2)
        
    else:
        print("no line")

    print(line_pos, peaks)

    # joystick 
    for event in pygame.event.get(): # User did something.
        if event.type == pygame.JOYBUTTONDOWN:
            print("Joystick button pressed.")
        elif event.type == pygame.JOYBUTTONUP:
            print("Joystick button released.")
    
    steering = joystick.get_axis(0)  # left stick x axis
    print("steering: "+str(steering))
    DUTY_CYCLE = int(SERVO_MIDDLE + 500000 * steering)
    
    gas = (joystick.get_axis(5) + 1) / 2  # right trigger, normalize from (-1, 1) to (0, 1)
    print("gas: "+str(gas))
    motor.duty_cycle = int(MOTOR_BRAKE + (180000 - MOTOR_BRAKE) * gas)

    
    if joystick.get_button(2):  # "x" button
        RUN_TIMER = 0 # stop the loop
        
        
    #DUTY_CYCLE = SERVO_MIDDLE + 5000 * (CAMERA_CENTER - line_pos)
    if DUTY_CYCLE > 2000000:
        DUTY_CYCLE = 2000000
    if DUTY_CYCLE < 1000000:
        DUTY_CYCLE = 1000000
        
    servo.duty_cycle =  DUTY_CYCLE

    

#Initialize lines position
#Check which lines are closer them in the next frame

        
        #print(line_pos)
        
motor.duty_cycle = MOTOR_BRAKE    
    

# Release resources
stream.close()
rawCapture.close()
camera.close()

# joystick
pygame.quit()


# In[6]:


# Release resources
stream.close()
rawCapture.close()
camera.close()
motor.duty_cycle = MOTOR_BRAKE   


# In[7]:


plt.imshow(I)
print(peaks)


# In[8]:



peaks = p[0]

line_left   = None
line_right  = None
peaks_left  = peaks[peaks < CAMERA_CENTER]
peaks_right = peaks[peaks > CAMERA_CENTER]

if peaks_left.size:
    line_left = peaks_left.max()
    
if peaks_right.size:
    line_right = peaks_right.min()
    
p


# In[9]:


L = I[200, :]
b, a = butter(3, 0.1)
Lf = filtfilt(b, a, L)

plt.plot(L)
plt.plot(Lf)


# In[10]:


plt.imshow(np.vstack(history))


# In[ ]:





# In[ ]:




