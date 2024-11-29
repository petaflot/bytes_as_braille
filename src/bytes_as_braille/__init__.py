# vim: ts=4 number et

from sys import stderr
try:
    from truecolor import fore_text, bold, COLORS
    print("Using truecolor", file=stderr)
except (ImportError, RuntimeError) as e:
    if str(e) == "Not a true color terminal":
        try:
            import termcolor
            print("Not a true color terminal... using 'termcolor'", file=stderr)
            def fore_text(txt, color=None):
                """
                    wrapper TODO color
                """
                return termcolor.colored(txt)
            def bold(txt):
                """
                    TODO bold text
                """
                return txt
        except ImportError:
            def fore_text(txt, color=None):
                """
                    wrapper TODO color
                """
                return txt
            def bold(txt):
                """
                    TODO bold text
                """
                return txt
            print("No colors will be used", file=stderr)
        
from bytes_as_braille.palettes import PALETTES
from os import get_terminal_size

DEFAULT = False
INTEGER = True
BRAILLE = None


def to_braille(bytestr, encoding = 'utf-8', byteorder = 'big', 
        show_ascii = False,
        colorblind = False,
        rainbow = True,
        colors = None,
    ):
    """ tries to decode a bytestring in the preferred encoding ; if it doesn't, use Braille symbols 

        inspired from https://github.com/sharkdp/hexyl, it is also possible to color bytes

        arguments:
            bytestring: some bytes
            encoding: try decoding the bytes first (default: 'utf-8') ; can be None to skip decoding
            byteorder: as the name suggests ('big'/'little')
            show_ascii: show ascii-printable when possible (no dots)
            colorblind: disable color output
            rainbow: set hue based on byte value ; if False, only color with colors dict
            colors: a dict that specifies how to color each byte, ie. {0xff: ('red', ('bold', ), }
    """
    # ordered, low values first (LSB if bottom-right, MSB is top-left, in columns)
    bytes_as_braille = {
        0x00: '⠀', 0x01: '⢀', 0x02: '⠠', 0x03: '⢠', 0x04: '⠐', 0x05: '⢐', 0x06: '⠰', 0x07: '⢰', 0x08: '⠈', 0x09: '⢈', 0x0a: '⠨', 0x0b: '⢨', 0x0c: '⠘', 0x0d: '⢘', 0x0e: '⠸', 0x0f: '⢸',
        0x10: '⡀', 0x11: '⣀', 0x12: '⡠', 0x13: '⣠', 0x14: '⡐', 0x15: '⣐', 0x16: '⡰', 0x17: '⣰', 0x18: '⡈', 0x19: '⣈', 0x1a: '⡨', 0x1b: '⣨', 0x1c: '⡘', 0x1d: '⡸', 0x1e: '⣘', 0x1f: '⣸',
        0x20: '⠄', 0x21: '⢄', 0x22: '⠤', 0x23: '⢤', 0x24: '⠔', 0x25: '⢔', 0x26: '⠴', 0x27: '⢴', 0x28: '⠌', 0x29: '⢌', 0x2a: '⠬', 0x2b: '⢬', 0x2c: '⠜', 0x2d: '⢜', 0x2e: '⠼', 0x2f: '⢼',
        0x30: '⡄', 0x31: '⣄', 0x32: '⡤', 0x33: '⣤', 0x34: '⡔', 0x35: '⣔', 0x36: '⡴', 0x37: '⣴', 0x38: '⡌', 0x39: '⣌', 0x3a: '⡬', 0x3b: '⣬', 0x3c: '⡜', 0x3d: '⣜', 0x3e: '⡼', 0x3f: '⣼',
        0x40: '⠂', 0x41: '⢂', 0x42: '⠢', 0x43: '⢢', 0x44: '⠒', 0x45: '⢒', 0x46: '⠲', 0x47: '⢲', 0x48: '⠊', 0x49: '⢊', 0x4a: '⠪', 0x4b: '⢪', 0x4c: '⠚', 0x4d: '⢚', 0x4e: '⠺', 0x4f: '⢺',
        0x50: '⡂', 0x51: '⣂', 0x52: '⡢', 0x53: '⣢', 0x54: '⡒', 0x55: '⣒', 0x56: '⡲', 0x57: '⣲', 0x58: '⡊', 0x59: '⣊', 0x5a: '⡪', 0x5b: '⣪', 0x5c: '⡚', 0x5d: '⣚', 0x5e: '⡺', 0x5f: '⣺',
        0x60: '⠆', 0x61: '⢆', 0x62: '⠦', 0x63: '⢦', 0x64: '⠖', 0x65: '⢖', 0x66: '⠶', 0x67: '⢶', 0x68: '⠎', 0x69: '⢎', 0x6a: '⠮', 0x6b: '⢮', 0x6c: '⠞', 0x6d: '⢞', 0x6e: '⠾', 0x6f: '⢾',
        0x70: '⡆', 0x71: '⣆', 0x72: '⡦', 0x73: '⣦', 0x74: '⡖', 0x75: '⣖', 0x76: '⡶', 0x77: '⣶', 0x78: '⡎', 0x79: '⣎', 0x7a: '⡮', 0x7b: '⣮', 0x7c: '⡞', 0x7d: '⣞', 0x7e: '⡾', 0x7f: '⣾',
        0x80: '⠁', 0x81: '⢁', 0x82: '⠡', 0x83: '⢡', 0x84: '⠑', 0x85: '⢑', 0x86: '⠱', 0x87: '⠉', 0x88: '⢉', 0x89: '⠩', 0x8a: '⢩', 0x8b: '⠙', 0x8c: '⢙', 0x8d: '⠹', 0x8e: '⢱', 0x8f: '⢹',
        0x90: '⡁', 0x91: '⣁', 0x92: '⡡', 0x93: '⣡', 0x94: '⡑', 0x95: '⣑', 0x96: '⡱', 0x97: '⣱', 0x98: '⡉', 0x99: '⣉', 0x9a: '⡩', 0x9b: '⣩', 0x9c: '⡙', 0x9d: '⣙', 0x9e: '⡹', 0x9f: '⣹',
        0xa0: '⠅', 0xa1: '⢅', 0xa2: '⠥', 0xa3: '⢥', 0xa4: '⠕', 0xa5: '⢕', 0xa6: '⠵', 0xa7: '⢵', 0xa8: '⠍', 0xa9: '⢍', 0xaa: '⠭', 0xab: '⢭', 0xac: '⠝', 0xad: '⢝', 0xae: '⠽', 0xaf: '⢽',
        0xb0: '⡅', 0xb1: '⣅', 0xb2: '⡥', 0xb3: '⣥', 0xb4: '⡕', 0xb5: '⣕', 0xb6: '⡵', 0xb7: '⣵', 0xb8: '⡍', 0xb9: '⣍', 0xba: '⡭', 0xbb: '⣭', 0xbc: '⡝', 0xbd: '⣝', 0xbe: '⡽', 0xbf: '⣽',
        0xc0: '⠃', 0xc1: '⢃', 0xc2: '⠣', 0xc3: '⢣', 0xc4: '⠓', 0xc5: '⢓', 0xc6: '⠳', 0xc7: '⢳', 0xc8: '⠋', 0xc9: '⢋', 0xca: '⠫', 0xcb: '⢫', 0xcc: '⠛', 0xcd: '⢛', 0xce: '⠻', 0xcf: '⢻',
        0xd0: '⡃', 0xd1: '⣃', 0xd2: '⡣', 0xd3: '⣣', 0xd4: '⡓', 0xd5: '⣓', 0xd6: '⡳', 0xd7: '⣳', 0xd8: '⡋', 0xd9: '⣋', 0xda: '⡫', 0xdb: '⣫', 0xdc: '⡛', 0xdd: '⣛', 0xde: '⡻', 0xdf: '⣻',
        0xe0: '⠇', 0xe1: '⢇', 0xe2: '⠧', 0xe3: '⢧', 0xe4: '⠗', 0xe5: '⢗', 0xe6: '⠷', 0xe7: '⢷', 0xe8: '⠏', 0xe9: '⢏', 0xea: '⠯', 0xeb: '⢯', 0xec: '⠟', 0xed: '⢟', 0xee: '⠿', 0xef: '⢿',
        0xf0: '⡇', 0xf1: '⣇', 0xf2: '⡧', 0xf3: '⣧', 0xf4: '⡗', 0xf5: '⣗', 0xf6: '⡷', 0xf7: '⣷', 0xf8: '⡏', 0xf9: '⣏', 0xfa: '⡯', 0xfb: '⣯', 0xfc: '⡟', 0xfd: '⣟', 0xfe: '⡿', 0xff: '⣿',
    }

    def color(b):
        try:
            if show_ascii and ( b >= 32 and b<= 126):
                try:
                    if 'bold' in colors[b][1]:
                        return fore_text( chr(b), bold(COLORS[colors[b][0]]) )
                    else:
                        raise IndexError
                except IndexError:
                    return fore_text( chr(b), COLORS[colors[b][0]] )
                except (KeyError, TypeError):
                    return chr(b)
                except NameError:
                    return bytes_as_braille[b]
            else:
                try:
                    return fore_text( bytes_as_braille[b], COLORS[colors[b][0]] )
                except (KeyError, TypeError):
                    if not rainbow:
                        return bytes_as_braille[b]
                    else:
                        from colorsys import hsv_to_rgb
                        return fore_text( bytes_as_braille[b], [int(v*255) for v in hsv_to_rgb( b/255, 1, 1)] )
                except ModuleNotFoundError:
                    return fore_text( bytes_as_braille[b], COLORS[None] )
                except NameError:
                    return bytes_as_braille[b]

        except ModuleNotFoundError:
            from termcolor import colored
            try:
                if show_ascii and ( b >= 32 and b<= 126):
                    return colored( chr(b), *colors[b] )
                else:
                    return colored( bytes_as_braille[b], *colors[b] )
            except KeyError:
                return bytes_as_braille[b]

    try:
        try:
            # TODO use wrapper, see lines 2-15
            #from truecolor import fore_text, bold
            if 'bold' in colors[None][1]:
                return fore_text(bytestr.decode(encoding), bold(COLORS[colors[None][0]]) )
            else:
                return fore_text(bytestr.decode(encoding), COLORS[colors[None][0]] )
        except (ModuleNotFoundError, TypeError, NameError):
            #try:
            #    from termcolor import colored
            #    return colred(bytestr.decode(encoding), *colors[None] )
            #except ModuleNotFoundError:
            return bytestr.decode(encoding)
        except RuntimeError as e:
            if str(e) == "Not a true color terminal":
                pass
    except AttributeError:
        if bytestr is None:
            return None
        else:
            raise
    except (UnicodeDecodeError, TypeError):
        #raise
        if byteorder == 'big':
            if colorblind:
                return( ''.join([bytes_as_braille[b] for b in bytestr]) )
            else:
                return( ''.join([color(b) for b in bytestr]) )
        elif byteorder == 'little':
            if colorblind:
                return( ''.join([bytes_as_braille[255-b] for b in bytestr[::-1]]) )
            else:
                return( ''.join([color(255-b) for b in bytestr[::-1]]) )
        else:
            raise Exception("InvalidValueForByteOrder")

