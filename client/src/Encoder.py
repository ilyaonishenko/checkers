import json


class Encoder(json.JSONEncoder):
    def default(self, o):
        try:
            return o.__json__()
        except AttributeError:
            return json.JSONEncoder.default(self, o)
