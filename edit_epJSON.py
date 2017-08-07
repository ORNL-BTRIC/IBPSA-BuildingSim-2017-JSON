
import json
import os

with open(os.path.join(os.path.dirname(__file__), "1ZoneUncontrolled.epJSON")) as f:
    input_file = json.load(f)

sun_exposure = input_file['BuildingSurface:Detailed']['Zn001:Flr001']['sun_exposure']

print(sun_exposure)

input_file['BuildingSurface:Detailed']['Zn001:Flr001']['sun_exposure'] = 'SunExposed'

with open(os.path.join(os.path.dirname(__file__), "1ZoneUncontrolled.epJSON")) as f:
    json.dump(input_file, f, sort_keys=True, indent=4)


