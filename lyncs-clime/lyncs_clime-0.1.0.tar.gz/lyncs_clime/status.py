"C-lime error messages"

__all__ = [
    "check_status",
]

from . import lib

MESSAGES = {
    lib.LIME_ERR_LAST_NOT_WRITTEN: "Last not written error",
    lib.LIME_ERR_PARAM: "Parameter error",
    lib.LIME_ERR_HEADER_NEXT: "Error with next record",
    lib.LIME_ERR_WRITE: "Writing error",
    lib.LIME_ERR_READ: "Reading error",
    lib.LIME_ERR_SEEK: "Seeking error",
    lib.LIME_ERR_MBME: "MB/ME flags incorrect",
    lib.LIME_ERR_CLOSE: "Closing error",
    # Not errors
    lib.LIME_LAST_REC_WRITTEN: "Not an error: last record written",
    lib.LIME_EOR: "Not an error: end of record",
    lib.LIME_EOF: "Not an error: end of file",
}


def check_status(status):
    "Checks the status integer returned by c-lime and raise error if needed"
    if status == 0:
        return

    raise RuntimeError(MESSAGES.get(status, "Unknown error"))
