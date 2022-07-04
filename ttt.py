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
    

async def read_sensors(protocol, addr, sensor_array):
    for sensor in sensor_array:
        response = await protocol.request(Message(code=GET, uri=addr + sensor)).response
        print("sensor: " + sensor + " --- response: {}". format(response.payload))



async def tictactoe(protocol, addr_mc):
    
    ttt_ar = [['0','0','0']
             ,['0','0','0']
             ,['0','0','0']]
    
    end = 0
    p = 1
    
    while end == 0:

        print('Aktuelles Spiel: ', ttt_ar)
        print('Player', p, ':')

        #x = input()
        x = await cursor_loc(protocol, addr_mc)

        ttt_ar[int(x[:1])][int(x[1:])] = str(p)
        end = await ttt_end(ttt_ar, p)
        if p == 1:
            p = 2
        else:
            p = 1

    if end == 1:
        print('Player 1 wins!')
    elif end == 2:
        print('Player 2 wins!')
    elif end == 3:
        print('Draw!')
        
async def ttt_end(ar, p):
    # Reihen
    if (ar[0][0] + ar[0][1] + ar[0][2]) in ['111','222'] or (ar[1][0] + ar[1][1] + ar[1][2]) in ['111','222'] or (ar[2][0] + ar[2][1] + ar[2][2]) in ['111','222']:
        return p
    
    # Spalten
    if (ar[0][0] + ar[1][0] + ar[2][0]) in ['111','222'] or (ar[0][1] + ar[1][1] + ar[2][1]) in ['111','222'] or (ar[0][2] + ar[1][2] + ar[2][2]) in ['111','222']:
        return p
    
    # Diagonal
    if (ar[0][0] + ar[1][1] + ar[2][2]) in ['111','222'] or (ar[0][2] + ar[1][1] + ar[2][0]) in ['111','222']:
        return p
    
    if '0' not in (ar[0][0] + ar[0][1] + ar[0][2] + ar[1][0] + ar[1][1] + ar[1][2] + ar[2][0] + ar[2][1] + ar[2][2]):
        return 3
    
    return 0

async def cursor_loc(protocol, addr_mc):

    # 0,0,1 = normalzustand
    # 0,1,0 = 90° links
    # 0,-1,0 = 90° rechts
    # -1,0,0 = 90° vorne
    # 1,0,0 = 90° hinten

    dir = 0
    cur_loc = '00'

    while dir == 0:

        # read = ACCE READ
        print('cur_loc =', cur_loc)
        read = await read_sensors(protocol, addr_mc, ["/saul/mma8x5x/SENSE_ACCEL"])
	
        read = read[read.find('"d":')+5 : read.find(']')]

        x,y,z = read.split(',')
        x = int(x)
        y = int(y)
        z = int(z)

        #x = int(read[:1])
        #y = int(read[1:2])
        #z = int(read[2:])

        # Normalzustand
        if x < 0.5 and y < 0.5 and z > 0.5:
            print('No Direction!')

        # Links
        if x < 0.5 and y > 0.5 and z < 0.5:
            cur_loc = await add_dir(cur_loc, 1)

        # Rechts
        if x < 0.5 and y < -0.5 and z < 0.5:
            cur_loc = await add_dir(cur_loc, 2)

        # Oben
        if x < -0.5 and y < 0.5 and z < 0.5:
            cur_loc = await add_dir(cur_loc, 3)

        # Unten
        if x > 0.5 and y < 0.5 and z < 0.5:
            cur_loc = await add_dir(cur_loc, 4)

        # Umgedreht
        if x < 0.5 and y < 0.5 and z < -0.5:
            return cur_loc
        
async def add_dir(cur_loc, dir):
    x = int(cur_loc[:1])
    y = int(cur_loc[1:])

    if dir == 1:
        y = y - 1
    elif dir == 2:
        y = y + 1
    elif dir == 3:
        x = x - 1
    elif dir == 4:
        x = x + 1

    if x == -1 : x = 2
    if x == 3  : x = 0

    if y == -1 : y = 2
    if y == 3  : y = 0

    return str(x) + str(y)
    

async def main():    
    protocol = await Context.create_client_context()
    
    addr_mc_ar = await get_addr(protocol)
    print(addr_mc_ar)
    
    addr_mc = addr_mc_ar[0]
    
    #sensor_array = await get_sensors(protocol, addr_mc)

    await read_sensors(protocol, addr_mc, ["/saul/mma8x5x/SENSE_ACCEL"])
    
    await tictactoe(protocol, addr_mc)

    await protocol.shutdown()
    
    
if __name__ == '__main__':
    asyncio.run(main())
