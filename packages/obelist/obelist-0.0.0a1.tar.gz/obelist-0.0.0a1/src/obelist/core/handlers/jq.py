import json

import pyjq
from icecream import ic

from . import Handler


class JQHandler(Handler):

    _default_set_dict = None

    _annotations = []

    def __init__(self, severities, config):
        super().__init__(severities, config)
        self._default_set_dict = self._config.get("set", {})
        self._rules = self._config.get("rules", [])

    def _set_value(self, match, set_dict, key):
        query = set_dict.get(key)
        if query is None:
            return None
        value = pyjq.all(query, match)[0]
        if self._debug:
            ic(value)
        return value

    def _handle_match(self, rule, match, set_dict, annotation):
        if self._debug:
            ic(match)
        annotation = annotation.copy()
        for key in annotation:
            # TODO: Catch errors
            annotation[key] = self._set_value(match, set_dict, key)
        annotation["severity"] = rule.get("severity")
        if annotation not in self._annotations:
            self._annotations.append(annotation)

    def _annotate(self, input):
        # TODO: Catch errors
        input = self._decode(input)
        json_dict = json.loads(input)
        for rule in self._rules:
            # TODO: Catch errors
            matches = pyjq.all(rule["match"], json_dict)
            set_dict = self._default_set_dict.copy()
            set_dict.update(rule.get("set", {}))
            annotation = self._template_annotation.copy()
            for match in matches:
                self._handle_match(rule, match, set_dict, annotation)
        return self._annotations
