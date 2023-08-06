#! /usr/bin/env python3

import argparse
from startcp import functions, printer



def main():

    parser = argparse.ArgumentParser(
        description="A CLI for automating coding competition setup for codechef codeforces."
    )

    parser.add_argument(
        "-u",
        "--url",
        default=False,
        help="Takes Competition URL As a Parameter for Parsing",
        action="store_true"
    )

    parser.add_argument(
        "-g",
        "--generate",
        default=False,
        help="Generate startcp_config file",
        action="store_true"
    )

    args = parser.parse_args()
    functions.run(args)


if __name__ == '__main__':
    main()
