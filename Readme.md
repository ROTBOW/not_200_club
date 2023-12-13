# Not 200 Club

This script processes an xlsx file located in the target directory. The directory must contain only this file. If the directory does not exist, it must be created manually.

The xlsx file, which can have any name, must adhere to a specific format:<br/>
`Seeker Name, Coach, Status, solo url, capstone url, group url`

The file should be exported as a "details only" xlsx file, an option available in SF.

The output is directed to a 'res' directory. If this directory does not exist, the script will create it. The output file is generated only after the script has finished executing.

## Instructions:
1. Place the xlsx file in the target directory. Ensure it is the only file in the directory.
2. Execute the script.
3. Allow the script to complete.
4. Retrieve the output file from the 'res' directory.

## Notes:
- The script's runtime is approximately one hour, this time will vary depending on the amount of cpu cores on the machine and the amount of seekers
- The script will save after each coach, if it fails it will have all data up to the last coach it finished
- The output file is generated in the 'res' directory upon script completion.
- The script will create the 'res' directory if it does not exist.

<br/><br/><br/>

# Emailer

This is a simple script that will send personalized emails to coaches about their caseload with the output of the sheet for them.
It will only email the coaches with their names in the .env file (to protect thier emails) that have names that correspond to the names in the sheets 