def bprint(*args, **kwargs):
    tba = {}
    for arg in ('encoding', 'byteorder', 'show_ascii', 'rainbow', 'colors', 'colorblind'):
        a = kwargs.pop(arg,None)
        if a:
            tba[arg] = a
    print( to_braille(*args, **tba), **kwargs)


def from_braille(braillestr, byteorder = 'big', encoding = 'utf-8'):
    """ converts braille-bytes back to bytes """
    # ordered, low values first (LSB if bottom-right, MSB is top-left, in columns)
    # makes more sense when BYTEORDER is set to 'big'
    braille_as_bytes = {
        '⠀': b'\x00', '⢀': b'\x01', '⠠': b'\x02', '⢠': b'\x03', '⠐': b'\x04', '⢐': b'\x05', '⠰': b'\x06', '⢰': b'\x07', '⠈': b'\x08', '⢈': b'\x09', '⠨': b'\x0a', '⢨': b'\x0b', '⠘': b'\x0c', '⢘': b'\x0d', '⠸': b'\x0e', '⢸': b'\x0f',
        '⡀': b'\x10', '⣀': b'\x11', '⡠': b'\x12', '⣠': b'\x13', '⡐': b'\x14', '⣐': b'\x15', '⡰': b'\x16', '⣰': b'\x17', '⡈': b'\x18', '⣈': b'\x19', '⡨': b'\x1a', '⣨': b'\x1b', '⡘': b'\x1c', '⡸': b'\x1d', '⣘': b'\x1e', '⣸': b'\x1f',
        '⠄': b'\x20', '⢄': b'\x21', '⠤': b'\x22', '⢤': b'\x23', '⠔': b'\x24', '⢔': b'\x25', '⠴': b'\x26', '⢴': b'\x27', '⠌': b'\x28', '⢌': b'\x29', '⠬': b'\x2a', '⢬': b'\x2b', '⠜': b'\x2c', '⢜': b'\x2d', '⠼': b'\x2e', '⢼': b'\x2f',
        '⡄': b'\x30', '⣄': b'\x31', '⡤': b'\x32', '⣤': b'\x33', '⡔': b'\x34', '⣔': b'\x35', '⡴': b'\x36', '⣴': b'\x37', '⡌': b'\x38', '⣌': b'\x39', '⡬': b'\x3a', '⣬': b'\x3b', '⡜': b'\x3c', '⣜': b'\x3d', '⡼': b'\x3e', '⣼': b'\x3f',
        '⠂': b'\x40', '⢂': b'\x41', '⠢': b'\x42', '⢢': b'\x43', '⠒': b'\x44', '⢒': b'\x45', '⠲': b'\x46', '⢲': b'\x47', '⠊': b'\x48', '⢊': b'\x49', '⠪': b'\x4a', '⢪': b'\x4b', '⠚': b'\x4c', '⢚': b'\x4d', '⠺': b'\x4e', '⢺': b'\x4f',
        '⡂': b'\x50', '⣂': b'\x51', '⡢': b'\x52', '⣢': b'\x53', '⡒': b'\x54', '⣒': b'\x55', '⡲': b'\x56', '⣲': b'\x57', '⡊': b'\x58', '⣊': b'\x59', '⡪': b'\x5a', '⣪': b'\x5b', '⡚': b'\x5c', '⣚': b'\x5d', '⡺': b'\x5e', '⣺': b'\x5f',
        '⠆': b'\x60', '⢆': b'\x61', '⠦': b'\x62', '⢦': b'\x63', '⠖': b'\x64', '⢖': b'\x65', '⠶': b'\x66', '⢶': b'\x67', '⠎': b'\x68', '⢎': b'\x69', '⠮': b'\x6a', '⢮': b'\x6b', '⠞': b'\x6c', '⢞': b'\x6d', '⠾': b'\x6e', '⢾': b'\x6f',
        '⡆': b'\x70', '⣆': b'\x71', '⡦': b'\x72', '⣦': b'\x73', '⡖': b'\x74', '⣖': b'\x75', '⡶': b'\x76', '⣶': b'\x77', '⡎': b'\x78', '⣎': b'\x79', '⡮': b'\x7a', '⣮': b'\x7b', '⡞': b'\x7c', '⣞': b'\x7d', '⡾': b'\x7e', '⣾': b'\x7f',
        '⠁': b'\x80', '⢁': b'\x81', '⠡': b'\x82', '⢡': b'\x83', '⠑': b'\x84', '⢑': b'\x85', '⠱': b'\x86', '⠉': b'\x87', '⢉': b'\x88', '⠩': b'\x89', '⢩': b'\x8a', '⠙': b'\x8b', '⢙': b'\x8c', '⠹': b'\x8d', '⢱': b'\x8e', '⢹': b'\x8f',
        '⡁': b'\x90', '⣁': b'\x91', '⡡': b'\x92', '⣡': b'\x93', '⡑': b'\x94', '⣑': b'\x95', '⡱': b'\x96', '⣱': b'\x97', '⡉': b'\x98', '⣉': b'\x99', '⡩': b'\x9a', '⣩': b'\x9b', '⡙': b'\x9c', '⣙': b'\x9d', '⡹': b'\x9e', '⣹': b'\x9f',
        '⠅': b'\xa0', '⢅': b'\xa1', '⠥': b'\xa2', '⢥': b'\xa3', '⠕': b'\xa4', '⢕': b'\xa5', '⠵': b'\xa6', '⢵': b'\xa7', '⠍': b'\xa8', '⢍': b'\xa9', '⠭': b'\xaa', '⢭': b'\xab', '⠝': b'\xac', '⢝': b'\xad', '⠽': b'\xae', '⢽': b'\xaf',
        '⡅': b'\xb0', '⣅': b'\xb1', '⡥': b'\xb2', '⣥': b'\xb3', '⡕': b'\xb4', '⣕': b'\xb5', '⡵': b'\xb6', '⣵': b'\xb7', '⡍': b'\xb8', '⣍': b'\xb9', '⡭': b'\xba', '⣭': b'\xbb', '⡝': b'\xbc', '⣝': b'\xbd', '⡽': b'\xbe', '⣽': b'\xbf',
        '⠃': b'\xc0', '⢃': b'\xc1', '⠣': b'\xc2', '⢣': b'\xc3', '⠓': b'\xc4', '⢓': b'\xc5', '⠳': b'\xc6', '⢳': b'\xc7', '⠋': b'\xc8', '⢋': b'\xc9', '⠫': b'\xca', '⢫': b'\xcb', '⠛': b'\xcc', '⢛': b'\xcd', '⠻': b'\xce', '⢻': b'\xcf',
        '⡃': b'\xd0', '⣃': b'\xd1', '⡣': b'\xd2', '⣣': b'\xd3', '⡓': b'\xd4', '⣓': b'\xd5', '⡳': b'\xd6', '⣳': b'\xd7', '⡋': b'\xd8', '⣋': b'\xd9', '⡫': b'\xda', '⣫': b'\xdb', '⡛': b'\xdc', '⣛': b'\xdd', '⡻': b'\xde', '⣻': b'\xdf',
        '⠇': b'\xe0', '⢇': b'\xe1', '⠧': b'\xe2', '⢧': b'\xe3', '⠗': b'\xe4', '⢗': b'\xe5', '⠷': b'\xe6', '⢷': b'\xe7', '⠏': b'\xe8', '⢏': b'\xe9', '⠯': b'\xea', '⢯': b'\xeb', '⠟': b'\xec', '⢟': b'\xed', '⠿': b'\xee', '⢿': b'\xef',
        '⡇': b'\xf0', '⣇': b'\xf1', '⡧': b'\xf2', '⣧': b'\xf3', '⡗': b'\xf4', '⣗': b'\xf5', '⡷': b'\xf6', '⣷': b'\xf7', '⡏': b'\xf8', '⣏': b'\xf9', '⡯': b'\xfa', '⣯': b'\xfb', '⡟': b'\xfc', '⣟': b'\xfd', '⡿': b'\xfe', '⣿': b'\xff',
    }
    def trans(c):
        try:
            return braille_as_bytes[c]
        except KeyError:
            return bytes(c,encoding)

    if byteorder == 'big':
        return b''.join([trans(b) for b in braillestr])
    elif byteorder == 'little':
        return ''.join([braille_as_bytes[255-b] for b in braillestr])
    else:
        raise Exception("InvalidValueForByteOrder")

