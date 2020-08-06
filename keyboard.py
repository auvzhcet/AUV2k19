import curses
from motion import movement
from motion import line_follower as lf
import time

m = movement.Movement()
thrust = 200

def motion(key):
    global thrust

    if key == 'w':
        m.forward(thrust)

    elif key == 's':
        m.backward(thrust)

    elif key == 'a':
        m.left(thrust)

    elif key == 'd':
        m.right(thrust)

    elif key == 'i':
        m.up(thrust)

    elif key == 'o':
        m.down(thrust)

    elif key == 'q':
        print("Quit")
        m.hold()
        lf.tearDown()
        time.sleep(1)
        exit()

    elif key == 'h':
        m.hold()

    elif key == 'm':
        m.tilt_forward(thrust)

    elif key == 'n':
        m.tilt_backward(thrust)

    elif key == 'p':
        m.pitch_control()

    elif key == 'l':
        m.hp_control(33)

    elif key == '+':
        thrust += 10
        if thrust >= 200:
            thrust = 200
    
    elif key == '-':
        thrust -= 10
        if thrust <= 0:
            thrust = 0

    elif key == 'v':
        lf.run()

    else:
        print('None')
        m.hold()


def main(stdscr):
        print('In the main loop.')
        stdscr.nodelay(True)
        stdscr.clear()

        while True:
            stdscr.addstr('Thrust = ' + str(thrust) + '\n')
            c = stdscr.getch()
            curses.flushinp()
            if c == -1:
                stdscr.clear()
                m.hold()
            else:
                stdscr.clear()
                stdscr.addstr('Pressed ' + chr(c) + '\n')
                motion(chr(c))

            time.sleep(0.06)


curses.wrapper(main)
