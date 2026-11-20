import csv
import logging
from dataclasses import dataclass
from enum import Enum

import requests
from requests.exceptions import RequestException

# Suspect IDs who left the data center on the 14th between 13:00 and 18:00
SUSPECTS: list[str] = ["id001", "id009", "id007", "id015"]

# Name of the stolen computer.
COMPUTER: str = "makar"

# URL-source of users
TALLBIT: str = "https://gist.github.com/Grokzen/11ddfa83c0f0d379d33d7abbfdd1c77e/raw"

# Required keys for the `parse_users` method
REQUIRED_KEYS: list[str] = ["id", "name", "access"]

# Required keys for the `load_rooms` method
TITLES: list[str] = ["Room", "Computer"]
TITLE_ROOM, TITLE_COMPUTER = TITLES

# Output headers for the `write_report` method
REPORT_TITLES: list[str] = ["id", "namn", "access", "status"]

# Files created during the first run
RAPPORT: str = "rapport.csv"
LOGGING_FILE: str = "logging.log"
logger = logging.getLogger(__name__)

PATH_ROOMS: str = "rooms.csv"


# @dataclass automatically generates __init__(), __repr__(), and __eq__()
# frozen=True enables duplicate checking through __hash__()
@dataclass(frozen=True)
class Room:
    """Represents a room in the building."""

    name: str

    def __post_init__(self) -> None:
        """Validates data before a Room object is created.

        Raises ValueError if the attribute value has an invalid format.
        """

        # Avoids repeated error handling in other parts of the program
        delar = self.delar
        if len(delar) != 3:
            raise ValueError("Rumsnamnet är inte tre fält. ")

        if delar[0] != "room":
            raise ValueError("Rumsnamnet börjar inte med 'room'. ")

        if not delar[1].isdecimal() or int(delar[1]) < 1:
            raise ValueError("Våningen är inte ett tal >= 1. ")

        if not delar[2].isdecimal() or int(delar[2]) < 1:
            raise ValueError("Rumsnumret är inte ett tal >= 1. ")

    @property
    def delar(self) -> list[str]:
        """Splits the room name at '-' and returns the parts as a list."""
        return self.name.split("-")

    @property
    def floor(self) -> int:
        """Returns the floor number as an integer."""
        return int(self.delar[1])

    @property
    def number(self) -> int:
        """Returns the room number as an integer."""
        return int(self.delar[2])

    def __str__(self) -> str:
        """Returns the room name as the string representation of the object."""
        return self.name


@dataclass
class User:
    """Represents a user with attributes."""

    id: str
    name: str
    access: str

    # Avoids repeated error handling in other parts of the program
    def __post_init__(self) -> None:
        """Validates data before a User object is created.

        Raises ValueError if an attribute value has an invalid format.
        """

        if not isinstance(self.id, str):
            raise ValueError("ID är inte en sträng. ")

        if not isinstance(self.name, str) or self.name.isdigit():
            raise ValueError("Namnet är inte en textsträng. ")

        if not all(char in "01" for char in self.access):
            raise ValueError("Access får bara innehålla 0-1. ")

    def __str__(self) -> str:
        """Represents the object when printed: name (id)."""

        return f"{self.name} ({self.id})"

    def has_access(self, room: str | Room, rooms: dict[str, Room] | list[Room]) -> bool:
        """Determines whether a user has access to a room.

        Parameters:
            room: A string or Room object, <room-floor-number>
            rooms: A dictionary with computer names as keys and Room objects 
                as values, or a list of Room objects.

        Returns:
            True if the user has access, otherwise False.

        Raises:
            ValueError: If the room does not exist or the access string has 
                an invalid length.
        """

        if isinstance(rooms, dict):
            rooms = list(rooms.values())

        unique = set(rooms)
        sorted_rooms = sorted(unique, key=lambda room: (room.floor, room.number))

        room_object = room if isinstance(room, Room) else Room(room)

        if room_object not in sorted_rooms:
            raise ValueError(f"Rummet finns inte i rumslistan: '{room_object}'. ")

        if len(self.access) != len(sorted_rooms):
            raise ValueError("Access inte samma längd som antal rum. ")

        index_room = sorted_rooms.index(room_object)
        return self.access[index_room] == "1"


