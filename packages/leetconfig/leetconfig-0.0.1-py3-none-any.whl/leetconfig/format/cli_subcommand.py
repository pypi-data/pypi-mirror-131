import sys

if sys.version_info < (3, 6):
    print("The leetconfig.cli_subcommand module only supports python >= 3.6")
    sys.exit(1)

import asyncio
import argparse
import logging

from abc import ABC
from asyncio import coroutine
from typing import List, Optional

LOGGER = logging.getLogger(__file__)


class ShowSubCommandHelpError(RuntimeError):
    pass


class UnregisteredSubcommandError(Exception):
    pass


class CLISubcommand(ABC):
    def __init__(
        self,
        command,
        description,
        subcommands=None,  # type: Optional[List[CLISubcommand]]
    ):
        self.depth = 0  # type: int
        self.parser = None  # type: Optional[argparse.ArgumentParser]
        self.full_command = None  # type: Optional[str]

        self.command = command
        self.description = description
        self.subcommands = subcommands

    def _register(
        self,
        depth,  # type: int
        parent_command,  # type: str
        parsers,  # type: argparse._SubParsersAction
    ):
        self.parser = parsers.add_parser(
            self.command,
            help=self.description,
            add_help=False,
            formatter_class=argparse.ArgumentDefaultsHelpFormatter,
        )
        self.depth = depth
        self.full_command = f"{parent_command} {self.command}"
        self.parser.set_defaults(subcommand=self)
        if self.subcommands is not None:
            subparsers = self.parser.add_subparsers()
            for subcommand in self.subcommands:
                subcommand._register(depth + 1, self.full_command, subparsers)

    @coroutine
    async def run(
        self, args  # type: List[str]
    ):
        if self.parser is None:
            raise UnregisteredSubcommandError("cannot run unregistered CLI subcommand")
        self.parser.print_help()


class CLISubcommandRunner:
    def __init__(
        self,
        program,  # type: str
        description,  # type: str
        subcommands,  # type: List[CLISubcommand]
    ):
        self.parser = argparse.ArgumentParser(
            prog=program,
            description=description,
            formatter_class=argparse.ArgumentDefaultsHelpFormatter,
        )
        self.program = program
        self.subcommands = subcommands
        self.event_loop = asyncio.get_event_loop()

    def run(self):
        subparsers = self.parser.add_subparsers()
        for subcommand in self.subcommands:
            subcommand._register(1, self.program, subparsers)

        args, _ = self.parser.parse_known_args()
        if not hasattr(args, "subcommand"):
            self.parser.print_help()
            sys.exit(1)
        try:
            self.event_loop.run_until_complete(
                args.subcommand.run(sys.argv[args.subcommand.depth + 1 :])
            )
        except ShowSubCommandHelpError:
            self.parser.print_help()
        except KeyboardInterrupt:
            LOGGER.info("User exited")
