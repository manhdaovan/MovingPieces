import os, sys
from random import randint
from PIL import Image
import math
import webbrowser
from datetime import datetime
from shutil import copytree

DEFAULT_VERTICAL_PIECES = 5
DEFAULT_HORIZONTAL_PIECES = 5

SAMPLE_PICTURES = ['funnypieces/samples/' + f
                   for f in os.listdir('funnypieces/samples')
                   if not f.startswith('.')]


def print_msg(msg="", type="error", display_help=None):
    if display_help:
        print ">>>", type.upper(), ":", msg, 'Please run "$python cmdi.py -h" for help.'
    else:
        print ">>>", type.upper(), ":", msg


def get_random_picture():
    return SAMPLE_PICTURES[randint(0, len(SAMPLE_PICTURES) - 1)]


def get_img(img_path):
    if os.path.exists(img_path):
        return Image.open(img_path)
    return False


def create_folder(folder_name):
    if not os.path.exists(folder_name):
        os.makedirs(folder_name)


def slice_base_img(img, vertical_pieces, horizontal_pieces):
    # Slice from horizontal first, then vertical (left to right, up to down)
    try:
        resource_folder = datetime.now().strftime("%Y%m%d%H%M%S")
        create_folder(resource_folder)
        img_folder = resource_folder + "/pieces"
        create_folder(img_folder)
        img_width, img_height = img.size
        print_msg(img_width, "img_size > width(px)")
        print_msg(img_height, "img_size > height(px)")

        left, upper, right, lower = 0, 0, 0, 0
        each_piece_height = int(math.ceil(img_height / vertical_pieces))
        each_piece_width = int(math.ceil(img_width / horizontal_pieces))
        count = 1
        for slice_h in range(horizontal_pieces):
            # Calculate left, upper, right, and lower of box to crop
            lower += each_piece_height
            for slice_v in range(vertical_pieces):
                if slice_v == 0:
                    left = 0
                    right = 0
                right += each_piece_width
                bbox = (left, upper, right, lower)
                working_slice = img.crop(bbox)
                left += each_piece_width
                #save the slice
                working_slice.save(os.path.join(img_folder, "slice_" + str(count) + ".png"), "png")
                count += 1
            upper += each_piece_height
        return img_folder, "done", each_piece_width, each_piece_height
    except Exception as e:
        print sys.exc_info()
        return False, e.message, False, False


def build_html_page(folder, vertical_pieces, horizontal_pieces, piece_width, piece_height):
    resource_folder = os.path.dirname(folder)
    running_folder = os.path.join(resource_folder, "templates")
    html_file = open(os.path.join(running_folder, "FunnyPieces.html"), "w")

    build_html_header(html_file, running_folder)
    build_html_page_content(html_file, vertical_pieces, horizontal_pieces, piece_width, piece_height)
    build_init_script(html_file, vertical_pieces)
    build_html_footer(html_file, running_folder)

    html_file.close()

    return 'file://' + os.path.abspath(os.path.join(running_folder, "FunnyPieces.html"))


def build_html_header(html_file, running_folder):
    with open(os.path.join(running_folder, "template_header.html"), "r") as header:
        for line in header:
            html_file.write(line)


def build_html_footer(html_file, running_folder):
    with open(os.path.join(running_folder, "template_footer.html"), "r") as footer:
        for line in footer:
            html_file.write(line)


def build_html_page_content(html_file, vertical_pieces, horizontal_pieces, piece_width, piece_height):
    piece_index = 0
    all_pieces = [0] * (vertical_pieces * horizontal_pieces)

    for k in range(0, vertical_pieces * horizontal_pieces):
        all_pieces[k] = k

    # Remove first piece (blank piece)
    all_pieces.remove(0)

    for i in range(0, vertical_pieces):
        row = '<div id="row_' + str(i) + '" class="row">'
        for j in range(0, horizontal_pieces):
            if piece_index == 0:
                row += '<div id="item_' \
                       + str(piece_index) \
                       + '" class="first_item" data-id="' \
                       + str(piece_index) \
                       + '">BLANK PIECE</div>'
            else:
                next_img = all_pieces[randint(0, len(all_pieces) - 1)]
                all_pieces.remove(next_img)
                row += '<div id="item_' + str(piece_index) \
                       + '" class="item" data-id="' \
                       + str(piece_index) \
                       + '"><img src="imgs/slice_' \
                       + str(next_img + 1) \
                       + '.png"></div>'
            piece_index += 1
        row += '</div>'
        html_file.write(row)


def build_init_script(html_file, vertical_pieces):
    script = '<script>$(function () {$(".item, .first_item").click(function () {chooseThis($(this));checkMove(' \
             + str(vertical_pieces) + ');});});</script>'
    html_file.write(script)


def open_html_page(html_page):
    if html_page:
        new = 2  # open in a new tab, if possible
        webbrowser.open(html_page, new=new)


def copy_resources_to(img_folder):
    try:
        resource_folder = os.path.dirname(img_folder)
        copytree(os.path.join("funnypieces/templates"), os.path.join(resource_folder, "templates"))
        copytree(img_folder, os.path.join(resource_folder, "templates/imgs"))
        print_msg(os.path.abspath(resource_folder), "resource_folder")
    except OSError as e:
        print('Directory not copied. Error: %s' % e)


def copy_sample_image_to(img, img_folder):
    try:
        resource_folder = os.path.dirname(img_folder)
        img.save(os.path.join(resource_folder, "templates/imgs/sample.png"), "png")
    except Exception as e:
        print('Directory not copied. Error: %s' % e)


def create_funny_pieces(img, vertical_pieces, horizontal_pieces):
    try:
        folder, result, piece_width, piece_height = slice_base_img(img, vertical_pieces, horizontal_pieces)
        if not result:
            print_msg(folder)
            return
        copy_resources_to(folder)
        copy_sample_image_to(img, folder)
        html_page = build_html_page(folder, vertical_pieces, horizontal_pieces, piece_width, piece_height)
        if html_page:
            open_html_page(html_page)
    except Exception as e:
        print_msg(e.message)
