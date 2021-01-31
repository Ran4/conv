#!/usr/bin/env python3
from argparse import ArgumentParser
from enum import Enum, auto
import ast
import sys
USAGE = """
Converts structures between different formats.


Example:

```bash
$ curl some_endpoint
{"name": "foo", "active": false, "redirect_url": null}

$ curl some_endpoint | conv.py json python
{"name": "foo", "active": False, "redirect_url": None}
```
"""
import json
from typing import Dict, List, Optional, Union


class Language(Enum):
    Json = "json"
    Python = "python"


def raise_if_not_valid_for_language(s: str, language: str) -> None:
    if language == "json":
        json.loads(s)
    elif language == "python":
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
        from_language="json",
        to_language="python",
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

    if from_language == "json" and to_language == "python":
        return str(load_json(s))

    elif from_language == "python" and to_language == "json":
        python_object = ast.literal_eval(s)
        return json.dumps(python_object, indent=indent)

    else:
        raise ValueError(
            f"Unsupported conversion `{from_language} -> {to_language}`")


def test_conv_json_to_json():
    json_string = '{"name": "foo", "active": false, "redirect_url": null}'
    assert conv(json_string, "json", "json") == json_string


def test_conv_json_to_python():
    json_string = '{"name": "foo", "active": false, "redirect_url": null}'
    assert conv(json_string, "json", "python") == (
        "{'name': 'foo', 'active': False, 'redirect_url': None}"
    )


def test_conv_python_to_json():
    json_string = '{"name": "foo", "active": false, "redirect_url": null}'
    assert conv(json_string, "json", "python") == (
        "{'name': 'foo', 'active': False, 'redirect_url': None}"
    )


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


def detect_language(s: str):
    # json?
    try:
        json.loads(s)
        return "json"
    except Exception:
        pass

    # python?
    try:
        ast.literal_eval(s)
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
        from_language, to_language = "json", "python"
    elif args.to_language is None:
        from_language = detect_language(input_string)
        to_language = args.from_language
    else:
        from_language = args.from_language
        to_language = args.to_language

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
