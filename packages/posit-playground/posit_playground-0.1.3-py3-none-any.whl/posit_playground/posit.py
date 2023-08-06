from __future__ import annotations
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from _typeshed import Self
from typing import Dict
import struct
from math import inf, log2

from .utils import get_bin, get_hex, shl, shr, c2, AnsiColor, ansilen, strip_color, dbg_print
from .regime import Regime
from .f64 import F64


msb = lambda N: shl(1, N - 1, N)  # if N = 8bits: 1 << 8 i.e. 1000_0000
mask = lambda N: 2 ** N - 1  # N-bit ALL ones


def cls(bits, size, val=1):
    """
    count leading set
    counts leading `val`, leftwise
    """
    if val == 1:
        return _clo(bits, size)
    elif val == 0:
        return _clz(bits, size)
    else:
        raise ("val is binary! pass either 0 or 1.")


def _clo(bits, size):
    """
    count leading ones
    0b1111_0111 -> 4
    """
    bits &= mask(size)
    if bool(bits & (1 << (size - 1))) == False:
        return 0
    return 1 + _clo(bits << 1, size)


def _clz(bits, size):
    """count leading zeros"""
    return _clo(~bits, size)


class Posit:
    def __init__(self, size, es, sign, regime, exp, mant):
        self.size = size
        self.es = es
        self.sign = sign
        self.regime = regime
        if exp > (2 ** es - 1):
            # print("eror. exponent does not fit in `es`.")
            raise Exception("exponent does not fit in `es`.")
        else:
            self.exp = exp
        self.mant = mant

    def __eq__(self, other):
        if isinstance(other, self.__class__):
            return self.__dict__ == other.__dict__
        else:
            return False

    def __mul__(self, other):
        return mul(self, other)

    def __iadd__(self, inc: int):
        """
        Overload of the += operator.
        Increment your posit by `inc`.
        """
        bits = self.bit_repr()
        bits = (bits + inc) & mask(self.size)
        return from_bits(bits, self.size, self.es)

    def __isub__(self, dec: int):
        """
        Overload of the -= operator.
        Decrement your posit by `dec`.
        """
        return self.__iadd__(-dec)

    def __add__(self, rhs: int):
        """
        Overload of the + operator.
        Add `inc` to your posit.
        """
        bits = self.bit_repr()
        bits += (bits + rhs) & mask(self.size)
        return from_bits(bits, self.size, self.es)

    def __sub__(self, dec: int):
        """
        Overload of the - operator.
        Subtract your posit by `dec`.
        """
        return self.__add__(-dec)

    def __lt__(self, other):
        return self.eval() < other.eval()

    def __gt__(self, other):
        return self.eval() > other.eval()

    def __le__(self, other):
        return self.eval() <= other.eval()

    def __ge__(self, other):
        return self.eval() >= other.eval()

    @staticmethod
    def bit_abs(p1: Self, p2: Self):
        """Compute the 'bitwise' difference.
        e.g.: bit_abs( P<4,0> 0010, P<4,0> 0001 ) = 1
        """
        return p1.bit_repr() - p2.bit_repr() if p1 > p2 else p2.bit_repr() - p1.bit_repr()

    @property
    def is_special(self):
        """
        zero or infinity
        """
        return self.regime.k == None

    @property
    def mant_len(self):
        """length of mantissa field"""
        if self.is_special:  # there is no such thing as mantissa in a 0 / infinity
            return None

        # return max(0, self.size - 1 - self.regime.reg_len - self.es_effective)
        return self.size - 1 - self.regime.reg_len - self.es

    def bit_repr(self):
        """
        s_rrrr_e_mm =
        s_0000_0_00 |     sign
        0_rrrr_0_00 |     regime
        0_0000_e_00 |     exp
        0_0000_0_mm |     mant
        """
        if self.is_special:
            return 0 if self.sign == 0 else (1 << (self.size - 1))

        sign_shift = self.size - 1
        regime_shift = sign_shift - self.regime.reg_len
        exp_shift = regime_shift - self.es

        regime_bits = self.regime.calc_reg_bits()

        bits = (
            shl(self.sign, sign_shift, self.size)
            | shl(regime_bits, regime_shift, self.size)
            | shl(self.exp, exp_shift, self.size)
            | self.mant
        )

        if self.sign == 0:
            return bits
        else:
            # ~(1 << (self.size - 1)) = 0x7f if 8 bits
            return c2(bits & ~(1 << (self.size - 1)), self.size)

    def to_real(self):
        print("deprecated. Use .eval()")

    def eval(self):
        if self.regime.reg_len == None:  # 0 or inf
            return 0 if self.sign == 0 else inf
        else:
            F = self.mant_len
            try:
                return (
                    (-1) ** self.sign.real
                    * (2 ** (2 ** self.es)) ** self.regime.k
                    * (2 ** self.exp)
                    * (1 + self.mant / (2 ** F))
                )
            except OverflowError:
                if (2 ** self.es * self.regime.k + self.exp) < 0:
                    if self.sign.real:
                        return 1 / -inf
                    else:
                        return 1 / inf
                else:
                    if self.sign.real:
                        return -inf
                    else:
                        return inf

    def break_down(self):
        if self.regime.reg_len == None:  # 0 or inf
            pass
        else:
            F = self.mant_len
            if self.es == 0:
                return (
                    f"(-1) ** {AnsiColor.SIGN_COLOR}{self.sign.real}{AnsiColor.RESET_COLOR} * "
                    + f"(2 ** {AnsiColor.REG_COLOR}{self.regime.k}{AnsiColor.RESET_COLOR}) * "
                    + f"(1 + {AnsiColor.MANT_COLOR}{self.mant}{AnsiColor.RESET_COLOR}/{2**F})"
                )
            else:
                return (
                    f"(-1) ** {AnsiColor.SIGN_COLOR}{self.sign.real}{AnsiColor.RESET_COLOR} * "
                    + f"(2 ** (2 ** {AnsiColor.EXP_COLOR}{self.es}{AnsiColor.RESET_COLOR})) ** {AnsiColor.REG_COLOR}{self.regime.k}{AnsiColor.RESET_COLOR} * "
                    + f"(2 ** {AnsiColor.EXP_COLOR}{self.exp}{AnsiColor.RESET_COLOR}) * "
                    + f"(1 + {AnsiColor.MANT_COLOR}{self.mant}{AnsiColor.RESET_COLOR}/{2**F})"
                )

    def _color_code(self) -> Dict[str, str]:
        """
        sign length:     1
        regime length:   self.regime.reg_len
        exponent length: es
        mantissa length: size - sign_len - reg_len - ex_len
        """
        if self.is_special == False:
            mant_len = self.mant_len
            regime_bits_str = f"{self.regime.calc_reg_bits():064b}"[64 - self.regime.reg_len :]
            exp_bits_str = f"{self.exp:064b}"[64 - self.es :]
            mant_bits_str = f"{self.mant:064b}"[64 - mant_len :]

            ans = {
                "sign_color": AnsiColor.SIGN_COLOR,
                "sign_val": str(self.sign.real),
                "reg_color": AnsiColor.REG_COLOR,
                "reg_bits": regime_bits_str,
                "exp_color": AnsiColor.EXP_COLOR,
                "exp_bits": exp_bits_str,
                "mant_color": AnsiColor.MANT_COLOR,
                "mant_bits": mant_bits_str,
                "ansi_reset": AnsiColor.RESET_COLOR,
            }
        return ans

    def color_code(self, trimmed=True) -> str:
        if self.is_special:
            return "".join(
                [
                    AnsiColor.SIGN_COLOR,
                    str(self.sign.real),
                    AnsiColor.RESET_COLOR,
                    AnsiColor.ANSI_COLOR_GREY,
                    "0" * (self.size - 1),
                    AnsiColor.RESET_COLOR,
                ]
            )

        color_code_dict: Dict[str, str] = self._color_code()
        full_repr: str = "".join(x for x in color_code_dict.values())

        if trimmed == False:
            return full_repr
        else:
            diff_length: int = abs(ansilen(full_repr) - self.size)

            if diff_length == 0:
                # cool
                ans = full_repr
            else:
                if diff_length < self.es:
                    # strip es
                    color_code_dict["exp_bits"] = color_code_dict["exp_bits"][:-diff_length]
                elif diff_length >= self.es:
                    # wipe es
                    color_code_dict.pop("exp_color")
                    color_code_dict.pop("exp_bits")
                    diff_length -= self.es
                    if diff_length > 0:
                        # and also strip the regime
                        color_code_dict["reg_bits"] = color_code_dict["reg_bits"][:-diff_length]
                ans = "".join(x for x in color_code_dict.values())

            ans_no_color = strip_color(ans)
            assert len(ans_no_color) == self.size
            return ans

    def __repr__(self):
        exponent_binary_repr = get_bin(self.exp, self.size)
        mantissa_binary_repr = get_bin(self.mant, self.size)

        posit_bit_repr = self.bit_repr()

        # signature
        posit_signature = f"P<{self.size},{self.es}>:"
        ans = f"{posit_signature:<17}0b{get_bin(posit_bit_repr, self.size)}   0x{get_hex(posit_bit_repr, int(self.size/4))}\n"
        # color
        ans += f"{' ':<19}{self.color_code(trimmed=True)}   "
        # sign
        ans += f"\n{'s:':<19}{AnsiColor.SIGN_COLOR}{self.sign.real}{AnsiColor.RESET_COLOR}\n"
        if self.is_special == False:
            # regime
            ans += f"{'reg_bits:':<19}{self.regime}\n"
            # exponent
            if self.es:
                ans += f"{'exp:':<19}{' '*(self.size- self.es)}{AnsiColor.EXP_COLOR}{exponent_binary_repr[self.size-self.es:]}{AnsiColor.RESET_COLOR}\n"
            # mantissa
            ans += f"{'mant:':<19}{AnsiColor.ANSI_COLOR_GREY}{mantissa_binary_repr[:self.size-self.mant_len]}{AnsiColor.MANT_COLOR}{mantissa_binary_repr[self.size-self.mant_len:]}{AnsiColor.RESET_COLOR}\n"
            # ans += f"F = mant_len: {self.mant_len} -> 2 ** F = {2**self.mant_len}\n"
        ans += f"{' ':<19}{''.join(self.color_code(trimmed=False))}\n\n"
        # posit broken down
        ans += f"{' ':<19}{self.break_down()}\n"
        ans += f"{' ':<19}{self.eval()}\n"
        ans += f"{AnsiColor.ANSI_COLOR_CYAN}{'~'*45}{AnsiColor.RESET_COLOR}\n"
        return ans


