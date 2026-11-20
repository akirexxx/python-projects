from solution import solution, help_solution
import json
import pytest

# Om flera ensamma datorer hittas
def test_flera_ensamma(tmp_path):
    fil = tmp_path / "flera_ensamma.json"
    fil.write_text(
        json.dumps(
            {
                "dator_a": [10.0000, 30.0000],
                "dator_b": [60.0000, 40.0000],
                "dator_c": [70.0000, 30.0000],
            }
        )
    )
    with pytest.raises(ValueError):
        solution(str(fil)), "ValueError, fler än en dator hittas ensam"


# Om inga ensamma datorer hittas
def test_egen_ingen_ensam(tmp_path):
    fil = tmp_path / "ingen_ensam.json"
    fil.write_text(
        json.dumps(
            {
                "dator_a": [10.0002, 30.0003],
                "dator_b": [10.0003, 30.0002],
                "dator_c": [10.0004, 30.0001],
            }
        )
    )
    with pytest.raises(ValueError):
        solution(str(fil)), "ValueError, ingen ensam dator hittas"


# Felaktiga format, testar flera fall
@pytest.mark.parametrize(
    "indata, feltyp",
    [
        ({"a": ["59.3293", 18.0687]}, TypeError),  # latitud är en sträng
        ({"b": [59.3293, "18.0687"]}, TypeError),  # longitud är en sträng
        ({47: [59.3293, 18.0687]}, TypeError),     # namnet är ett heltal
        (["inte", "en", "dictionary"], TypeError), # datan är fel format
        ({"d": [59.3953]}, ValueError),            # listan har bara ett värde
    ],
)
def test_felaktiga_varden(tmp_path, indata, feltyp):
    fil = tmp_path / "felaktig_data.json"
    fil.write_text(json.dumps(indata))
    with pytest.raises(feltyp):
        solution(str(fil))


# Om endast latitud är inom tröskelvärdet men inte longitud
def test_over_troskel():
    a = [59.3291, 18.0681]
    b = [59.3292, 19.0689]
    over_troskel = help_solution(a, b)
    assert over_troskel is False


# True om skillnaden är mindre än tröskel
def test_under_troskel():
    a = [59.3291, 18.0681]
    b = [59.3292, 18.0682]
    under_troskel = help_solution(a, b)
    assert under_troskel is True


# Om två punkter är precis på gränsen från varandra
def test_haversine():
    a = [0.0, 180.0]
    b = [0.0, -179.999]
    resultat = help_solution(a, b)
    assert resultat is True