import time

class L:
    def __init__(self):
        self.content = []

    def write(self):
        fn = time.strftime("%d-%m-%Y-%H:%M:%S.log")
        with open(fn, 'w') as f:
            f.writelines(self.content)

    def add(self, v):
        self.content.append(v)