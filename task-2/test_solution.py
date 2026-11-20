from solution import solution
import pytest


def test_empty_rows(tmp_path):
    fil = tmp_path / "empty_rows.log"
    fil.write_text(
        "14 14 out id010\n"
        "14 13 out id011\n"
        "\n"
        "14 17 out id012\n"
        ) 
    result = solution(str(fil))
    assert len(result) == 3, "Should skip empty rows"

def test_uppercase(tmp_path):
    fil = tmp_path / "uppercase.log"
    fil.write_text("14 14 OUT ID010\n") 
    result = solution(str(fil)) 
    assert result == ["id010"], "Should convert uppercase to lowercase"

def test_no_match(tmp_path):
    fil = tmp_path / "no_match.log"
    fil.write_text("15 13 in id999\n")
    assert solution(str(fil)) == [], "Should return empty list when nothing matches"

def test_fields(tmp_path):
    fil = tmp_path / "fields.log"
    fil.write_text("14 17 out\n")
    with pytest.raises(ValueError):
        solution(str(fil)), "Should raise ValueError if not four fields"

def test_day(tmp_path):
    day = tmp_path / "day.log"
    day.write_text("32 13 out id010\n")
    with pytest.raises(ValueError):
        solution(str(day)), "Should raise ValueError if day contains invalid data"
    
def test_hour(tmp_path):
    hour = tmp_path / "hour.log"
    hour.write_text("15 24 out id010\n")
    with pytest.raises(ValueError):
        solution(str(hour)), "Should raise ValueError if hour contains invalid data"

def test_ID(tmp_path):
    ids = tmp_path / "ids.log"
    ids.write_text("30 13 out idfel\n")
    with pytest.raises(ValueError):
        solution(str(ids)), "Should raise ValueError if ID contains invalid data"

def test_stamp(tmp_path):
    stamp = tmp_path / "ids.log"
    stamp.write_text("30 13 hej id000\n")
    with pytest.raises(ValueError):
        solution(str(stamp)), "Should raise ValueError if stamp contains invalid data"