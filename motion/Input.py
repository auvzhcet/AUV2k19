import threading, sys, termios, tty

class InputThread(threading.Thread):
    def __init__(self):            
        threading.Thread.__init__(self)
        self.user_input = None

    def run(self):
        self.user_input = getch()

    def get_user_input(self):
        return self.user_input


def getch():
    fd = sys.stdin.fileno()
    old_settings = termios.tcgetattr(fd)
    try:
        tty.setraw(sys.stdin.fileno())
        ch = sys.stdin.read(1)

    finally:
        termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
    return ch