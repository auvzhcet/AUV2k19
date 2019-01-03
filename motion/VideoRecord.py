import cv2
import numpy as np

cap = cv2.VideoCapture(0)
fourcc = cv2.VideoWriter_fourcc(*'XVID')
out = cv2.VideoWriter('output.avi',fourcc, 20.0, (640,480))

def capture():
    global cap, out
    
    _, frame = cap.read()
    out.write(frame)

def destroy():
    global cap, out 
    cap.release()
    out.release()
    cv2.destroyAllWindows()
