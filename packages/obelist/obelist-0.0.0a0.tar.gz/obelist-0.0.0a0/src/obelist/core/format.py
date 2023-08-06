import textwrap

import pastel


printer = pastel.Pastel(True)
printer.add_style("header", options=["bold"])
printer.add_style("location", "light_blue")
# printer.add_style("code", "white")
printer.add_style("notice", options=["bold"])
printer.add_style("warning", "yellow", options=["bold"])
printer.add_style("error", "red", options=["bold"])


class BaseFormat:

    _github = False

    _title = None
    _annotations = []

    def __init__(self, title, annotations):
        self._printer = printer
        self._title = title
        self._annotations = annotations

    def _print(self, str):
        print(printer.colorize(str))

    def _print_prologue(self, group_name=None):
        pass

    def _print_annotation(self, annotation):
        pass

    def _print_annotations(self):
        for annotation in self._annotations:
            self._print_annotation(annotation)

    def _print_epilogue(self, group_name=None):
        pass

    def print(self, group_name=None):
        self._print_prologue(group_name)
        self._print_annotations()
        self._print_epilogue(group_name)


class CommandFormat(BaseFormat):
    def _print_prologue(self, group_name=None):
        if group_name:
            group = f"::group::{group_name}"
            print(group)

    def _print_annotation(self, annotation):
        severity_name = annotation["severity_name"]
        file = f"file={annotation['file']}"
        line = f"line={int(annotation['line'])}"
        end_line = f"endLine={int(annotation['end-line'])}"
        title = f"title={annotation['title']}"
        message = annotation["message"]
        print(f"::{severity_name} {file},{line},{end_line},{title}::{message}")

    def _print_epilogue(self, group_name=None):
        if group_name:
            print("::endgroup::")


class ConsoleFormat(BaseFormat):
    def _print_prologue(self, group_name=None):
        self._print(f"<header>{self._title}</header>")

    def _print_annotation(self, annotation):
        print("")
        file = annotation["file"]
        line = int(annotation["line"])
        end_line = int(annotation["end-line"])
        end_line = "" if end_line == line else f":{end_line}"
        location = f"  <location>{file}:{line}{end_line}</location>"
        self._print(location)
        # with open(filename, "r") as file:
        #     lines = file.readlines()
        #     line = lines[line_num - 1].rstrip("\n")
        #     line = style.print(f"<code>{line}</code>")
        #     print(line)
        severity_name = annotation["severity_name"]
        severity_len = " " * len(severity_name)
        if annotation["severity_name"] == "notice":
            severity_name = annotation["severity_name"]
            severity_name = f"<notice>{severity_name.capitalize()}:</notice>"
        if annotation["severity_name"] == "warning":
            severity_name = annotation["severity_name"]
            severity_name = f"<warning>{severity_name.capitalize()}:</warning>"
        if annotation["severity_name"] == "error":
            severity_name = annotation["severity_name"]
            severity_name = f"<error>{severity_name.capitalize()}:</error>"
        initial_indent = "      " + severity_len
        msg = annotation["message"]
        msg = textwrap.fill(
            msg, 79, initial_indent=initial_indent, subsequent_indent="    "
        )
        msg = msg.lstrip()
        self._print(f"    {severity_name} {msg}")
