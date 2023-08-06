from argparse import ArgumentParser


def get_output_flag(default_location):
    """ Get the output dir from the command line flag, if possible. """
    parser = ArgumentParser()
    parser.add_argument("--output", type=str, nargs=1, default=[default_location])
    args = parser.parse_args()
    return args.output[0]