def input(
        prompt = None,
        byteorder = 'big',
        encoding = 'utf-8',
        palette = PALETTES['white_on_grey'],
        mode = DEFAULT, UID_MAX_LENGTH = 64
    ):
    """
    interactive input function that automatically converts ints to bytes if possible. _always_ return an encoded string.

    for async version, use ainput()

    INABIAF: control characaters may be "hidden" in multibyte characters and interfere with the expected operation ;
        to input bytes on purpose, prefer HEX notation

    :parameters:
        mode:
            DEFAULT:  normal mode (try to convert automatically, Braille symbols treated as byte values)
            INTEGER:  integer input mode (don't try to convert integer to bytes, return string as-is*)
            BRAILLE:  Braille input mode (don't treat Braille characters as bytes but as UTF symbols)
    """
    from readchar import readkey

    def conv(s):
        if mode is False:   # default
            try:
                b = (int(s,0)).to_bytes(len(s), byteorder=byteorder).lstrip(b'\x00')
            except (ValueError, OverflowError):
                b = from_braille(s)
            #except OverflowError:   # can't convert negative int to unsigned

        elif mode is True:  # INTEGER
            b = bytes(s, 'utf-8')

        elif mode is None:  # BRAILLE
            try:
                b = (int(s,0)).to_bytes(len(s), byteorder=byteorder).lstrip(b'\x00')
            except ValueError:
                b = bytes(s, 'utf-8')

        return b, len(b)


    if type(prompt) is str:
        prompt = ( prompt ,'>⠊> ','>⠃> ')
    elif prompt is None:
        prompt = ('>⠝> ','>⠊> ','>⠃> ')
    p = { DEFAULT: prompt[0], INTEGER: prompt[1], BRAILLE: prompt[2], }

    text = ''
    disp = ''


    while True:
        print('\r',(get_terminal_size().columns-1)*' ', end='\r')    # arbitrary-sized padding to erase excess text, TODO deserves improvement TODO

        b, l = conv(text)
        disp = to_braille(b, show_ascii = True, rainbow = False, colors = palette)
        print(f"{p[mode]}{fore_text(disp)}", end='', flush=True)
        match readkey():
            case x if x in ('\n','\r'):
                #print('\r'+' '*(l+len(prompt)), end='\r\n')
                print('')
                return b if len(b) else None
            case '\x04':
                print("\ninput mode: [s]td, [i]nt, [b]raille ; [enter] inserts EOL ; [d] inserts EOF ; [r]esets input ; ctrl+D again raises EOF")
                match readkey():
                    case 's':
                        mode = DEFAULT
                    case 'i':
                        mode = INTEGER
                    case 'b':
                        mode = BRAILLE
                    case '\n':
                        text += '\n'
                    case 'r':
                        text = ''
                    case 'd':
                        text += '\x04'
                    case '\x04':
                        raise EOFError

            case '\x7f':    # not sure which key '\x7f' is? thought it was backspace
                text = text[:-1]
            case '\x08':    # backspace
                text = text[:-1]
            case '\x1b[A':  # up
                text += '↑'
            case '\x1b[B':  # down
                text += '↓'
            case '\x1b[C':  # right
                text += '→'
            case '\x1b[D':  # left
                text += '←'
            case '\x1b[H':  # home
                text += '↤'
            case '\x1b[F':  # end
                text =+ '↦'
            case '\x1b[5~': # page up
                text += '↥'
            case '\x1b[6~': # page down
                text += '↧'
            case k if k:
                text += k

