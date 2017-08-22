class TagModel:
    def __init__(self):
        self.deps = {}

    def addDeps(self, deps):
        self.deps.update(deps)

    def getDepsKeys(self):
        return self.deps

    # test method
    def show(self):
        print ("----- SOME SHIT -----")
        for dep, repos in self.deps.items():
            print (dep)
            for repo in repos:
                repo.show()
                for tag in repo.history:
                    tag.show()


class Tag:
    def __init__(self):
        self.itemName = ""
        self.itemNum = -1
        self.orderNum = -1
        self.date = -1
        self.sHash = -1

    def setItemName(self, name):
        self.itemName = name

    def setItemNum(self, num):
        self.itemNum = num

    def setOrderNum(self, num):
        self.orderNum = num

    def setDate(self, date):
        self.date = date

    def setShortHash(self, hash):
        self.sHash = hash

    def show(self):
        print ("itName: ", self.itemName)
        print ("itNum: ", self.itemNum)
        print ("ordNum: ", self.orderNum)
        print ("date: ", self.date)
        print ("sHash: ", self.sHash)

class Repo:
    def __init__(self):
        self.last = Tag()
        self.history = []
        self.link = " "

    def setLink(self, link):
        self.link = link
    def getLink(self):
        return self.link

    def show(self):
        print ("-", self.link)