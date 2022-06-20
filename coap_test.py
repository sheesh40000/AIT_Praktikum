from aiocoap import *
import asyncio


async def get_addr(protocol):
    addr = "coap://[2001:67c:254:b0b2:affe:4000:0:1]/"
    response = await protocol.request(Message(code=GET, uri=addr + "endpoint-lookup/")).response
    
    resp_str = str(response.payload)
    print(resp_str)
    
    addr_pos = resp_str.find('base="');
    print(addr_pos)
    
    addr_mc = resp_str[addr_pos + 6:resp_str.find('"', addr_pos + 6)]
    print(addr_mc)
    
    return addr_mc
    
    
async def get_sensors(protocol, addr_mc):
    response = await protocol.request(Message(code=GET, uri=addr_mc + "/.well-known/core")).response
    print("response: {}". format(response.payload))

    sensor_list = str(response.payload)[2:]
    sensor_array = []
    for s in sensor_list.split(","):
        s_repl = s.replace("<", "").replace(">", "")
        sensor_array.append(s_repl)
        print(s_repl)    
    
    return sensor_array
    
    
async def read_sensors(protocol, addr, sensor_array):
    for sensor in sensor_array:
        response = await protocol.request(Message(code=GET, uri=addr + sensor)).response
        print("response: {}". format(response.payload))

    
async def main():    
    protocol = await Context.create_client_context()
    
    addr_mc = await get_addr(protocol)
    sensor_array = await get_sensors(protocol, addr_mc)
    await read_sensors(protocol, addr_mc, sensor_array)
    protocol.shutdown()
    
    return NULL

    
if __name__ == '__main__':
    asyncio.run(main())

    
    
'''

async def test_get():

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
        
        
async def test_put():
    addr = "coap://[2001:67c:254:b0b2:affe:4000:0:1]/"
    context = await Context.create_client_context()

    await asyncio.sleep(2)

    payload = b"test"
    request = Message(code=PUT, payload=payload, uri=addr + "other/block")

    response = await context.request(request).response

    print('Result: %s\n%r'%(response.code, response.payload))


'''