class NoUniqueCulpritError(Exception):
    """Custom exception raised when no unique culprit is found."""

    def __init__(self, message: str) -> None:
        """Initializes the exception and adds an additional reference message."""

        super().__init__(f"{message} --(ärende RANSOM-4K)")


def parse_users(data: list[dict]) -> list[User]:
    """Checks that the data is a list[dict] with the required keys
        and creates User objects.

    Parameter:
        data: Unvalidated data retrieved from the web.

    Returns:
        list[User]: A validated list of User objects.

    Raises:
        ValueError: If required keys are missing or the data 
            has an invalid format.
    """

    if not isinstance(data, list):
        raise ValueError("Datan är inte en lista. ")

    users = []

    for row, element in enumerate(data):
        if not isinstance(element, dict):
            raise ValueError(f"Är inte en dictionary, fel på rad {row}. ")
        for key in REQUIRED_KEYS:
            if key not in element:
                raise ValueError(
                    f"Obligatorisk nyckel saknas: {key}, fel på rad: {row}. "
                )

        id = element.get("id")
        name = element.get("name")
        access = element.get("access")

        if not isinstance(id, str):
            raise ValueError(f"ID är inte en sträng, fel på rad: {row}")
        if not isinstance(name, str):
            raise ValueError(f"Namn är inte en sträng, fel på rad: {row}")
        if not isinstance(access, str):
            raise ValueError(f"Access är inte en sträng, fel på rad: {row}")

        # The User class validates the values of the keys
        user_object = User(
            id=element["id"], name=element["name"], access=element["access"]
        )
        users.append(user_object)
    return users


def load_rooms(path: str) -> dict[str, Room]:
    """Takes a file path, reads a CSV file, validates the headers,
        and creates a dictionary containing Room objects.

    Parameter:
        path: The path to the current file.

    Returns:
        dict: A dictionary with computer names as keys and
            Room objects as values.

    Raises:
        ValueError: If the file does not contain the correct headers.
    """

    rooms = {}

    with open(path, "r", newline="", encoding="utf8") as file:
        content = csv.DictReader(file)

        if TITLES != content.fieldnames:
            raise ValueError(f"Fel rubriker, förväntade rubriker: {TITLES}")

        # The Room class validates the values
        for element in content:
            room_name = element[TITLE_ROOM]
            computer_name = element[TITLE_COMPUTER]
            room_object = Room(room_name)
            rooms[computer_name] = room_object
    return rooms


def find_culprit(
    suspects: list[str],
    computer: str,
    users: list[User],
    computer_rooms: dict[str, Room],
) -> User:
    """Finds the culprit who stole the computer.

    Parameters:
        suspects: A list of IDs belonging to suspected users.
        computer: The name of the stolen computer.
        users: A list of User objects.
        computer_rooms: A room dictionary with {computer name (str): 
            room name (Room)}.

    Returns:
        User: The User object representing the culprit.

    Raises:
        ValueError: If the computer does not exist.
        NoUniqueCulpritError: If a unique culprit cannot be identified.
    """

    if computer not in computer_rooms:
        raise ValueError("Datorn finns inte i rumslistan.")

    found_suspects = []
    stolen_room = computer_rooms[computer]

    for user in users:
        if user.id not in suspects:
            continue
        if user.has_access(stolen_room, computer_rooms):
            found_suspects.append(user)

    if len(found_suspects) > 1:
        raise NoUniqueCulpritError(f"Flera misstänkta hittades: {found_suspects}")
    elif len(found_suspects) < 1:
        raise NoUniqueCulpritError("Ingen misstänkt hittades.")

    return found_suspects[0]


