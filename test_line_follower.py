from motion import line_follower as lf
from motion import movement
import time

m = movement.Movement()


def main():
    tick = time.time()
    while True:
        try:
            if time.time() - tick > 12:
                m.hold()
                time.sleep(2)
                break
            else:
                m.hp_control(90)
                m.forward(150)
        except Exception as e:
            print(e)
            m.hold()
            break
    while True:
        print('\n<--------------------->')
        try:
            lf.run()
        except KeyboardInterrupt:
            lf.tearDown()
            m.hold()
            print('Manual Stop')
            break
        except Exception as e:
            lf.tearDown()
            m.hold()
            print(e)
            break


if __name__ == "__main__":
    main()
