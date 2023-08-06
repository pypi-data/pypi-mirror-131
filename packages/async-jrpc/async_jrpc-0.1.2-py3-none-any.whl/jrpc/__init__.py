from httpx import AsyncClient


class Client(AsyncClient):
    def __init__(self, url: str = None, **kwargs):
        self.url = url
        super(Client, self).__init__(**kwargs)

    async def call(self, method: str, *args, **kwargs):
        if self.url is None:
            raise NotImplementedError("URL is not defined. Use raw_call() instead.")
        return await self.raw_call(self.url, method, *args, **kwargs)

    async def raw_call(self, url: str, method: str, *args, **kwargs):
        if args and kwargs:
            raise ValueError("Only args or kwargs can be filled, not both.")

        data = {
            "jsonrpc": "2.0",
            "method": method,
            "params": args if args else kwargs,
            "id": 1
        }
        r = await self.post(url, json=data)
        return r.json()["result"]
