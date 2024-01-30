# --------------------------------------------------------------------------------------
# Copyright (c) 2023 Sean Kerr
# --------------------------------------------------------------------------------------

# system imports
from dataclasses import dataclass

from typing import Any
from typing import Dict
from typing import List
from typing import Optional
from typing import TypeAlias
from typing import Union

from typing_extensions import Protocol

Message: TypeAlias = Union[bytes, str]


@dataclass(frozen=True)
class Args:
    arg: Optional[Any] = None
    args: Optional[List[Any]] = None
    kwargs: Optional[Dict[str, Any]] = None


class Serializer(Protocol):
    def arg_from_json(self, arg: Any) -> Any:
        """
        Deserialize a JSON argument into its python equivalent.

        Parameters:
            arg (object): Any object type.
        """

    def arg_to_json(self, arg: Any) -> Any:
        """
        Serialize an argument into its JSON equivalent.

        Parameters:
            arg (object): Any object type.
        """

    def message_from_args(self, args: Args) -> Message:
        """
        Serialize arguments into their message equivalent.

        Parameters:
            args (Args): Arguments.
        """

    def message_to_args(self, message: Message) -> Args:
        """
        Deserialize a message into its python equivalent.

        Parameters:
            message (Message): Message.
        """
