from aiohttp import ClientSession
from asyncio import get_event_loop
from .gateway import DiscordGateway
from ..errors import ApiError

class Client:
    def __init__(self, loop = get_event_loop()):
        self.baseurl = "https://discord.com/api/v9"
        self.loop = loop
        self.ws = None
        self.session = ClientSession(loop = self.loop)
        
    def run(self, *args, **kwargs):
        """
        If you don't want use gateway.
        Please do like this. 
        `client.run("token", gateway = False)`
        """
        self.loop.run_until_complete(self.start(*args, **kwargs))
        
    def print(self, *args, **kwargs):
        pass
        
    async def start(self, token, gateway:bool = True):
        self.token = token
        await self.login()
        if gateway:
            await self.connect()
        
    def dispatch(self, name, *args, **kwargs):
        eventname = "on_" + name
        if hasattr(self, eventname):
            coro = getattr(self, eventname)
            self.loop.create_task(coro(*args, **kwargs))
            
    def event(self, coro):
        """
        This is send gateway event.
        Examples:
            client = Client()
        
            @client.event
            async def on_ready():
                print("ready")
            client.run("ToKeN")
        """
        setattr(self, coro.__name__, coro)
        return coro
        
    async def json_or_text(self, r):
        if r.headers["Content-Type"] == "application/json":
            return await r.json()
        
    async def ws_connect(self, url):
        return await self.session.ws_connect(url)
    
    async def login(self):
        self.user = await self.request("GET", "/users/@me")
    
    async def request(self, method:str, path:str, *args, **kwargs):
        headers = {
            "Authorization": f"Bot {self.token}"
        }
        if kwargs.get("json"):
            headers["Content-Type"] = "application/json"
        kwargs["headers"] = headers
        async with self.session.request(method, self.baseurl + path, *args, **kwargs) as r:
            if r.status == 429:
                raise ApiError("Now api is limit. Wait a minute please.")
            elif r.status == 404:
                raise ApiError("Not Found Error")
            return await self.json_or_text(r)
        
    async def connect(self):
        if self.ws is None:
            self.ws = await DiscordGateway.start_gateway(self)
            await self.ws.catch_message()
            while not self.ws.closed:
                await self.ws.catch_message()

