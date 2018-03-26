#-*- coding: utf-8 -*-
import ConfigParser

class Picconf():
    def __init__(self, name):
        p = ConfigParser.ConfigParser()
        p.read(name)
        self.ip      = p.get('sys', 'ip')
        self.port    = p.getint('sys', 'port')

        self.th_x    = p.getint('size', 'th_x')
        self.th_y    = p.getint('size', 'th_y')
        self.x       = p.getint('size', 'x')
        self.y       = p.getint('size', 'y')

        self.th_name = p.get('name', 'th_name')
        self.name    = p.get('name', 'name')

        self.picroot = p.get('pic', 'root')

    def dis(self):
        print(self.port)
        print(self.picroot)

conf    = Picconf('./conf.txt')

if __name__ == "__main__":
    conf.dis()
