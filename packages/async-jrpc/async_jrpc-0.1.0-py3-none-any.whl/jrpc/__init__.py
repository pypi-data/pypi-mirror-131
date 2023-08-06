from httpx import AsyncClient


class JRPCClient(AsyncClient):
    def __init__(self, url: str, **kwargs):
        self.url = url
        super(JRPCClient, self).__init__(**kwargs)

    async def call(self, method: str, *args, **kwargs):
        if args and kwargs:
            raise ValueError("Only args or kwargs can be filled, not both.")
        data = {
            "jsonrpc": "2.0",
            "method": method,
            "params": args if args else kwargs,
            "id": 1
        }
        r = await self.post(self.url, json=data)
        return r.json()["result"]

