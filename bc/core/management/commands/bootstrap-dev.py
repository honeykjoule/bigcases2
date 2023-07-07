from django.core.management.base import CommandParser
from bc.core.management.commands.command_utils import VerboseCommand
from bc.core.management.commands.make_dev_data import MakeDevData


class Command(VerboseCommand):
    """
    A command for creating dummy data in the system.
    Parses arguments and then sends them to the class to actually make the
    data.
    """

    help = "Create dummy data in your system for development purposes. Uses Factories"

    DEFAULT_BIG_CASES = 10
    DEFAULT_LITTLE_CASES = 3

    def add_arguments(self, parser: CommandParser) -> None:
        parser.add_argument(
            "--big-cases",
            "-b",
            type=int,
            default=self.DEFAULT_BIG_CASES,
            help=f"The number of big cases to create in addition to any "
            f"subscriptions to real cases (which are set to big cases). "
            f"(integer) Default = {self.DEFAULT_BIG_CASES}",
        )
        parser.add_argument(
            "--little-cases",
            "-l",
            type=int,
            default=self.DEFAULT_LITTLE_CASES,
            help=f"The number of little cases to create. "
            f"(integer) Default = {self.DEFAULT_LITTLE_CASES}",
        )
        parser.add_argument(
            "--real-cases",
            "-r",
            type=int,
            action="append",
            help=f"Subscribe to a real case from Court Listener with this "
            f"Court Listener docket id (integer).  This will be "
            f"subscribed as a big case.  You can use this option "
            f"multiple times to subscribe to multiple cases. Ex: "
            f"--real-subscription 67490069 --real-subscription 67490070",
        )

    def handle(self, *args, **options) -> None:
        self.requires_migrations_checks = True
        super(Command, self).handle(*args, **options)

        num_big_cases = self.DEFAULT_BIG_CASES
        if options["big_cases"]:
            num_big_cases = options["big_cases"]

        num_little_cases = self.DEFAULT_LITTLE_CASES
        if options["little_cases"]:
            num_little_cases = options["little_cases"]

        real_cases = None
        if options["real_cases"]:
            real_cases = options["real_cases"]

        self._show_and_log("Creating dummy data.... ")
        maker = MakeDevData(
            num_big_cases,
            num_little_cases,
            real_cases,
        )
        result_summary = maker.create()
        self._show_and_log(result_summary)
        self._show_and_log("Done.")

    def _show_and_log(self, info_str: str = ""):
        if len(info_str) > 0:
            self.logger.info(info_str)
            print(info_str)
