from dataclasses import is_dataclass, asdict
import json
from datetime import datetime, date

class EnhancedJSONEncoder(json.JSONEncoder):
    def default(self, o):
        try:
            if is_dataclass(o):
                return asdict(o)
            if isinstance(o, (datetime, date)):
                return o.isoformat()
            return super().default(o)
        except TypeError:
            try:
                return o.__dict__
            except AttributeError:
                return None