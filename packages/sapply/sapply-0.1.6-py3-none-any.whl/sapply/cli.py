from sapply.cmapdefs import cmapdefs
from sapply.charmap import read_charmap
from sapply.flip import flip
from sapply.zalgo import zalgo
from sapply.morse import to_morse
import pathlib
from signal import signal, SIGPIPE, SIG_DFL
import sys
import site

signal(SIGPIPE, SIG_DFL)

MAJOR, MINOR, PATCH = '0', '1', '0'

def convert(char_map, text):
    out = ""
    for char in text:
        if char in char_map:
            out += char_map[char]
        elif char.lower() in char_map:
            out += char_map[char.lower()]
        else:
            out += char
    return out

def strikethrough(text, strikeover):
    return ''.join([char + strikeover for char in text])

def optmatch(cmd, short, long=''):
    if (long == ''):
        return (cmd == short)
    else:
        return (cmd == short or cmd == long)

def mapto(cmap: str):
    file = cmapdefs[cmap]
    root    = pathlib.Path(f'{site.getsitepackages()}/sapply')
    local   = pathlib.Path(f'{site.getusersitepackages()}/sapply')
    path = ''
    if (root.is_dir()):
        path = pathlib.Path(f'{root}/resources/{file}').expanduser()
    else:
        path = pathlib.Path(f'{local}/resources/{file}').expanduser()
    return (read_charmap(path))

def main():
    cmds = ['flip', 'zalgo', 'morse']

    subcmd = None
    text = None
    effects = None

    for cmd in cmds:
        if cmd in sys.argv:
            subcmd = cmd

    if subcmd is None:
        text = sys.argv[1]
        effects = sys.argv[2:]
    else:
        text    = sys.argv[2]
        effects = sys.argv[3:]

    if not text:
        sys.exit()

    # Subcommands
    # Add subargs for each of these commands
    # Pass args parameter and parse commands in each function
    if (subcmd == 'flip'):
        flip(text)
    if (subcmd == 'zalgo'):
        zalgo(text)
    if (subcmd == 'morse'):
        print(to_morse(text.upper()))
    if (subcmd is not None):
        return

    # Main
    out = ""
    if(len(effects) < 2):
        cmd = effects[0]
        match cmd:
            case '--sub'                        : out = convert(mapto('subscript'), text)
            case '--super'                      : out = convert(mapto('superscript'), text)
            case '-ds'      | '--doublestruck'  : out = convert(mapto('doubleStruck'), text)
            case '-oe'      | '--oldeng'        : out = convert(mapto('oldEnglish'), text)
            case '-med'     | '--medieval'      : out = convert(mapto('medieval'), text)
            case '-mono'    | '--monospace'     : out = convert(mapto('monospace'), text)
            case '-b'       | '--bold'          : out = convert(mapto('bold'), text)
            case '-i'       | '--italics'       : out = convert(mapto('italic'), text)
    elif(len(effects) < 3):
        cmd = effects[0]
        opt = effects[1]
        # Handle combinable effects
        match cmd, opt:
            case '--cmap', None:
                opt = effects[1]
                cmap = read_charmap(opt)
                out = convert(cmap, text)
            case '-b'  | '--bold'   , '-s'  | '--sans'  : out = convert(mapto('boldSans'), text)
            case '-i'  | '--italics', '-b'  | '--bold'  : out = convert(mapto('boldItalic'), text)
            case '-i'  | '--italics', '-s'  | '--sans'  : out = convert(mapto('italicSans'), text)
            case '-st' | '--strike' , '-'               : out = strikethrough(text, u'\u0336')
            case '-st' | '--strike' , '~'               : out = strikethrough(text, u'\u0334')
    print(out)
