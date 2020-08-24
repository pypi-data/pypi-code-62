from decimal import *


class Luckyseven:
    def prng(self, b, n, mu, i, j, p):
        getcontext().prec = p
        M = Decimal(b) / Decimal(10 ** n - mu)
        P = (10 ** p) * M
        R = (P % 10 ** (i + j) - P % 10 ** i) / 10 ** i
        return R
