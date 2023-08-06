# -*- encoding: utf-8 -*-
# vnu-validator v0.10.0
# Python Wrapper for the v.Nu HTML Validator
# Copyright © 2018, Shlomi Fish.
# See /LICENSE for licensing information.

"""
Main routine of vnu-validator.

:Copyright: © 2018, Shlomi Fish.
:License: BSD (see /LICENSE).
"""

__all__ = ('main',)


def main():
    """Main routine of vnu-validator."""
    print("Hello, world!")
    print("This is vnu-validator.")
    print("You should customize __main__.py to your liking (or delete it).")


if __name__ == '__main__':
    main()
"""
Entrypoint module, in case you use `python -mvnu_validator`.


Why does this file exist, and why __main__? For more info, read:

- https://www.python.org/dev/peps/pep-0338/
- https://docs.python.org/2/using/cmdline.html#cmdoption-m
- https://docs.python.org/3/using/cmdline.html#cmdoption-m
"""
from vnu_validator.cli import main

if __name__ == "__main__":
    main()
