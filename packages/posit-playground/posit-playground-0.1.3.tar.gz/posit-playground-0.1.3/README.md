<a href="https://github.com/urbanij/posit-playground/actions"><img src="https://github.com/urbanij/posit-playground/actions/workflows/main.yml/badge.svg"></a>
[![codecov](https://codecov.io/gh/urbanij/posit-playground/branch/main/graph/badge.svg?token=U37RUDDRN1)](https://codecov.io/gh/urbanij/posit-playground)
<!-- <a href="https://pypi.org/project/posit-playground/"><img src="https://img.shields.io/pypi/dm/posit-playground"></a> -->

# posit-playground

Goals:
- [x] output nice bit representations
- [x] build posit `from_double` and `from_bits`
- [ ] implement basic math operations
    - [ ] add/sub
    - [ ] mul
    - [ ] div


## Install

- stable

```sh
pip install posit-playground
```

<!-- - main

```sh
pip install git+https://github.com/urbanij/posit-playground.git
``` -->

## Usage

```python
from posit_playground import from_bits, from_double

p1 = from_bits(
    bits=0b000110111011101,
    size=16,
    es=3,
)

p2 = from_double(
    x=2.312,
    size=6,
    es=1,
)

p1 * p1 # implements posit multiplication
```

or better yet, launch a notebook on binder 

[![Binder](https://mybinder.org/badge_logo.svg)](https://mybinder.org/v2/gh/urbanij/posit-playground/HEAD?labpath=notebooks%2F1_posit_playground_demo.ipynb)

or visit [notebooks/1_posit_playground_demo.ipynb](https://github.com/urbanij/posit-playground/blob/main/notebooks/1_posit_playground_demo.ipynb)


## Changelog

See [CHANGELOG.md](changelog.md).

## Demo

<!-- [![asciicast](https://asciinema.org/a/455652.svg)](https://asciinema.org/a/455652) -->


Screenshot of posit-playground in action, with a corner case example in which the exponent is chopped off the bit fields

![Imgur](https://imgur.com/0M8USPC.jpg)

