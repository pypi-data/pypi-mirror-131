from pydantic import BaseModel
from typing import Optional, List

from .transformers import get_transformer_class, TokenT
from .fs import load_from_yaml

FILENAME: str = "types.yaml"


class TypeField(BaseModel):
    """
    Represents one Field in a Type
    {'name': 'first_name', 'type': 'string', 'optional': False},
    """
    name: str
    type: str
    optional: Optional[bool]


class TypeDefinition(BaseModel):
    """
    Represents one new Type in the list of typedefs
    {'typename': 'User',
     'fields': [
        {'name': 'first_name', 'type': 'string', 'optional': False},
        {'name': 'last_name', 'type': 'string', 'optional': False},
        {'name': 'age', 'type': 'int', 'optional': False},
        {'name': 'weight', 'type': 'float', 'optional': True} ]
    }
    """
    typename: str
    fields: List[TypeField]


class IR(BaseModel):
    """
    Intermediate Representation of the entire file that was passed in
    {'typedefs': [
        {'typename': 'User',
         'fields': [
             {'name': 'first_name', 'type': 'string', 'optional': False},
             {'name': 'last_name', 'type': 'string', 'optional': False},
             {'name': 'age', 'type': 'int', 'optional': False},
             {'name': 'weight', 'type': 'float', 'optional': True} ]
         }
      ]
    }
    """
    typedefs: List[TypeDefinition]

    @property
    def typedef_c(self) -> int:
        """
        Count of type definitions we read
        :return: (int)
        """
        return len(self.typedefs)


class TypeBuf:
    def __init__(self, filename: str, languages: tuple[str]):
        self.filename: str = filename
        self.languages = languages
        self.intermediate_representation: IR = IR(**load_from_yaml(self.filename))

    def __dict__(self) -> dict:
        return {
            'filename': self.filename,
            'languages': self.languages,
            'IR': self.intermediate_representation.dict(),
        }

    def compile(self) -> None:
        """
        Generates the output str
        :return:
        """
        if self.intermediate_representation.typedef_c < 1:
            return
        if len(self.languages) < 1:
            return

        # Loop through the langs specified
        for lang in self.languages:
            transformer_class = get_transformer_class(lang)

            # For each new Typedef in the definitions file
            for typedef in self.intermediate_representation.typedefs:
                transformer = transformer_class(typedef)
                transformer.generate_filename()
                for fn in transformer.method_order:
                    transformer.output_buf += fn()

                transformer.write_buf()
