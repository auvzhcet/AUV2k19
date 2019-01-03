import pigpio
import time
from Input import InputThread


pin_f = 11
pin_b = 12

pin_r = 23
pin_l = 15

width_h = 1600
width_l = 1400
thrust = 0

pi = pigpio.pi()
print("Initialisation. Setting pulse width to 1500")
pi.set_servo_pulsewidth(pin_l,1500)
pi.set_servo_pulsewidth(pin_r,1500)
pi.set_servo_pulsewidth(pin_f,1500)
pi.set_servo_pulsewidth(pin_b,1500)
button_delay = 0.01

time.sleep(1)

def motion(key, thrust):
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
        print('Hold')
        pi.set_servo_pulsewidth(pin_l,1500)
        pi.set_servo_pulsewidth(pin_r,1500)
        pi.set_servo_pulsewidth(pin_f,1500)
        pi.set_servo_pulsewidth(pin_b,1500)

    else:
        print('None')
        pi.set_servo_pulsewidth(pin_l,1500)
        pi.set_servo_pulsewidth(pin_r,1500)
        pi.set_servo_pulsewidth(pin_f,1500)
        pi.set_servo_pulsewidth(pin_b,1500)


def main():
    print('In the main loop.')
    it = InputThread()
    it.start()
    while True: 
        key = it.get_user_input()
        time.sleep(0.01)
        if key != None:
            print('The user input was', key)
            motion(key)
            it = InputThread()
            it.start()

if __name__ == '__main__':
    main()
