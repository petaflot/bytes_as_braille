#!/usr/bin/python

def binary_clock( format = "%Y-%m-%d %H:%M:%S", **kwargs ):
    from bytes_as_braille import bytes_as_braille
    from datetime import datetime

    timestr = datetime.now().strftime(format)
    res = ''
    for c in timestr:
        try:
            s = bytes_as_braille(int(c).to_bytes(1,'big'), encoding=None, **kwargs)
        except ValueError:
            s = c
        res += s

    print(res)

if __name__ == '__main__':
    binary_clock()
