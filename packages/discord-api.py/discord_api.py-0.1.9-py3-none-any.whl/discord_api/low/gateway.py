import sys
from ..gateway import KeepAlive
import aiohttp

class DiscordGateway:
    def __init__(self, client, ws):
        self.ws = ws
        self.token = client.token
        self.client = client
        self.closed = self.ws.closed
        
    @classmethod
    async def start_gateway(cls, client):
        data = await client.request("GET", "/gateway")
        ws = await client.ws_connect(data["url"])
        self = cls(client, ws)
        return self

    async def login(self):
        payload = {
            "op": 2,
            "d": {
                "token": self.token,
                "intents": self.client.intents,
                "properties": {
                    "$os": sys.platform,
                    "$browser": "discord-api.py",
                    "$device": "discord-api.py"
                }
            }
        }
        await self.send(payload)
        
    async def send(self, data:dict):
        await self.ws.send_json(data)
        
    async def catch_message(self):
        async for msg in self.ws:
            if msg.type is aiohttp.WSMsgType.TEXT:
                await self.event_catch(msg)
            elif msg.type is aiohttp.WSMsgType.ERROR:
                raise msg.data
                
    async def event_catch(self, msg):
        data = msg.json()
        self.sequence = data["s"]
        if data["op"] != 0:
            if data["op"] == 10:
                self.interval = data["d"]['heartbeat_interval'] / 1000.0
                self.keepalive = KeepAlive(ws = self, interval = self.interval)
                await self.send(self.keepalive.get_data())
                self.keepalive.start()
                await self.login()
            elif data["op"] == 1:
                await self.send(self.keepalive.get_data())
        else:
            self.client.dispatch("gateway_response", data["t"], data["d"])
