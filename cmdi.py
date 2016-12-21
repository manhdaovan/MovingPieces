"""Command line interface to FunnyPieces"""

import sys, getopt
import funnypieces
from funnypieces import print_msg


def print_help(help_string=None):
    help_string = """
    Use command:
    $python path/to/cmdi.py [OPTIONS]
    With OPTIONS:
    -h --help  show help string
    -f         absolute path to input file
               If no file input, a random image from samples will be selected.
    Eg:
    $python somewhere/cmdi.py -h
    $python somewhere/cmdi.py -f /absolute/path/image_file.png
    Or with no param(s):
    $python somewhere/cmdi.py
    """ if not help_string else help_string
    print_msg(help_string, "help")
    sys.exit()


def main():
    try:
        opts, args = getopt.getopt(sys.argv[1:], "f:h", ["--file", "--help"])
    except:
        print_help()

    #Init default value
    img_path = funnypieces.get_random_picture()
    vertical_pieces = funnypieces.DEFAULT_VERTICAL_PIECES
    horizontal_pieces = funnypieces.DEFAULT_HORIZONTAL_PIECES

    #Get params value
    for opt, arg in opts:
        if opt in ("-h", "--help"):
            print_help()
        elif opt in ("-f", "--file"):
            img_path = arg

    print_msg(img_path, type='GET FILE')

    try:
        img_instance = funnypieces.get_img(img_path)
        if not img_instance:
            print_msg("File 404.")
            return
    except:
        print_msg("File 404.")
        sys.exit()

    funnypieces.create_funny_pieces(img_instance, vertical_pieces, horizontal_pieces)


if __name__ == '__main__':
    main()
