from NodeRead import NodeRead

import pigpio
import time
import IMU

pin_f = 11
pin_b = 12
pin_r = 23
pin_l = 15

THRUSTER_PINS = [pin_f, pin_b, pin_r, pin_l]

width_h = 1600
width_l = 1400

noderead = NodeRead()


def get_rot_thrust(x_rot):
    max_thrust = 400
    thrust_per_degree = max_thrust/90
    rot_thrust = x_rot*thrust_per_degree
    if rot_thrust >= 200:
        rot_thrust = 200

    if rot_thrust <= -200:
        rot_thrust = -200

    return rot_thrust


class Movement:
    def __init__(self):
        self.pi = pigpio.pi()

        self.man_under_thrust = 150

        print("Initialisation. Setting pulse width to 1500")
        for pin in THRUSTER_PINS:
            self.pi.set_servo_pulsewidth(pin, 1500)

        time.sleep(1)

    def forward(self, thrust):
        self.pi.set_servo_pulsewidth(pin_l, width_h + thrust)
        self.pi.set_servo_pulsewidth(pin_r, width_h + thrust)

    def backward(self, thrust):
        self.pi.set_servo_pulsewidth(pin_l, width_l - thrust)
        self.pi.set_servo_pulsewidth(pin_r, width_l - thrust)

    def left(self, thrust):
        self.pi.set_servo_pulsewidth(pin_l, 1500)
        self.pi.set_servo_pulsewidth(pin_r, width_h + thrust)

    def right(self, thrust):
        self.pi.set_servo_pulsewidth(pin_l, width_h + thrust)
        self.pi.set_servo_pulsewidth(pin_r, 1500)

    def up(self, thrust):
        self.pi.set_servo_pulsewidth(pin_f, width_h + thrust)
        self.pi.set_servo_pulsewidth(pin_b, width_h + thrust)

    def down(self, thrust):
        self.pi.set_servo_pulsewidth(pin_f, width_l - thrust)
        self.pi.set_servo_pulsewidth(pin_b, width_l - thrust)

    def hold(self):
        for pin in self.pins:
            self.pi.set_servo_pulsewidth(pin, 1500)

    def tilt(self, thrust):
        self.pi.set_servo_pulsewidth(pin_f, width_l - thrust)
        self.pi.set_servo_pulsewidth(pin_b, width_h + thrust)

    def tilt_backward(self, thrust):
        self.pi.set_servo_pulsewidth(pin_b, width_l - thrust)
        self.pi.set_servo_pulsewidth(pin_f, width_h + thrust)

    def _pitch_control(self, x_rot):
        print('P-controlled pitch')
        x_rot, y_rot = IMU.get_rotations()

        max_thrust = 400
        thrust_per_degree = max_thrust/90
        rot_thrust = x_rot*thrust_per_degree
        print('x_rot = ', x_rot)
        if rot_thrust >= 200:
            rot_thrust = 200
        if rot_thrust <= -200:
            rot_thrust = -200
        print('rot_thrust = ', rot_thrust)

        self.pi.set_servo_pulsewidth(pin_f, 1500 + rot_thrust)
        self.pi.set_servo_pulsewidth(pin_b, 1500 - rot_thrust)

    def stabilize_pitch(self):
        print('P-controlled pitch')
        x_rot, y_rot = IMU.get_rotations()
        self.pitch_control(x_rot)

    def _height_control(self, x_rot, p):
        try:
            print('Height/Pitch Control')
            x_rot, y_rot = IMU.get_rotations()
            p = noderead.read_serial_data()
            print('Pressure String: ', p)
            p = int(p)

            offset = 440
            p_UW = p - offset
            max_thrust = 400
            desired_depth = 33
            thrust_per_unit = max_thrust/desired_depth
            print('pressure: ', p)
            under_thrust = (desired_depth - p_UW)*thrust_per_unit

            if under_thrust >= 200:
                under_thrust = 200
            print('under_thrust = ', under_thrust)

            rot_thrust = get_rot_thrust(x_rot)
            if rot_thrust >= 100:
                rot_thrust = 100
            if rot_thrust <= -100:
                rot_thrust = -100

            print('rot_thrust  = ', rot_thrust)
            forward_thrust = int(1500 - under_thrust + rot_thrust)
            backward_thrust = int(1500 - under_thrust - rot_thrust)
            print(forward_thrust, backward_thrust)

            self.pi.set_servo_pulsewidth(pin_f, forward_thrust)
            self.pi.set_servo_pulsewidth(pin_b, backward_thrust)

        except:
            print('Exception')
            x_rot, y_rot = IMU.get_rotations()

            under_thrust = self.man_under_thrust
            print('under_thrust :', under_thrust)

            rot_thrust = get_rot_thrust(x_rot)
            if rot_thrust >= 100:
                rot_thrust = 100
            if rot_thrust <= -100:
                rot_thrust = -100

            print('rot_thrust  = ', rot_thrust)
            forward_thrust = int(1500 - under_thrust + rot_thrust)
            backward_thrust = int(1500 - under_thrust - rot_thrust)
            print(forward_thrust, backward_thrust)

            self.pi.set_servo_pulsewidth(pin_f, forward_thrust)
            self.pi.set_servo_pulsewidth(pin_b, backward_thrust)

    def stabilized_hp(self):
        print('Height/Pitch Control')
        x_rot, y_rot = IMU.get_rotations()
        p = noderead.read_serial_data()
        print('Pressure String: ', p)
        p = int(p)
        self._height_control(x_rot, p)
