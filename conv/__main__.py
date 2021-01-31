#!/usr/bin/env python3
from argparse import ArgumentParser
import sys
import json
import ast

from . import conv, Language


def detect_language(s: str) -> Language:
    # json?
    try:
        json.loads(s)
        return Language.Json
    except Exception:
        pass

    # python?
    try:
        ast.literal_eval(s)
        return Language.Python
    except Exception:
        pass

    print(f"ERROR: Could not detect language", file=sys.stderr)
    exit(1)


def get_parser():
    parser = ArgumentParser()

    language_choices = [lang.value for lang in Language]
    parser.add_argument("from_language", choices=language_choices, nargs="?")
    parser.add_argument("to_language", choices=language_choices, nargs="?")
    parser.add_argument("--indent", type=int, default=4)
    parser.add_argument("--compact", action="store_true")
    parser.add_argument(
        "-f", "--file",
        help="read from file instead of stdin",
        dest="filename",
    )
    parser.add_argument(
        "-o",
        "-O",  # The user probably means "-o"
        "--output-file",
        help="write to file instead of stdout",
        dest="output_filename",
    )
    return parser



def main():
    args = get_parser().parse_args()

    if args.filename:
        with open(args.filename) as f:
            input_string = f.read()
    else:
        input_string = input()

    if args.from_language is None and args.to_language is None:
        from_language, to_language = Language.Json, Language.Python
    elif args.to_language is None:
        from_language = detect_language(input_string)
        to_language = Language(args.from_language)
    else:
        from_language = Language(args.from_language)
        to_language = Language(args.to_language)

    output_string = conv(
        input_string,
        from_language=from_language,
        to_language=to_language,
        indent=None if args.compact else args.indent,
    )

    if args.output_filename:
        with open(args.output_filename, "w") as f:
            f.write(output_string)
        print(f"Wrote to file {args.output_filename}")
    else:
        print(output_string)


if __name__ == "__main__":
    main()
