import click

from obelist import cli

states = {
    "valid": click.style("valid", fg="green"),
    "not_validated": click.style("not validated", fg="yellow"),
    "invalid": click.style("invalid", fg="red"),
}


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
    for config, filename, validity in app.list(absolute, states):
        id = click.style(f"{config.id}", bold=True)
        filename = click.format_filename(filename)
        filename = click.style(f"{filename}", fg="blue")
        click.echo(f"{id}: {filename} ({validity})")
