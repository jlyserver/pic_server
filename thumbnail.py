#-*- coding: utf-8 -*-

import os
import sys
from PIL import Image

'''
@infile:  输入文件位置
@outfile: 输出文件位置
@x:       长
@y:       高
@return:  True=success
          None=failed
'''
def thumb(infile, outfile, x, y):
    if x < 1 or y < 1:
        return None
    try:
        im = Image.open(infile)
        size = (x, y)
        im.thumbnail(size)
        o = os.path.splitext(outfile)[0]
        l = '%s_%d×%d'%(o, x, y) + '.jpg'
        im.save(l)
        return True
    except IOError:
        return None

if __name__ == '__main__':
    if len(sys.argv) != 5:
        print('error!')
    else:
        r = thumb(sys.argv[1], sys.argv[2], int(sys.argv[3]), int(sys.argv[4]))
        print(r)