def from_bits(bits, size, es) -> Posit:
    """
    Posit decoder.

    Break down P<size, es> in its components (sign, regime, exponent, mantissa).

    Prameters:
    bits (unsigned): sequence of bits representing the posit
    size (unsigned): length of posit
    es (unsigned): exponent field size.

    Returns:
    Posit object
    """
    if es > size - 1:
        raise ValueError("`es` field can't be larger than the full posit itself.")

    sign = bits >> (size - 1)

    if (bits << 1) & mask(size) == 0:  # 0 or inf
        return Posit(size, es, sign, Regime(size=size), 0, 0)

    if log2(bits) > size:
        raise Exception("cant fit {} in {} bits".format(bits, size))

    u_bits = bits if sign == 0 else c2(bits, size)
    reg_msb = 1 << (size - 2)
    reg_s = bool(u_bits & reg_msb)
    if reg_s == True:
        k = cls(u_bits << 1, size, 1) - 1
        reg_len = 2 + k  # min(k + 2, size - 1)
    else:
        k = -cls(u_bits << 1, size, 0)
        reg_len = 1 - k  # min(-k + 1, size - 1)

    r = Regime(size=size, k=k)

    assert r.reg_len == reg_len

    regime_bits = ((u_bits << 1) & mask(size)) >> (size - reg_len)

    es_effective = min(es, size - 1 - reg_len)

    # align remaining of u_bits to the left after dropping sign (1 bit) and regime (`reg_len` bits)
    exp = ((u_bits << (1 + reg_len)) & mask(size)) >> (size - es)  # max((size - es), (size - 1 - reg_len))

    mant = ((u_bits << (1 + reg_len + es)) & mask(size)) >> (1 + reg_len + es)

    posit = Posit(
        size=size,
        es=es,
        sign=sign,
        regime=r,
        exp=exp,
        mant=mant,
    )

    assert bits == posit.bit_repr()

    return posit


