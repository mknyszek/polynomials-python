import sys, math;

class Mod:
    M = 17
    @staticmethod
    def set_mod(n):
        if n > 0 and isinstance(n, int):
            Mod.M = n
        else:
            raise Exception("Modulus must be a positive integer.")
    
    @staticmethod
    def math_mod(a):
        return (abs(a * Mod.M) + a) % Mod.M

    @staticmethod
    def exp_mod(a, b):
        if b == 0:
            return 1
        else:
            z = Mod.exp_mod(a, b // 2)
            if b % 2 == 0:
                return Mod.math_mod(z*z)
            else:
                return Mod.math_mod(a*z*z)

    @staticmethod
    def egcd(a, b):
        if b == 0:
            return (a, 1, 0)
        else:
            (d, x, y) = Mod.egcd(b, a % b)
            return (d, y, x - (a // b)*y)

    def __init__(self, n):
        self.value = Mod.math_mod(n)

    def __neg__(self):
        return Mod(-self.value)

    def __add__(self, m):
        if isinstance(m, Mod):
            return Mod(self.value + m.value)
        else:
            return Mod(self.value + m)

    def __sub__(self, m):
        if isinstance(m, Mod):
            return Mod(self.value - m.value)
        else:
            return Mod(self.value - m)

    def __mul__(self, m):
        if isinstance(m, Mod):
            return Mod(self.value * m.value)
        else:
            return Mod(self.value * m)

    def __iadd__(self, m):
        return self+m

    def __isub__(self, m):
        return self-m

    def __imul__(self, m):
        return self*m
    
    def __pow__(self, k):
        return Mod(Mod.exp_mod(self.value, k))

    def __str__(self):
        return str(self.value)

    def __eq__(self, m):
        if isinstance(m, Mod):
            return self.value == m.value
        else:
            return self.value == Mod.math_mod(m)

    def __ne__(self, m):
        if isinstance(m, Mod):
            return self.value != m.value
        else:
            return self.value != Mod.math_mod(m)

    def inverse(self):
        if self.value == 0:
            raise Exception("Inverse of 0 is undefined.")
        val = Mod.egcd(Mod.M, self.value)
        if val[0] == 1:
            return Mod(val[2])
        else:
            raise Exception("Mod and value are not co-prime. Inverse is undefined.")

class PolyMod:
    @staticmethod
    def interpolate(points):
        deltas = []
        s = PolyMod([0])
        for i in range(len(points)):
            num = PolyMod([1])
            den = Mod(1)
            for j in range(len(points)):
                if i != j:
                    num *= PolyMod([-points[j][0], 1])
                    den *= points[i][0]-points[j][0]
            try:
                num *= den.inverse()
            except Exception:
                raise Exception("Caught improper inverse. Interpolation impossible.")
                return None
            deltas.append(num)
        for i in range(len(points)):
            s += deltas[i]*points[i][1]
        return s
    
    def __init__(self, terms = []):
        self.terms = [Mod(i) if not isinstance(i, Mod) else i for i in terms]
        self.degree = self.__degree()
        
    def __getitem__(self, n):
        return self.terms[n]
    
    def __setitem__(self, n, v):
        self.terms[n] = Mod(v)
        return
        
    def __call__(self, v):
        sum = Mod(0)
        n = Mod(v)
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
            if i != self.degree and self.terms[i] != 0:
                out += "+"
            if i == 0 and self.terms[i] != 0:
                out += str(self.terms[i])
            elif self.terms[i] != 1 and self.terms[i] != 0:
                out += str(self.terms[i])
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
        return PolyMod(ply)
        
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
        return PolyMod(ply)
        
    def __mul__(self, p):
        ply = []
        if isinstance(p, PolyMod):
            for i in range(len(self.terms)):
                for j in range(len(p)):
                    try:
                        ply[i+j] += self.terms[i]*p[j]
                    except:
                        ply.insert(i+j, self.terms[i]*p[j])
        else:
            for i in range(len(self.terms)):
                ply.insert(i, self.terms[i] * p)
        return PolyMod(ply)
        
    def __iadd__(self, p):
        return self+p
        
    def __isub__(self, p):
        return self-p
        
    def __imul__(self, p):
        if isinstance(p, PolyMod):
            return self*p
        else:
            for i in range(len(self.terms)):
                self.terms[i] *= p
        return self
        
    def __degree(self):
        c = 0
        for i in reversed(self.terms):
            if i != 0:
                return len(self.terms)-1-c
            c += 1
        return 0

    def __eq__(self, p):
        j = 0
        for i in p.terms:
            if self.terms[j] != i:
                return False
            j += 1
        return True

    def __ne__(self, p):
        return not (self == p)
    
    def zero(self):
        for i in self.terms:
            if i != 0:
                return False
        return True
