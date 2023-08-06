from lxml import etree

from . import Handler


class XPathHandler(Handler):

    _root_node = None

    _default_set_dict = None

    _annotations = []

    def __init__(self, severities, config):
        super().__init__(severities, config)
        parser = etree.XMLParser(resolve_entities=False)
        self._root_node = etree.fromstring(input, parser)
        self._default_set_dict = self._config.get("set", {})

    def _set_value(self, match, set_dict, key):
        query = set_dict.get(key)
        if query is None:
            return None
        return match.xpath(query)[0]

    def _handle_match(self, rule, match, set_dict, annotation):
        for key in annotation:
            # TODO: Catch errors
            annotation[key] = self._set_value(match, set_dict, key)
        annotation["severity"] = rule.get("severity")
        if annotation not in self._annotations:
            self._annotations.append(annotation)

    def _annotate(self, input):
        for rule in self._rules:
            # TODO: Catch errors
            matches = self._root_node.xpath(rule["match"])
            set_dict = self._default_set_dict.copy()
            set_dict.update(rule.get("set", {}))
            annotation = self._template_annotation.copy()
            for match in matches:
                self._handle_match(rule, match, set_dict, annotation)
        return self._annotations
