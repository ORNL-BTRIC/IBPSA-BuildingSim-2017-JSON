# IBPSA-BuildingSim-2017-JSON

#### General thoughts

* **EnergyPlus 8.8** : epJSON input will be used internally and as experimental input (to allow for schema changes and user feedback around key names)

* **EnergyPlus 8.9** : epJSON becomes 1st class citizen along with IDF.

* **EnergyPlus 9.0 - 9.3** : deprecate IDF input (add deprecation notices to documentation, warning message from command line when using IDF, and compile warnings), but still have automatic translation within EnergyPlus

* **EnergyPlus 10.0** : remove IDF input, freeze IDD/IDF, and move translation program out of EnergyPlus

* This should minimize impact on existing IDF workflows and provide three years for users/companies to transition.

### Command line

IDF input (with epJSON converted output)

`./energyplus -c -d Outputs/ -w USA_IL_Chicago-OHare.Intl.AP.725300_TMY3.epw 1ZoneUncontrolled.idf`

epJSON input (with IDF converted output)

`./energyplus -c -d Outputs/ -w USA_IL_Chicago-OHare.Intl.AP.725300_TMY3.epw 1ZoneUncontrolled.epJSON`

### Run example programs

Run schema validation example python script

`python schema_validation.py`

Run bad schema validation example python script

`python schema_validation_bad.py`

Load, edit, and save epJSON example python script

`python edit_epJSON.py`

### Example IDF/epJSON

IDF
```
BuildingSurface:Detailed,
  Zn001:Flr001,            !- Name
  Floor,                   !- Surface Type
  FLOOR,                   !- Construction Name
  ZONE ONE,                !- Zone Name
  Adiabatic,               !- Outside Boundary Condition
  ,                        !- Outside Boundary Condition Object
  NoSun,                   !- Sun Exposure
  NoWind,                  !- Wind Exposure
  1.000000,                !- View Factor to Ground
  4,                       !- Number of Vertices
  15.24000,0.000000,0.0,  !- X,Y,Z ==> Vertex 1 {m}
  0.000000,0.000000,0.0,  !- X,Y,Z ==> Vertex 2 {m}
  0.000000,15.24000,0.0,  !- X,Y,Z ==> Vertex 3 {m}
  15.24000,15.24000,0.0;  !- X,Y,Z ==> Vertex 4 {m}
```

epJSON
```
{
  "BuildingSurface:Detailed": {
    "Zn001:Flr001": {
      "construction_name": "FLOOR",
      "number_of_vertices": 4,
      "outside_boundary_condition": "Adiabatic",
      "outside_boundary_condition_object": "",
      "sun_exposure": "NoSun",
      "surface_type": "Floor",
      "vertices": [
        {
          "vertex_x_coordinate": 15.24,
          "vertex_y_coordinate": 0.0,
          "vertex_z_coordinate": 0.0
        },
        {
          "vertex_x_coordinate": 0.0,
          "vertex_y_coordinate": 0.0,
          "vertex_z_coordinate": 0.0
        },
        {
          "vertex_x_coordinate": 0.0,
          "vertex_y_coordinate": 15.24,
          "vertex_z_coordinate": 0.0
        },
        {
          "vertex_x_coordinate": 15.24,
          "vertex_y_coordinate": 15.24,
          "vertex_z_coordinate": 0.0
        }
      ],
      "view_factor_to_ground": 1,
      "wind_exposure": "NoWind",
      "zone_name": "ZONE ONE"
    }
}
```

#### epJSON performance gains
The table below shows this speed up for two different files; one reference building and one worst case input with an extreme number of surfaces (45,382 in 80 zones vs 871 in 118 zones). The table also shows the speed up in ProcessInput, parsing input, and parsing schema.

These numbers are probably conservative now (doesn't include embedded schema, etc)

|  | Outpatient |  |  | prj10 |  |  |
| :-: | :-: | :-: | :-: | :-: | :-: | :-: |
|  | E+ 8.5 Release | PR - IDF | PR - JSON | E+ 8.5 Release | PR - IDF | PR - JSON |
| ProcessInput | 366 | 300 (18%) | 234 (36%) | 4322 | 3355 (22%) | 1637 (62%) |
| GetSurfaceData | 28 | 13 (54%) | 13 (54%) | 72688 | 21001 (71%) | 21001 (71%) |
| GetObjectItem | 38 | 29 (24%) | 29 (24%) | 41617 | 333 (99.2%) | 333 (99.2%) |
| VerifyName | 2 | 0 (100%) | 0 (100%) | 11055 | 5 (99.9%) | 5 (99.9%) |
| Parse IDF | 174 | 135 (22%) | 69 (60%) | 4130 | 3190 (23%) | 1472 (64%) |
| Parse IDD | 192 | 165 (14%) | 165 (14%) | 192 | 165 (14%) | 165 (14%) |


#### JSON Outputs

* JSON outputs for Tabular and Timeseries outputs
* Outputs separate files:
  * detailed_zone
  * detailed_HVAC
  * timestep
  * hourly
  * daily
  * monthly
  * runperiod
* Can output CBOR and MessagePack binary formats
  * 71% and 50% size reductions compared to JSON and CSV respectively
* Intended for 8.8 release (dependent on JSON input)
* Eventually it can replace ESO, CSV, etc but that is open to discussion

```
Output:JSON,
       \memo Output from EnergyPlus can be written to JSON format files.
       \unique-object
  A1 , \field Option Type
       \required-field
       \type choice
       \key TimeSeries
       \key TimeSeriesAndTabular
  A2 , \field Output JSON
       \type choice
       \key Yes
       \key No
       \default Yes
  A3 , \field Output CBOR
       \type choice
       \key Yes
       \key No
       \default No
  A4 ; \field Output MessagePack
       \type choice
       \key Yes
       \key No
       \default No
```

```
Running the Outpatient Reference Model for an annual simulation has the following file sizes:

eplusout.mtr - 2.1M
eplusmtr.csv - 1.6M
eplusout.eso - 31M
eplusout.csv - 24M
eplusout.sql - 31M

eplusout_hourly.json - 42M
eplusout_hourly.cbor - 12M (~71% reduction to JSON, 50% compared to CSV)

eplusout.json - 5.0M
eplusout.cbor - 1.2M (76% reduction)
```