def mul(p1: Posit, p2: Posit, debug_print=False) -> Posit:
    assert p1.size == p2.size
    assert p1.es == p2.es

    size, es = p1.size, p1.es
    sign = p1.sign ^ p2.sign

    # handles 0 * inf and inf * 0
    if ((p1.is_special and p1.sign == 0) and (p2.is_special and p2.sign == 1)) or (
        (p1.is_special and p1.sign == 1) and (p2.is_special and p2.sign == 0)
    ):
        return Posit(size, es, 1, Regime(size=size, k=None), 0, 0)
    # handles 0 * anything and anything * 0
    if (p1.is_special and p1.sign == 0) or (p2.is_special and p2.sign == 0):
        return Posit(size, es, 0, Regime(size=size, k=None), 0, 0)
    # handles inf * anything and anything * inf
    if (p1.is_special and p1.sign == 1) or (p2.is_special and p2.sign == 1):
        return Posit(size, es, 1, Regime(size=size, k=None), 0, 0)

    F1, F2 = p1.mant_len, p2.mant_len

    k = p1.regime.k + p2.regime.k
    exp = p1.exp + p2.exp

    mant_1_left_aligned = p1.mant << (size - 1 - F1)
    mant_2_left_aligned = p2.mant << (size - 1 - F2)

    ### left align and set a 1 at the msb position, indicating a fixed point number represented as 1.mant
    f1 = msb(size) | mant_1_left_aligned
    f2 = msb(size) | mant_2_left_aligned
    mant = (f1 * f2) & mask(2 * size)  # fixed point mantissa product of 1.fff.. * 1.ffff.. on 2N bits

    if debug_print:
        dbg_print(
            f"""{' '*size}{AnsiColor.MANT_COLOR}{get_bin(f1, size)[:1]}{AnsiColor.RESET_COLOR}{get_bin(f1, size)[1:]} x
{' '*size}{AnsiColor.MANT_COLOR}{get_bin(f2, size)[:1]}{AnsiColor.RESET_COLOR}{get_bin(f2, size)[1:]} =
{'-'*(2*size + 2)}
{AnsiColor.MANT_COLOR}{get_bin(mant, 2*size)[:2]}{AnsiColor.RESET_COLOR}{get_bin(mant, 2*size)[2:]}"""
        )

    mant_carry = bool((mant & msb(2 * size)) != 0).real

    if debug_print:
        dbg_print(f"mant_carry = {AnsiColor.MANT_COLOR}{mant_carry.real}{AnsiColor.RESET_COLOR}")
        dbg_print(
            f"k + exp + mant_carry = {AnsiColor.REG_COLOR}{k}{AnsiColor.RESET_COLOR} + {AnsiColor.EXP_COLOR}{exp}{AnsiColor.RESET_COLOR} + {AnsiColor.MANT_COLOR}{mant_carry}{AnsiColor.RESET_COLOR}"
        )

    exp_carry = bool((exp & msb(es + 1)) != 0).real
    if exp_carry == 1:
        k = k + 1  # k_adjusted_I
        # wrap exponent
        exp = exp & (2 ** es - 1)  # exp_adjusted_I

    if debug_print:
        dbg_print(
            f"k + exp + mant_carry = {AnsiColor.REG_COLOR}{k}{AnsiColor.RESET_COLOR} + {AnsiColor.EXP_COLOR}{exp}{AnsiColor.RESET_COLOR} + {AnsiColor.MANT_COLOR}{mant_carry}{AnsiColor.RESET_COLOR}"
        )

    if mant_carry == 1:
        exp = exp + 1  # exp_adjusted_II
        exp_carry = bool((exp & msb(es + 1)) != 0).real  # exp_carry_I
        if exp_carry == 1:
            k = k + 1  # k_adjusted_II
            # wrap exponent
            exp = exp & (2 ** es - 1)  # exp_adjusted_III
        mant = mant >> 1  # mant_adjusted_I

    if debug_print:
        dbg_print(
            f"k + exp + mant_carry = {AnsiColor.REG_COLOR}{k}{AnsiColor.RESET_COLOR} + {AnsiColor.EXP_COLOR}{exp}{AnsiColor.RESET_COLOR} + {AnsiColor.MANT_COLOR}{mant_carry}{AnsiColor.RESET_COLOR}"
        )

    # adjust k overflow/underflow
    if k >= 0:
        # k = min(k, size - 2)
        if k > size - 2:
            k_is_oob = True
            k = size - 2
        else:
            k_is_oob = False
            k
    else:
        if k < -(size - 2):
            k_is_oob = True
            k = -(size - 2)
        else:
            k_is_oob = False
            k
        # k = max(k, -(size - 2))

    if debug_print:
        print(f"k + exp + mant_carry = {k} + {exp} + {mant_carry}")

    r = Regime(size=size, k=k)
    reg_len = r.reg_len

    mant_non_fractional_part = mant & (0b11 << (2 * size - 2))  # who cares
    mant_fractional_part = mant & (2 ** (2 * size - 2) - 1)

    mant_len = size - 1 - es - reg_len

    len_mant_fractional_part_discarded = 2 * size - 2 - mant_len

    mant_fractional_part_discarded = mant_fractional_part & (2 ** len_mant_fractional_part_discarded - 1)
    mant_fractional_part_left = mant_fractional_part >> len_mant_fractional_part_discarded

    # threshold = (2 ** len_mant_fractional_part_discarded) / 2
    threshold = (1 << len_mant_fractional_part_discarded) >> 1

    if debug_print:
        print(f"mant_fractional_part = {get_bin(mant_fractional_part, 2*size)}")
        print(
            f"mant_fractional_part_left = {get_bin(mant_fractional_part_left, 2*size-len_mant_fractional_part_discarded)}"
        )
        print(
            f"mant_fractional_part_discarded = {get_bin(mant_fractional_part_discarded, len_mant_fractional_part_discarded)}"
        )
        print(f"{mant_len=}")
        print(f"mant_fractional_part_discarded >  threshold: {mant_fractional_part_discarded > threshold}")
        print(f"mant_fractional_part_discarded == threshold: {mant_fractional_part_discarded == threshold}")
        print(f"mant_fractional_part_discarded <  threshold: {mant_fractional_part_discarded < threshold}")

    round_to_nearest = True
    if round_to_nearest and k_is_oob == False:
        ### still not fully working

        if (sign == 0 and mant_fractional_part_discarded > threshold) or (
            sign == 1 and mant_fractional_part_discarded >= threshold
        ):
            if mant_fractional_part_left < (2 ** mant_len - 1):
                mant_fractional_part_left += 1
            elif mant_fractional_part_left == (2 ** mant_len - 1):
                mant_fractional_part_left = 0
                if exp < (2 ** es - 1):
                    exp += 1
                elif exp == (2 ** es - 1):
                    exp = 0
                    if k < size - 2:
                        k += 1

    # default would be rounding down

    posit = Posit(
        size=size,
        es=es,
        sign=sign,
        regime=Regime(size=size, k=k),
        exp=exp,
        mant=mant_fractional_part_left,
    )
    return posit


