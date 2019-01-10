import curses
from curses import wrapper
import pigpio
import time
from Input import InputThread
import VideoRecord as vr 
import IMU
from NodeRead import NodeRead

pin_f = 11
pin_b = 12

pin_r = 23
pin_l = 15

thruster_pins = [pin_f, pin_b, pin_r, pin_l]

width_h = 1600
width_l = 1400
thrust = 0
man_under_thrust = 150

pi = pigpio.pi()
print("Initialisation. Setting pulse width to 1500")
for pin in thruster_pins:
    pi.set_servo_pulsewidth(pin,1500)

button_delay = 0.01
nodeRead = NodeRead()

time.sleep(1)

def hold(pins):
    for pin in pins:
        pi.set_servo_pulsewidth(pin,1500)

def pitch_control():
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

    pi.set_servo_pulsewidth(pin_f, 1500 + rot_thrust)
    pi.set_servo_pulsewidth(pin_b, 1500 - rot_thrust)


def get_rot_thrust(x_rot):
    max_thrust = 400
    thrust_per_degree = max_thrust/90
    rot_thrust = x_rot*thrust_per_degree
    if rot_thrust >= 200:
        rot_thrust = 200

    if rot_thrust <= -200:
        rot_thrust = -200

    return rot_thrust


def height_control():
    global man_under_thrust
    try:
        print('Height/Pitch Control')
        x_rot, y_rot = IMU.get_rotations()
        p = nodeRead.read_serial_data()
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

        pi.set_servo_pulsewidth(pin_f, forward_thrust)
        pi.set_servo_pulsewidth(pin_b, backward_thrust)
    
    except:
        print('Exception')
        x_rot, y_rot = IMU.get_rotations()
        
        under_thrust = man_under_thrust
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

        pi.set_servo_pulsewidth(pin_f, forward_thrust)
        pi.set_servo_pulsewidth(pin_b, backward_thrust)
            

    
def motion(key):
    global thrust, thruster_pins, man_under_thrust

    if key == 'w':
        print("Move forward")
        pi.set_servo_pulsewidth(pin_l,width_h + thrust)
        pi.set_servo_pulsewidth(pin_r,width_h + thrust)

    elif key == 's':    
        print("Move backward") 
        pi.set_servo_pulsewidth(pin_l,width_l - thrust)
        pi.set_servo_pulsewidth(pin_r,width_l - thrust)

    elif key == 'a':    
        print("Turn left")
        pi.set_servo_pulsewidth(pin_l,1500)
        pi.set_servo_pulsewidth(pin_r,width_h + thrust)

    elif key == 'd':    
        print("Turn right")
        pi.set_servo_pulsewidth(pin_l,width_h + thrust)
        pi.set_servo_pulsewidth(pin_r,1500)

    elif key == 'i':    
        print("Move underwater")
        pi.set_servo_pulsewidth(pin_f,width_h + thrust)
        pi.set_servo_pulsewidth(pin_b,width_h + thrust)

    elif key == 'o':    
        print("Move upwards")
        pi.set_servo_pulsewidth(pin_f,width_l - thrust)
        pi.set_servo_pulsewidth(pin_b,width_l - thrust)

    elif key == 'q':
        print("Quit")
        hold(thruster_pins)
        vr.destroy()
        time.sleep(1)
        exit()

    elif key == 'h':
        print('Hold')
        hold(thruster_pins)

    elif key == '+':
        if 0 <= thrust < 100:
            thrust += 10
        print('Incresed Thrust To:', thrust)

    elif key == '-':
        if 0 < thrust <= 100:
            thrust -= 10
        print('Decreased Thrust To:', thrust)

    elif key == 'm':    
        print("Tilt front")
        pi.set_servo_pulsewidth(pin_f,width_l - thrust)
        pi.set_servo_pulsewidth(pin_b, width_h + thrust)

    elif key == 'n':    
        print("Tilt backward")
        pi.set_servo_pulsewidth(pin_b,width_l - thrust)
        pi.set_servo_pulsewidth(pin_f, width_h + thrust)

    elif key == 'p':
        pitch_control()

    elif key == 'l':
        height_control()

    elif key == '9':
        man_under_thrust -= 10
        print('Decrease man_under thrust: ', man_under_thrust)

    elif key == '0':
        man_under_thrust += 10
        print('Increase man_under thrust: ', man_under_thrust)


    else:
        print('None')
        hold(thruster_pins)

def main(stdscr):
        global thrust, thruster_pins
        print('In the main loop.')
        stdscr.nodelay(True)
        stdscr.clear()

        while True:
            vr.capture()
            c = stdscr.getch()
            curses.flushinp()

            if c == -1:
                stdscr.clear()
                stdscr.addstr('Thrust is ' + str(thrust) + '\n')
                hold(thruster_pins)

            else:
                stdscr.clear()
                stdscr.addstr('Pressed ' + chr(c) + '\n')
                motion(chr(c))

            time.sleep(0.06)

curses.wrapper(main)