class Status(Enum):
    """Represents the status in the report."""

    HAR_ACCESS = "har\u2009access"
    SAKNAR_ACCESS = "saknar\u202faccess"

    @staticmethod
    def check_access(has_access: bool) -> str:
        """Returns a text string depending on the access status."""

        if has_access:
            return Status.HAR_ACCESS.value
        return Status.SAKNAR_ACCESS.value


def write_report(
    path: str,
    suspects: list[str],
    computer: str,
    users: list[User],
    computer_rooms: dict[str, Room],
) -> None:
    """Writes a report to a CSV file containing suspected users
        and whether they had access to the room containing the stolen computer.

    Parameters:
        path: The name of the report file.
        suspects: A list of IDs belonging to suspected users.
        computer: The name of the stolen computer.
        users: A list of User objects.
        computer_rooms: A room dictionary with 
            {computer name (str): room name (Room)}.

    Raises:
        ValueError: If the computer is missing from the room list.
    """

    stolen_room = computer_rooms.get(computer)

    if stolen_room is None:
        raise ValueError("Datorn finns inte i rumslistan. ")

    with open(path, "w", newline="", encoding="utf-8") as fil:
        rapport = csv.writer(fil)
        rapport.writerow(REPORT_TITLES)

        # Maps string IDs in suspects to User objects
        users_dict = {user.id: user for user in users}

        for sus_id in suspects:
            user = users_dict.get(sus_id)
            if user is None:
                continue
            status = Status.check_access(user.has_access(stolen_room, computer_rooms))
            rapport.writerow([user.id, user.name, user.access, status])


def load_users(url: str) -> list[dict]:
    """Calls the URL, retrieves JSON data containing users,
        and logs the request attempts to a log file.

    Parameter:
        url: A parameter containing a URL.

    Returns:
        list: The unvalidated data.

    Raises:
        RuntimeError: If the request fails due to 4xx or 5xx status codes.
        ValueError: If the JSON data cannot be parsed.
    """

    try:
        svar = requests.get(url, timeout=5)
        svar.raise_for_status()
        users = svar.json()
        logger.info("Anropet lyckades. ")
        return users

    except RequestException as error:
        logger.error(f"Anropet misslyckades: {error}")
        raise RuntimeError(
            "Kunde inte hämta användarna från webben. "
            "Kontrollera din internetanslutning. "
        ) from error

    except ValueError as error:
        logger.error(f"Kunde inte tolka JSON: {error}")
        raise ValueError(
            "Kunde inte tolka JSON-datan. Kontrollera URL-källan. "
        ) from error
    finally:
        logger.info("Anropningsförsök har gjorts. ")


def solution() -> str:
    """Coordinates all functions to identify the culprit.

    The function calls the program's functions step by step:
        1. Loads the room list from a CSV file using `load_rooms`.
        2. Retrieves users from the web using `load_users`.
        3. Logs the request attempt, whether successful or unsuccessful, to a log file.
        4. Validates the user data using `parse_users`.
        5. Writes the results to a report file using `write_report`.
        6. Identifies the suspect(s) who had access using `find_culprit`.

    Returns:
        str: The name of the culprit.

    Raises:
        NoUniqueCulpritError: If a unique culprit cannot be identified.
        RuntimeError: If the request to the URL fails.
        ValueError: If the computer or suspect ID does not exist,
            or if the data retrieved from the web cannot be parsed.
    """
    logging.basicConfig(
        format="%(asctime)s: %(levelname)-7s: %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
        filename=LOGGING_FILE,
        encoding="utf-8",
        level=logging.DEBUG,
    )

    loaded_rooms = load_rooms(PATH_ROOMS)
    loaded_users = load_users(TALLBIT)
    parsed_users = parse_users(loaded_users)

    # The report is also generated if `find_culprit` raises a NoUniqueCulpritError.
    write_report(RAPPORT, SUSPECTS, COMPUTER, parsed_users, loaded_rooms)
    suspects = find_culprit(SUSPECTS, COMPUTER, parsed_users, loaded_rooms)

    return suspects.name


if __name__ == "__main__":
    skyldig = solution()
    print(f"\nDen skyldige är: {skyldig}")