def from_double(x, size, es):
    """
    Build Posit from 64-bit floating point (double).

    Prameters:
    x (float): real number
    size (unsigned): length of posit
    es (unsigned): exponent field size.

    Returns:
    Posit object
    """
    if x == 0:
        return from_bits(0, size, es)
    if x == inf:
        return from_bits((1 << (size - 1)), size, es)

    n_f64_bits = struct.unpack("L", struct.pack("d", x))[0]
    f64obj = F64(bits=n_f64_bits)

    p_sign = f64obj.sign

    f64exp_wo_bias = f64obj.exp - F64.EXP_BIAS

    ### when es == 0 the result is automatically correct as well.
    k = f64exp_wo_bias >> es  # f64exp_wo_bias // (2 ** es)
    p_exp = f64exp_wo_bias - ((1 << es) * k)  # f64exp_wo_bias - (2 ** es) * k

    ### print(f"es={es}  {f64exp_wo_bias}%{2**es}={f64exp_wo_bias//(2**es)}   {2**es} * {k}+ {p_exp} == {f64exp_wo_bias}")

    r = Regime(size, k)
    mant_len = size - 1 - es - r.reg_len
    mant_len_diff = F64.MANT_SIZE - mant_len
    p_mant = shr(f64obj.mant, mant_len_diff, F64.MANT_SIZE)

    mant_discarded = f64obj.mant & (2 ** mant_len_diff - 1)

    ### print(get_bin(f64obj.mant, F64.MANT_SIZE))
    ### print(get_bin(p_mant, mant_len))
    ### print(" " * mant_len + get_bin(mant_discarded, mant_len_diff))

    # threshold at half of the range of the possible numbers representable in `mant_len_diff` bits.
    threshold = (1 << mant_len_diff) >> 1  # threshold = (2 ** mant_len_diff) / 2
    round_to_nearest = True
    if round_to_nearest:
        if p_sign == 0:
            if mant_discarded > threshold:
                # in P<8,0> 9.0 is between 8.0 and 10.0 and is rounded to 8.0 (thus down) [softposit's]
                p_mant += 1
        else:
            if mant_discarded >= threshold:
                # likewise -9.0 is between -8.0 and -10.0 and is rounded to -8.0 (thus up) [softposit's]
                p_mant += 1

    # round down would be automatic

    return Posit(
        size=size,
        es=es,
        sign=p_sign,
        regime=r,
        exp=p_exp,
        mant=p_mant,
    )


