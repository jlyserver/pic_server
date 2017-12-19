#-*- coding: utf-8 -*-
import ConfigParser

class Picconf():
    def __init__(self, name):
        p = ConfigParser.ConfigParser()
        p.read(name)
        self.port    = p.getint('sys', 'port')

        self.picroot = p.get('pic', 'root')

    def dis(self):
        print(self.port)
        print(self.picroot)

conf    = Picconf('./conf.txt')

if __name__ == "__main__":
    conf.dis()
