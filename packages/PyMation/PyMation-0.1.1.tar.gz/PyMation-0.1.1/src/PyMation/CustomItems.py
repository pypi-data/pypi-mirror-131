from types import FunctionType as FT
import contextlib, io

class CustomExceptions():
    def __init__(self):
        self.excdata = []

    def Add(self, name):
        class NewException(Exception):
            def __init__(self, m):
                self.message = m
            def __str__(self):
                return self.message
        NewException.__name__ = name

        if not NewException in self.excdata:
            self.excdata.append(NewException)
            return NewException
        else:
            print("Exception Error %s already exists." %name)
        
    def Get(self):
        return {Exce.__name__:Exce for Exce in self.excdata}

    def Delete(self, name):
        if name in self.excdata:
            del self.excdata[name]
            print("Custom Exception %s deleted." %name)
        else:
            print("Custom Exception %s does not exist" %name)

class CustomFunctions():
    def __init__(self):
        self.funcdata = {}
        self.func_code = {}
        self.func_prst = {}

    def Add(self, name, code, **paraglobs):
        NewCode = compile("""def """+name+"""("""+(', '.join(paraglobs['params']) if 'params' in paraglobs else "")+"""):\n """+str(code), name, "exec")
        NewFunc = FT(NewCode.co_consts[0], (({**paraglobs['globs'], **globals()} if 'globs' in paraglobs else globals())), name)
        if not name in self.funcdata:
            self.funcdata[name] = NewFunc
            self.func_code[name] = {"code": str(code), "params": paraglobs['params'] if 'params' in paraglobs else []}
            self.func_prst[name] = []
            return NewFunc
        else:
            print("Custom Function %s already exists." %name)

    def AddP(self, name, partst):
        if name in self.funcdata:
            self.func_prst[name] = partst
        else:
            print("Custom Function %s does not exist" %name)

    def Get(self):
        return self.funcdata

    def GetC(self):
        return self.func_code

    def GetP(self):
        return self.func_prst

    def Delete(self, name, pr=True):
        if name in self.funcdata:
            del self.funcdata[name]
            del self.func_code[name]
            del self.func_prst[name]
            if pr:
                print("Custom Function %s deleted." %name)
        else:
            print("Custom Function %s does not exist" %name)

def raises(func, params):
    try:
        with contextlib.redirect_stdout(io.StringIO()):
            func(*params)
    except Exception as e:
        print(e)
        return True
    else:
        return False