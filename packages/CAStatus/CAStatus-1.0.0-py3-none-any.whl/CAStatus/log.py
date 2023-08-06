from CAImport.tools import Singleton
from datetime import datetime


def simpleUTC():
    return str(datetime.utcnow())[:-7]


class Log(Singleton):

    def __init__(self, logPath, timeFunc=simpleUTC) -> None:
        self.logPath = logPath
        self.timeFunc = timeFunc

    def __call__(self, *txt, join_=' ', end='\n'):
        def checkLength():
            with open(self.logPath, 'r') as file:
                logs = file.readlines()
                if len(logs) > 1000:
                    return logs[len(logs) - 700:]
                return False

        def cleaner():
            logs = checkLength()
            if logs:
                with open(self.logPath, 'w') as file:
                    file.writelines(logs)

        with open(self.logPath, 'a') as file:
            txt = [str(el) for el in txt]
            file.write(self.timeFunc() + '  ')
            file.write(join_.join(txt)+end)
        cleaner()
