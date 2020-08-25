from ru.ru_gen import _cli as BASE


_help = "This is a test"
_cli = BASE + (
    (
        "--extra",
        dict(
            required=True,
            help="An extra argument",
        ),
    ),
)


def run(parser, args):
    pass
