#!/usr/bin/env python3
# -*- mode:python; coding: utf-8 -*-
#
# 
#
#2345678901234567890123456789012345678901234567890123456789012345678901234567890
#--------+---------+---------+---------+---------X---------+---------+---------+
import sys

class Circle:
    def __init__(self, x, y, radius):
        self.x = x
        self.y = y
        self.radius = radius

    def __repr__(self):
        return f'Rectangle({self.x}, {self.y}, {self.radius})'

def main():
    c = Circle(100, 80, 30)
    repr(c)

if __name__ == "__main__":
    sys.exit(main())

#2345678901234567890123456789012345678901234567890123456789012345678901234567890
#--------+---------+---------+---------+---------X---------+---------+---------+
