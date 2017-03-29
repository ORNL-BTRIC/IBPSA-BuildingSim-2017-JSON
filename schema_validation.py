import json
import jsonschema
import os

with open(os.path.join(os.path.dirname(__file__), "1ZoneUncontrolled.jdf")) as f2:
    input_file = json.load(f2)

with open(os.path.join(os.path.dirname(__file__), "Energy+.jdd")) as f:
    schema = json.load(f)

jsonschema.validate(input_file, schema)
