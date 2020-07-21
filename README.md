# Race On self-driving car

### Race-on competition result 
We won the third place overall in USC [Race-on](https://raceon.io/) competition in Spring 2020.

### SSH Remote raspberry pi
```
ssh pi@raspberrypi-304.local
```

password: raspeberry

### TODO
- [ ] Add PID
- [x] Understand the parameters of the codes
- [ ] Improve the contrast code
- [ ] Collect images for modeling


### Branches
- master: Final release for the whole project upon completion
- staging: Default branch which will be used for running in races
- Iterm: PID addition to the code
- joystick: Joystick code for controlling the car
- original_master_code: Original code provided by the organization team
- race-1-basic: Changes made to the original_master_code for testing purpose before it is pushed to staging

### Test Results
[9:04 PM, 2/27/2020] Posha Dave: Works:
1) scan-line: 280
2) straight speed: 27000, turn speed: 18000

-------------------------------------------------------
Anticlockwise - Works:
Clockwise - Works: 10.6 sec
1) scan-line: 280
2) straight speed: 30000, turn speed: 18000

--------------------------------------------------------
Anticlockwise - Works: 10.27 sec
Clockwise - Works: 9.40 sec
1) scan-line: 280
2) straight speed: 30000, turn speed: 20000
[9:27 PM, 2/27/2020] Posha Dave: Works:
1) scan-line: 280
2) straight speed: 27000, turn speed: 18000

-------------------------------------------------------
Anticlockwise - Works:
Clockwise - Works: 10.6 sec
1) scan-line: 280
2) straight speed: 30000, turn speed: 18000

--------------------------------------------------------
Anticlockwise - Works: 10.27 sec
Clockwise - Works: 9.40 sec
1) scan-line: 280
2) straight speed: 30000, turn speed: 20000

---------------------------------------------------------
With PID
Anticlockwise - Works: 10.38 sec
Clockwise - Works: 10.20 sec
1) scan-line: 280
2) straight speed: 30000, turn speed: 20000
