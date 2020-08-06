# AUV2k19
---
> Software stack for the vehicle that participated in SAVe 2019
>
*Note: Major portion of this code was hastily written a month before the competition. Hence, brace yourself for bad coding practices!*

### Repository Structure 
- `motion`: Includes all codes related to motion
  - `movement.py`: the main motion module that includes all basic movements. It is intended to be used as a library for all major tasks.
  - `line_follower.py`:  the code we used in the competition. The name is misleading. Its actually bouy detection and following, which was the fist task of the competition. 
  - `camera.py`: camera utility functions and vision-based bouy detection algorithms. This module should ideally be inside the `vision` folder.
  - `thrust.py`, `thrust_new.py` and `thrust_bouy.py` are just test scripts and can be safely ignored.
- `sensors`: sensor related modules
  - `IMU.py`: A utility script to read IMU data. The code here is copied and not written by us.
    - This might help if you want to interface IMU with Pi. [Accelerometer, Gyroscope, and Magnetometer Analysis with Raspberry Pi Part I: Basic Readings — Maker Portal](https://makersportal.com/blog/2019/11/11/raspberry-pi-python-accelerometer-gyroscope-magnetometer)
  - `NodeRead.py`: Need of NodeRead.py and how it works?
    - Our Vehicle had two controllers: Pi and NodeMCU
    - We used NodeMCU because pressure sensor throws analog data which can't be read by Pi.
    - Hence NodeMCU was used for reading  analog data from pressure sensor.
    - NodeMCU then sent this data to Pi over a USB acting as a TTY(terminal)
    - NodeRead.py is used to read this data from terminal.
    - Note: You will node nead this if you use and ADC(Anolog to Digital Convertor) to convert pressure sensor data to digital form.
    - A special thanks to [Ishan Singh](https://github.com/proishan11) for writing this code. 
- `vision`: camera related code
  - `VideoRecord.py`: A script to record and save video.
- `keyboard.py`: 
  - A script to manuall control the AUV using keyboard.
  - Generally you have to press `enter` to give input to a program. To avoid that, I used the `curses` module.
-  `main.py`:
   -  This is the driver script for `line_follower.py`
   -  This is the script that we ran in the SAVe competition.
   -  So yes, running `python main.py` helped us reach finals and secure 4th rank in SAVe 2019.
 -  Test Scripts: Ideally, they should have been in a separate test folder. But currently they are present in the root folder itself.
    - `test_camera.py`: check if camera is working
    - `test_depth.py`: test the code that maintains depth and pitch simultaneously.
    - `test_pitch.py`: check the code that maintains pitch

### Hydrophones
- Read `hydrophones_study.md`
- Most of the work in this area is done by [Jawad Akhtar](https://github.com/syedjawadakhtar)


### Tech Stack
- OpenCV
- Numpy
- Python
- Raspberry Pi 3B+
- Node MCU
- Pressure Sensor
- IMU MPU6050