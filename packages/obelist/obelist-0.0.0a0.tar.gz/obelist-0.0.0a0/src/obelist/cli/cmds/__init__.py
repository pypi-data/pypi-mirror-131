import click

from obelist import cli
from obelist.core.app import Application

from . import debug
from . import list
from . import parse
from . import path


@click.group(cls=cli.StylizedGroup)
@click.help_option("-h", "--help", help=cli.HELP_STR)
@click.version_option("--version", help=cli.VERSION_STR, message="%(version)s")
@click.option(
    "-p",
    "--path",
    metavar="<PATH>",
    envvar="OBELIST_PATH",
    multiple=True,
    type=click.Path(),
    help="""
        Set a configuration search path (overriding the `OBELIST_PATH`
        environment variable and the default search path)
    """,
)
@click.pass_context
def main(ctx, path):
    """Generate GitHub annotations from arbitrary input data"""
    app = Application()
    app.set_config_search_paths(path)
    ctx.obj = app


main.add_command(debug.debug)
main.add_command(list.list)
main.add_command(parse.parse)
main.add_command(path.path)


if __name__ == "__main__":
    main()
