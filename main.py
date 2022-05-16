import cv2
import numpy as np
from matplotlib import pyplot as pltq
import serial

""" serial setting """
ser = serial.Serial()
ser.baudrate = 115200
ser.port = '/dev/ttyUSB0'
digi = 0
ss = ''
x = 0
ser.open()

"""camera setting """
size = 100
curX = 300
cap = cv2.VideoCapture(0)
# display text
font = cv2.FONT_HERSHEY_SIMPLEX
text_scale = 0.7
text_line_thickness = 1
text_color = (100, 255, 0)

while cap.isOpened():
    # serial stuff
    if ser.in_waiting: 
        cc = ser.read(1)
        if (cc.isdigit()==True):
            ss = ss + cc.decode("utf-8")
            digi += 1
            if digi > 4:
                x = int(((int(ss) - 20000)/15000)*580)
                print(ss)
                digi = 0
                ss = ''

    ret, frame = cap.read()
    fps = cap.get(cv2.CAP_PROP_FPS)
    #print(fps)
    image = cv2.flip(frame, 0)
    #image = cv2.flip(image, 1)

    # Draw circle
    cv2.circle(image,(curX,600-x), 20, (0,255,0), 2)
    # display FPS
    cv2.putText(image, str(fps), (7, 35), font, text_scale, text_color,text_line_thickness, cv2.LINE_AA)
    # show image
    cv2.imshow('webcam', image)
    if cv2.waitKey(1) & 0xFF == ord('q'):
   	 break

cap.release()
cv2.destroyAllWindows()
ser.close()