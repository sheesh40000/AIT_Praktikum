from aiocoap import *
import asyncio

from datetime import datetime



async def get_addr(protocol):
    addr = "coap://[2001:67c:254:b0b2:affe:4000:0:1]/"
    response = await protocol.request(Message(code=GET, uri=addr + "endpoint-lookup/")).response
    
    resp_str = str(response.payload)
    
    addr_mc = []
    for splitted in resp_str.split('base="'):
        if splitted[:4] == 'coap':
            addr_mc.append(splitted[:splitted.find('"')])
    
    return addr_mc
    
    
async def get_sensors(protocol, addr_mc):
    response = await protocol.request(Message(code=GET, uri=addr_mc + "/.well-known/core")).response
    print("response: {}". format(response.payload))

    sensor_list = str(response.payload)[2:]
    sensor_array = []
    for s in sensor_list.split(","):
        s_repl = s.replace("<", "").replace(">", "").replace("'", "")
        sensor_array.append(s_repl)
        print(s_repl)    
    
    return sensor_array
 
    
# Fkt: Werte der Sensoren anzeigen / Werte der Sensoren aktualisieren
async def read_sensors(protocol, addr, sensor_array):
    for sensor in sensor_array:
        response = await protocol.request(Message(code=GET, uri=addr + sensor)).response
        print("sensor: " + sensor + " --- response: {}". format(response.payload))


async def leds_out(protocol, addr, sensors):
    for s in sensors:
        payload = bytes(str(0), 'ascii')
        #payload = b"0"
        request = Message(code=PUT, payload=payload, uri=str(addr + s))
        response = await protocol.request(request).response
    

async def leds_on(protocol, addr, sensors):
    for s in sensors:
        payload = bytes(str(1), 'ascii')
        #payload = b"1"
        request = Message(code=PUT, payload=payload, uri=str(addr + s))
        response = await protocol.request(request).response
        
    
async def led_blink(protocol, addr):
    sensors = ["/led/red","/led/blue","/led/green"]
    
    print("Begin led_blink()")
    await read_sensors(protocol, addr, sensors)
    
    print("Begin leds_out()")
    await leds_out(protocol, addr, sensors)        
    print("leds off")
    
    await read_sensors(protocol, addr, sensors)
    await asyncio.sleep(3)
    
    print("Begin leds_on()")
    await leds_on(protocol, addr, sensors)        
    print("leds on")
    
    await read_sensors(protocol, addr, sensors)

    
async def main():    
    protocol = await Context.create_client_context()
    
    addr_mc_ar = await get_addr(protocol)
    print(addr_mc_ar)
    
    addr_mc = addr_mc_ar[0]
    
#    await read_sensors(protocol, addr_mc, ["/btn/0", "/btn/1"])
    
    await read_sensors(protocol, addr_mc, ["/sensor/hum"])
    
    #sensor_array = await get_sensors(protocol, addr_mc)
    
    
    #now = datetime.now().time()
    #print("now =", now)
    
    # await read_sensors(protocol, addr_mc, sensor_array)
    
    
    #now = datetime.now().time()
    #print("now =", now)
    
    #await led_blink(protocol, addr_mc)
    
    await protocol.shutdown()
    
    
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
