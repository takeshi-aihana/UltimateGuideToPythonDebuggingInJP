#!/usr/bin/env python3
# -*- mode:python; coding: utf-8 -*-
#
# 
#
#2345678901234567890123456789012345678901234567890123456789012345678901234567890
#--------+---------+---------+---------+---------X---------+---------+---------+

import sys
import logging
# logging.disable(logging.DEBUG)
logging.basicConfig(level=logging.DEBUG,
                    format=' %(asctime)s - %(levelname)s - %(message)s')

import traceback
import sys

def func():
    try:
        raise SomeError('Something went wrong...')
    except:
        traceback.print_exc(file=sys.stderr)

def main():
    logging.debug('')
    func()

if __name__ == "__main__":
    sys.exit(main())

#2345678901234567890123456789012345678901234567890123456789012345678901234567890
#--------+---------+---------+---------+---------X---------+---------+---------+
