import string
import pytest

numbers = string.digits
reversed_numbers = string.digits[::-1]

english_alphabet = string.ascii_lowercase
reversed_alphabet = string.ascii_lowercase[::-1]

path = "note.log"


def solution(path) -> str:
    """Encrypt and decrypt with 'the Atbash cipher'

    Lowercase letters and numbers in ASCII are replaced with their mirrored values.
    Other characters, including uppercase letters and 'åäö', remain the same.

    Args: 
        note: The encrypted or regular string
    
    Returns:
        str: A string of the encrypted or decrypted note

    Assumptions:
        The cipher is of the Atbash type.
    """

    result = []

    with open(path, "r", encoding="utf-8") as file:
        note = file.read()

        for character in note:
            # only affects and converts lowercase letters
            if character in english_alphabet:
                current_index = english_alphabet.index(character)
                new_letter = reversed_alphabet[current_index]
                result.append(new_letter)

            # only affects and converts numbers
            elif character.isdigit():
                current_index = numbers.index(character)
                new_number = reversed_numbers[current_index]
                result.append(new_number)

            # keeps other characters unchanged
            else:
                result.append(character)
    return "".join(result)


if __name__ == "__main__":
    print(solution(path))


