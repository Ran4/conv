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


