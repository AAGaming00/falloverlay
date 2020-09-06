
from os import path
from threading import Thread
f = open(path.expandvars('%APPDATA%\..\LocalLow\Mediatonic\FallGuys_client\Player.log'))
p = 0
f.seek(p)
latest_data = f.read()
p = f.tell()
import logging
from websocket_server import WebsocketServer

def new_client(client, server):
    server.send_message_to_all("connected")

server = WebsocketServer(13254, host='127.0.0.1', loglevel=logging.INFO)
server.set_fn_new_client(new_client)
thread = Thread(target = server.run_forever)
thread.start()
while True:
    f.seek(p)
    latest_data = f.read()
    p = f.tell()
    if latest_data:
        print(latest_data)
        print(str(p).center(10).center(80, '='))
        if "[CompletedEpisodeDto]" in latest_data:
            print("[OverlayServer] match end.")
            server.send_message_to_all(latest_data.partition("[CompletedEpisodeDto] ==")[2])
    if f.closed:
        print('that\'s wierd, the file is closed. now trying to reopen it.')
        f = open(path.expandvars('%APPDATA%\..\LocalLow\Mediatonic\FallGuys_client\Player.log'))
        p = 0
        f.seek(p)
        latest_data = f.read()
        p = f.tell()