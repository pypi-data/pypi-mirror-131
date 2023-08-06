import math

# TODO deg transition to optimize time


class UncertainNumber (object):

    def __init__(self, number, uncertainty=0.0, deg_unc=None, add_signs=20, preprocessing=0, *args, **kwargs):
        if isinstance(number, (tuple,list)):
            if len(number) >= 2:
                uncertainty = number[1]
                number = number[0]
            elif len(number) == 1:
                number = number[0]
            else:
                raise TypeError("Not consistent types - tuplec must contain 2 elements")

        self.preproc = preprocessing
        self.add_signs = add_signs
        self.deg_un = deg_unc
        self.unc = self.round_up(abs(uncertainty), un=True, preprocessing=preprocessing) if uncertainty != 0 and self.need_ch(uncertainty) else uncertainty
        self.deg_un = self.deg_un if not self.deg_un is None or self.unc == 0 else -self.deg(self.unc)
        self.num = number if number == 0 or uncertainty == 0 else round(number, self.deg_un + self.add_signs)

    def __round__(self, n=None):
        return self._round(self.num, n)

    def _round(self, num, n=0):
        if num == 0:
            return 0

        return round(num, n - self.deg(num))

    def round_up(self, num, n=None, un=False, compensation=True, preprocessing=None):
        if num == 0:
            return 0

        dg = -self.deg(num)
        dg10 = 10 ** dg

        num = (round(num, 4 + dg) if preprocessing in {None, 0} else round(num, preprocessing + dg)) if not preprocessing is None or un else num
        if un:
            self.deg_un = dg

        if n in {None, 0}:
            num = math.ceil(num * dg10)/dg10 if num > 0 else math.floor(num * dg10)/dg10
        else:
            n10 = 10 ** n
            num = math.ceil(num * n10 * dg10) / dg10 / n10 if num > 0 else math.floor(num * n10 * dg10) / dg10 / n10

        if compensation:
            num = round(num, n + dg if not n is None else dg)

        return num

    def deg(self, num):
        return math.floor(math.log10(abs(num))) if num != 0 else -math.inf

    def need_ch(self, num):
        return round(num, -math.floor(math.log10(abs(num)))) != num if num != 0 else False

    def fixit(self, other, op="this operation"):
        if isinstance(other, UncertainNumber):
            return other
        if isinstance(other, (float, int)):
            return UncertainNumber(other, add_signs=self.add_signs, preprocessing=self.preproc)
        elif isinstance(other, (tuple, list)):
            return UncertainNumber(other[0], other[1], add_signs=self.add_signs, preprocessing=self.preproc)
        else:
            self._illegal(op)
            raise TypeError('other must be of type int, float, array or tuple')

    def __add__(self, other, ir=False):
        other = self.fixit(other, "+")
        return UncertainNumber(self.num + other.num, self.unc + other.unc, add_signs=self.add_signs if not ir else other.add_signs, preprocessing=self.preproc if not ir else other.preproc)

    def __radd__(self, other):  # defines other + self
        other = self.fixit(other, "+")
        return self.__add__(other, ir=True)

    def __iadd__(self, other):
        other = self.fixit(other, "+")
        self.num += other.num
        self.unc += other.unc
        self.__init__(self.num, self.unc, add_signs=self.add_signs, preprocessing=self.preproc)

    def __sub__(self, other):
        if other is self:
            return UncertainNumber(0, 0.0, add_signs=self.add_signs, preprocessing=self.preproc)

        other = self.fixit(other, "-")
        return UncertainNumber(self.num - other.num, self.unc + other.unc, add_signs=self.add_signs, preprocessing=self.preproc)

    def __rsub__(self, other):  # defines other + self
        if other is self:
            return UncertainNumber(0, 0.0, add_signs=other.add_signs, preprocessing=other.preproc)

        other = self.fixit(other, "-")
        return UncertainNumber(other.num - self.num, self.unc + other.unc, add_signs=other.add_signs, preprocessing=other.preproc)

    def __isub__(self, other):
        if other is self:
            self.__init__(0, 0.0, add_signs=self.add_signs, preprocessing=self.preproc)

        other = self.fixit(other, "-")
        self.num -= other.num
        self.unc += other.unc
        self.__init__(self.num, self.unc, add_signs=self.add_signs, preprocessing=self.preproc)

    def __mul__(self, other, ir=False):
        other = self.fixit(other, "*")
        _product = self.num * other.num
        return UncertainNumber(_product, (_product * (self.unc / self.num + other.unc / other.num) if _product != 0 else (self.unc * other.num if self.num == 0 else other.unc * self.num)), add_signs=self.add_signs if not ir else other.add_signs, preprocessing=self.preproc if not ir else other.preproc)

    def __rmul__(self, other):  # defines other + self
        other = self.fixit(other, "*")
        return self.__mul__(other, ir=True)

    def __imul__(self, other):
        other = self.fixit(other, "*")
        sn = self.num
        self.num *= other.num
        self.unc = (self.num * (self.unc / sn + other.unc / other.num) if self.num != 0 else (self.unc * other.num if sn == 0 else other.unc * sn))
        self.__init__(self.num, self.unc, add_signs=self.add_signs, preprocessing=self.preproc)

    def __truediv__(self, other):
        if other is self:
            return UncertainNumber(1, 0.0, add_signs=self.add_signs, preprocessing=self.preproc)

        other = self.fixit(other, "/")
        _div = self.num / other.num
        return UncertainNumber(_div, (_div * (self.unc / self.num + other.unc / other.num) if self.num != 0 else self.unc/other.num), add_signs=self.add_signs, preprocessing=self.preproc)

    def __rdiv__(self, other):  # defines other + self
        if other is self:
            return UncertainNumber(1, 0.0, add_signs=other.add_signs, preprocessing=other.preproc)

        other = self.fixit(other, "/")
        _div = other.num / self.num
        return UncertainNumber(_div, (_div * (self.unc / self.num + other.unc / other.num) if other.num != 0 else other.unc/self.num), add_signs=other.add_signs, preprocessing=other.preproc)

    def __idiv__(self, other):
        if other is self:
            self.__init__(1, 0.0, add_signs=self.add_signs, preprocessing=self.preproc)

        other = self.fixit(other, "+")
        sn = self.num
        self.num /= other.num
        self.unc = (self.num * (self.unc / sn + other.unc / other.num) if sn != 0 else self.unc/other.num)
        self.__init__(self.num, self.unc, add_signs=self.add_signs, preprocessing=self.preproc)

    def __abs__(self):
        return abs(self.num)

    def __neg__(self):  # defines -c (c is UncertainNumber)
        return UncertainNumber(-self.num, self.unc, add_signs=self.add_signs, preprocessing=self.preproc)

    def __eq__(self, other):
        return self.num == other.num and self.unc == other.unc

    def ae(self, other):
        return (self.num + self.unc >= other.num and self.num - self.unc <= other.num) or (other.num + other.unc >= self.num and other.num - other.unc <= self.num)

    def __ne__(self, other):
        return not self.__eq__(other)

    def __str__(self):
        return "%g \u00b1 %g" % (self.num if self.add_signs == 0 or self.deg_un is None or abs(self.deg_un) == math.inf else round(self.num, self.deg_un), self.unc)

    def __repr__(self):
        return 'UncertainNumber ' + str(self)

    def __pow__(self, power):
        power = self.fixit(power, "**")
        pwr = self.num ** power.num
        return UncertainNumber(pwr, (pwr / self.num if self.num != 0 else pwr) * self.unc * power.num + (math.log(self.num) * power.unc * pwr if self.num != 0 else power.unc), add_signs=self.add_signs, preprocessing=self.preproc)

    def __rpow__(self, base):
        base = self.fixit(base, "**")
        pwr = base.num ** self.num
        return UncertainNumber(pwr, (pwr / base.num if base.num != 0 else pwr) * base.unc * self.num + (math.log(base.num) * self.unc * pwr if base.num != 0 else self.unc), add_signs=base.add_signs, preprocessing=base.preproc)

    def __ipow__(self, power):
        power = self.fixit(power, "**")
        pwr = self.num ** power.num
        sn = self.num
        self.num = pwr
        self.unc = (pwr / sn if self.num != 0 else pwr) * self.unc * power.num + (math.log(sn) * power.unc * pwr if sn != 0 else power.unc)
        self.__init__(self.num, self.unc, add_signs=self.add_signs, preprocessing=self.preproc)

    def __gt__(self, other):
        other = self.fixit(other, ">")
        return self.num - self.unc > other.num + other.unc

    def __ge__(self, other):
        other = self.fixit(other, ">=")
        return self.num - self.unc >= other.num - other.unc

    def __lt__(self, other):
        other = self.fixit(other, "<")
        return self.num + self.unc < other.num - other.unc

    def __le__(self, other):
        other = self.fixit(other, "<=")
        return self.num + self.unc <= other.num + other.unc

    def _illegal(self, op):
        print('illegal operation "%s" for uncertain number' % op)

def mean_un(arr):
    for i in range(len(arr)):
        if not isinstance(arr[i], UncertainNumber):
            arr[i] = UncertainNumber.fixit(arr[i],"convert")
    arr_num = [i.num for i in arr]
    arr_unc = [i.unc for i in arr]
    x = sum(arr_num)/len(arr_num)
    std = sum([(x-i)**2 for i in arr_num])/(len(arr_num)-1)
    delta = (sum(arr_unc)/len(arr_unc))**2

    return UncertainNumber(x, ((delta if delta > (1/10)*std else 0) + (std if std > (1/10)*delta else 0))**(1/2), add_signs=arr[0].add_signs, preprocessing=arr[0].preproc)

un = UncertainNumber

if __name__ == "__main__":
    o = un(1, 0.05)
    oh = un(6, 0.4)
    g = un(3,0)
    oo = o ** oh + o * oh - oh / o
    ooo = mean_un([un(1, 0.05),un(1.1, 0.05),un(0.9, 0.05),un(0.7, 0.05),un(1.3, 0.05)])
    print(oo)
    print(ooo)
    print(un(1,0)*g)