# Distance Analysis Between Positions
Can you identify the stolen computer? Hopefully, it's the one that isn't near any of the other devices.

## Program overview
The program takes a file path as input and analyzes a JSON file. The data consists of computer names as keys and coordinates (latitude and longitude) as values. The program returns the name of the computer that is geographically not located near any other computer.

## How to run program
1. Open a terminal in the project directory
2. Run the following command to install the dependencies: `uv sync`
2. Run the file `solution.py` by the command `uv run solution.py`

## How to run tests
1. Open a terminal in the project directory
2. Run the following command to install the dependencies: `uv sync`
3. Run the file `solution.py` by the command `uv run pytest`

## Required Modules

```python
import json
from math import atan2, cos, degrees, radians, sin, sqrt

import pytest
```

## Example input

```python
path = "tracking.json"
LAVSKRIKA = 0.001

print(solution(path))
```
## Example output

```python
makar
```

`makar`  is the name of the stolen computer. 
- Location: Uppsala, Sweden
- Coordinates: 59.8586, 17.6391

## Treshold value

The threshold is set to 0.001 degrees, which corresponds to approximately 111 meters.
Calculation: `0.001 degrees × 111,000 meters = 111 meters`

If the threshold had been set to 0.0001, the distance would correspond to approximately 11 meters. This would be quite restrictive if legitimate computers, for example, were located in the same building or in nearby buildings. As a result, the program might identify more than one computer as isolated and raise an exception.

On the other hand, setting the threshold to 1 would correspond to approximately 111 kilometers, which would be too large a range. In that case, the program might fail to identify any isolated computer and raise an exception.

What should be considered "near" naturally depends on the circumstances and what is considered reasonable. For example, if a Swedish company has legitimate users spread across the entire country, a threshold of 111 meters would probably be too small. In that scenario, it might also be difficult to identify the stolen computer unless it had moved significantly farther away, perhaps even abroad.

### The Haversine Formula

I have implemented the Haversine formula in the helper function to ensure that the specified threshold always represents the same distance in meters, regardless of where on Earth the coordinates are located.

The calculation takes into account that the distance represented by one degree of longitude decreases as you move further north or south. Comparing latitude and longitude differences separately can otherwise produce misleading results, since one degree of longitude represents different distances depending on the latitude.

Without the Haversine formula, the method would also be unable to automatically recognize that two points located close to the boundary of ±180 degrees longitude are actually near each other.

The formula was developed with the help of the following resource:

- https://calculatingdistance.com/haversine-formula/

## Assumptions

1. The JSON data is structured as a dictionary containing computer names and their coordinates.
2. There is exactly one geographically isolated computer to identify. Otherwise, the program raises an exception.
3. All coordinate lists follow the order: latitude, longitude.
4. The threshold value is specified in degrees.

## Author

Lotta Reiman
