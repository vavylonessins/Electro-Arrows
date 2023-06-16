from levels import *
from const import *
import random
import tracer
import os


edi_help = """
new
del
cls
lst (!!)
gen
get
"""


def random_path():

    ret = "./levels/"

    for i in range(16):
        ret += random.choice(HEX_LETTERS)
    
    return ret+".arrows"


def loading(percentage: float):

    p = int(percentage)
    s = str(p)
    s = ' '*(3-len(s))+s

    # os.system(['clear', 'cls'][os.name=='nt'])

    print('\r['+'#'*p+' '*(100-p)+']',s,'%',end='')


lvlmgr = LevelManager()
lvlmgr.load()

run = 1

while run:
    cmd = input("cmd?[new/Red/del/edi/t01/exi]> ").strip()

    if cmd == "exi":
        run = 0
    
    if cmd == "new":

        name = input("name?[str]> ".strip())

        crdt = pytime.mktime(datetime.datetime.now().timetuple())

        is_3d = int(input("3D?[0/1]> ").strip())

        verid = min(max(int(input("game ver[0-5]?> ").strip()), 0), 5)

        mods = []

        while 1:
            mod = input("mod?[str.str.str,exi for exit]> ")

            if mod == "exi":
                break

            mods.append(mod)
        
        level = Level(lvlmgr, random_path())

        level.name = name
        level.crdt = crdt
        level.is_3d = is_3d
        level.ver_id = verid
        level.mods = mods.copy()
        level.chunks = []

        level.write()

        print("Success!")
    
    elif cmd == "red" or len(cmd) == 0:
        
        levels = lvlmgr.as_dict()
        names = list(levels.keys())

        for n, i in enumerate(names):
            print(str(n+1)+")", i)
        
        ind = int(input(f"level?[1-{n+1}]> "))

        name = names[ind-1]

        level = levels[name]

        tracer.on()
        level.init()
        tracer.off()

        level.print_format()
        print(int(tracer.get()/1000), "s")
        print(int(tracer.get()/100),"ds")
        print(int(tracer.get()/10),"cs")
        print(int(tracer.get()/1),"ms")
        print(int(tracer.get()*10),"µs")
        print(int(tracer.get()*100),"ns")
        print(int(tracer.get()*1000),"ps")
        print(int(tracer.get()*10000),"fs")
        print(int(tracer.get()*100000),"as")
    
    elif cmd == "edi":
        
        levels = lvlmgr.as_dict()
        names = list(levels.keys())

        for n, i in enumerate(names):
            print(str(n+1)+")", i)
        
        ind = int(input(f"level?[1-{n+1}]> "))

        name = names[ind-1]

        level = levels[name]

        level.init()

        level.print_format()

        while 1:
            print(edi_help)
            cmd = input("cmd?> ")

            if cmd == "exi":
                break

            elif cmd == "new":
                c = Chunk(level)
                c.x = int(input("pos x?> "))
                c.y = int(input("pos y?> "))
                c.height = int(input("height?> "))
                c.init()
                level.chunks.append(c)
                level.write()

                c.print_format()
    
    elif cmd == "t01":
        
        levels = lvlmgr.as_dict()
        names = list(levels.keys())

        for n, i in enumerate(names):
            print(str(n+1)+")", i)
        
        ind = int(input(f"level?[1-{n+1}]> "))

        name = names[ind-1]

        level: Level = levels[name]
        level.init()

        progress = 0

        for y in range(16):
            for x in range(16):

                z = 255
                progress += 1

                level.init_chunk(x, y, z)

                loading(100*progress/16/16)

        print()

        level.write()
