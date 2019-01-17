from motion import line_follower as lf
from motion import movement

m = movement.Movement()

def main():
    while True:
        try:
            lf.run()
        except KeyboardInterrupt:
            lf.tearDown()
            m.hold()
            print('Oh No!')
            break

if __name__ == "__main__":
    main()
