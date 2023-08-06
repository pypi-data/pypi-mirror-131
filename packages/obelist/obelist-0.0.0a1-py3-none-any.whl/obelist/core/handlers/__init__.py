import re

import charset_normalizer

from ... import errors


class Handler:

    _severities = None
    _config = None

    _debug = False

    _rules = []
    _rewrites = []

    _template_annotation = {
        "filename": None,
        "line": None,
        "end_line": None,
        "code": None,
        "severity": None,
        "message": None,
    }

    def __init__(self, severities, config):
        self._severities = severities
        self._config = config
        self._rules = config.get("rules", {})
        self._rewrites = config.get("rewrite", {})
        for rules in self._rewrites.values():
            # Compile regular expressions (and catch any errors)
            for rule in rules:
                # TODO: Catch errors
                match = rule["match"]
                rule["match_re"] = re.compile(match)

    # self._input_rules = self._format["input"]
    # severities = self._format["severities"]
    # self._match_attrs = self._format["match-attrs"]
    # for severity_name in severities:
    #     severity = severities.get(severity_name)
    #     self._severities.append(severity)

    def _decode(self, bytes):
        # TODO: Catch encoding errors
        charset_data = charset_normalizer.from_bytes(bytes).best()
        return str(charset_data)

    def _handle_rewrites(self, annotation):
        for key, rules in self._rewrites.items():
            for rule in rules:
                value = str(annotation[key])
                # TODO: Handle errors
                new_value = rule["match_re"].sub(rule["replace"], value)
                annotation[key] = new_value

    def _validate_severity(self, annotation):
        severity = annotation["severity"]
        if severity not in self._severities:
            severities = ", ".join(self._severities)
            message = (
                f"Invalid severity: {severity}\n\n"
                + f"Available severities: {severities}"
            )
            raise errors.ConfigurationError(message=message)

    def _annotate(self, input):
        pass

    def annotate(self, input, debug):
        self._debug = debug
        annotations = self._annotate(input)
        # We do this validation last because the user can modify the severity
        # at any stage before now
        for annotation in annotations:
            self._handle_rewrites(annotation)
            self._validate_severity(annotation)
        return annotations
