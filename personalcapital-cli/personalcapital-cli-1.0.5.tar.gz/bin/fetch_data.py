# Standard Library
import argparse
from collections import Counter
import logging
from pathlib import Path
import sys
from typing import Callable, Dict, IO

# Third Party Code
from clint_utilities import parse_args, setup_logging

# PCAPCLI Code
from pcapcli.fetch.ascii_table import print_table
from pcapcli.fetch.data import (
    connect,
    fetch_account_info,
    get_firm_replacements,
    get_loan_limits,
)
from pcapcli.fetch.output import print_csv, print_json

PERSISTED_SESSION_FILE = Path(".", "fetch.http.session")
CLI_ARGS = {
    "description": "Personal Capital Interface",
    "args": {
        "--print-account-table": {
            "dest": "print_accounts",
            "action": "store_true",
            "default": False,
        },
        "--print-json": {
            "dest": "print_json",
            "action": "store_true",
            "default": False,
        },
        "--print-csv": {"dest": "print_csv", "action": "store_true", "default": False},
        "--firm-replacements-file": {"dest": "firm_replacements_file"},
        "--loan-limits-file": {"dest": "loan_limits_file"},
        "--email-address": {"dest": "email_address"},
        "--password": {},
        "--quiet": {"action": "store_true", "default": False},
        "--verbose": {"action": "store_true", "default": False},
    },
}

logger = logging.getLogger(__name__)


def validate_arguments(args: argparse.Namespace) -> None:
    # Throw an error if none of the functions are selected
    if not (args.print_accounts or args.print_json or args.print_csv):
        raise ValueError(
            "Please specify only one of --print-account-table, --print-json, --print-csv"
        )
    # Throw an error if more than one of the functions are selected
    if Counter([args.print_accounts, args.print_json, args.print_csv])[True] > 1:
        raise ValueError(
            "Please specify only one of --print-account-table, --print-json, --print-csv"
        )
    # Throw an error if authentication parameters are not specified.
    if not all([args.email_address, args.password]):
        raise ValueError("You must supply both --email-address and --password.")


def select_representation(args: argparse.Namespace) -> Callable[[Dict, IO], None]:
    if args.print_accounts:
        return print_table
    elif args.print_json:
        return print_json
    elif args.print_csv:
        return print_csv
    raise ValueError(
        "Please specify either one of --print-account-table, --print-json, --print-csv"
    )


def main():
    args = parse_args(CLI_ARGS)
    log_level = (args.quiet and "ERROR") or (args.verbose and "DEBUG") or "INFO"
    setup_logging(
        log_level,
        extra_loggers={
            __name__: {"level": log_level, "handlers": ["default"], "propagate": True},
            "pcapapi": {"level": log_level, "handlers": ["default"], "propagate": True},
        },
    )
    validate_arguments(args)
    select_representation(args=args)(
        fetch_account_info(
            connection=connect(
                email=args.email_address,
                password=args.password,
                session_path=PERSISTED_SESSION_FILE,
            ),
            loan_limits=get_loan_limits(args.loan_limits_file),
            firm_replacements=get_firm_replacements(args.firm_replacements_file),
            session_path=PERSISTED_SESSION_FILE,
        ),
        sys.stdout,
    )


if __name__ == "__main__":  # pragma: no cover
    main()  # pragma: no cover
