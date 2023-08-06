from instanceTuner.set import setFunction as sf
from instanceTuner.operator import CustomizeOperator as co
from CAStatus.log import Log, simpleUTC as utc
import json


def validJSON(path):
    with open(path, 'r') as file:
        try:
            json.load(file)
            return True
        except Exception as e:
            return False


class Status(Log):

    def __init__(self, statusPath, logPath, timeFunc=utc) -> None:
        super().__init__(logPath, timeFunc=timeFunc)
        self.statusPath = statusPath

    def __init__(self) -> None:
        self.status = 'on start'
        if validJSON(self.statusPath):
            self.read()
        else:
            self.Setattr('status', 'on start')

    @sf
    def __call__(self,
                 fn: co(lambda __instance: callable(__instance)),
                 *args, **kwargs):

        return fn(*args, **kwargs)

    @sf
    def __call__(self, name: str, value) -> None:
        setattr(self, name, value)
        super()(name, ':', value)
        self.write()

    def __setattr__(self, name: str, value) -> None:
        self.__dict__[name] = value

    def write(self):
        with open(self.statusPath, 'w') as file:
            json.dump(self.__dict__, file, skipkeys=True,
                      allow_nan=True, indent=4)

    def read(self):
        with open(self.statusPath, 'r') as file:

            jsonDict = json.load(file)

            if 'topMarkets' in jsonDict:
                setattr(self, 'topMarkets', jsonDict['topMarkets'])

            for k, v in self.__dict__.items():
                self.Setattr(k, v)


def exceptLoop(func, *args, **kwargs):
    try:
        return func(*args, **kwargs)
    except Exception as e:
        Status()('error', str(e))
        return exceptLoop(func, *args, **kwargs)
