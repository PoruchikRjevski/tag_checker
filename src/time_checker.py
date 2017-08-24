import time

class TimeChecker:
    def __init__(self):
        self.first = 0
        self.result = 0

    def start(self):
        self.first = time.time()

    def stop(self):
        self.result = time.time() - self.first

    def howMuchStr(self):
        return "exec time, s: " + str(round(self.result, 4))
