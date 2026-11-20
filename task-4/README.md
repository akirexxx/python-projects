# Find the culprit
Investigate the evidence, identify which suspect had access to the room where the stolen computer was located, and determine who is most likely responsible for the theft.

## Program overview

The program returns the name of the person from the list of suspects who had access to the room where the stolen computer was located.

The program uses four classes: Room, User, Status, and NoUniqueCulprit. It reads the room list, retrieves and validates the list of users from the internet, and eliminates suspects who do not have access to the room containing the stolen computer. The web request is also logged to a file.

All methods are brought together and called from the `solution()` function, which also generates a report.

## Required Modules

```python
import csv
import logging
from dataclasses import dataclass
from enum import Enum

import requests
from requests.exceptions import RequestException
```

## How to run program
1. Open a terminal in the project directory
2. Run the following command to install the dependencies: `uv sync`
2. Run the file `solution.py` by the command `uv run solution.py`

## How to run tests
1. Open a terminal in the project directory
2. Run the following command to install the dependencies: `uv sync`
3. Run the file `solution.py` by the command `uv run pytest`

## Example input

```python
skyldig = solution()
print(f"\nDen skyldige är: {skyldig}")
```

## Example output

```python
The culprit is: Robert Bennett
```

## Constants

```python
SUSPECTS: list[str] = ["id001", "id009", "id007", "id015"]
COMPUTER: str = "makar"
TALLBIT: str = "https://gist.github.com/Grokzen/11ddfa83c0f0d379d33d7abbfdd1c77e/raw"

REQUIRED_KEYS: list[str] = ["id", "name", "access"]

TITLES: list[str] = ["Room", "Computer"]
TITLE_ROOM, TITLE_COMPUTER = TITLES

REPORT_TITLES: list[str] = ["id", "namn", "access", "status"]
RAPPORT: str = "rapport.csv"

LOGGING_FILE: str = "logging.log"

PATH_ROOMS: str = "rooms.csv"
```

## Generated files

The program creates the following files during its first run and writes to them on subsequent runs:
- **logging.log** - Append to each time the program runs
- **rapport.csv** - Overwritten each time the program runs 

## Assumptions

1. There is exactly one culprit to identify. Otherwise, the program raises an exception.
2. The room list is a CSV file containing the required headers, which are subsequently used as dictionary keys.
3. There is at least one computer in each room, but the room list does not need to be sorted.
4. All room names follow the format: room-floor-number.
5. The JSON data retrieved from the internet is a list[dict] containing the required keys.
6. Floor numbers and room numbers start at 1.
7. An active internet connection is available.

## Analysis

### Adding a new room

If a new room is added to the building without updating the users' access permissions, the `user.has_access()` method raises an exception.

This is because the method checks that the length of the access string matches the total number of rooms when determining whether a user has access to a particular room.

Without this check, the user's permissions would theoretically remain correct up to the newly added room, but the positions of the permissions would become misaligned from that point onwards. As a result, the program would be unable to determine access to the last room because the corresponding 1 or 0 would be missing.

### Data retrieved from the Internet

The website from which the data is retrieved is outside our control. URLs pointing to external sources may become unavailable or the content may be moved to a different location. This could cause the code to stop working as intended over time.

Data validation is essential, as we do not want to process manipulated or malicious data. Incorrectly formatted data could cause the program to crash or perform unintended operations. From a security perspective, insufficient validation could allow an attacker to exploit weaknesses in the program's data handling.

The `load_users()` function aborts the request and raises an exception if the server takes longer than five seconds to respond. Without a timeout, there is a risk that the program could hang while waiting for a response. In theory, the program could wait indefinitely, potentially tying up resources and making the program unavailable. From a security perspective, this can be related to a Denial of Service (DoS) attack, where a system is deliberately overloaded to make it unavailable.

The `raise_for_status()` method has a built-in check that detects unsuccessful HTTP responses: 4xx (client errors) and 5xx (server errors). If the status code is 2xx (successful), the method does nothing.

`RequestException` is the parent class of exceptions raised during requests, such as HTTPError, Timeout, and `ConnectionError`. Instead of creating separate except blocks for each possible scenario, I chose to use `RequestException`, which catches all of these errors. The specific error message is also captured in this block and written to the logging file.

Errors unrelated to network communication are intended to be handled by ValueError if the JSON data is invalid. The program's error handling is therefore designed to handle most unexpected interruptions and provide the user with an appropriate error message.


