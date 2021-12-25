import cv2
from picamera import PiCamera
from picamera.array import PiRGBArray

name = 'Fateme' #replace with your name
RES_WIDTH, RES_HEIGHT = 640, 480
FRAMERATE = 30

cam = PiCamera()
cam.resolution = (RES_WIDTH, RES_HEIGHT)
cam.framerate = FRAMERATE
rawCapture = PiRGBArray(cam, size=(RES_WIDTH, RES_HEIGHT))
    
pics_count = 1
keyboard_input = -1

for frame in cam.capture_continuous(rawCapture, format="bgr", use_video_port=True):
    image = frame.array
    cv2.imshow("Press c to capture", image)
    rawCapture.truncate(0)
    keyboard_input = cv2.waitKey(1)
    
    if (chr(keyboard_input%256).lower() == 'q') or pics_count == 11:
        break
    
    if chr(keyboard_input%256).lower() == 'c':
        img_name = "dataset/"+ name +"/image{}.jpg".format(pics_count)
        cv2.imwrite(img_name, image)
        print("{} written!".format(img_name))
        pics_count += 1
            

cv2.destroyAllWindows()
