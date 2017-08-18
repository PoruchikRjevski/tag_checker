import configparser

class CfgLoader:

    def __init__(self):
        self.cfg = configparser.ConfigParser()
        
    def loadCfg(self, fileName):
        self.cfg.read(fileName)
    