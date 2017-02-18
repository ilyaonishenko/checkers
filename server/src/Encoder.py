import json


class Encoder(json.JSONEncoder):
    def default(self, o):
        return o.__json__()
