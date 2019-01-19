from motion import line_follower as lf
import cv2
# from motion import movement

# m = movement.Movement()

def main():
    while True:
        try:
            lf.run()
        except KeyboardInterrupt:
            lf.tearDown()
            # m.hold()
            print('Manual Stop')
            break
        except Exception as e:
            lf.tearDown()
            # m.hold()
            print(e.__doc__)
            break

if __name__ == "__main__":
    main()
