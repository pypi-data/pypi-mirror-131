import sys

import click

from obelist import cli


@click.command(cls=cli.StylizedCommand)
# TODO: allow multiple inputs to be specified
@click.argument("input", required=False, default="-", type=click.File("rb"))
@click.help_option("-h", "--help", help=cli.HELP_STR)
# TODO: Implement some sort of config guesssing
# TODO: Allow this to be configured in a global config file
@click.option(
    "-q",
    "--quiet",
    is_flag=True,
    help="Suppress all non-essential output",
)
# TODO: Allow this to be configured in a global config file
@click.option(
    "-d",
    "--debug",
    is_flag=True,
    help="Print debug information during parsing",
)
# editorconfig-checker-disable
# TODO: https://click.palletsprojects.com/en/8.0.x/options/#choice-options
# TODO: https://click.palletsprojects.com/en/8.0.x/options/#dynamic-defaults-for-prompts
# editorconfig-checker-enable
@click.option(
    "-p",
    "--parser",
    "parser_id",
    metavar="ID",
    required=True,
    help="Specify the parser to use",
)
# TODO: Allow this to be configured in a global config file
# TODO: https://click.palletsprojects.com/en/8.0.x/options/#choice-options
@click.option(
    "-e",
    "--error-on",
    metavar="LEVEL",
    default="notice",
    show_default=True,
    help="Exit on the specified severity level (notice, warning, error)",
)
# editorconfig-checker-disable
# TODO: https://click.palletsprojects.com/en/8.0.x/options/#choice-options
# TODO: https://click.palletsprojects.com/en/8.0.x/options/#dynamic-defaults-for-prompts
# editorconfig-checker-enable
@click.option(
    "-f",
    "--format",
    "format",
    metavar="FORMAT",
    required=True,
    help="Specify the input format",
)
# TODO: Allow this to be configured in a global config file
# TODO: https://click.palletsprojects.com/en/8.0.x/options/#choice-options
@click.option(
    "-s",
    "--sort-by",
    metavar="ATTR",
    default="filename",
    show_default=True,
    help="Sort annotations by the specified attribute (filename, severity)",
)
@click.option(
    "-w",
    "--write",
    "write_file",
    metavar="FILE",
    default="/dev/stdout",
    type=click.File("a"),
    help="""
        Append annotation commands to the specified file instead of printing
        them (can be used in combination with `obelist print` command)
    """,
)
# TODO: Allow this to be configured in a global config file
@click.option(
    "-c",
    "--console",
    is_flag=True,
    envvar="PRINT_CONSOLE",
    help="""
        Print visible annotations to the console (can also be set with the
        `PRINT_CONSOLE` environment variable value)
    """,
)
# TODO: Allow this to be configured in a global config file
@click.option(
    "-b",
    "--before-context",
    metavar="LINES",
    default=2,
    show_default=True,
    type=int,
    help="""
        Print the specified number of lines before each annotated section
    """,
)
# TODO: Allow this to be configured in a global config file
@click.option(
    "-a",
    "--after-context",
    metavar="LINES",
    default=0,
    show_default=True,
    type=int,
    help="""
        Print the specified number of lines after each annotated section
    """,
)
@click.pass_obj
def parse(
    app,
    input,
    quiet,
    debug,
    parser_id,
    error_on,
    format,
    sort_by,
    write_file,
    console,
    before_context,
    after_context,
):
    """Generate annotations from input data using a parser configuration

    The `INPUT` argument, if specified, must reference any type of readable
    file. You can specify `-` to read from standard input (STDIN). However,
    when no `INPUT` value is provided, the program will attempt to read from
    STDIN by default.

    If you set the `OBELIST_NO_ERROR` environment variable to `true`, the
    command will ignore the `--error-on` option and never exit with an error.
    You can use this feature in conjunction with the `--write` option to log
    annotations without stopping the build because of a single command error.
    Afterward, you can process the annotation log in bulk with the `format`
    command and the `--error-on` option as desired.

    When the program exits because of a parsed error message, the returned
    error code corresponds to the highest error message encountered:

    - 100: notice
    - 101: warning
    - 102: error

    If the `GITHUB_ACTIONS` environment variable is set to `true`, this program
    will print GitHub workflow commands to send parser output to the GitHub
    Actions runner. GitHub Actions automatically sets this environment variable
    to `true` when running any workflow.

    The GitHub Actions runner does not print GitHub workflow commands to the
    output log. If you want preview the GitHub workflow commands, you can set
    the `GITHUB_ACTIONS` environment variable to `true` when running this
    program locally.
    """
    # TODO: IF console is false and this is not being run in a GitHub Actions
    # workflow, exit immediately
    app.configure(quiet, debug, error_on, write_file, console)
    app.load_configs()
    app.parse(parser_id, input, format)
    status_code = app.print(sort_by, before_context, after_context)
    sys.exit(status_code)
