from motion import movement
from motion import camera

import numpy as np
import time

m = movement.Movement()


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
    cam = camera.Camera()
    lower = np.array([115, 0, 0])
    upper = np.array([135, 255, 255])

    while True:
        try:
            m.hp_control(33)
            image = cam.read()
            cam.mask_image(lower, upper)
            centroid = cam.centroid_if_object_present()
            if centroid:
                (cx, cy) = centroid
                correct_error(cx, cy, image)
                if cam.should_touch_manoeuver():
                    m.forward(100)
                    print("Going Forward")
                    time.sleep(3)
                    m.backward(100)
                    print("Going backward")
                    time.sleep(3)
            else:
                print("Go left!")
                m.left(100)
                if cam.centroid_if_object_present():
                    break

        except KeyboardInterrupt:
            cam.tearDown()
            # m.hold()
