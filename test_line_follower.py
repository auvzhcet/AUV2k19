from motion import line_follower as lf
from motion import movement

m = movement.Movement()

def main():
    while True:
        try:
            lf.run()
        except KeyboardInterrupt:
            print('Oh No!')
            m.hold()
            break

if __name__ == "__main__":
    main()