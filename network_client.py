import socket
import time
import threading
import socket


class VlcbClient(threading.Thread):
    """
    Class to connect to a Cbus network via ethernet
    """

    def __init__(self, function, host, port):
        """
        Initialization of the class requires 3 parameters
        :param function:  The name of the function the executes when a recognised Event is Received.
        :param host Address of the CBUS network interface.
        :param host port address.
        """
        super().__init__()
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # Create a socket object
        self.host = host  # Get local machine name
        self.port = port  # Reserve a port for your service.
        self.s.connect((host, port))
        self.function = function

    def run(self):
        try:
            while True:
                # print('receiving data...')
                data = self.s.recv(1024)
                output = data.decode()
                messages = output.split(';')
                del messages[-1]
                for msg in messages:
                    # self.action_opcode(data.decode())
                    self.function(msg + ";")
                # print(data.decode()+ " : " +mergCbus.getOpCode(data.decode()))
                # self.execute(data.decode())
                if not data:
                    break
        except KeyboardInterrupt:
            print('interrupted!')
            self.close()
        print('connection closed')

    def send(self, msg):
        # time.sleep(1)
        # print("Child Send : " + msg)
        self.s.send(msg.encode())


def process_message(msg):
    print(msg)


def main(name: str) -> None:
    cbus_header = ':SB060N'
    cbus_ethernet = CbusEthernet(process_message, "localhost", 5550)
    cbus_ethernet.start()
    cbus_ethernet.send(f'{cbus_header}0D;')
    while True:
        pass


if __name__ == '__main__':
    main('network Client')