import asyncio


class VLCBServer:
    """
    Create a Network Server for a VLCB Network

    Example:
        new_server = VLCBServer('127.0.0.1', 5550)
        new_server.start()
    """
    def __init__(self, host='127.0.0.1', port=5550):
        self.host = host
        self.port = port
        self.clients = []

    async def handle_client(self, reader, writer):
        # Add the new client to the list of connected clients
        client = writer
        self.clients.append(client)
        print(f'Connections {len(self.clients)}')

        try:
            # Inform everyone that a new client has connected
            client_address = writer.get_extra_info('peername')
            print(f"New client connected: {client_address}")
            # await self.broadcast(f"Client {client_address} has joined the chat.\n", client)

            # Receive messages from this client and broadcast them to others
            while True:
                data = await reader.read(1024)  # Read up to 100 bytes from client
                if not data:
                    break

                message = data.decode()
                # print(f"Received message from {client_address}: {message}")
                # messages = message.split(';')
                # del messages[-1]
                # for msg in messages:
                await self.broadcast(message, client)

        except Exception as e:
            print(f"Error with client {client_address}: {e}")

        finally:
            # Remove the client and close the connection
            print(f"Client {client_address} has disconnected")
            self.clients.remove(client)
            writer.close()
#            await writer.wait_closed()

    async def broadcast(self, message, sender):
        """Broadcast message to all clients except the sender."""
        for client in self.clients:
            if client != sender:  # Don't send the message back to the sender
                try:
                    client.write(message.encode())
                    await client.drain()  # Ensure data is sent
                except Exception as e:
                    print(f"Error sending {message} to client: {e}")

    async def start_server(self):
        server = await asyncio.start_server(self.handle_client, self.host, self.port)
        addr = server.sockets[0].getsockname()
        print(f"Serving on {addr}")

        async with server:
            await server.serve_forever()


# Usage
if __name__ == "__main__":
    host = '127.0.0.1'
    port = 5550

    server = VLCBServer(host, port)
    asyncio.run(server.start_server())
