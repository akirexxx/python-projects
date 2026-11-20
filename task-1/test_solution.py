from solution import solution
import pytest

def test_solution(tmp_path):
    numbers = tmp_path / "numbers.log"
    number = tmp_path / "number.log"
    numbers.write_text("0123456789")
    number.write_text("9")
    assert solution(str(numbers)) == "9876543210", "Should reverse all numbers"
    assert solution(str(number)) == ("0")


def test_aao(tmp_path):
    fil = tmp_path / "aao.log"
    fil.write_text("ÅÄÖ and åäö remain unchanged", encoding="utf-8")
    assert solution(str(fil)) == "ÅÄÖ zmw åäö ivnzrm fmxszmtvw"


def test_empty(tmp_path):
    fil = tmp_path / "aao.log"
    fil.write_text("")
    assert solution(str(fil)) == "", "Should handle empty string"


def test_characters(tmp_path):
    test_characters = tmp_path / "character.log"
    test_next = tmp_path / "next.log"
    test_characters.write_text("[], ?, , :, {}, %")
    test_next.write_text("abC\n+%")
    assert solution(str(test_characters)) == "[], ?, , :, {}, %", (
        "Other characters should remain unchanged"
    )
    assert solution(str(test_next)) == "zyC\n+%"


def test_letters(tmp_path):
    fil = tmp_path / "letters.log"
    fil.write_text("abcdefghijklmnopqrstuvwxyz")
    assert solution(str(fil)) == "zyxwvutsrqponmlkjihgfedcba", (
        "Should reverse every lowercase letter"
    )
