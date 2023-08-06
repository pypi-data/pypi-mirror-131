from typing import TypeVar, Union, Type, Optional, Dict

AnyIP = r"(\d+)\.(\d+)\.(\d+)\.(\d+)"
AnyDigit = r"(\d+)"
AnyStr = r"(.+)"
AnyUrl = r"(http[s]?://.+)"
Bool = r"(True|False)"

NonTextElement = TypeVar("NonTextElement")
MessageChain = TypeVar("MessageChain")


class Args:
    args: Dict[str, Union[str, Type[NonTextElement]]]
    default: Dict[str, Union[str, Type[NonTextElement]]]

    def __init__(self, **kwargs):
        self.args = kwargs

    def default(self, **kwargs):
        self.default = kwargs
        return self


class Default:
    args: Union[str, Type[NonTextElement]]
    default: Union[str, Type[NonTextElement]]

    def __init__(
            self,
            args: Union[str, Type[NonTextElement]],
            default: Optional[Union[str, NonTextElement]] = None
    ):
        self.args = args
        self.default = default


Argument_T = Union[str, Type[NonTextElement], Default]
