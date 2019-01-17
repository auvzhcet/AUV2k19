import cv2
import numpy as np

cap = cv2.VideoCapture(0)
fourcc = cv2.VideoWriter_fourcc(*'XVID')
out = cv2.VideoWriter('output.avi', fourcc, 20.0, (640,480))

def capture():
    global cap, out
    
    _, frame = cap.read()
    out.write(frame)

def destroy():
    global cap, out 
    cap.release()
    out.release()
    cv2.destroyAllWindows()

    
def main():
    global cap, out

    while True:
        _, frame = cap.read()
        # cv2.imshow("frame", frame)
        out.write(frame)

        # key = cv2.waitKey(20)
        # if key & 0xFF == ord('q'):
        #   break


    cap.release()
    out.release()
    # cv2.destroyAllWindows()

if __name__ == '__main__':
    main()
