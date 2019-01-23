from motion import movement

m = movement.Movement()

def main():
    while True:
        try:
            m.hp_control(75)
        except KeyboardInterrupt:
            print('Oh No!')
            m.hold()
            break
        except Exception as e:
            print(e)
            m.hold()
            break
if __name__ == "__main__":
    main()
