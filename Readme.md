# Not 200 Club

This script processes an xlsx file located in the target directory. The directory must contain only this file. If the directory does not exist, it must be created manually.

The xlsx file, which can have any name, must adhere to a specific format:<br/>
`Seeker Name, Coach, Status, solo url, capstone url, group url`

The file should be exported as "details only", an option available in SF.

The script, enhanced with threading, completes its execution in approximately one hour. Interruptions during this period will result in loss of all current data. However, the reduced runtime minimizes this risk.

The output is directed to a 'res' directory. If this directory does not exist, the script will create it. The output file is generated only after the script has finished executing.

## Instructions:
1. Place the xlsx file in the target directory. Ensure it is the only file in the directory.
2. Execute the script.
3. Allow the script to complete.
4. Retrieve the output file from the 'res' directory.

## Notes:
- The script's runtime is approximately one hour.
- Interruptions or crashes during execution will result in loss of all current data.
- The output file is generated in the 'res' directory upon script completion.
- The script will create the 'res' directory if it does not exist.

This document was written with the assistance of CursorBot, a tool powered by GPT-4.