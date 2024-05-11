class oprtimize1:
    image: list[tuple] = []
    def __init__(self, func):
        self.func = func
        self.image = []
    
    def __call__(self, *arg, **kwarg):
        if arg[1]==0:
            return [arg[0]]
        
        for (key, value) in self.image:
            if arg[0] == key:
                return value
        
        res = self.func(*arg, **kwarg)
        self.image.append((arg[0].copy(), res.copy()))
        return res

    