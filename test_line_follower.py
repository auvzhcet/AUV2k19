from motion import line_follower as lf
from motion import movement
import os
m = movement.Movement()

def main():
    while True:
        print('\n<--------------------->')
        # m.hp_control(40)
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
