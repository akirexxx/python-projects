import csv

import pytest

from solution import (
    NoUniqueCulpritError,
    Room,
    User,
    find_culprit,
    load_rooms,
    parse_users,
    solution,
    write_report,
)

def exempelrum():
    return [
        Room("room-2-2"),  
        Room("room-1-1"), 
        Room("room-2-3"), 
        Room("room-1-2"), 
        Room("room-2-1"), 
    ]


def exempelanvandare():
    return [
        User("id1", "Anna", "01000"),
        User("id2", "Bo", "00010"),
        User("id3", "Cia", "00100"),
        User("id4", "Dan", "01000"),
    ]


def exempeldatorer():
    return {
        "pc-c": Room("room-2-1"),
        "pc-a": Room("room-1-1"),
        "pc-e": Room("room-2-3"),
        "pc-b": Room("room-1-2"),
        "pc-d": Room("room-2-2"),
    }


# Accesslängden är längre | kortare än rumsantal
@pytest.mark.parametrize(
    "access_kod, forvantat_fel",
    [
        ("1001", "Access inte samma längd som antal rum"),
        ("100100", "Access inte samma längd som antal rum"),
    ],
)
def test_length_access(access_kod, forvantat_fel):
    rooms = exempelrum()
    user = User("id800", "Lars Larsson", access_kod)
    with pytest.raises(ValueError, match=forvantat_fel):
        user.has_access(Room("room-2-2"), rooms)


# Rummet existerar inte i rumslistan
def test_non_existing_room():
    rooms = exempelrum()
    user = User("id123", "Kalle Anka", "10101")
    with pytest.raises(ValueError, match="Rummet finns inte"):
        user.has_access(Room("room-14-1"), rooms)


# Testa access första och sista rummet i byggnaden
def test_access():
    rooms = exempelrum()
    user_one = User("id100", "Legolas", "10000")
    assert user_one.has_access(Room("room-1-1"), rooms) is True
    assert user_one.has_access(Room("room-2-3"), rooms) is False


# Flera misstänkta hade access till stulna rummet
def test_multiple_suspects():
    exempel_anvandare = [
        User("id001", "Frodo", "11111"),
        User("id002", "Gandalf", "11111"),
    ]
    with pytest.raises(NoUniqueCulpritError, match="Flera misstänkta"):
        find_culprit(["id001", "id002"], "pc-e", exempel_anvandare, exempeldatorer())


# Inga användare hade access till det stulna rummet
def test_no_suspects():
    exempel_anvandare = [
        User("id001", "Frodo", "00000"),
        User("id002", "Gandalf", "00000"),
    ]
    with pytest.raises(NoUniqueCulpritError, match="Ingen misstänkt"):
        find_culprit(["id001", "id002"], "pc-e", exempel_anvandare, exempeldatorer())


# Bara den misstänkte som har access returneras som misstänkt
def test_correct_suspect():
    users = [
        User("id1", "Anna", "10000"),
        User("id2", "Bo", "00010"),
    ]
    suspects_list = ["id1", "id2"]
    suspects = find_culprit(suspects_list, "pc-a", users, exempeldatorer())
    assert suspects.name == "Anna"


# Kontrollerar att User-objekt skapas korrekt
def test_object_parse_users():
    data = [
        {"id": "id013", "name": "Lisa Exempel", "access": "10110"},
        {"id": "id014", "name": "Karin Exempel", "access": "10110"},
    ]

    users = parse_users(data)
    assert isinstance(users, list)
    assert len(users) == 2
    assert all(isinstance(u, User) for u in users)


