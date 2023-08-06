from typing import Union

from .python import PythonTransformer
from .typescript import TypeScriptTransformer

TokenT = Union[
    PythonTransformer,
    TypeScriptTransformer,
]


def get_transformer_class(language: str):
    if language.lower() == 'python':
        return PythonTransformer
    if language.lower() == 'typescript':
        return TypeScriptTransformer
    else:
        raise ValueError(
            'No compilation tokens found for programming language [%s]..' % language
        )
