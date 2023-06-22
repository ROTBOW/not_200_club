# Not 200 Club

Hey!

This script takes a xlsx file from the target folder, (if the folder doesn't exist you will have to create it) it has to be the only file in the target folder.

The xlsx file can be named anything but needs to be formatted in a very specific way. Shown as follows:
Seeker Name, Coach, Status, solo url, capstone url, group url

<del>
    It can take upwards of 7-9 hours to run, (this is in cases of an excess of 2100+ URLs to test),
    best to leave it running in the background. As of now, if the script is stopped or crashes for whatever reason, it will lose all current progress. as the library used to write to the xlsx file can <b>not</b> read and write. only write.
</del>

With threading the script should only take about an hour to run!, 

It will output to a folder called res, if there is no res folder the script will create one.
The script will have to complete before it creates the output file.