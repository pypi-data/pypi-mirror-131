import argparse

from hmin import __version__
from hmin._plot import hmin_plot
from hmin._predict import hmin_predict


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--version", "-v", action="version", version="%(prog)s {}".format(__version__))
    parser.set_defaults(func=lambda x: parser.print_usage())
    subparsers = parser.add_subparsers()

    # predict
    subparser_predict = subparsers.add_parser("predict")
    subparser_predict.add_argument("--file_path", "-f", required=True, help="excel fiel path")
    subparser_predict.add_argument("--number_col", "-n", required=True)
    subparser_predict.add_argument("--threshold", "-t", required=True)
    subparser_predict.set_defaults(func=hmin_predict)

    # plot dendogram
    subparser_plot = subparsers.add_parser("plot")
    subparser_plot.add_argument("--file_path", "-f", required=True, help="excel fiel path")
    subparser_plot.add_argument("--number_col", "-n", required=True)
    subparser_plot.set_defaults(func=hmin_plot)

    args = parser.parse_args()

    func = args.func

    func(args)
