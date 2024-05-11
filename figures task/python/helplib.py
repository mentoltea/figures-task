import optimize



class square:
    def __init__(self, x, y):
        self.x = x
        self.y = y
    
    def __add__(self, vec: tuple[int]):
        return square(self.x+vec[0], self.y+vec[1])
    
    def __padd__(self, vec: tuple[int]):
        return self.add(vec)
    
    def __eq__(self, s):
        return self.x==s.x and self.y==s.y
    
    def __str__(self):
        return f"({self.x},{self.y})"

    def __hash__(self) -> int:
        return (tuple((self.x, self.y))).__hash__()
    
    def copy(self):
        return square(self.x, self.y)
        
        
class figure:
    squares: list[square] = []
    
    def __init__(self, parent=None):
        self.squares = []
        if parent!=None:
            self.squares = []
            for i in parent.squares:
                self.squares.append(i.copy())
            
    
    def app(self, s: square):
        self.squares.append(s)
    
    def __add__(self, vec: tuple[int]):
        fig = self.copy()
        for i in range(len(fig.squares)):
            s = fig.squares[i]
            #print(s, vec)
            fig.squares[i] = s + vec
            #print(s)
        #print(self, fig)
        return fig
    
    def __padd__(self, vec: tuple[int]):
        return self.add(vec)
    
    def __eq__(self, f):
        if f == None:
            return False
        if len(self.squares) != len(f.squares):
            return False
        for s in self.squares:
            if not s in f.squares:
                return False
        return True
    
    def __str__(self):
        s = "{ "
        for i in self.squares:
            s += str(i) + ', '
        s += "}"
        return s
    
    def __hash__(self) -> int:
        s = 0
        for i in self.squares:
            s += i.__hash__()
        return s
        
        
    def rotate(self): #rotates anticloclwise 90 degrees
        for s in self.squares:
            s.x, s.y = -s.y, s.x
    
    def sortx(self, rev=0):
        self.squares.sort(reverse = rev, key = lambda s: s.x)
        return self.squares
    
    def sorty(self, rev=0):
        self.squares.sort(reverse = rev, key = lambda s: s.y)
        return self.squares
    
    def copy(self):
        res = figure(self)
        return res
    
    def minx(self):
        if len(self.squares) ==0:
            return 0
        return self.sortx()[0].x
    
    def maxx(self):
        if len(self.squares) ==0:
            return 0
        return self.sortx(rev=1)[0].x
    
    def miny(self):
        if len(self.squares) ==0:
            return 0
        return self.sorty()[0].y
    
    def maxy(self):
        if len(self.squares) ==0:
            return 0
        return self.sorty(rev=1)[0].y
        
    def suit(self, f) -> bool: # f is a plane (not exactly)
        if len(self.squares) == 0:
            return True
        
        if len(f.squares) == 0:
            return False
        
        smax = self.maxx()
        smix = self.minx()
        smay = self.maxy()
        smiy = self.miny()
        
        fmax = self.maxx()
        fmix = self.minx()
        fmay = f.maxy()
        fmiy = f.miny()
        
        #print(smax, smix, fmax, fmix)
        if smax-smix > fmax-fmix or smay-smiy > fmay-fmiy:
            return False
            
        self += (fmix-smix, fmiy-smiy)
        
        return suitnormalized(self, f)

"""
    def visualise(self):
        xswing = self.maxx() - self.minx() +1
        yswing = self.maxy() - self.miny() +1
        sc = self.copy()
        sc += (-self.minx(), -self.miny())
        print(sc)
        matr = [[0] * xswing] * yswing
        #print(matr)
        for i in sc.squares:
            #print(yswing - i.y -1,xswing - i.x -1)
            matr[yswing - i.y -1][xswing - i.x -1] = "*"
            #print(matr)
        print(matr)
        for y in matr:
            temp = ""
            for x in y:
                temp += x
            print(temp)
        print("\n")
        
    """
        
class plane(figure):
    def init(self, n, m):
        #self = figure
        for i in range(n):
            for j in range(m):
                self.app( square(i,j) )


def formfigures(fi: figure, k: int) -> list[figure]:
    global name
    #print(f, k)
    #if fi==None:
    #    f: figure = figure()
    #else:
    #    f = fi.copy()
    f: figure = fi.copy()
    
    if k == 0:
        return [f]
        
    
    
        
    if len(f.squares)==0:
        f.app( square(0,0) )
        return formfigures(f, k-1)
    
    potential = []
    for i in f.squares:
        potential.append(i + (0,1))
        potential.append(i + (1,0))
        potential.append(i + (0,-1))
        potential.append(i + (-1,0))
    
    res = []
    ignore = []
    #print(list(map(str, potential)))
    for i in range(len(potential)):
        if i in ignore:
            continue
        for j in range(i+1, len(potential)):
            if potential[i] == potential[j]:
                ignore.append(j)
        p = potential[i]
        #print(p)
        if not p in f.squares:
            fc = f.copy()
            fc.app(p)
            res += formfigures(fc, k-1)
    ignore = []
    for i in range(len(res)):
        if i in ignore:
            continue
        for j in range(i+1, len(res)):
            if res[i] == res[j]:
                ignore.append(j)
    ignore.sort(reverse=1)
    for i in ignore:
        res.remove(res[i])
    return res

#formfigures = optimize.oprtimize1(formfigures)

def suitnormalized(fig: figure, p: figure) -> bool:
    if fig.maxx() > p.maxx() or fig.maxy() > p.maxy():
        return False
    #print(fig.maxx())
    for i in fig.squares:
        if not i in p.squares:
            f1 = fig.copy() + (1,0)
            #print(fig, f1)
            f2 = fig.copy() + (0,1)
            #print(fig, f2)
            return suitnormalized(f1, p) or suitnormalized(f2, p)
    return True


res = formfigures(figure(), 3)
print(len(res))

