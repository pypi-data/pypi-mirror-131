import click

from obelist import cli


@click.command(cls=cli.StylizedCommand)
@click.argument("config_id")
@click.help_option("-h", "--help", help=cli.HELP_STR)
@click.pass_obj
def debug(app, config_id):
    """Debug issues with a parser configuration"""
    app.debug(config_id)
