import time

try:
    from sensors import IMU
except Exception as e:
    print(e.__doc__)
    print("Error in importing IMU")

try:
    from sensors.NodeRead import NodeRead
except Exception as e:
    print(e.__doc__)
    print("Error in importing NodeRead")

import pigpio


class Movement:
    def __init__(self):

        self.pi = pigpio.pi()
        try:
            self.noderead = NodeRead()
        except Exception as e:
            print(e.__doc__)
            print('Undable to initialise Node MCU read script')

        self.pin_f = 11
        self.pin_b = 12
        self.pin_r = 15
        self.pin_l = 23

        self.THRUSTER_PINS = [self.pin_f, self.pin_b, self.pin_r, self.pin_l]

        print("Initialisation. Setting pulse width to 1500")
        for pin in self.THRUSTER_PINS:
            self.pi.set_servo_pulsewidth(pin, 1500)

        time.sleep(1)

    def forward(self, thrust):
        print('Forward')
        self.pi.set_servo_pulsewidth(self.pin_l, 1500 + thrust)
        self.pi.set_servo_pulsewidth(self.pin_r, 1500 + thrust)

    def backward(self, thrust):
        print('Backward')
        self.pi.set_servo_pulsewidth(self.pin_l, 1500 - thrust)
        self.pi.set_servo_pulsewidth(self.pin_r, 1500 - thrust)

    def left(self, thrust):
        print('Left')
        self.pi.set_servo_pulsewidth(self.pin_l, 1500 - thrust)
        self.pi.set_servo_pulsewidth(self.pin_r, 1500 + thrust)

    def right(self, thrust):
        print('Right')
        self.pi.set_servo_pulsewidth(self.pin_l, 1500 + thrust)
        self.pi.set_servo_pulsewidth(self.pin_r, 1500 - thrust)

    def up(self, thrust):
        print('Up')
        self.pi.set_servo_pulsewidth(self.pin_f, 1500 + thrust)
        self.pi.set_servo_pulsewidth(self.pin_b, 1500 + thrust)

    def down(self, thrust):
        print('Down')
        self.pi.set_servo_pulsewidth(self.pin_f, 1500 - thrust)
        self.pi.set_servo_pulsewidth(self.pin_b, 1500 - thrust)

    def tilt_forward(self, thrust):
        print('Tilt_Forward')
        self.pi.set_servo_pulsewidth(self.pin_f, 1500 - thrust)
        self.pi.set_servo_pulsewidth(self.pin_b, 1500 + thrust)

    def tilt_backward(self, thrust):
        print('Tilt_Backward')
        self.pi.set_servo_pulsewidth(self.pin_f, 1500 + thrust)
        self.pi.set_servo_pulsewidth(self.pin_b, 1500 - thrust)

    def hold(self):
        print('Hold')
        for pin in self.THRUSTER_PINS:
            self.pi.set_servo_pulsewidth(pin, 1500)

    def custom_thrusts(self, thrusts):
        '''
        Args:
        thrusts -- A dictionary of pins and their respective thrusts
        '''

        print('Custom Thrusts')
        for pin, thrust in thrusts.items():
            self.pi.set_servo_pulsewidth(pin, thrust)

    def _get_rot_thrust(self):
        try:
            x_rot, y_rot = IMU.get_rotations()
            max_thrust = 500
            thrust_per_degree = max_thrust/90
            rot_thrust = x_rot*thrust_per_degree
            print('x_rot = ', x_rot)

        except Exception as e:
            print(e.__doc__)
            print('IMU Error')
            rot_thrust = 0

        return rot_thrust

    def pitch_control(self):
        print('P-controlled pitch')

        rot_thrust = self._get_rot_thrust()

        if rot_thrust >= 200:
            rot_thrust = 200
        if rot_thrust <= -200:
            rot_thrust = -200
        print('rot_thrust = ', rot_thrust)

        self.pi.set_servo_pulsewidth(self.pin_f, 1500 - rot_thrust)
        self.pi.set_servo_pulsewidth(self.pin_b, 1500 + rot_thrust)

    def _get_under_thrust(self, desired_depth):
        try:
            p = self.noderead.read_serial_data()
            print('Pressure String: ', p)
            p = int(p)

            offset = 440
            p_UW = p - offset
            max_thrust = 400
            thrust_per_unit = max_thrust/desired_depth
            print('pressure: ', p)
            under_thrust = (desired_depth - p_UW)*thrust_per_unit
        except Exception as e:
            print(e.__doc__)
            print("Pressure sensing error")
            under_thrust = 65

        return under_thrust
        
    def hp_control(self, desired_depth):
        print('HP Control')
        under_thrust = self._get_under_thrust(desired_depth)

        if under_thrust >= 200:
            under_thrust = 200
        if under_thrust <= -200:
            under_thrust = -200
        print('under_thrust = ', under_thrust)

        rot_thrust = self._get_rot_thrust()
        if rot_thrust >= 100:
            rot_thrust = 100
        if rot_thrust <= -100:
            rot_thrust = -100
        print('rot_thrust  = ', rot_thrust)

        forward_thrust = int(1500 - under_thrust - rot_thrust)
        backward_thrust = int(1500 - under_thrust + rot_thrust)

        print(forward_thrust, backward_thrust)

        self.pi.set_servo_pulsewidth(self.pin_f, forward_thrust)
        self.pi.set_servo_pulsewidth(self.pin_b, backward_thrust)
