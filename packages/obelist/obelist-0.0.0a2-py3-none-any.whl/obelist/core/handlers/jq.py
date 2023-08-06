import json

import pyjq
from icecream import ic

from . import Handler


class JQHandler(Handler):
    def _set_value(self, match, set_dict, key):
        query = set_dict.get(key)
        if query is None:
            return None
        value = pyjq.all(query, match)[0]
        if self._debug:
            ic(value)
        return value

    def _annotate(self, input):
        # TODO: Catch errors
        input = self._decode(input)
        json_dict = json.loads(input)

        def matches_fn(query):
            return pyjq.all(query, json_dict)

        self._generate_matches(matches_fn)
        return self._annotations
