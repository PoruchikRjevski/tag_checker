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


class Tag:
    def __init__(self):
        self.item = -1;
        self.order_num = -1;
        self.date = -1
        self.hash = -1

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
        print (self.link)