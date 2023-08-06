import shutil

import click
import obelist

HELP_STR = "Print this help message and exit"
VERSION_STR = "Print the program version number and exit"


class StylizedHelpFormatter(click.HelpFormatter):

    """This subclass stylizes the formatting of text-based help pages."""

    def write_usage(self, *args, **kwargs):
        """Writes a stylized usage line into the buffer."""
        prefix = kwargs.get("prefix", "Usage:")
        prefix = click.style(prefix, bold=True)
        super().write_usage(*args, prefix="")
        usage = self.getvalue()
        self.buffer = []
        # Silence vulture
        self.buffer
        usage = click.style(usage, italic=True)
        self.write(f"{prefix}\n\n  {usage}")

    def write_heading(self, heading):
        """Writes a stylized heading into the buffer."""
        heading = click.style(f"{heading}:", bold=True)
        self.write(f"{'':>{self.current_indent}}{heading}\n\n")

    def write_dl(self, rows, **kwargs):
        """Writes a stylized definition list into the buffer."""
        new_rows = []
        for term, definition in rows:
            term = click.style(term, italic=True)
            new_rows.append((term, definition))
        super().write_dl(new_rows, **kwargs)


class StylizedContext(click.Context):

    """This class adds stylized help formatting to the context object."""

    formatter_class = StylizedHelpFormatter


class StylizedCommand(click.Command):

    """This class augments the stylized help formatting."""

    context_class = StylizedContext

    def _add_description(self, ctx, formatter):
        help_lines = self.help.strip().splitlines()
        if len(help_lines) > 1:
            heading = click.style("Description:", bold=True)
            formatter.write(f"\n{heading}\n")
            self.help = "\n".join(help_lines[2:])
            self.format_help_text(ctx, formatter)

    def format_help(self, ctx, formatter):
        """Writes the augmented help into the formatter if it exists."""
        width = obelist.DEFAULT_COLUMNS
        terminal_width = shutil.get_terminal_size().columns
        width = min(width, terminal_width)
        short_help = self.get_short_help_str(width)
        self.format_usage(ctx, formatter)
        formatter.write(f"\n  {short_help}\n")
        if self.help:
            self._add_description(ctx, formatter)
        self.format_options(ctx, formatter)
        self.format_epilog(ctx, formatter)


class StylizedMultiCommand(click.MultiCommand, StylizedCommand):

    """This subclass mixes in the stylized help formatting."""

    pass


class StylizedGroup(click.Group, StylizedMultiCommand):

    """This subclass mixes in the stylized help formatting."""

    context_class = StylizedContext


# Silence vulture
StylizedGroup.context_class