def from_posit(p: Posit, size, es) -> Posit:
    """
    From P<any,any> to P<any',any'>
    """
    pass


def posit8(*args, **kwargs):
    """This gives me a [Softposit](https://gitlab.com/cerlane/SoftPosit-Python)'s like api.
    from posit_playground import posit8

    posit8(3.1)

    posit8(bits=0x6f)
    """
    if len(kwargs) == 0 and len(args) == 1:
        return from_double(x=args[0], size=8, es=0)
    elif len(args) == 0 and len(kwargs) == 1 and "bits" in kwargs:
        return from_bits(bits=kwargs["bits"], size=8, es=0)


def posit16(*args, **kwargs):
    """This gives me a [Softposit](https://gitlab.com/cerlane/SoftPosit-Python)'s like api.
    from posit_playground import posit16

    posit16(3.1)

    posit16(bits=0x6aff)
    """
    if len(kwargs) == 0 and len(args) == 1:
        return from_double(x=args[0], size=16, es=1)
    elif len(args) == 0 and len(kwargs) == 1 and "bits" in kwargs:
        return from_bits(bits=kwargs["bits"], size=16, es=1)


def posit32(*args, **kwargs):
    """This gives me a [Softposit](https://gitlab.com/cerlane/SoftPosit-Python)'s like api.
    from posit_playground import posit32

    posit32(3.1)

    posit32(bits=0x612fabc3)
    """
    if len(kwargs) == 0 and len(args) == 1:
        return from_double(x=args[0], size=32, es=2)
    elif len(args) == 0 and len(kwargs) == 1 and "bits" in kwargs:
        return from_bits(bits=kwargs["bits"], size=32, es=2)


