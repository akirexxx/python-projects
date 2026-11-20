import json
from math import atan2, cos, degrees, radians, sin, sqrt

import pytest

path = "tracking.json"

# -------- THRESHOLD: 0.001 degrees, which is approximately 111 meters -------
# Considered a reasonable distance for defining the same location, e.g. within 
# the same or nearby buildings.

TRESHOLD = 0.001

def solution(path):
    """Identifies the geographically isolated computer with no nearby neighboring computers.

    Parameters:
        path: The path to the current JSON file.

    Returns:
        str: The name of the isolated computer.

    Raises:
        TypeError: If the loaded data has an invalid format.
        ValueError: If the loaded data contains an incorrect number of values
            or if the program does not find exactly one isolated computer.
    """

    har_grannar = {}

    with open(path, encoding="utf-8") as file:
        content = json.load(file)

    # Validates input data to prevent errors in comparisons and function calls.
    if not isinstance(content, dict):
        raise TypeError("JSON-innehållet måste vara en dictionary. ")

    for namn, position in content.items():
        if not isinstance(position, list):
            raise TypeError(f"Positionen: [{position}] måste vara en lista. ")

        # JSON converts the key to a string.
        elif namn.isdigit():
            raise TypeError(f"Datornamnet: [{namn}] får inte enbart bestå av siffror. ")

        elif not all(isinstance(coordinate, int | float) for coordinate in position):
            raise TypeError("Koordinaterna får endast innehålla: float | int")

        elif len(position) != 2:
            raise ValueError(f"[{position}] måste vara två värden. (ärende RANSOM-3F)")

    # The list is expected to contain 'computer1': neighbor1, neighbor2 [...]
    for namn in content:
        har_grannar[namn] = []

    # Nested for-loop that compares one computer's position with the remaining computers
    for index_a, (namn_a, position_a) in enumerate(content.items()):
        for index_b, (namn_b, position_b) in enumerate(content.items()):

            # Each computer is compared with every other computer only once
            if index_a >= index_b:
                continue

            resultat = help_solution(position_a, position_b)

            # If computer_a has computer_b as a neighbor, the reverse also applies
            if resultat:
                har_grannar[namn_a].append(namn_b)
                har_grannar[namn_b].append(namn_a)

    ensamma = []

    # Find the computer without any neighbors
    for namn, grannar in har_grannar.items():
        if len(grannar) == 0:
            ensamma.append(namn)

    if len(ensamma) == 0:
        raise ValueError("Ingen ensam dator hittades. (ärende RANSOM-3F)")
    elif len(ensamma) > 1:
        raise ValueError("Fler än en dator hittades ensam. (ärende RANSOM-3F)")

    return ensamma[0]


def help_solution(position_a, position_b, treshold=TRESHOLD):
    """Determines whether two positions are close to each other based on a constant.

    Parameters:
        position_a, position_b: Validated lists containing float | int values,
            in the following order: latitude, longitude.

    Returns:
        bool: True if the coordinate difference is within the threshold,
            otherwise False.
    """

    latitud_a, longitud_a = position_a
    latitud_b, longitud_b = position_b

    # The formula requires converting the coordinates to radians
    lat_a = radians(latitud_a)
    lon_a = radians(longitud_a)
    lat_b = radians(latitud_b)
    lon_b = radians(longitud_b)

    diff_latitud = abs(lat_a - lat_b)
    diff_longitud = abs(lon_a - lon_b)

    # The Haversine formula calculates the distance while accounting for the Earth's curvature
    haversine_value = sin(diff_latitud / 2)**2 + cos(lat_a) * cos(lat_b) * sin(diff_longitud / 2)**2
    central_angle = 2 * atan2(sqrt(haversine_value), sqrt(1 - haversine_value))

    gradavstand = degrees(central_angle)

    return gradavstand <= treshold
    

if __name__ == "__main__":
    print(solution(path))
