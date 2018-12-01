#import pillow
import argparse
import os

def validate_image_path(input_string, extensions=('jpg', 'png')):
    if not os.path.isfile(input_string):
        msg = "File doesn't exist: '{0}'.".format(input_string)
        raise argparse.ArgumentError(msg)
    filename, extension = input_string.split('.')
    if not extension in extensions:
        msg = "File is not an jpg or png image: '{0}'.".format(input_string)
        raise argparse.ArgumentTypeError(msg)
    return input_string


def validate_directory(input_string):
    if not os.path.isdir(input_string):
        msg = "Input string is not an existing directory: '{0}'.".format(
            input_string
        )
        raise argparse.ArgumentError(msg)
    return input_string


def parse_arguments():
    parser = argparse.ArgumentParser(
        description='Resize input image with parameters.'
    )
    parser.add_argument(
        'image_path',
        type=validate_image_path,
        help='input image filename'
    )
    parser.add_argument(
        '--height', '-ih',
        type=int,
        help='required image height',
        default=0
    )
    parser.add_argument(
        '--width', '-w',
        type=int,
        help='required width',
        default=0
    )
    parser.add_argument(
        '--scale', '-s',
        type=float,
        help='required width',
        default=1
    )
    parser.add_argument(
        '--output', '-o',
        type=validate_directory,
        help='directory to record result image file',
        default=None
    )
    return parser.parse_args()


def resize_image(path_to_original, path_to_result):
    pass


if __name__ == '__main__':

    args = parse_arguments()
    print(args)
