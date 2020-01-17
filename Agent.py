from math import *

class Agent:
    def __init__(self, energy, boost, mapa, buff_pac_size = 9):
        self.energy = energy
        self.boost = boost
        self.mapa = mapa
        self.dir_pac = []
        self.buff_pac_size = buff_pac_size
        self.buff_pac_pos = []
        self.map = mapa

    def set_dirs(self, dirs):
        self.dir_pac = dirs

    def set_buff_pac_pos(self, buff_pos):
        self.buff_pac_pos = buff_pos

    def check_pos_buff(self, pac_pos):
        if self.distance_to_point(pac_pos, self.buff_pac_pos[-1]) > 1:
            return True
        return False

    def check_pac_buff(self, pac_buf):
        if pac_buf[0] == pac_buf[2] and pac_buf[1] == pac_buf[3]:
            return True
        return False

    def closest_point(self, p_pos, points):
        if len(points) == 0:
            return points[0]
        dist = sqrt((p_pos[0]-points[0][0])**2 + (p_pos[1]-points[0][1])**2)
        idx = 0
        for p in points[1:]:
            dist2 = sqrt((p_pos[0]-p[0])**2 + (p_pos[1]-p[1])**2)
            if dist > dist2:
                idx = points.index(p)
                dist = dist2

        return points[idx]

    def dir_to_point(self, p_pos, point):
        theta = round(degrees(atan2((p_pos[1] - point[1]),(p_pos[0] - point[0]))))

        if theta >= 45 and theta < 135:
           if theta <= 90:
                dirs = ['w','a','d','s']
           else:
                dirs = ['w','d','a','s']
        elif theta >= -135 and theta < -45:
            if theta >= -90:
                dirs = ['s','a','d','w']
            else:
                dirs = ['s','d','a','w']
        elif theta >= -45 and theta < 45:
            if theta >= 0:
                dirs = ['a','w','d','s']  #['a','w','s','d']
            else:
                dirs = ['a','s','w','d']
        elif theta >= 135 and theta <= 180:
            dirs = ['d','w','a','s']
        elif theta < -135 and theta > -180:
            dirs = ['d','s','a','w']

        return dirs

    def reverse_dir_to_point(self,p_pos, point):
        theta = round(degrees(atan2((p_pos[1] - point[1]), (p_pos[0] - point[0]))))

        if theta >= 45 and theta < 135:
           if theta <= 90:
                dirs = ['s','d','a','w']
           else:
                dirs = ['s','a','d','w']
        elif theta >= -135 and theta < -45:
            if theta >= -90:
                dirs = ['w','d','a','s']
            else:
                dirs = ['w','a','d','s']
        elif theta >= -45 and theta < 45:
            if theta >= 0:
                dirs = ['d','s','w','a']
            else:
                dirs = ['d','w','s','a']
        elif theta >= 135:
            dirs = ['a','s','w','d']
        elif theta < -135:
            dirs = ['a','w','d','s']
        return dirs

    def run_from_ghosts(self, pac_pos, ghosts_pos):
        return None

    def distance_from_ghost(self, p_pos, g_pos):
        return sqrt((p_pos[0] - g_pos[0])**2 + (p_pos[1] - g_pos[1] )**2)

    def distance_to_point(self, p_pos, point):
        return sqrt((p_pos[0] - point[0])**2 + (p_pos[1] - point[1] )**2)

    def change_dir_escaping(self, pac_pos, g_pos, point):
        dstX = pac_pos[0] - point[0]
        dstY = pac_pos[1] - point[1]
        dstXG = pac_pos[0] - g_pos[0]
        dstYG = pac_pos[1] - g_pos[1]
        dirs = []

        if dstX < 0 and dstXG > 0:
            dirs += ['a']
        else:
            dirs += ['d']
        if dstY < 0 and dstYG < 0:
            dirs += ['s']
        else:
            dirs += ['w']

        return dirs

    def distance_from_ghosts(self,state):
        x1 = state['pacman'][0]
        y1 = state['pacman'][1]
        x2 = state['ghosts'][0][0][0]
        y2 = state['ghosts'][0][0][1]
        distance = sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)

        return distance

    def distance_ghost_attack(self,p_pos,tmp):
        return sqrt((tmp[0] - p_pos[0]) ** 2 + (tmp[1] - p_pos[1]) ** 2)

    def reverse_from_ghost(self, dirs):
        rv = []
        for x in dirs:
            if x == 'w':
                rv.append('s')
            elif x == 'a':
                rv.append('d')
            elif x == 's':
                rv.append('w')
            else:
                rv.append('a')
        return rv

