import socket
import asyncio


class VlcbClient():
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
        # super().__init__()
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # Create a socket object
        self.host = host  # Get local machine name
        self.port = port  # Reserve a port for your service.
        self.s.connect((host, port))
        self.function = function

    async def run(self):
        print(f'Starting messages_from_server')
        while True:
            # print(f'Receive from Server Loop')
            try:
                # Receive messages from the server
                message = self.s.recv(1024).decode()
                # print(f'Receive Loop 2')
            except Exception as e:
                if e.args[0] in (35, 10035):
                    pass
                # If an error occurs, break out of the loop
                else:
                    print(f"Error {str(e)}")
                    break
            else:
                messages = message.split(';')
                del messages[-1]
                for msg in messages:
                    print(f'Message Received from Server: {msg}')
                    self.function((msg + ';'))

            await asyncio.sleep(0.0001)

    def send(self, msg):
        # time.sleep(1)
        # print("Child Send : " + msg)
        self.s.send(msg.encode())


def process_message(msg):
    print(f'Process Message: {msg}')


async def main(name: str) -> None:
    cbus_header = ':SB060N'
    VLCB_client = VlcbClient(process_message, "localhost", 5550)
    asyncio.create_task(VLCB_client.run())
    # cbus_ethernet.start()
    VLCB_client.send(f'{cbus_header}0D;')
    while True:
        await asyncio.sleep(1)


if __name__ == '__main__':
    # main('network Client')
    asyncio.run(main('network Client'))