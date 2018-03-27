import asyncio
import json
import os
import struct
import sys
import time

class DiscordRPC:
    def __init__(self, client_id):
        if sys.platform == 'linux':
            self.ipc_path = (os.environ.get('XDG_RUNTIME_DIR', None) or os.environ.get('TMPDIR', None) or
                             os.environ.get('TMP', None) or os.environ.get('TEMP', None) or '/tmp') + '/discord-ipc-0'
            self.loop = asyncio.get_event_loop()
        elif sys.platform == 'win32':
            self.ipc_path = r'\\?\pipe\discord-ipc-0'
            self.loop = asyncio.ProactorEventLoop()
        self.sock_reader: asyncio.StreamReader = None
        self.sock_writer: asyncio.StreamWriter = None
        self.client_id = client_id

    async def read_output(self):
        print("RPC: Reading output")
        data = await self.sock_reader.read(1024)
        code, length = struct.unpack('<ii', data[:8])
        # print('\tOP Code: {}; Length: {}\nResponse:\n{}\n'.format(            code, length, json.loads(data[8:].decode('utf-8'))))

    def send_data(self, op: int, payload: dict):
        payload = json.dumps(payload)
        self.sock_writer.write(struct.pack('<ii', op, len(payload)) + payload.encode('utf-8'))

    async def handshake(self):
        if sys.platform == 'linux':
            self.sock_reader, self.sock_writer = await asyncio.open_unix_connection(self.ipc_path, loop=self.loop)
        elif sys.platform == 'win32':
            self.sock_reader = asyncio.StreamReader(loop=self.loop)
            reader_protocol = asyncio.StreamReaderProtocol(self.sock_reader, loop=self.loop)
            self.sock_writer, _ = await self.loop.create_pipe_connection(lambda: reader_protocol, self.ipc_path)
        self.send_data(0, {'v': 1, 'client_id': self.client_id})
        data = await self.sock_reader.read(1024)
        code, length = struct.unpack('<ii', data[:8])
        # print('\tOP Code: {}; Length: {}\nResponse:\n{}\n'.format(            code, length, json.loads(data[8:].decode('utf-8'))))

    def send_rich_presence(self, activity):
        current_time = time.time()
        payload = {
            "cmd": "SET_ACTIVITY",
            "args": {
                "activity": activity,
                "pid": os.getpid()
            },
            "nonce": '{:.20f}'.format(current_time)
        }
        print("RPC: Sending data")
        sent = self.send_data(1, payload)
        self.loop.run_until_complete(self.read_output())

    def close(self):
        self.sock_writer.close()
        self.loop.close()

    def start(self):
        self.loop.run_until_complete(self.handshake())

if __name__ == '__main__':
    client_id = '1234567892138470' #Your application's client ID as a string. (This isn't a real client ID)
    RPC = rpc.DiscordRPC(client_id) #Send the client ID to the rpc module
    RPC.start() #Start the RPC connection

    current_time = time.time()

    #This is the activity information sent to the client
    activity = {
        "state": "This is the state",
        "details": "Here are some details",
        "timestamps": {
            "start": int(current_time)
        },
        "assets": {
            "small_text": "Text for small_image",
            "small_image": "img_small",
            "large_text": "Text for large_image",
            "large_image": "img_large"
        },
        "party": {
            "size": [1, 6]
        }
    }

    RPC.send_rich_presence(activity)
    time.sleep(60)
    #Presence is set for 60 seconds, afterwards the script will end and the presence will disappear from your profile.
