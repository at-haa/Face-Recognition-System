$ sudo apt update
$ sudo apt upgrade -y
$ sudo apt autoremove
$ sudo apt install python3-opencv -y
$ pip3 install rpi_lcd
$ pip3 install dlib
$ pip3 install face_recognition
$ pip3 install imutils

# Enable Camera Interface in raspi-config
$ sudo raspi-config  
# Select Interface Options
# Select Camera
# Select YES

# Enable I2C Interface in raspi-config
# Select Interface Options
# Select I2C
# Select YES

# Select <Finish>

$ sudo reboot now

$ sudo apt install motion -y
# Download debian file if there were error
$ sudo modprobe bcm2835-v4l2
$ sudo nano /etc/motion/motion.conf
# following lines must be changed
----------------------------------------------------------------------------------------------------
# Start in daemon (background) mode and release terminal (default: off)
daemon on
...
# Restrict stream connections to localhost only (default: on)
stream_localhost off
...
# Target base directory for pictures and films
# Recommended to use absolute path. (Default: current working directory)
target_dir /home/pi/Monitor

v4l2_palette 15     # Nummer aus der Tabelle davor entnehmen, 15 enstpricht YUYV
... 
# Image width (pixels). Valid range: Camera dependent, default: 352 
width 640 

# Image height (pixels). Valid range: Camera dependent, default: 288 
height 480 # Maximum number of frames to be captured per second. 

# Valid range: 2-100. Default: 100 (almost no limit). 
framerate 10 
...
stream_maxrate 30
----------------------------------------------------------------------------------------------------

$ sudo nano /etc/default/motion
# The following lines must be changed
----------------------------------------------------------------------------------------------------
start_motion_daemon=yes
----------------------------------------------------------------------------------------------------

$ mkdir /home/pi/Monitor
$ sudo chgrp motion /home/pi/Monitor
$ chmod g+rwx /home/pi/Monitor

$ sudo service motion start
# Camera will be streamed on port 8081

$ DISPLAY=:0 chromium-browser -kiosk -app=http://127.0.0.1:8081
# Show Stream on LCD using chromium

$ git clone repo