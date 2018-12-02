from PIL import Image
import argparse
import os

def validate_image_path(input_string):
    if not os.path.isfile(input_string):
        msg = "The file doesn't exist: '{0}'.".format(input_string)
        raise IOError(msg)
    try:
        image = Image.open(input_string, 'r')
        image.close()
        return True
    except OSError:
        return False


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
        type=str,
        help='input image filename'
    )
    parser.add_argument(
        '--height', '-ih',
        type=int,
        help='required image height',
        default=None
    )
    parser.add_argument(
        '--width', '-w',
        type=int,
        help='required width',
        default=None
    )
    parser.add_argument(
        '--scale', '-s',
        type=float,
        help='required width',
        default=None
    )
    parser.add_argument(
        '--output', '-o',
        type=validate_directory,
        help='directory to record result image file',
        default=None
    )
    return parser.parse_args()


def calc_result_size(origin_size, result_size, scale):
    if scale is not None:
        if not result_size == (None, None):
            msg = "Both the scale and result image size are given."
            raise AttributeError(msg)
        calculated_size = [round(dim * scale) for dim in origin_size]
        proportion_changed = False
        return calculated_size, proportion_changed
    if result_size == (None, None):
        msg = "No information about result size is given."
        raise AttributeError(msg)
    origin_width, origin_height = origin_size
    origin_proportion = origin_width / origin_height
    result_width, result_height = result_size
    proportion_changed = False
    if result_width is None:
        calculated_scale = result_height / origin_height
        calculated_width = round(origin_width * calculated_scale)
        return (calculated_width, result_height), proportion_changed
    if result_height is None:
        calculated_scale = result_width / origin_width
        calculated_height = round(origin_height * calculated_scale)
        return (result_width, calculated_height), proportion_changed
    calculated_proportion = result_width / result_height
    if not origin_proportion == calculated_proportion:
        proportion_changed = True
    return result_size, proportion_changed


def get_output_path(path_to_original, calculated_size, path_to_result):
    calculated_width, calculated_height = calculated_size
    string_size = "_{0}x{1}".format(calculated_width, calculated_height)
    image_filename = os.path.basename(path_to_original)
    filename_array = os.path.splitext(image_filename)
    output_filename = string_size.join(filename_array)
    if path_to_result is not None:
        output_path = os.path.join(path_to_result, output_filename)
    else:
        output_path = os.path.join(
            os.path.dirname(path_to_original),
            output_filename
        )
    return output_path


def resize_image(path_to_original, path_to_result, result_size, scale):
    origin_image = Image.open(path_to_original)
    origin_size = origin_image.size
    calculated_size, proportion_changed = calc_result_size(
        origin_size,
        result_size,
        scale
    )
    result_image = origin_image.resize(calculated_size)
    origin_image.close()
    output_path = get_output_path(
        path_to_original,
        calculated_size,
        path_to_result,
    )
    result_image.save(output_path)
    return proportion_changed


if __name__ == '__main__':
    args = parse_arguments()
    if not validate_image_path(args.image_path):
        exit("Can't read an origin image")
    proportion_changed = resize_image(
        args.image_path,
        args.output,
        (args.width, args.height),
        args.scale
        )
    if proportion_changed:
        print("Warning: the image proportions are changed!")