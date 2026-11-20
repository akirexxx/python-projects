# Encrypt and decrypt with the Atbash cipher

Unknown hackers have launched a vicious ransomware attack against Anaconda Industries, leaving behind a cryptic message on the company’s website. Now, it’s up to the IT team to crack the code and figure out what the message really means.

## Program overview

The program allows the user to enter a message and have that message encrypted or decrypted. The encryption is of the Atbash type and can therefore only decrypt messages that follow this logic. 

Lowercase letters and numbers in ASCII are replaced with their mirrored values. Other characters, including uppercase letters and 'åäö', remain the same.

## Note

[scrambled note](note.log)

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
print(solution(path))
```

## Example outout

```python
"Era servrar är låsta och backuperna är raderade. Skicka 75 bitcoin före måndag kl 09:00, annars säljer vi kunduppgifterna på nätet!"
```


## Author

Lotta Reiman
