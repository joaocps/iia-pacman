import random
import sys
import json
import asyncio
import websockets
import os
from mapa import Map
from Agent import *


async def agent_loop(server_address="localhost:8000", agent_name="69892-73761"):
    async with websockets.connect("ws://{}/player".format(server_address)) as websocket:

        # Receive information about static game properties
        await websocket.send(json.dumps({"cmd": "join", "name": agent_name}))
        msg = await websocket.recv()
        game_properties = json.loads(msg)

        mapa = Map(game_properties['map'])
        # init agent properties
        key = 'a'
        agent = Agent(None, None, None)
        pac_buf = []

        while True:
            r = await websocket.recv()
            state = json.loads(r)  # receive game state

            # Points
            energy = state['energy'] 
            boosts = state['boost']
            points = energy + boosts

            if not state['lives'] or points == []:
                print("GAME OVER")
                return

            # Pacman Position
            pac_pos = state['pacman']
            pac_buf.append(state['pacman'])
            agent.set_buff_pac_pos(pac_buf)
            # Ghost(s) Position(s)
            ghosts_pos = [g[0] for g in state['ghosts']]
            # Ghost(s) State
            ghosts_state = [g[1] for g in state['ghosts']]
            # Ghost(s) timeout
            ghosts_time = [g[2] for g in state['ghosts']]

            # Closest Point
            cp = agent.closest_point(pac_pos, points)

            dirs = []

            #print()
            #print('Lives: ',state['lives'])
            #print('Ghosts Pos: ',ghosts_pos)
            #print('Pacman Pos: ',pac_pos)
            #print('Cp: ',cp)

            if len(state['ghosts']) == 0:
                dirs = agent.dir_to_point(pac_pos, cp)
            elif len(state['ghosts']) >= 1:

                if len(pac_buf) == 4 and agent.check_pac_buff(pac_buf):
                    dirs = agent.dir_pac
                    pac_buf = []
                    continue
                elif len(pac_buf) > 1 and agent.check_pos_buff(pac_pos):
                    dirs = agent.dir_pac
                    continue
                elif len(pac_buf) == 4 and not agent.check_pac_buff(pac_buf):
                    pac_buf = []

                if any(ghosts_state) == True:
                    g_pos = [ghosts_pos[i] for i,g in enumerate(ghosts_state) if g == True]
                    for pos in g_pos:
                        dst_ghost = agent.distance_from_ghost(pac_pos, pos)
                        if dst_ghost > 1:
                            dirs = agent.dir_to_point(pac_pos, pos)
                            agent.set_dirs(dirs)
                            break
                        else:
                            dirs = agent.dir_to_point(pac_pos, cp)
                            agent.set_dirs(dirs)
                            #break
                if any(ghosts_state) == False:
                    g_pos = [ghosts_pos[i] for i,g in enumerate(ghosts_state) if g == False]
                    for pos in g_pos:
                        dst_ghost = agent.distance_from_ghost(pac_pos, pos)
                        if dst_ghost < 3:
                            dirs = agent.reverse_dir_to_point(pac_pos, pos)
                            if agent.distance_to_point(pac_pos, cp) > 1: #and agent.distance_to_point(pac_pos, pos) < 5:
                                dirs = agent.dir_to_point(pac_pos, pos)
                                agent.set_dirs(dirs)
                                #dirs = agent.change_dir_escaping(pac_pos, pos, cp)
                                #print('inside if dist cp == 1: ',dirs)
                            break
                        else:
                            dirs = agent.dir_to_point(pac_pos, cp)
                            agent.set_dirs(dirs)
                            #break


            for d in dirs:
                npos = mapa.calc_pos(pac_pos,d)
                if npos != pac_pos:
                    key = d
                    break

            # send new key
            await websocket.send(json.dumps({"cmd": "key", "key": key}))


loop = asyncio.get_event_loop()
SERVER = os.environ.get('SERVER', 'localhost')
PORT = os.environ.get('PORT', '8000')
NAME = os.environ.get('NAME', 'student')
loop.run_until_complete(agent_loop("{}:{}".format(SERVER, PORT), NAME))