# a = from_bits(0xFB, 8, 0)
# b = from_bits(0x0C, 8, 0)
# m = a * b
# print(a)

# cc = from_bits(0xFF, 8, 0)
# print(cc)

a1 = posit8(bits=0b00000100)
a2 = posit8(bits=0b00111000)
a = a1 * a2

if __name__ == "__main__":

    print(f"run `pytest posit.py -v` to run the tests.")

    # p1 = from_bits(27598, 16, 1)
    # p2 = from_bits(15701, 16, 1)
    # print(mul(p1, p2))

    # p1 = from_bits(55662, 16, 1)
    # p2 = from_bits(32244, 16, 1)
    # print(mul(p1, p2))

    # p1 = from_bits(2904643641, 32, 2)
    # p2 = from_bits(1545728239, 32, 2)
    # print(mul(p1, p2))

    # p1 = from_bits(0b00111001110110111000000110101010, 32, 2)
    # p2 = from_bits(0b01100000001111111100000111111001, 32, 2)
    # print(mul(p1, p2))

    # p1 = from_bits(0b01100011, 8, 0)
    # p2 = from_bits(0b00111111, 8, 0)
    # print(p1)
    # print(p2)
    # ans = mul(p1, p2)
    # # assert mul(p1, p2) == from_bits(0b01110101, 8, 0)  ### only last bit wrong (checked against softposit python)
    # print(ans)

    # p1 = from_bits(0b0111000101100011, 16, 0)
    # p2 = from_bits(0b0100000101110001, 16, 0)
    # print(p1)
    # print(p2)
    # ans = mul(p1, p2)
    # print(ans)

    # p1 = from_bits(0b100110, 6, 0)
    # p2 = from_bits(0b110010, 6, 0)
    # print(p1)
    # print(p2)
    # ans = mul(p1, p2)
    # print(ans)

    # p1 = from_bits(0b01100011111011001, 17, 0)
    # p2 = from_bits(0b11111100010100011, 17, 0)
    # print(p1)
    # print(p2)
    # ans = mul(p1, p2)
    # print(ans)

    # p1 = from_bits(0b011111011100011111011001, 24, 0)
    # p2 = from_bits(0b111111100011100010100011, 24, 0)
    # print(p1)
    # print(p2)
    # ans = mul(p1, p2)
    # print(ans)

    # p1 = from_bits(0b001011, 6, 1)
    # p2 = from_bits(0b100111, 6, 1)
    # print(p1)
    # print(p2)
    # ans = mul(p1, p2)
    # print(ans)

    # p1 = from_bits(0b01110000011100001010001111010111, 32, 2)  # 312.3199996948242
    # p2 = from_bits(0b00101100110011001100110011001101, 32, 2)  # 0.20000000018626451
    # ans = mul(p1, p2)  # 62.46400022506714
    # assert ans == from_bits(0b01100111110011101101100100010111, 32, 2)

    # p1 = from_bits(0b0011101000111100, 16, 1)  # 0.81982421875
    # p2 = from_bits(0b0011000011100111, 16, 1)  # 0.5281982421875
    # print(p1)
    # print(p2)
    # # assert mul(p1, p2) == from_bits(0b0010101110110111, 16, 1)
    # ans = mul(p1, p2)
    # print(ans)

    # p1 = from_bits(0b00110001, 8, 0)  # 0.765625
    # p2 = from_bits(0b01100010, 8, 0)  # 2.25
    # print(p1)
    # print(p2)
    # # assert mul(p1, p2) == from_bits(0b01100010, 8, 0)  # 1.71875    # last bit fails
    # ans = mul(p1, p2)
    # print(ans)

    # p1 = from_bits(0b10110001, 8, 0)  # -1.46875
    # p2 = from_bits(0b01101010, 8, 0)  # 3.25
    # print(p1)
    # print(p2)
    # # assert mul(p1, p2) == from_bits(0b10001110, 8, 0) # -5.0
    # ans = mul(p1, p2)  #              10001111
    # print(ans)

    # p1 = from_bits(0b1001001100001100, 16, 1)  # 0x930c   # -12.953125
    # p2 = from_bits(0b0101010101010010, 16, 1)  # 0x5552   # 2.6650390625
    # print(p1)
    # print(p2)
    # # assert mul(p1, p2) == from_bits(0b1000101110101111, 16, 1)
    # ans = mul(p1, p2)
    # print(ans)
