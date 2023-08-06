from argparse import ArgumentParser
from typing import List, Type

from cline import AnyTask, ArgumentParserCli

import startifact.tasks


class StartifactCLI(ArgumentParserCli):
    def make_parser(self) -> ArgumentParser:
        """
        Gets the argument parser.
        """

        parser = ArgumentParser(
            description="Stages artifacts to Amazon Web Services",
            epilog="Made with love by Cariad Eccleston: https://github.com/cariad/startifact",
        )

        parser.add_argument("project", help="Project name", nargs="?")
        parser.add_argument(
            "artifact_version",
            help="Artifact version",
            nargs="?",
        )

        parser.add_argument(
            "--download",
            help="download an artifact to a local path (version is optional)",
            metavar="TO",
        )

        parser.add_argument(
            "--filename",
            help="save the filename as metadata when staging/restore the filename when downloading",
            action="store_true",
        )

        parser.add_argument(
            "--info",
            help="get artifact information",
            action="store_true",
        )

        parser.add_argument(
            "--metadata",
            help="set metadata when staging",
            metavar="KEY=VALUE",
            action="append",
        )

        parser.add_argument(
            "--setup",
            help="perform initial setup then exit",
            action="store_true",
        )

        parser.add_argument(
            "--stage",
            help="stage an artifact from a local path (name and version required)",
            metavar="FROM",
        )

        parser.add_argument(
            "--dry-run",
            help="dry-run the staging of an artifact from a local path (name and version required)",
            metavar="FROM",
        )

        parser.add_argument(
            "--version",
            help="show version then exit",
            action="store_true",
        )
        parser.add_argument(
            "--log-level",
            help="log level",
            metavar="LEVEL",
            default="CRITICAL",
        )
        return parser

    def register_tasks(self) -> List[Type[AnyTask]]:
        """
        Gets the tasks that this CLI can perform.
        """

        return [
            startifact.tasks.DownloadTask,
            startifact.tasks.DryRunStageTask,
            startifact.tasks.InfoTask,
            startifact.tasks.StageTask,
            startifact.tasks.SetupTask,
        ]
