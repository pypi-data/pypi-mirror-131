import os

import click

from obelist import cli

VALID = click.style(f"valid", fg="green")
NOT_VALIDATED = click.style(f"not validated", fg="yellow")
INVALID = click.style(f"invalid", fg="red")


@click.command(cls=cli.StylizedCommand)
@click.help_option("-h", "--help", help=cli.HELP_STR)
@click.option(
    "-a",
    "--absolute",
    is_flag=True,
    help="Print absolute filenames",
)
@click.pass_obj
def list(app, absolute):
    """Print a list of parser configurations and exit"""
    app.load_configs()
    configs = app.get_configs()
    # TODO: Indicate active config when multiple configs share the same ID
    for config in configs:
        id = click.style(f"{config.id}", bold=True)
        filename = config.filename
        if not absolute:
            filename = os.path.relpath(filename)
        filename = click.format_filename(filename)
        filename = click.style(f"{filename}", fg="blue")
        validity = NOT_VALIDATED
        if config.valid is not None:
            validity = config.valid and VALID or INVALID
        click.echo(f"{id}: {filename} ({validity})")
