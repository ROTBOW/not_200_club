# Not 200 Club

This script processes an xlsx file located in the target directory. If this directory does not exist, the script will create it. which will cause the script to throw an empty target folder error since the newly created target folder will be empty. 

The xlsx file, which can have any name, must adhere to a specific format:<br/>
`Seeker Name, Coach, Status, solo url, capstone url, group url, email`
for example the file would look like this:
| Placement: Placement Name | Owner Name  | Status   | Student Account: Solo Project Live Link | Student Account: Capstone Project Live Link | Student Account: Group Project Live Link | Email         |
|---------------------------|-------------|----------|-----------------------------------------|---------------------------------------------|------------------------------------------|---------------|
| John Smith                | Josiah Leon | Greenlit | https://fakeurl.com/                    | https://fakeurl2.com/                       | fakeurl3.com                             | fake@mail.com |

The file should be exported as a "details only" xlsx file, an option available in salesforce for reports.

The script outputs to the 'res' directory. If this directory does not exist, the script will create it. The output file is generated only after the script has finished executing.

## Instructions:
1. Place the xlsx file in the target directory. Ensure it is the only file in the directory.
2. Execute the script.
3. Allow the script to complete.
4. Retrieve the output file from the 'res' directory.

## Notes:
- The script's runtime is approximately one hour, this time will vary depending on the amount of cpu cores on the machine and the amount of seekers
- The script will save after each coach, if it fails it will have all data up to the last coach it finished
- The output file is generated in the 'res' directory upon script completion.

<br/><br/><br/>

# Emailer

This script sends emails to coaches about their caseload with the output of the sheet for them.
It will only email the coaches with their names in the .env file (to protect thier emails) that have names that correspond to the names in the sheets

The script will grab the most recent output file in the res folder, if the folder doesn't exist, or is empty, the script will throw an error.

In order for the script to run properly you will need a .env file, this file is not saved to the repo for security, it should contain names to emails for the sheets and the login info for the emailing service.