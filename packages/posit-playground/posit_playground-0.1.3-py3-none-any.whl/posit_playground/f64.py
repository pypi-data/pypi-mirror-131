import struct
from .utils import get_bin


class F64:
    """Helper class F64, used to implement `.from_double()`.

    F64(bits = 0x40a866a3d70a3d71)
    or
    F64(x_f64 = 24.0123)
    """

    SIZE = 64
    ES = 11
    MANT_SIZE = 52

    EXP_BIAS = 2 ** (ES - 1) - 1
    MASK = 2 ** SIZE - 1

    def __init__(self, **kwargs):
        assert self.SIZE == 1 + self.ES + self.MANT_SIZE

        if len(kwargs) == 1 and "bits" in kwargs:
            self.bits = kwargs["bits"]
        elif len(kwargs) == 1 and "x_f64" in kwargs:
            self.bits = F64._init_with_x_f64(kwargs["x_f64"])
        else:
            raise Exception("wrong constructor parameters. pass either `bits` or `x_f64`.")

    @staticmethod
    def _init_with_x_f64(x_f64):
        return struct.unpack("L", struct.pack("d", x_f64))[0]

    @property
    def sign(self):
        bits = self.bits
        return bits >> (F64.SIZE - 1)

    @property
    def exp(self):
        bits = self.bits
        return ((bits & (2 ** (F64.SIZE - 1) - 1)) >> F64.MANT_SIZE) & (2 ** F64.MANT_SIZE - 1)

    @property
    def mant(self):
        bits = self.bits
        return bits & (2 ** F64.MANT_SIZE - 1)

    def break_down(self) -> str:
        return f"(-1) ** {self.sign} * (2 ** ({self.exp} - {self.EXP_BIAS})) * (1 + {self.mant}/2**{self.MANT_SIZE}) =\n {(-1)**self.sign} * (2 ** {(self.exp - self.EXP_BIAS)}) * (1 + {self.mant}/2**{self.MANT_SIZE})"

    def eval(self) -> float:
        s, exp, mant = self.sign, self.exp, self.mant
        return (-1) ** s * (2 ** (exp - self.EXP_BIAS)) * (1 + mant / 2 ** self.MANT_SIZE)

    def __repr__(self):
        return f"{self.sign}, {get_bin(self.exp, F64.ES)}, {get_bin(self.mant, F64.MANT_SIZE)}"


# if __name__ == "__main__":
#     a = 0.03125
#     b = 0.25

#     # a/b = 0.125

#     a = F64(x_f64=a)
#     b = F64(x_f64=b)

#     a/b


# bits = 0x40a866a3d70a3d71
# bits == F64(x_f64 = F64(bits = bits).eval()).bits

# n = 0.31231432453412317
# n == F64(bits = F64(x_f64 = n).bits).eval()
