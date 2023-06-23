# This file was copied from CourtListener
# TODO create 1 common library that both (all) FLP can use

import logging
import os

from django.core.management import BaseCommand, CommandError

logger = logging.getLogger(__name__)


class VerboseCommand(BaseCommand):
    def handle(self, *args, **options):
        verbosity = options.get("verbosity")
        if not verbosity:
            logger.setLevel(logging.WARN)
        elif verbosity==0:
            logger.setLevel(logging.WARN)
        elif verbosity==1:  # default
            logger.setLevel(logging.INFO)
        elif verbosity > 1:
            logger.setLevel(logging.DEBUG)


class CommandUtils(object):
    """A mixin to give some useful methods to subclasses."""

    @staticmethod
    def ensure_file_ok(file_path):
        """Check to make sure that a file path exists and is valid."""
        if not os.path.exists(file_path):
            raise CommandError(f"Unable to find file at {file_path}")
        if not os.access(file_path, os.R_OK):
            raise CommandError(f"Unable to read file at {file_path}")