async def ainput(
        prompt = None,
        byteorder = 'big',
        encoding = 'utf-8',
        palette = PALETTES['white_on_grey'],
        mode = DEFAULT, UID_MAX_LENGTH = 64
    ):
    """
        same as input() above, only async
    """
    #from bytes_as_braille.read_key_async import read_key
    from aioconsole import ainput as read_key

    def conv(s):
        if mode is False:   # default
            try:
                b = (int(s,0)).to_bytes(len(s), byteorder=byteorder).lstrip(b'\x00')
            except (ValueError, OverflowError):
                b = from_braille(s)
            #except OverflowError:   # can't convert negative int to unsigned

        elif mode is True:  # INTEGER
            b = bytes(s, 'utf-8')

        elif mode is None:  # BRAILLE
            try:
                b = (int(s,0)).to_bytes(len(s), byteorder=byteorder).lstrip(b'\x00')
            except ValueError:
                b = bytes(s, 'utf-8')

        return b, len(b)


    if type(prompt) is str:
        prompt = ( prompt ,'>⠊> ','>⠃> ')
    elif prompt is None:
        prompt = ('>⠝> ','>⠊> ','>⠃> ')
    p = { DEFAULT: prompt[0], INTEGER: prompt[1], BRAILLE: prompt[2], }

    text = ''
    disp = ''


    while True:
        print('\r',(get_terminal_size().columns-1)*' ', end='\r')    # arbitrary-sized padding to erase excess text, TODO deserves improvement TODO

        b, l = conv(text)
        disp = to_braille(b, show_ascii = True, rainbow = False, colors = palette)
        print(f"{p[mode]}{fore_text(disp)}", end='', flush=True)
        match await read_key():
            case x if x in ('\n','\r'):
                #print('\r'+' '*(l+len(prompt)), end='\r\n')
                print('')
                return b if len(b) else None
            case '\x04':
                print("\ninput mode: [s]td, [i]nt, [b]raille ; [enter] inserts EOL ; [d] inserts EOF ; [r]esets input ; ctrl+D again raises EOF")
                match await read_key():
                    case 's':
                        mode = DEFAULT
                    case 'i':
                        mode = INTEGER
                    case 'b':
                        mode = BRAILLE
                    case '\n':
                        text += '\n'
                    case 'r':
                        text = ''
                    case 'd':
                        text += '\x04'
                    case '\x04':
                        raise EOFError

            case '\x7f':    # not sure which key '\x7f' is? thought it was backspace
                text = text[:-1]
            case '\x08':    # backspace
                text = text[:-1]
            case '\x1b[A':  # up
                text += '↑'
            case '\x1b[B':  # down
                text += '↓'
            case '\x1b[C':  # right
                text += '→'
            case '\x1b[D':  # left
                text += '←'
            case '\x1b[H':  # home
                text += '↤'
            case '\x1b[F':  # end
                text =+ '↦'
            case '\x1b[5~': # page up
                text += '↥'
            case '\x1b[6~': # page down
                text += '↧'
            case k if k:
                text += k
