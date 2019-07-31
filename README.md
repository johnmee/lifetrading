# Life Trading Exercise

John Mee 31-Jul-2019

## Data Import Task

* Your task is to design a general process to import external csv files into a database
* You will need to specify the database schema, feel free to use what you see as the most appropriate
database technology
* You will need to provide code to process files and import them to the database, feel free to use any
language that fits well with your choice of database technology
* You will need to document how you see the process running in an automated way so that files are
processed within 10 minutes of their arrival

The requirements are as follows
* New file reports are dropped into a local folder at regular times in the day
* Multiple types of reports may be dropped into this folder
* Each file should be processed, and a status recorded to the database to say they have
arrived
* For specific report types, the contents of the file should also be imported into the database
and the status updated to imported
* You are free to add any additional status values as appropriate
* The modification time of the file represents the download date/time, this should be
recorded to the database
* Each report type has a specific filename pattern, this includes the report type but also
additional information relating to that file. There will always be a trade date encoded in the
filename.
* Different report types may have different filename patterns
* Each report type has a different set of columns, all columns should be imported

Bonus requirement
* Each report may be revised during the day, the prior report should be considered out of date
and replaced with this one.
