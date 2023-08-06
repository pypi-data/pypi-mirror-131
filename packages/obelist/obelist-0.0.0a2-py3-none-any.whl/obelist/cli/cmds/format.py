import sys

import click

from obelist import cli


@click.command(cls=cli.StylizedCommand)
@click.help_option("-h", "--help", help=cli.HELP_STR)
# TODO: Dry this option out with the parse command
@click.option(
    "-q",
    "--quiet",
    is_flag=True,
    help="Suppress all non-essential output",
)
# TODO: Dry this option out with the parse command
@click.option(
    "-e",
    "--error-on",
    metavar="LEVEL",
    default="notice",
    show_default=True,
    help="Exit on the specified severity level (notice, warning, error)",
)
# TODO: Dry this option out with the parse command
@click.option(
    "-s",
    "--sort-by",
    metavar="ATTR",
    default="filename",
    show_default=True,
    help="Sort annotations by the specified attribute (filename, severity)",
)
# TODO: Dry this option out with the parse command
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
# TODO: Dry this option out with the parse command
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
# TODO: Dry this option out with the parse command
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
@click.argument("input_file", type=click.File("r"))
@click.pass_obj
def format(
    app,
    quiet,
    error_on,
    sort_by,
    console,
    before_context,
    after_context,
    input_file,
):
    """Format annotation commands read from INPUT_FILE

    This command is useful when you want to aggregate annotations from multiple
    sources, allowing you group them by severity level or filename.
    """
    # TODO: Clean this up
    # Set defaults for options not used by this command
    debug = False
    write_file = click.File(mode="w")(value="/dev/stdout")
    app.configure(quiet, debug, error_on, write_file, console)
    app.read_commands(input_file)
    status_code = app.print(sort_by, before_context, after_context)
    sys.exit(status_code)
