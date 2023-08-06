import os, shutil

class Pfile():
    def __init__(self, filename, path):
        self.filename = filename
        self.path = path
        self.fullpath = path + "\\" + filename
        try:
            with open(self.fullpath, "r") as f:
                pass
        except FileNotFoundError:
            with open(self.fullpath, "w") as f:
                pass

    def load(self) -> list:
        with open(self.fullpath, "r") as f:
            return f.readlines()

    def write(self, *args):
        for arg in args:
            if isinstance(arg, list):
                with open(self.fullpath, "r+") as f:
                    l = f.readlines()
                l[arg[1]] = str(arg[0]) + "\n"
                with open(self.fullpath, "w") as fw:
                    fw.writelines(l)
            else:
                with open(self.fullpath, "a") as f:
                    f.write(str(arg + "\n"))

    def inser(self, *args: list):
        for arg in args:
            with open(self.fullpath, "r+") as f:
                l = f.readlines()
            l.insert(arg[1], str(arg[0]) + "\n")
            with open(self.fullpath, "w") as fw:
                fw.writelines(l)

    def clear(self, *lines: int):
        with open(self.fullpath, "r+") as f:
            l = f.readlines()
            for line in lines:
                l[line] = ""
        with open(self.fullpath, "w") as fw:
            fw.writelines(l)
    
    def delete(self):
        os.remove(self.fullpath)

class Pfolder(): 
    def __init__(self, foldername, path):
        self.foldername = foldername
        self.path = path
        self.fullpath = self.path + "//" + self.foldername
        os.mkdir(path + "//" + foldername)
    
    def getfiles(self):
        return os.listdir(self.fullpath)

    def delete(self):
        shutil.rmtree(self.fullpath)

def filedir(file):
    return os.path.dirname(os.path.realpath(file))