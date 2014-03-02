from math import *

class Polynomial:
    def __init__(self, terms = []):
        self.terms = terms
        self.degree = self.__degree()
        
    def __getitem__(self, n):
        return self.terms[n]
    
    def __setitem__(self, n, v):
        self.terms[n] = v
        return
        
    def __call__(self, n):
        sum = 0
        i = 0
        while i < len(self.terms):
            sum += self.terms[i] * (n**i)
            i += 1
        return sum
    
    def __len__(self):
        return len(self.terms)
        
    def __str__(self):
        out = ''
        i = self.degree
        while i >= 0:
            if self.terms[i] < 0:
                out += "-"
            elif i != self.degree and self.terms[i] != 0:
                out += "+"
            if i == 0 and self.terms[i] != 0:
                out += str(abs(self.terms[i]))
            elif abs(self.terms[i]) != 1 and self.terms[i] != 0:
                out += str(abs(self.terms[i]))
                if i != 1:
                    out += 'x^' + str(i)
                else:
                    out += 'x'
            elif self.terms[i] != 0:
                if i != 1:
                    out += 'x^' + str(i)
                else:
                    out += 'x'
            i -= 1
        return out
    
    def __add__(self, p):
        ply = []
        c = 0
        for i in range(max(len(self.terms), len(p))):
            if c >= len(self.terms):
                ply.insert(i, p[i])
            elif c >= len(p):
                ply.insert(i, self.terms[i])
            else:
                ply.insert(i, p[i] + self.terms[i])
            c += 1
        return Polynomial(ply)
        
    def __sub__(self, p):
        ply = []
        c = 0
        for i in range(max(len(self.terms), len(p))):
            if c >= len(self.terms):
                ply.insert(i, -p[i])
            elif c >= len(p):
                ply.insert(i, self.terms[i])
            else:
                ply.insert(i, self.terms[i] - p[i])
            c += 1
        return Polynomial(ply)
        
    def __mul__(self, p):
        ply = []
        if isinstance(p, Polynomial):
            for i in range(len(self.terms)):
                for j in range(len(p)):
                    try:
                        ply[i+j] += self.terms[i]*p[j]
                    except:
                        ply.insert(i+j, self.terms[i]*p[j])
        else:
            for i in range(len(self.terms)):
                ply.insert(i, self.terms[i] * p)
        return Polynomial(ply)
        
    def __div__(self, p):
        if isinstance(p, Polynomial):
            if not p.zero():
                q = Polynomial()
                r = Polynomial(self.terms)
                print r
                while not r.zero() and r.degree >= p.degree:
                    t_c = r[r.degree] / p[p.degree]
                    t_x = r.degree - p.degree
                    t = Polynomial([0]*(t_x) + [t_c])
                    q = q + t
                    r = r - (t * p)
                return q, r
            else:
                print "Division by zero! Canceling divison."
                return None
        else:
            ply = []
            for i in range(len(self.terms)):
                ply.insert(i, self.terms[i] * p)
            return Polynomial(ply)
            
    def __mod__(self, p):
        if isinstance(p, Polynomial):
            if not p.zero():
                q = Polynomial()
                r = Polynomial(self.terms)
                print r
                while not r.zero() and r.degree >= p.degree:
                    t_c = r[r.degree] / p[p.degree]
                    t_x = r.degree - p.degree
                    t = Polynomial([0]*(t_x) + [t_c])
                    q = q + t
                    r = r - (t * p)
                return r
            else:
                print "Division by zero! Canceling divison."
                return None
        
    def __iadd__(self, p):
        return self+p
        
    def __isub__(self, p):
        return self-p
        
    def __imul__(self, p):
        if isinstance(p, Polynomial):
            return self*p
        else:
            for i in range(len(self.terms)):
                self.terms[i] *= p
        return self
        
    def __idiv__(self, p):
        if isinstance(p, Polynomial):
            return self/p
        else:
            for i in range(len(self.terms)):
                self.terms[i] /= p
        return self
        
    def __imod__(self, p):
        if isinstance(p, Polynomial):
            return self%p
        else:
            for i in range(len(self.terms)):
                self.terms[i] %= p
        return self
        
    def __degree(self):
        c = 0
        for i in reversed(self.terms):
            if i != 0:
                return len(self.terms)-1-c
            c += 1
        return 0
    
    def zero(self):
        for i in self.terms:
            if i != 0:
                return False
        return True
