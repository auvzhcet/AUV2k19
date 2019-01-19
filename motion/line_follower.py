#!/usr/bin/env python
import cv2
import numpy
from motion import movement
import time

cap = cv2.VideoCapture(0)
fourcc = cv2.VideoWriter_fourcc(*'XVID')
out_image = cv2.VideoWriter('recording.avi', fourcc, 20.0, (640, 480))

m = movement.Movement()

# RED: 115-135
# Yellow: 90-109
def mask_image(image):
    hsv = cv2.cvtColor(image, cv2.COLOR_RGB2HSV)
    lower = numpy.array([90, 0, 0])
    upper = numpy.array([109, 255, 255])
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
    linear_thrust = 1650
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

def run():
    global touch, s_time
    

    rec, image = cap.read()
    mask = mask_image(image)
    centroid, contour_area = centroid_if_object_present(image, mask)
    out_image.write(image)
    if not touch:
        if centroid:
            if contour_area > 100000:
                touch = True
                s_time = time.time()
            else:
                (cx, cy) = centroid
                correct_error(cx, cy, image)
        else:
            print("Go left!")
            m.left(100)

    else:
        print('!!!!!! touch  !!!!!!!!!!!!')
        if (time.time() - s_time <= 2):
            m.forward(100)
        elif (2 < time.time() - s_time <= 3):
            m.hold()
        elif (3 < time.time() - s_time <= 7):
            m.backward(100)
        else:
            m.hold()
            touch = False


def main():
    while True:
        rec, image = cap.read()

        mask = mask_image(image)
        centroid = centroid_if_object_present(image, mask)
        out_image.write(image)

        if centroid:
            (cx, cy) = centroid
            correct_error(cx, cy, image)
        else:
            print("Go left!")
            m.left(100)

        cv2.imshow("window", image)
        cv2.imshow("mask", mask)
        key = cv2.waitKey(20)
        if key & 0xFF == ord('q'):
            tearDown()
            break


if __name__ == '__main__':
    main()
