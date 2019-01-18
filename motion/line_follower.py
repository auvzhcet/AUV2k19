#!/usr/bin/env python
import cv2
import numpy
from motion import movement

cap = cv2.VideoCapture(0)
fourcc = cv2.VideoWriter_fourcc(*'XVID')
out_image = cv2.VideoWriter('recording.avi', fourcc, 20.0, (640,480))

m = movement.Movement()

def mask_image(image):
    hsv = cv2.cvtColor(image, cv2.COLOR_RGB2HSV)
    lower = numpy.array([115, 0, 0])
    upper = numpy.array([150, 255, 255])
    mask = cv2.inRange(hsv, lower, upper)
    cv2.flip(mask, 1)
    _, mask = cv2.threshold(mask, 0, 255, cv2.THRESH_BINARY+cv2.THRESH_OTSU)
    return mask

def max_contour_center(image, mask):
    im2, contours, hierarchy = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    c = max(contours, key = cv2.contourArea)
    
    # Add contour area check

    x,y,w,h = cv2.boundingRect(c)

    cv2.rectangle(image, (x,y), (x+w, y+h), (0, 255, 0), 2)

    cx, cy = (x + w/2), (y + h/2)

    return cx, cy, image


def draw_centroid(overlay, cx, cy):
    cv2.circle(overlay, (cx, cy), 20, (0, 0, 255), -1)


def centroid_from_mask(image, mask):
    M = cv2.moments(mask)
    if M['m00'] > 0:
        cx = int(M['m10']/M['m00'])
        cy = int(M['m01']/M['m00'])
    else:
        cx, cy = 0, 0
    draw_centroid(image, cx, cy)
    return cx, cy


def correct_error(cx, cy, image):
    h, w, d = image.shape
    # NOTE: If it doesn't seems to work, try changing to cy to cx
    err = cx - w/2
    # NOTE: If the motion is too erratic, then consider a median range
    #      where there shall be no lateral movement

    # TODO: Propel linearly
    linear_thrust = 1600
    slope = 5/16
    rot_thrust = err*slope
    
    rot_thrust = max(-100, min(rot_thrust, 100))
    if rot_thrust >= 0:
        print('Left')
    else:
        print('Right')

    print('rot_thrust = ', rot_thrust)
    thrusts = {
        m.pin_l: linear_thrust + rot_thrust,
        m.pin_r: linear_thrust - rot_thrust
    }
    m.custom_thrusts(thrusts)


def run():
    # NOTE: To avoid randomly occuring ZeroDivisionError and variable not
    #       initialized error, wrap the whole thing in try/escape.
    rec, image = cap.read()
    # image = cv2.imread("plank_video_new.jpeg")
    mask = mask_image(image)
    # cx, cy = centroid_from_mask(image, mask)
    
    correct_error(cx, cy, image)

    # Record the video for debugging purposes
    out_image.write(image)

    # cv2.imshow("window", image)
    # key = cv2.waitKey(20)
    # if key & 0xFF == ord('q'):
    #     break


def tearDown():
    global cap, out_image
    cap.release()
    out_image.release()
    cv2.destroyAllWindows()


def main():
    while True:
        rec, image = cap.read()
        # image = cv2.imread("plank_video_new.jpeg")

        mask = mask_image(image)
        cx, cy = centroid_from_mask(image, mask)
        correct_error(cx, cy, image)

        cv2.imshow("window", image)
        key = cv2.waitKey(20)
        if key & 0xFF == ord('q'):
            break

if __name__ == '__main__':
    main()
