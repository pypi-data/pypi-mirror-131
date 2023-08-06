from datetime import datetime

default_levels = {"DEBUG": 4, "ERROR": 1, "WARNING": 2, "INFO": 3, "IMPORTANT": 0}
default_format = "[[DATE]]  [[LEVEL]]:[[LOG_NAME]] >>  [[CONTENT]]"

DEBUG = 4
ERROR = 1
WARNING = 2
INFO = 3
IMPORTANT = 0
OFF = -1

class Logger:

    def __init__(self, file=None, level=3, name="root", console_print=True, format=default_format, autoclear=False):
        self.levels = default_levels.copy()
        self.file = file
        self.level = level
        self.name = name
        self.print = console_print
        self.format = format
        if not autoclear: 
            file = open(str(self.file), encoding="cp1251", mode="a")
            file.write("\n\n%s\n\n\n" % datetime.now().strftime("%H:%M:%S %d.%m.%y"))
        else: file = open(str(self.file), encoding="cp1251", mode="w")
        file.close()


    def addLevel(self, name, level=1):
        if not isinstance(level, int): return False
        self.levels[name] = level
        return name

    def removeLevel(self, name):
        if name not in self.levels: return False
        del self.levels[name]
        return name

    def log(self, name, content, req_print=False):
        if name not in self.levels or self.levels[name] > self.level: return False
        date = datetime.now().strftime("%H:%M:%S %d.%m.%y")
        text = self.format.replace("[[DATE]]", date).replace("[[LEVEL]]", name).replace("[[LOG_NAME]]", self.name).replace("[[CONTENT]]", str(content))
        if self.print or req_print: print(text)
        if self.file:
            file = open(str(self.file), encoding="cp1251", mode="a")
            file.write(text + '\n')
            file.close()
        return content

    def debug(self, content, req_print=False): return self.log("DEBUG", content, req_print)
    def error(self, content, req_print=False): return self.log("ERROR", content, req_print)
    def warning(self, content, req_print=False): return self.log("WARNING", content, req_print)
    def info(self, content, req_print=False): return self.log("INFO", content, req_print)
    def important(self, content, req_print=False): return self.log("IMPORTANT", content, req_print)
