#!/usr/bin/env python3
from argparse import ArgumentParser
from enum import Enum
import ast
import sys
import json
from typing import Dict, List, Optional, Union


class Language(Enum):
    Json = "json"
    Python = "python"


def raise_if_not_valid_for_language(s: str, language: Language) -> None:
    if language is Language.Json:
        json.loads(s)
    elif language is Language.Python:
        json.dumps(s)
    else:
        raise Exception(f"Programmer error: unhandled language {language}")


def load_json(s: str) -> Union[Dict, List]:
    try:
        return json.loads(s)
    except Exception as e:
        print(f"ERROR: Input is not valid json: {e}", file=sys.stderr)
        exit(1)


def conv(
        s: str,
        from_language: Language,
        to_language: Language,
        indent: Optional[int]=4,
    ) -> str:
    if from_language == to_language:
        try:
            raise_if_not_valid_for_language(s, language=from_language)
        except Exception as e:
            print(
                f"ERROR: Input is not valid {from_language}: {e}",
                file=sys.stderr,
            )
            exit(1)
        return s

    if from_language is Language.Json and to_language is Language.Python:
        return str(load_json(s))

    elif from_language is Language.Python and to_language is Language.Json:
        python_object = ast.literal_eval(s)
        return json.dumps(python_object, indent=indent)

    else:
        raise ValueError(
            f"Unsupported conversion `{from_language} -> {to_language}`")


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

    print(f"ERROR: could not detect language", file=sys.stderr)
    exit(1)


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
