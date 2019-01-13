import curses
import movement
import time

m = movement.Movement()


def motion(key):
    # TODO: When the movement class supports thrust as attribute, then
    #       extend the +/- functionality.
    if key == 'w':
        print("Move forward")
        m.forward(100)

    elif key == 's':
        print("Move backward")
        m.backward(100)

    elif key == 'a':
        print("Turn left")
        m.left(100)

    elif key == 'd':
        print("Turn right")
        m.right(100)

    elif key == 'i':
        print("Move underwater")
        m.up(100)

    elif key == 'o':
        print("Move upwards")
        m.down(100)

    elif key == 'q':
        print("Quit")
        m.hold()
        time.sleep(1)
        exit()

    elif key == 'h':
        print('Hold')
        m.hold()

    elif key == 'm':
        print("Tilt front")
        m.tilt(100)

    elif key == 'n':
        print("Tilt backward")
        m.tilt_backward(100)

    elif key == 'p':
        m.stabilize_pitch()

    elif key == 'l':
        m.stabilized_hp()

    else:
        print('None')
        m.hold()


def main(stdscr):
        print('In the main loop.')
        stdscr.nodelay(True)
        stdscr.clear()

        while True:
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
