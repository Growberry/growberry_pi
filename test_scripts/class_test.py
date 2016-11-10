
import datetime

class Settings:
    def __init__(self):
        self._a = 1
        self._b = 2
        print "initial vars = ",self._a,self._b


    def update(self):
        self._a -=1
        self._b +=1
        print "updated vars = ",self.a,self.b

    @property
    def a(self):
        return self._a

    @property
    def b(self):
        return self._b

class UseSettings:
    def __init__(self,g):
        self.a = g.a
        self.b = g.b
        self.settings = g
        print g
        print "initial settings = ", self.a,self.b

    def use(self):
        print "a + b = ", self.settings.a + self.settings.b


if __name__=='__main__':

    sunrise =




    G = Settings()
    H = UseSettings(G)
    H.use()
    G.update()
    H.use()

# H.settings.update()
# H.use()




