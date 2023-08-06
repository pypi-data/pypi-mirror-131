import os
import pathlib

from operator import itemgetter

from .. import errors

from . import query
from . import format


class Parser:

    _app = None
    _config = None

    _input = None

    _format = None
    _query_language = None
    _severities = None

    _regex_matchers = []
    _annotations = []

    _severity_levels = ["notice", "warning", "error"]

    _highest_severity = 0

    _log_group = ""

    _error_severity = 0

    def __init__(self, app, config):
        self._app = app
        self._config = config

    def _read_config(self, format):
        # TODO: Move this to a command-line option
        self._log_group = self._config.get("log-group")

        formats = self._config.get("formats")
        self._format = formats.get(format)
        self._query_language = self._format.get("syntax")
        self._severities = self._format.get("severities")

        for severity_level, severity_name in enumerate(self._severity_levels):
            severity = self._severities.get(severity_name)
            if severity:
                severity["severity_name"] = severity_name
                severity["severity_level"] = severity_level

    # TODO: Introduce annotation classes to handle this
    def _make_annotations(self):
        if self._query_language == "regex":
            query_handler = query.RegexHandler(self._format)
            annotations = query_handler.annotate(self._input)
            return annotations
        if self._query_language == "xpath":
            query_handler = query.XPathHandler(self._format)
            annotations = query_handler.annotate(self._input)
            return annotations
        if self._query_language == "jq":
            query_handler = query.JQHandler(self._format)
            annotations = query_handler.annotate(self._input)
            return annotations
        raise errors.NotImplementedError()

    def parse(self, input, format):
        # TODO: Figure out a better way to check for this
        if not self._app._quiet and input.name == "<stdin>":
            # Figure out how to do this with the logging plugin for Click
            print("Reading from standard input...")
        self._input = input.read()
        self._read_config(format)
        self._annotations = self._make_annotations()

    def _process_annotations(self, sort_by):
        annotations = self._annotations
        for annotation in annotations:
            severity_name = annotation["severity_name"]
            try:
                severity_level = self._severity_levels.index(severity_name)
            except ValueError:
                severity_level = 0
            annotation["severity_level"] = severity_level
            if severity_level > self._highest_severity:
                self._highest_severity = severity_level
            file = pathlib.Path(annotation["file"])
            annotation["file"] = file.relative_to(".")
        if sort_by == "file":
            for annotation in annotations:
                file = annotation["file"]
                line = annotation["line"]
                end_line = annotation.get("end-line")
                if end_line == line:
                    end_line = ""
                elif end_line is not None:
                    end_line = f":{end_line}"
                annotation["location"] = f"{file}:{line}:{end_line}"
            annotations = sorted(annotations, key=itemgetter("location"))
        if sort_by == "severity":
            severity_levels = []
            severity_levels.sort()
            annotations = sorted(
                annotations, key=itemgetter("severity_level"), reverse=True
            )
        return annotations

    def _get_status_code(self, error_on):
        try:
            error_on_severity = self._severity_levels.index(error_on)
        except ValueError as err:
            raise errors.ConfigurationError(
                message=f"Invalid severity name: {error_on}"
            )
        status_code = 0
        if (
            self._highest_severity is not None
            and self._highest_severity >= error_on_severity
        ):
            status_code = 100 + self._highest_severity
        return status_code

    def print(self, sort_by, error_on):
        annotations = self._process_annotations(sort_by)
        title = self._config["title"]
        if self._app._verbose:
            report = format.ConsoleFormat(title, annotations)
            report.print()
        if os.environ.get("GITHUB_ACTIONS") == "true":
            report = format.CommandFormat(title, annotations)
            report.print(self._log_group)
        return self._get_status_code(error_on)
