import pigpio
import time

import sys, termios, tty, os, time

pin_f = 11
pin_b = 12

pin_r = 23
pin_l = 15

width_h = 1600
width_l = 1400


pi = pigpio.pi()
print("Initialisation. Setting pulse width to 1500")
pi.set_servo_pulsewidth(pin_l,1500)
pi.set_servo_pulsewidth(pin_r,1500)
pi.set_servo_pulsewidth(pin_f,1500)
pi.set_servo_pulsewidth(pin_b,1500)
time.sleep(1)

button_delay = 0.01


def getch():
    fd = sys.stdin.fileno()
    old_settings = termios.tcgetattr(fd)
    try:
        tty.setraw(sys.stdin.fileno())
        ch = sys.stdin.read(1)

    finally:
        termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
    return ch


def motion(key):
    if key == 'w':
        print("Move forward")
        pi.set_servo_pulsewidth(pin_l,width_h)
        pi.set_servo_pulsewidth(pin_r,width_h)

    elif key == 's':    
        print("Move backward") 
        pi.set_servo_pulsewidth(pin_l,width_l)
        pi.set_servo_pulsewidth(pin_r,width_l)

    elif key == 'a':    
        print("Turn left")
        pi.set_servo_pulsewidth(pin_l,1500)
        pi.set_servo_pulsewidth(pin_r,width_h)

    elif key == 'd':    
        print("Turn right")
        pi.set_servo_pulsewidth(pin_l,width_h)
        pi.set_servo_pulsewidth(pin_r,1500)

    elif key == 'i':    
        print("Move underwater")
        pi.set_servo_pulsewidth(pin_f,width_h)
        pi.set_servo_pulsewidth(pin_b,width_h)

    elif key == 'o':    
        print("Move upwards")
        pi.set_servo_pulsewidth(pin_f,width_l)
        pi.set_servo_pulsewidth(pin_b,width_l)

    elif key == 'q':
        print("Quit")
        pi.set_servo_pulsewidth(pin_l,1500)
        pi.set_servo_pulsewidth(pin_r,1500)
        pi.set_servo_pulsewidth(pin_f,1500)
        pi.set_servo_pulsewidth(pin_b,1500)
        exit()

    elif key == 'h':
        pi.set_servo_pulsewidth(pin_l,1500)
        pi.set_servo_pulsewidth(pin_r,1500)
        pi.set_servo_pulsewidth(pin_f,1500)
        pi.set_servo_pulsewidth(pin_b,1500)

def main():
    print('In the main loop.')
    while True: 
        char = getch()
        print(char)
        motion(char)
        time.sleep(button_delay)

if __name__ == '__main__':
    main()