# Om användardatan har ogiltiga värden eller fel format
@pytest.mark.parametrize(
    "webbdata, exception_typ, forvantat_fel",
    [
        (
            [{"id": 45, "name": "Karin", "access": "10110"}],
            ValueError,
            "ID är inte en sträng",
        ),
        (
            [{"inte_id": "id1", "name": "Emma", "access": "10110"}],
            ValueError,
            "Obligatorisk nyckel saknas",
        ),
        (
            [{"id": "id2", "inte_name": "Emelie", "access": "10110"}],
            ValueError,
            "Obligatorisk nyckel saknas",
        ),
        (
            [{"id": "id3", "name": "Karl", "inte_access": "10110"}],
            ValueError,
            "Obligatorisk nyckel saknas",
        ),
        (
            [{"id": "id4", "name": "Robert", "access": "20110"}],
            ValueError,
            "får bara innehålla 0-1",
        ),
        ("inte_lista", ValueError, "Datan är inte en lista"),
        (
            [{"id": "id3", "name": "Karl", "access": 10110}],
            ValueError,
            "Access är inte en sträng",
        ),
    ],
)
def test_format_parse_users(webbdata, exception_typ, forvantat_fel):
    with pytest.raises(exception_typ, match=forvantat_fel):
        parse_users(webbdata)


# Om indatan inte är i formatet <room-floor-number>
@pytest.mark.parametrize(
    "indata, forvantat_fel",
    [
        ("Room,Computer\nHEJ-1-1,pc-a\n", "Rumsnamnet börjar inte med 'room'"),
        ("Room,Computer\nroom-HEJ-3,pc-e\n", "Våningen är inte ett tal"),
        ("Room,Computer\nroom-1-HEJ,pc-b\n", "Rumsnumret är inte ett tal"),
        ("Room,Computer\nroom-3-0,pc-b\n", "Rumsnumret är inte ett tal >= 1"),
        ("Room,Computer\nroom-0-1,pc-b\n", "Våningen är inte ett tal >= 1"),
        ("Room,Computer\nroom-1,pc-b\n", "Rumsnamnet är inte tre fält"),
        ("FELRUBRIK\nroom-1-2,pc-b\n", "Fel rubriker"),
    ],
)
def test_format_load_rooms(tmp_path, indata, forvantat_fel):
    fil = tmp_path / "test_rooms.csv"
    fil.write_text(indata)
    with pytest.raises(ValueError, match=forvantat_fel):
        load_rooms(str(fil))


# Room objekt försöker skapas direkt med fel format
def test_room_validation():
    with pytest.raises(ValueError):
        Room("fel-format")


# User objekt försöker skapas direkt med fel format
def test_user_validation():
    with pytest.raises(ValueError):
        User(45, "Michael Andersson", "00101000001010111")


# Rapport skrivs med rubriker, skyldig och övriga misstänkta (behåller ordningen)
def test_report_guilty_found(tmp_path):
    rapport = tmp_path / "rapport.csv"
    write_report(
        rapport, ["id3", "id1", "id2"], "pc-d", exempelanvandare(), exempeldatorer()
    )
    assert rapport.read_text(encoding="utf-8") == (
        "id,namn,access,status\n"
        "id3,Cia,00100,saknar\u202faccess\n"
        "id1,Anna,01000,saknar\u202faccess\n"
        "id2,Bo,00010,har\u2009access\n"
    )


# Rapport skrivs även om ingen misstänkt har access
def test_report_only_suspects(tmp_path):
    rapport = tmp_path / "rapport.csv"
    write_report(rapport, ["id1", "id3"], "pc-d", exempelanvandare(), exempeldatorer())
    assert rapport.read_text(encoding="utf-8") == (
        "id,namn,access,status\n"
        "id1,Anna,01000,saknar\u202faccess\n"
        "id3,Cia,00100,saknar\u202faccess\n"
    )


# Den stulna datorn saknas i rumslistan
def test_no_report(tmp_path):
    rapport = tmp_path / "rapport.csv"

    with pytest.raises(ValueError, match="Datorn finns inte"):
        write_report(
            rapport,
            ["id1", "id3"],
            "datorn_saknas",
            exempelanvandare(),
            exempeldatorer(),
        )


# Testar access vid olika antal rum på våningarna
def egna_exempelrum():
    return [
        Room("room-1-1"),
        Room("room-2-1"),
        Room("room-2-2"),
        Room("room-2-3"),
        Room("room-3-1"),
        Room("room-3-2"),
    ]


def test_number_rooms():
    rooms = egna_exempelrum()
    user = User("id100", "Legolas", "110010")
    assert user.has_access(Room("room-1-1"), rooms) is True
    assert user.has_access(Room("room-2-1"), rooms) is True
    assert user.has_access(Room("room-3-1"), rooms) is True
