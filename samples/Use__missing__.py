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

class MyDict(dict):
    def __missing__(self, key):
        message = f'{key} not present in the dictionary!'
        logging.warning(message)
        return message    # もしくは代わりに何かエラーを発行する


def main():
    logging.debug('')

if __name__ == "__main__":
    sys.exit(main())

#2345678901234567890123456789012345678901234567890123456789012345678901234567890
#--------+---------+---------+---------+---------X---------+---------+---------+
