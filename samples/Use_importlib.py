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

def func():
    print('This is result')
    #print('New result...')

def main():
    logging.debug('')

if __name__ == "__main__":
    sys.exit(main())

#2345678901234567890123456789012345678901234567890123456789012345678901234567890
#--------+---------+---------+---------+---------X---------+---------+---------+
