# Analys av accessloggar
Find out who left the data center and identify the potential suspect/s. 

## Program overview
The program takes the path to a log file as input and returns the ID numbers that match specific criteria.

## How to run program
1. Open a terminal in the project directory
2. Run the following command to install the dependencies: `uv sync`
2. Run the file `solution.py` by the command `uv run solution.py`

## How to run tests
1. Open a terminal in the project directory
2. Run the following command to install the dependencies: `uv sync`
3. Run the file `solution.py` by the command `uv run pytest`

## Constants

```python
SUSPICIOUS_DAY = ["14"]
SUSPICIOUS_HOUR =  ["13", "14", "15", "16", "17", "18"]
SUSPICIOUS_STAMP = ["out"]
```

## Example input

```python
path = "access.log"
print(solution(path))
```

## Example output

The list contains the ID numbers of individuals who left the building on the 14th between 13:00 and 18:00.

```python
['id001', 'id009', 'id007', 'id015']
```

## Assumptions

1. Each line consists of four fields in the following format: DAY TIME [in | out] ID.
2. A new log file is created for each month.
3. The function uses three constants: suspicious_day, suspicious_hours, and suspicious_stamp. These constants must be assigned values but can be modified depending on which events need to be investigated.

## Error handling

The program does not crash when empty lines are encountered. Instead, it continues processing and displays a message identifying the ignored line along with the results. One advantage of this approach, compared to raising a ValueError, is that there is no need to troubleshoot the issue and run the program again.

However, if a line contains invalid data, the program stops and raises a ValueError. This indicates that the log file may have been generated incorrectly. Unlike an empty line, invalid data could lead to misleading results, which is why the program stops execution.

## Author

Lotta Reiman

