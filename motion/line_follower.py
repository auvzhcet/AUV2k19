#!/usr/bin/env python
import cv2
import numpy
from motion import movement
import time

cap = cv2.VideoCapture(0)
fourcc = cv2.VideoWriter_fourcc(*'XVID')
out_image = cv2.VideoWriter('recording-%s.avi' % time.time(), fourcc, 20.0, (640, 480))

m = movement.Movement()

# RED: 115-135
# Yellow: 90-109
# Geen: 29-61
def mask_image(image, color_no):
    hsv = cv2.cvtColor(image, cv2.COLOR_RGB2HSV)
    # NOTE: Orange Gate not very clearly visible
    lower_array = [numpy.array([115, 0, 0]), numpy.array([21, 0, 0]), numpy.array([40, 0, 0])]
    upper_array = [numpy.array([135, 255, 255]), numpy.array([95, 255, 255]), numpy.array([47, 255, 255])]
    
    lower = lower_array[color_no]
    upper = upper_array[color_no]

    mask = cv2.inRange(hsv, lower, upper)
    cv2.flip(mask, 1)
    _, mask = cv2.threshold(mask, 0, 255, cv2.THRESH_BINARY+cv2.THRESH_OTSU)
    return mask


def centroid_if_object_present(image, mask):
    im2, contours, hierarchy = cv2.findContours(
        mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    try:
        contour = max(contours, key=cv2.contourArea)
        contour_area = cv2.contourArea(contour)
    except:
        contour_area = 0
    
    print("Contour Area = ", contour_area)

    if contour_area > 500:
        print("OBJECT PRESENT")
        x, y, w, h = cv2.boundingRect(contour)

        # TODO: Remove this line.
        cv2.rectangle(image, (x, y), (x+w, y+h), (0, 255, 0), 2)

        cx, cy = (x + w/2), (y + h/2)
        draw_centroid(image, cx, cy)
        return ((cx, cy), contour_area)

    return False, False


def draw_centroid(overlay, cx, cy):
    cv2.circle(overlay, (int(cx), int(cy)), 20, (0, 0, 255), -1)


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

    err_y = cy - h/2
    constant = 90
    y_slope = 1/30.
    m.hp_control(err_y*y_slope + constant)

    thrusts = {
        m.pin_l: linear_thrust + rot_thrust,
        m.pin_r: linear_thrust - rot_thrust,
    }
    m.custom_thrusts(thrusts)


def tearDown():
    """
    Call as API to release camera.
    """
    global cap, out_image
    cap.release()
    out_image.release()
    cv2.destroyAllWindows()

touch = False
s_time = None

color_no = 0
def run():
    global touch, s_time, color_no


    rec, image = cap.read()
    mask = mask_image(image, color_no)
    centroid, contour_area = centroid_if_object_present(image, mask)
    out_image.write(image)
    if not touch:
        if centroid:
            if contour_area > 90000:
                touch = True
                s_time = time.time()
                color_no = color_no + 1
            else:
                (cx, cy) = centroid
                correct_error(cx, cy, image)
        else:
            if color_no > 1:
                print("Go Left!")
                m.left(100)
            else:
                print("Go Right!")
                m.right(100)

    else:
        print('!!!!!! touch  !!!!!!!!!!!!')
        if (time.time() - s_time <= 1):
            m.forward(100)
        elif (1 < time.time() - s_time <= 2):
            m.hold()
        elif (2 < time.time() - s_time <= 6):
            m.backward(150)
        else:
            m.hold()
            touch = False


def main():
    while True:
        rec, image = cap.read()

        # See on Yellow
        mask = mask_image(image, 1)
        centroid = centroid_if_object_present(image, mask)
        out_image.write(image)

        if centroid:
            (cx, cy) = centroid
            # correct_error(cx, cy, image)
        else:
            print("Searching! Go Right!")
            # m.right(100)
            # m.pitch_control()

        cv2.imshow("Image", cv2.resize(image, (640, 480)))
        cv2.imshow("Mask", cv2.resize(mask, (640, 480)))
        key = cv2.waitKey(20)
        if key & 0xFF == ord('q'):
            tearDown()
            break


if __name__ == '__main__':
    main()
