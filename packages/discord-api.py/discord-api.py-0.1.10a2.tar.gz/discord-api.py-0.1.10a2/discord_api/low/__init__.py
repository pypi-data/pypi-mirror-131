"""
# discord_api.low

## How to use?

### First

Please watch this [page](https://discord.com/developers/docs/reference)

### Second

`client.request(method, path)`

Example:
```python
# This can fetch a user
data = await client.request("GET", "/users/929849294892948")
```

### Third

use `gateway_response` event

Example:
```python
# This can catch a message create event.
@client.event
async def on_gateway_response(type, data):
    if type == "MESSAGE_CREATE":
        print(data)
    elif type == "READY":
        print("ready")
```

## sample code

```python
from discord_api.low import Client
from asyncio import run
client = Client()
@client.event
async def on_gateway_response(type, data):
    if type == "READY":
        # This can send message
        channelid = "0381948294829"
        await client.request("POST", f"/channels/{channelid}/messages", json = {"content": "start"})
        
client.run("Your token")
```
"""

from .client import Client
