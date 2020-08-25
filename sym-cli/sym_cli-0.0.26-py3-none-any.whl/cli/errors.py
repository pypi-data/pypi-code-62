import shlex
from subprocess import CalledProcessError
from typing import Mapping, Pattern, Type

from click import ClickException
from sentry_sdk import capture_exception

ErrorPatterns = Mapping[Pattern[str], Type[Exception]]


def raise_if_match(patterns: ErrorPatterns, msg: str):
    if error := next((err for pat, err in patterns.items() if pat.search(msg)), None):
        raise error


class CliErrorMeta(type):
    _exit_code_count = 1

    def __new__(cls, name, bases, attrs):
        cls._exit_code_count += 1
        klass = super().__new__(cls, name, bases, attrs)
        klass.exit_code = cls._exit_code_count
        return klass


class CliError(ClickException, metaclass=CliErrorMeta):
    def __init__(self, *args, report=False, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.report = report

    def show(self):
        if self.report:
            capture_exception()
        super().show()


class CliErrorWithHint(CliError):
    def __init__(self, message, hint, **kwargs) -> None:
        msg = f"{message}\n\nHint: {hint}"
        super().__init__(msg, **kwargs)


class UnavailableResourceError(CliErrorWithHint):
    def __init__(self) -> None:
        super().__init__(
            "You don't have permission to access the Sym resource you requested.",
            "Request approval and then try again.",
        )


class ResourceNotSetup(CliErrorWithHint):
    def __init__(self) -> None:
        super().__init__(
            "The Sym resource you requested is not set up properly.",
            "Contact your Sym administrator.",
            report=True,
        )


class TargetNotConnected(CliErrorWithHint):
    def __init__(self) -> None:
        super().__init__(
            "The instance you tried to SSH into is not connected to AWS Session Manager.",
            "Ask your Sym administrator if they've set up Session Manager.",
        )


class AccessDenied(CliErrorWithHint):
    def __init__(self) -> None:
        super().__init__(
            "You don't have access to connect to this instance.",
            "Have you requested access?",
        )


class InstanceNotFound(CliError):
    def __init__(self, instance) -> None:
        super().__init__(f"Could not find instance {instance}")


class BotoError(CliErrorWithHint):
    def __init__(self, wrapped: "ClientError", hint: str) -> None:
        message = f"An AWS error occured!\n{str(wrapped)}"
        super().__init__(message, hint)


class FailedSubprocessError(CliError):
    def __init__(self, wrapped: CalledProcessError):
        super().__init__(f"Cannot run {shlex.join(wrapped.cmd)}")


class SuppressedError(FailedSubprocessError):
    def __init__(self, wrapped: CalledProcessError, echo=False):
        if echo:
            print(wrapped.stderr)
        super().__init__(wrapped)

    def show(self):
        pass


class WrappedSubprocessError(FailedSubprocessError):
    def __init__(self, wrapped, hint, **kwargs) -> None:
        messages = [
            f"Cannot run {wrapped.cmd[0]} [{wrapped.returncode}]",
            f"Hint: {hint}",
            f"\nThe original error was:",
            wrapped.stderr,
        ]
        CliError.__init__(self, "\n".join(messages), **kwargs)


class SamlClientNotSetup(CliErrorWithHint):
    def __init__(self) -> None:
        super().__init__(
            "Your SAML client is not set up.", "Consult the docs for your client.",
        )
