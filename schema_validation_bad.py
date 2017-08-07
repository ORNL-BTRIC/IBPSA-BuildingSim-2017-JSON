import json
import jsonschema
import os

with open(os.path.join(os.path.dirname(__file__), "1ZoneUncontrolled_bad.epJSON")) as f2:
    input_file = json.load(f2)

with open(os.path.join(os.path.dirname(__file__), "Energy+.schema.epJSON")) as f:
    schema = json.load(f)

jsonschema.validate(input_file, schema)
