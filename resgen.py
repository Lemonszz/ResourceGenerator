import sys
import os
import shutil
import errno

vars = sys.argv
vars.pop(0)
src = "./resources/"
dest = "./out/"

if not os.path.exists(src):
    os.makedirs(src)

if not os.path.exists(dest):
    os.makedirs(dest)

srcFiles = os.listdir(src)


def copy(src, dest):
    try:
        shutil.rmtree(dest)
        shutil.copytree(src, dest)
    except OSError as e:
        if(e.errno == errno.ENOTDIR):
            shutil.copy(src, dest)
        else:
            print("D: Something went wrong. Error: %s" % e)

copy(src, dest)

replaceLater = [];
for subdir, dirs, files in os.walk(dest):
    for f in files:
        replaceLater.append(os.path.join(subdir, f))

for fp in replaceLater:
    print("Found - " + fp)
    for varient in vars:
        endLoc = fp.replace("[replace]", varient)
        if not endLoc == fp:
            print("Replacing - " + fp + ", " + varient)
            shutil.copy(fp, endLoc)
        s = ""
        try:
            with open(endLoc, "r") as f:
                s = f.read()
                s = s.replace("[replace]", varient)
                print("Replacing - " + endLoc + "," + varient)
                f.close()
            with open(endLoc, "w") as f:
                f.write(s)
                print("writing - " + endLoc)
                f.close()
        except Exception:
            continue

    print("Completed - " + fp + "\n")
    os.remove(fp)