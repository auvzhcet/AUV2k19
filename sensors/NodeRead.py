import serial
import time
import os

class NodeRead:

    def __init__(self):

        self.baud_rate = 9600
        lists = os.listdir('/dev/')
        for i in lists:
            if 'ttyUSB' in i:
                port = i
                break
                                           
        self.node_port = '/dev/' + port
        print(self.node_port)
        self.node_serial = None

    def make_connection(self):
        self.node_serial = serial.Serial(port = self.node_port, baudrate=self.baud_rate)
        self.node_serial.timeout = 2
                

    def read_serial_data(self):
        self.make_connection()
        if(self.node_serial.is_open):
            #print("Port active")
            while(True):
                try:
                    size = self.node_serial.inWaiting()
                    #print(size)
                except:
                    print("No connection")
                    self.make_connection()
                if(size):
                    # print("Receiving data")
                    try:
                        data = self.node_serial.read(size)
                        print(data)
                        data = int(data)
                        #print(data)
                    except:
                        print("Read Error")
                    self.node_serial.close()
                    if int(data) == 1024:
                        raise ValueError("1024 speaks DANGER!")
                    return data

        else:
            return None
            print("Node Closed")


def main():
    serial = NodeRead()
    while(True):
        data = serial.read_serial_data()
        os.system('clear')
        print(data)

if __name__ == '__main__':
    main()
