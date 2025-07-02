import json
from types import SimpleNamespace

def parse_filters(data: json):
    return json.loads(data, object_hook=lambda d: SimpleNamespace(**d))
