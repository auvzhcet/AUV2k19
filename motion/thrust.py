import curses
from curses import wrapper
import pigpio
import time
from Input import InputThread
import VideoRecord as vr 
import IMU

pin_f = 11
pin_b = 12

pin_r = 23
pin_l = 15

thruster_pins = [pin_f, pin_b, pin_r, pin_l]

width_h = 1600
width_l = 1400
thrust = 0

pi = pigpio.pi()
print("Initialisation. Setting pulse width to 1500")
for pin in thruster_pins:
    pi.set_servo_pulsewidth(pin,1500)

button_delay = 0.01

time.sleep(1)

def hold(pins):
    for pin in pins:
        pi.set_servo_pulsewidth(pin,1500)

def pitch_control(x_rot):
    max_thrust = 300
    thrust_per_degree = max_thrust/90
    rot_thrust = x_rot*thrust_per_degree
    
    if rot_thrust >= 200:
        rot_thrust = 200

    pi.set_servo_pulsewidth(pin_f, 1500 + rot_thrust)
    pi.set_servo_pulsewidth(pin_b, 1500 - rot_thrust)


def motion(key):
    global thrust, thruster_pins

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
        print('P-controlled pitch')
        x_rot, y_rot = IMU.get_rotations()
        pitch_control(x_rot)


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
