import re

import charset_normalizer
from lxml import etree
import json
import pyjq

from .. import errors


class Handler:

    _format = {}

    _match_attrs = {}

    _severities = []

    def __init__(self, format):
        self._format = format
        severities = self._format["severities"]
        self._match_attrs = self._format["match-attrs"]
        for severity_name in severities:
            severity = severities.get(severity_name)
            self._severities.append(severity)

    def _decode(self, bytes):
        # TODO: Catch encoding errors
        charset_data = charset_normalizer.from_bytes(bytes).best()
        return str(charset_data)

    def annotate(self, input):
        raise errors.NotImplementedError


class RegexHandler(Handler):
    def __init__(self, format):
        super().__init__(format)
        # Compile regular expressions (and catch any errors)
        for severities in self._severities:
            # TODO: Catch errors
            match = severities["match"]
            severities["match_re"] = re.compile(match)

    def _get_match(self, line):
        for severity in self._severities:
            return severity["match_re"].search(line)

    def _get_matches(self, input):
        matches = []
        input_lines = input.strip().splitlines()
        for line in input_lines:
            line = line.rstrip("\n")
            match = self._get_match(line)
            if match:
                matches.append(match)
        return matches

    def _add_file(self, match_attrs, match, annotation):
        file = match_attrs["file"]
        match_groupdict = match.groupdict()
        if match_groupdict:
            file = file.format(**match_groupdict)
        match_groups = match.groups()
        if match_groups:
            file = file.format(*match_groups)
        annotation["file"] = file
        return annotation

    def _add_line(self, match_attrs, match, annotation):
        line = match_attrs["line"]
        match_groupdict = match.groupdict()
        if match_groupdict:
            line = line.format(**match_groupdict)
        match_groups = match.groups()
        if match_groups:
            line = line.format(*match_groups)
        annotation["line"] = line
        return annotation

    def _add_end_line(self, match_attrs, match, line, annotation):
        end_line = match_attrs.get("end-line", line)
        if end_line == line:
            return annotation
        match_groupdict = match.groupdict()
        if match_groupdict:
            end_line = line.format(**match_groupdict)
        match_groups = match.groups()
        if match_groups:
            end_line = line.format(*match_groups)
        annotation["end-line"] = end_line
        return annotation

    def _add_title(self, match_attrs, match, annotation):
        title = match_attrs["title"]
        match_groupdict = match.groupdict()
        if match_groupdict:
            title = title.format(**match_groupdict)
        match_groups = match.groups()
        if match_groups:
            title = title.format(*match_groups)
        annotation["title"] = title
        return annotation

    def _add_message(self, match_attrs, match, annotation):
        message = match_attrs["message"]
        match_groupdict = match.groupdict()
        if match_groupdict:
            message = message.format(**match_groupdict)
        match_groups = match.groups()
        if match_groups:
            message = message.format(*match_groups)
        annotation["message"] = message
        return annotation

    def _create_annotation(self, matcher, match, line):
        annotation = {"severity_name": matcher["severity_name"]}
        match_attrs = matcher.get("match-attrs", self._match_attrs)
        annotation = self._add_file(match_attrs, match, annotation)
        annotation = self._add_line(match_attrs, match, annotation)
        annotation = self._add_end_line(match_attrs, match, line, annotation)
        annotation = self._add_title(match_attrs, match, annotation)
        annotation = self._add_message(match_attrs, match, annotation)

    def _get_annotations(self, matches):
        annotations = []
        # TODO: Handle exceptions when a user tries to use positional and named
        # groups simultaneously
        for line, matcher, match in matches:
            annotation = self._create_annotation(matcher, match, line)
            annotations.append(annotation)
        return annotations

    def annotate(self, input):
        input = self._decode(input)
        matches = self._get_matches(input)
        return self._get_annotations(matches)


class XPathHandler(Handler):
    def annotate(self, input):
        annotations = []
        root = etree.fromstring(input)
        for severity in self._severities:
            matches = root.xpath(severity["match"])
            match_attrs = severity.get("match-attrs", self._match_attrs)
            for match in matches:
                annotation = {}
                # TODO: Catch errors
                file = match_attrs["file"]
                line = match_attrs["line"]
                end_line = match_attrs.get("line", line)
                title = match_attrs["title"]
                message = match_attrs["message"]
                # TODO: Catch errors
                annotation["severity_name"] = severity["severity_name"]
                annotation["file"] = match.xpath(file)[0]
                annotation["line"] = match.xpath(line)[0]
                annotation["end-line"] = match.xpath(end_line)[0]
                annotation["title"] = match.xpath(title)[0]
                annotation["message"] = match.xpath(message)[0]
                annotations.append(annotation)
        return annotations


class JQHandler(Handler):
    def annotate(self, input):
        annotations = []
        input = self._decode(input)
        json_dict = json.loads(input)
        for severity in self._severities:
            matches = pyjq.all(severity["match"], json_dict)
            match_attrs = severity.get("match-attrs", self._match_attrs)
            for match in matches:
                annotation = {}
                # TODO: Catch errors
                file = match_attrs["file"]
                line = match_attrs["line"]
                end_line = match_attrs.get("line", line)
                title = match_attrs["title"]
                message = match_attrs["message"]
                # TODO: Catch errors
                annotation["severity_name"] = severity["severity_name"]
                annotation["file"] = pyjq.all(file, match)[0]
                annotation["line"] = pyjq.all(line, match)[0]
                annotation["end-line"] = pyjq.all(end_line, match)[0]
                annotation["title"] = pyjq.all(title, match)[0]
                annotation["message"] = pyjq.all(message, match)[0]
                annotations.append(annotation)
        return annotations
