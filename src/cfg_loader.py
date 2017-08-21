import configparser

class CfgLoader:
    def __init__(self):
        self.cfg = configparser.ConfigParser()
        print ("init")
        
    def loadCfg(self, fileName):
        self.cfg.read(fileName)
        print ("loadScfg")
    