from aiocoap import *
import asyncio

async def test():

    protocol = await Context.create_client_context()
    addr = "coap://[2001:67c:254:b0b2:affe:4000:0:1]/"

    responses = [
        protocol.request(Message(code=GET, uri=u)).response
        for u
        in (addr + "time", addr + "endpoint-lookup/")
    ]
    for f in asyncio.as_completed(responses):
        response = await f
        print("Response from {}: {}".format(response.get_request_uri(), response.payload))
        
        
if __name__ == '__main__':
    asyncio.run(test())
