# Not 200 Club

Hey!

This script takes a xlsx file from the target folder, (if the folder doesn't exist you will have to create it) it has to be the only file in the target folder.

The xlsx file can be named anything but needs to be formatted in a very specific way. Shown as follows:
Seeker Name, Coach, URL

It can take upwards of 1-3 hours to run, (this is in cases of an excess of 700+ URLs to test),
best to leave it running in the background. As of now, if the script is stopped or crashes for whatever reason, it will lose all current progress. as the library used to write to the xlsx file can <b>not</b> read and write. only write.

This is something I want to change, options include:
* Using a different library
* Having each coach be their own file instead of a sheet.

It will output to a folder called res, if there is no res folder the script will create one.
The script will have to complete before it creates the output file.

* [ ] Create a universal sheet for all projects
    * [ ] How many seekers took longer than 10 sec
    * [ ] How many seekers are not getting 200s
    * [ ] How many no-URLs and bad-URLs