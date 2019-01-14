#!/usr/bin/env python
import cv2
import numpy
import pigpio

# cap = cv2.VideoCapture('plank_video.mp4')
cap = cv2.VideoCapture(1)

pi = pigpio.pi()


def mask_image(image):
    hsv = cv2.cvtColor(image, cv2.COLOR_RGB2HSV)
    lower = numpy.array([115, 0, 0])
    upper = numpy.array([150, 255, 255])
    mask = cv2.inRange(hsv, lower, upper)
    cv2.flip(mask, 1)
    return mask


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
    print("[DEBUG] ERR: ", err)
    # NOTE: If the motion is too erratic, then consider a median range
    #      where there shall be no lateral movement

    # TODO: Propel linearly
    linear_thrust = 1600
    slope = 5/8

    if err < 0:
        # Move the robot left
        print("Move Left")
        thrust_new = -1*err*slope + linear_thrust
        pi.set_servo_pulsewidth(23, thrust_new)
        pi.set_servo_pulsewidth(15, linear_thrust)

    else:
        # Move the robot right
        print("Move Right")
        thrust_new = err*slope + linear_thrust
        pi.set_servo_pulsewidth(15, thrust_new)
        pi.set_servo_pulsewidth(23, linear_thrust)


def main():
    # NOTE: To avoid randomly occuring ZeroDivisionError and variable not
    #       initialized error, wrap the whole thing in try/escape.
    while True:
        rec, image = cap.read()
        # image = cv2.imread("plank_video_new.jpeg")
        mask = mask_image(image)
        cx, cy = centroid_from_mask(image, mask)
        correct_error(cx, cy, image)

        # cv2.imshow("window", image)
        # cv2.waitKey(25)


if __name__ == '__main__':
    main()
