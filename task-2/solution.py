path = "access.log"

# Criteria for identifying exits on the 14th between 13:00 and 18:00
SUSPICIOUS_DAY = ["14"]
SUSPICIOUS_HOUR =  ["13", "14", "15", "16", "17", "18"]
SUSPICIOUS_STAMP = ["out"]

def solution(path):
    """Retrieve ID:s from log file based on a specified time frame
    
    Parameter:
        path: path to the log file
    Returns: 
        list: A list of ID:s matching specified criteria
    Raises:
        ValueError if row in log contains invalid data
    """

    suspicious_id = []
    
    with open(path, encoding="utf-8") as file:
        
        # Identifies row number if row has invalid data
        for row, line in enumerate(file, start=1):
            fields = line.split()

            if not fields:
                print(f"Ignorerar tom rad: {row}")
                continue

            elif len(fields) != 4:
                raise ValueError(f"Fel i rad: [{row}], har inte fyra fält. ")
            
            day = fields[0]
            hour = fields[1]
            stamp = fields[2].lower() 
            id_number = fields[3].lower()

            # error handling which stops the program before ID summary
            if not day.isdigit() or int(day) > 31 or int(day) < 1:
                raise ValueError(f"Fel i rad: [{row}], ogiltig dag: {day}")

            elif not hour.isdigit() or int(hour) > 23 or int(hour) < 1: 
                raise ValueError(f"Fel i rad: [{row}], ogiltig timme: {hour}")

            elif stamp not in("out", "in"):
                raise ValueError(f"Fel i rad: [{row}], ogiltig stämpel: {stamp}")

            elif not id_number.startswith("id") or not id_number[2:].isdigit():
                raise ValueError(f"Fel i rad: [{row}], ogiltigt ID: {id_number}")

            if (
                day in SUSPICIOUS_DAY
                and hour in SUSPICIOUS_HOUR
                and stamp in SUSPICIOUS_STAMP
                and id_number not in suspicious_id
                ):
                
                suspicious_id.append(id_number)
                
    return suspicious_id

if __name__ == "__main__":
    print(solution(path))
