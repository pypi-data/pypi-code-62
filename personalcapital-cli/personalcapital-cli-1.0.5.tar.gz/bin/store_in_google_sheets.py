# Standard Library
import argparse
import json
import logging
from pathlib import Path
import sys
from typing import List

# Third Party Code
from clint_utilities import parse_args, setup_logging
from googleapiclient.discovery import Resource

# PCAPCLI Code
from pcapcli import ensure_file_exists
from pcapcli.store.google_sheets import (
    append_data,
    get_service,
    get_sheets,
    SCOPES,
    update_pivot,
)

USER_CREDENTIALS_PATH_DEFAULT = Path(".", "google.user_credentials.pickle")
CLIENT_CREDENTIALS_PATH_DEFAULT = Path(".", "google.client_credentials.json")


CLI_ARGS = {
    "description": "Updates the Net Worth spreadsheet.",
    "args": {
        "--spreadsheet-id": {},
        "--client-credentials-file": {"dest": "client_credentials_file",},
        "--user-credentials-file": {"dest": "user_credentials_file",},
        "--quiet": {"action": "store_true", "default": False},
        "--verbose": {"action": "store_true", "default": False},
    },
}

logger = logging.getLogger(__name__)


def get_data():
    return json.load(sys.stdin)


def validate_args(args: argparse.Namespace):
    try:
        ensure_file_exists(args.client_credentials_file)
    except FileNotFoundError:
        logger.error(
            "Google Client credentials file %s not found.", args.client_credentials_file
        )
        raise
    try:
        ensure_file_exists(args.user_credentials_file)
    except FileNotFoundError:
        logger.error(
            "Google User credentials file %s not found.", args.user_credentials_file
        )
        raise


def update_spreadsheet(
    service: Resource, spreadsheet_id: str, data: List[List],
):
    # Build a lookup table for Sheet Name -> Sheet ID
    sheets = get_sheets(service=service, spreadsheet_id=spreadsheet_id)

    # Append this series of data to the end of the "Ledger" sheet
    # and get back the final row of the data set (for use in updating pivot tables).
    last_row = append_data(
        spreadsheet_id=spreadsheet_id,
        data=data,
        current_data_start="Ledger!A1",
        service=service,
    )

    # Update the "Summary" sheet pivot table
    update_pivot(
        spreadsheet_id=spreadsheet_id,
        src_sheet_id=sheets["Ledger"],
        src_last_row=last_row,
        dst_sheet_id=sheets["Summary"],
        row_tuples=[
            (5, True, "ASCENDING", None),
            (6, True, "ASCENDING", None),
            (1, True, "ASCENDING", {}),
        ],
        column_tuples=[(0, False, "DESCENDING"),],
        value_data=[4,],
        service=service,
    )

    # Update to "Net Worth" sheet pivot table.
    update_pivot(
        spreadsheet_id=spreadsheet_id,
        src_sheet_id=sheets["Ledger"],
        src_last_row=last_row,
        dst_sheet_id=sheets["Net Worth"],
        row_tuples=[(0, False, "ASCENDING", None),],
        column_tuples=[(5, True, "ASCENDING"),],
        value_data=[4,],
        service=service,
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
    validate_args(args)
    service = get_service(
        client_credentials_path=(
            args.client_credentials_file
            and Path(args.client_credentials_file)
            or CLIENT_CREDENTIALS_PATH_DEFAULT
        ),
        scopes=SCOPES,
        user_credentials_path=(
            args.user_credentials_file
            and Path(args.user_credentials_file)
            or USER_CREDENTIALS_PATH_DEFAULT
        ),
    )
    update_spreadsheet(
        service=service, spreadsheet_id=args.spreadsheet_id, data=get_data()
    )


if __name__ == "__main__":  # pragma: no cover
    main()  # pragma: no cover
