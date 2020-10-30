import os
import re
import time

def alertbasenotexist():
    input('Java base dir not avalible!')
    exit(-1)

def alertparam():
    input('Invalid folder name found under Java base!')
    exit(-1)

def alertnotfind():
    input('No Java version folder found under Java base!')
    exit(-1)

def comparelist(l1,l2):
    lenflag = len(l1) > len(l2)
    for i,j in zip(l1,l2):
        if i > j:
            return True
        elif i < j:
            return False
    return lenflag

jdkpath = os.getenv('JDK','C:\\Program Files\\Java\\jdk')
cd = os.path.dirname(jdkpath)
if not os.path.exists(cd):
    alertbasenotexist()
try:
    os.chdir(cd)
except Exception as e:
    alertbasenotexist()

highver=[]
highentry=None
pattern = re.compile('^jdk[0-9][0-9._]*$')#jdk1.8.0_171 like or jdk9_171 like(guessed)
for item in os.scandir(cd):
    name = item.name
    if item.is_dir() and pattern.match(name):
        ver=name[3:].split('_')
        if len(ver) < 1 or len(ver) > 2:
            alertparam()
        ver.append('')
        vermain = ver[0]
        versub = ver[1]
        vermain=vermain.split('.')
        if len(vermain) < 3:
            vermain = (vermain+[0,0,0])[:3]
        vermain.append(versub)
        try:
            vermain = [int(i) for i in vermain]
        except ValueError as e:
            alertparam()
        if comparelist(vermain,highver):
            highver = vermain
            highentry = item

if highentry == None:
    alertnotfind()
if highentry.is_symlink():
    exit(0)
input(f"new Java folder {highentry} avalible! Input yes to switch to it!")
curname = None
for item in os.scandir(cd):
    if item.is_dir() and pattern.match(item.name) and item.is_symlink():
        if curname != None:
            input("More than one source loaction of %JDK%! Check it!")
            exit(1)
        curname = item.name
if os.path.exists(jdkpath):
    if curname == None:
        now = time.localtime()
        tail = f"_{now[0]}-{now[1]}-{now[2]}_{now[3]}-{now[4]}-{now[5]}_old_"
        input("Source loaction of %JDK% not present! put %JDK% into backup : "+tail)
        os.rename(jdkpath,jdkpath+tail)
    else:
        os.unlink(curname)
        os.rename(jdkpath,curname)
elif os.path.lexists(jdkpath):
    os.remove(jdkpath)

if os.path.lexists(jdkpath):
    input("%JDK% is still there! manually delete it!")
    exit(1)

os.rename(highentry,jdkpath)
os.symlink(jdkpath,highentry,True)
input('Done!')

