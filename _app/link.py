class Link():
    def __init__(self):
        self.prev=None
        self.next=None
        self.no=0
        self.id=None
        self.echo = True # turn of echo to screen

    def getClassName(self):
        return self.__class__.__name__

    def isEcho(self):
        return self.echo
    def setEcho(self, onoff):
        self.echo = onoff
        return self

    def setNo(self, no):
        #self.no += 1
        self.no = no
        return self
    def getNo(self):
        return self.no

    def setId(self, id):
        self.id = id
    def getId(self):
        return self.id

    def getNext(self):
        return self.next

    def getPrev(self):
        return self.prev

    def getPId(self, msg=None):
        # go backward
        if msg == None: # first time

            if self.prev == None: # (A
                msg = '{}.'.format(self.getNo())
            else:
                msg = self.prev.getPId('{}.'.format(self.getNo()))
        else:
            if self.prev == None:
                msg = '{}.{}'.format(self.getNo(), msg)
            else:
                msg = self.prev.getPId('{}.{}'.format(self.getNo(), msg))
        return msg


    def log(self, line):

        print('[{}]'.format(self.getClassName()), line)
        return self

    def add(self, link):
        # add to last item in list
        link.prev = self
        if self.next == None: # add to the end and return
            link.setNo(1)
            self.next = link
        else:
            link.setNo(1)
            self.next.add(link)

        return self

def main():
    import os
    os.environ['LB-TESTING'] = '1'
    a = Link()
    assert(a.prev == None)
    assert(a.next == None)
    assert(a.id == None)
    assert(a.no == 0)

    b = Link()
    a.add(b)
    assert(a.prev == None)
    assert(a.next != None)
    assert(a.id == None)
    assert(a.no == 0)

    assert (b.prev != None)
    assert (b.next == None)
    assert (b.id == None)
    assert (b.no == 1)
    os.environ['LB-TESTING'] = '0'

if __name__ == "__main__":
    main()