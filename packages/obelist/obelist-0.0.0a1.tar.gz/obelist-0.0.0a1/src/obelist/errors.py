import click

# TODO: Figure out what to do about styling Click error messages
#
# The code snippet above works as a monkey patch for the base `ClickException`
# class, but does not work for the `UsageError`, which has its own `show`
# method.
#
# In addition, at the moment, when I run `obelist debug` with a missing
# argument, there seems to be a double new line between the usage message and
# the error message, and I am not sure why. I am also not sure why in the hint
# about using `--help` is not displayed.
#
# Link dump:
#
# - https://stackoverflow.com/questions/39596070/
# - https://github.com/ewels/MultiQC/commit/62cc60
# - https://click.palletsprojects.com/en/8.0.x/api/#exceptions
# - https://stackoverflow.com/questions/61465229/
# Seems to be definitive: (grep "Table 7. LSB service exit codes")
# https://freedesktop.org/software/systemd/man/systemd.exec.html#id-1.20.8
# from click._compat import get_text_stderr
# from click.utils import echo
#
# def show(self, file=None):
#     "Show a stylized error message"
#     if file is None:
#         file = get_text_stderr()
#
#     error_text = click.style("Error:", fg="red", bold=True)
#     message = self.format_message()
#     echo(f"{error_text} {message}", file=file)
# TODO: Use proper exit codes:
# https://stackoverflow.com/questions/1101957/


class BaseError(click.ClickException):

    DEFAULT_MESSAGE = "Unknown failure"

    # TODO: Should just be be able to pass previous exception as an argument
    # instead of using the `message` attribute
    def __init__(self, *args, **kwargs):
        message = kwargs.get("message")
        if message is None:
            message = self.DEFAULT_MESSAGE
        kwargs["message"] = message
        super().__init__(*args, **kwargs)


class NotImplementedError(BaseError):

    DEFAULT_MESSAGE = "Functionality not implemented"


class DecodingError(BaseError):

    DEFAULT_MESSAGE = "Unable to decode character data"


class YamlError(BaseError):

    DEFAULT_MESSAGE = "YAML error"


class YamlSchemaError(YamlError):

    DEFAULT_MESSAGE = "YAML schema validation failed"


class JQError(BaseError):

    DEFAULT_MESSAGE = "JQ error"


class ConfigurationError(BaseError):

    DEFAULT_MESSAGE = "Configuration failed"


class NoFormatError(BaseError):

    DEFAULT_MESSAGE = "Format not found"


class InvalidSyntaxError(BaseError):

    DEFAULT_MESSAGE = "Invalid syntax value"
