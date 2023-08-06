from random import randint
import colorama as coll
def colgen(col):
    if col == "red":
        print(coll.Fore.RED)
    if col == "green":
        print(coll.Fore.GREEN)
    if col == "yellow":
        print(coll.Fore.YELLOW)
    if col == "black":
        print(coll.Fore.BLACK)
    if col == "blue":
        print(coll.Fore.BLUE)
def colres():
    print (coll.Fore.RESET)


class MASive:
    def __init__(self,x=0,y=0,m=[]):
        self.x = x
        self.y = y
        self.m = m

    def Ms_R_SendMAS(self,mlen=0,min_v=0,max_v=0):
        i = 0
        m = []
        for i in range(mlen):
            m.append(randint(min_v,max_v))
        return m

    def Ms_SendMAS(self,m=[]):
        return m



    def Ms_R_SendMAS_2D(self,width_m=0,height_m=0,min_v=0,max_v=0):
        i = 0
        j = 0
        m = [[randint(min_v, max_v) for j in range(width_m)] for i in range(height_m)]
        return m

    def Ms_Print_m(self,m=[],col = "red",v = "1D"):
        colgen(col)
        if v == "1D"or v == "1d":
            print(m)
        elif v == "2D"or v == "2d":
            for j in m:
                print(j)
        colres()



    def LOC(self,m=[],xp=0,yp=0,v="1D"):
        if v == "1D" or v == "1d":
            return m[xp]
        elif v == "2D" or v == "2d":
            return m[xp][yp]

        


    def Sort(self,m=[]):
        m.sort()
        return m