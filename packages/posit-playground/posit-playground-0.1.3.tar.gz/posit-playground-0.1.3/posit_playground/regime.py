import pytest

from .utils import AnsiColor, get_bin


class Regime:
    def __init__(self, size, k=None):
        """k is None when the regime represents a 0 or infinity posit."""
        self.size = size
        if k == None or (k <= (size - 2) and k >= (-size + 2)):
            self.k = k
            self.is_out_of_range = False
        else:
            self.is_out_of_range = True
            # raise Exception("k = {} is out of bound".format(k))
            if k >= 0:
                self.k = size - 2
            else:
                self.k = -(size - 2)

    @property
    def reg_s(self):
        """
        'regime sign': leftmost regime bit
        (of the unsigned posit, i.e. two's complemented if negative"""
        if self.k == None:  # 0 or inf
            return None
        else:
            return bool(self.k >= 0).real

    @property
    def reg_len(self):
        """regime length, regardless of whether it's out of bound or not."""
        if self.k == None:  # 0 or inf
            return None
        elif self.k >= 0:
            return self.k + 2  # not bound checked
            # return min(self.size - 1, self.k + 2) # bound checked
        else:
            return -self.k + 1  # not bound checked
            # return min(self.size - 1, -self.k + 1) # bound checked

    def calc_reg_bits(self):
        if self.k == None:
            return 0
        elif self.k >= 0:
            # if self.reg_len < self.size:
            #     return (2 ** (self.k + 1) - 1) << 1
            # else:
            #     return 2 ** (self.k + 1) - 1
            return (2 ** (self.k + 1) - 1) << 1
        else:
            if self.reg_len < self.size:
                return 1
            else:
                # when out of bounds, e.g.
                # >>> Regime(size=8, k=-7)
                # (reg_s, reg_len) = (0, 8) -> k = -7
                # regime: 00000000
                raise Exception("regime bit fields all zeros is unexpected. the posit is a 'special' representation.")

    def __eq__(self, other):
        if isinstance(other, self.__class__):
            return self.__dict__ == other.__dict__
        else:
            return False

    def color_code(self):
        regime_bits_binary = get_bin(self.calc_reg_bits(), self.size)
        return f"{AnsiColor.ANSI_COLOR_GREY}{regime_bits_binary[:self.size - self.reg_len]}{AnsiColor.REG_COLOR}{regime_bits_binary[self.size-self.reg_len:]}{AnsiColor.RESET_COLOR}"

    def __repr__(self):
        return f"{self.color_code()} -> " + f"(reg_s, reg_len) = ({self.reg_s}, {self.reg_len}) -> k = {self.k}"


if __name__ == "__main__":
    print(f"run `pytest regime.py -v` to run the tests.")
