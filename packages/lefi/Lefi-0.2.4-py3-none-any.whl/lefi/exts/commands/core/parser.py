from __future__ import annotations

import inspect
from typing import TYPE_CHECKING, Any, Dict, List, Optional, Tuple, Union

from .command import Command
from .converters import _CONVERTERS

if TYPE_CHECKING:
    from .context import Context

__all__ = ("StringParser",)


class StringParser:
    """
    A class representing a StringParser.

    Attributes:
        command_name (Optional[str]): The name of the command.
        command (Optional[Command]): The [Command](./command.md) object.
        arguments (List[str]): The arguments of the command.
        content (str): The content of the command.
        prefix (Union[Tuple[str], str]): The prefix of the command.
    """

    def __init__(self, content: str, prefix: Union[str, Tuple[str, ...], List[str]]) -> None:
        """
        Initialize a StringParser.

        Parameters:
            content (str): The content of the command.
            prefix (Union[Tuple[str], str]): The prefix of the command.
        """
        self.command_name: Optional[str] = None
        self.command: Optional[Command] = None
        self.arguments: List[str] = []
        self.content = content
        self.prefix = prefix
        self.context: Context

    def find_command(self) -> Optional[str]:
        """
        Find the command.

        Returns:
            The command name.
        """
        tokens = self.content.split(" ")

        if prefix := self.parse_prefix():

            if tokens[0].startswith(prefix):
                self.command_name = tokens[0][len(prefix) :]

            self.arguments = tokens[1:]

            return self.command_name

        return None

    def parse_prefix(self) -> Optional[str]:
        """
        Parse the prefix.

        Returns:
            The prefix.
        """
        if isinstance(self.prefix, (tuple, list)):
            find_prefix = [self.content.startswith(prefix) for prefix in self.prefix]

            for index, prefix in enumerate(find_prefix):
                if prefix is not True:
                    continue

                return self.prefix[index]

        elif not isinstance(self.prefix, (tuple, list)):
            return self.prefix

        return None

    async def parse_arguments(self) -> Tuple[Dict, List]:
        """
        Parse the arguments.

        Returns:
            The arguments and the keyword-arguments.
        """
        keyword_arguments: Dict = {}
        arguments: List = []

        if self.command is not None:
            signature = inspect.signature(self.command.callback)
            parameters = signature.parameters.copy()  # type: ignore

            parameters.popitem(False)  # type: ignore
            if self.command.parent:
                parameters.popitem(False)  # type: ignore

            for index, (argument, parameter) in enumerate(parameters.items()):
                if parameter.kind is parameter.POSITIONAL_OR_KEYWORD:
                    arguments.append(await self.convert(parameter, self.arguments[index - 1]))

                elif parameter.kind is parameter.KEYWORD_ONLY:
                    keyword_arguments[argument] = await self.convert(parameter, " ".join(self.arguments[index - 1 :]))

        return keyword_arguments, arguments

    async def convert(self, parameter: inspect.Parameter, data: str) -> Any:
        if parameter.annotation is parameter.empty:
            return str(data)

        name = parameter.annotation.removeprefix("lefi.")
        if converter := _CONVERTERS.get(name):
            return await converter.convert(self.context, data)

        if parameter.annotation is not parameter.empty and callable(parameter.annotation):
            return parameter.annotation(data)

        return str(data)

    @property
    def invoker(self) -> Optional[Command]:
        """
        Get the invoker.

        Returns:
            The invoker [Command](./command.md).
        """
        return self.command

    @property
    def invoked_with(self) -> Optional[str]:
        """
        The prefix the command was invoked with.

        Returns:
            The prefix.
        """
        return self.parse_prefix()
