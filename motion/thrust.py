import pigpio
import time
from Input import InputThread


pin_f = 11
pin_b = 12

pin_r = 23
pin_l = 15

thruster_pins = [pin_f, pin_b, pin_r, pin_l]

width_ = 1600
width_ = 1400
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

    else:
        print('None')
        hold(thruster_pins)


def main():
    print('In the main loop.')
    it = InputThread()
    it.start()
    while True: 
        key = it.get_user_input()
        time.sleep(0.01)
        if key != None:
            motion(key)
            it = InputThread()
            it.start()

if __name__ == '__main__':
    main()
