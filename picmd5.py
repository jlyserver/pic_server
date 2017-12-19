#-*- coding: utf-8 -*-

import hashlib
import os
import datetime
import sys

def filemd5(filename):
    if not os.path.isfile(filename):
        return None
    myhash = hashlib.md5()
    f = file(filename,'rb')
    while True:
        b = f.read(8096)
        if not b :
            break
        myhash.update(b)
    f.close()
    return myhash.hexdigest()

if __name__ == '__main__':
    if len(sys.argv) > 1:
        s = filemd5(sys.argv[1])
        print(s)
    else:
        print('error')
