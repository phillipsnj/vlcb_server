import serial
import serial.tools.list_ports as list_ports
import socket
import asyncio
import time


class CanUsb4:
    """
    CanUSB4 - Connect an CANUSB4 to a VLCB Server

    Usage:
        CanUsb(USB Port, Server Port

    Example "
    """
    def __init__(self, com_port, server, port):
        self.com_port = com_port
        self.server = server
        self.port = port
        self.usb = serial.Serial(self.com_port)
        self.server_host = '127.0.0.1'
        self.server_port = 5550
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # Create a socket object

        try:
            self.client.connect((self.server, self.port))
        except Exception as e:
            print(f"Connection Error {repr(e)}")

        self.client.setblocking(False)

    async def messages_from_usb(self):
        buffer = ''
        print(f"Starting messages_from_usb")
        while True:
            # print(f"Messagse from USB")
            if self.usb.inWaiting() > 0:
                data = self.usb.read().decode()
                buffer = buffer + data
                if data == ';':
                    # print(f'Message from USB {buffer}')
                    self.send_to_server(buffer)
                    buffer = ''
            await asyncio.sleep(0.0001)

    async def messages_from_server(self):
        print(f'Starting messages_from_server')
        while True:
            # print(f'Receive from Server Loop')
            try:
                # Receive messages from the server
                message = self.client.recv(1024).decode()
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
                    # print(f'Message Received from Server: {msg}')
                    self.send_to_usb((msg + ';'))

            await asyncio.sleep(0.0001)

    def send_to_server(self, msg):
        # print(f'Send to Server {msg}')
        try:
            self.client.send(msg.encode())
        except Exception as e:
            if e.args[0] == 57:
                pass
            # If an error occurs, break out of the loop
            else:
                print(f"Error {str(e)}")

    def send_to_usb(self, msg):
        print(f"Send to USB {msg}")
        # for i in msg:
        #     self.ser.write(str.encode(str(i)))
        self.usb.write(msg.encode())


def process_message(msg):
    print(f"Process Message {msg}")


async def main() -> None:
    canusb4s = []
    usb_port = '/dev/cu.usbmodem214301'
    # for port in list(list_ports.comports()):
    #     string = ','.join(str(x) for x in port)
    #     print(f"{string}")
    #     port_name = str(port[2])[12:21]
    #     if port_name.upper() == '04D8:F80C':
    #         print(f"I'm using {str(port[0])}")
    #         # com_port = str(port[0])
    #         # canusb4 = CanUsb4(com_port, process_message)
    #         # canusb4s.append(canusb4)
    #         # asyncio.create_task(canusb4.run())
    #         # await canusb4.start()
    #         # print(f"Canusb4 Started")
    canusb4 = CanUsb4(usb_port, '127.0.0.1', 5550)
    # loop = asyncio.get_event_loop()
    # asyncio.create_task(canusb4.messages_from_server())
    asyncio.create_task(canusb4.messages_from_usb())
    asyncio.create_task(canusb4.messages_from_server())

    while True:
        await asyncio.sleep(1)


if __name__ == '__main__':
    asyncio.run(main())
