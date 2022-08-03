## Project background
A University has a trusted scientific partner for medical research. The University Medical school needs to be able to download pharmaceutical trial data from this partner in a secure and reliable fashion.
Although the scientific partner intends to move to a RESTful web-based API in the near future they are currently using a simple FTP service, despite the accepted risks and known vulnerabilities.

## Task 1: Core requirements
It is envisaged that a client-side application is needed that allows the staff in the Medical school to securely download data in both a scheduled (cron/scheduled task) and interactive manner, e.g., requesting data for a specific date (the default being "today").
Data must be validated (see Task 3) before it is accepted, copied for investigation, and then securely archived in a logical directory hierarchy.
It is vitally important that there are no accidentally duplicated data sets as this could create bias problems during analysis, therefore a tracking mechanism must be used to keep each set unique.
## Task 2: User interface requirements
The application should have command line options (for automated scheduling) and a user-friendly interactive front-end (to launch manual requests). Both aspects should follow best practice principles in UI (user interface)/UX (user experience).
## Task 3: Data issues to identify and report
Previous manual data downloads have revealed problems with the downloaded csv files.
This has led to a suspicion that some data files are manually collated and edited before being uploaded to the FTP. Consequently, there has been some communication regarding the variable quality of the data.
Common issues identified include:
- Malformed files (causing difficulties when importing into other applications, e.g., spreadsheets, databases, cloud-based machine learning etc.)
- Duplicated batch_ids (see Technical Information)
- Missing headers or misspelt/incorrect headers, e.g. "batch" rather than "batch_id"
- Missing columns on a row
- Invalid entries, e.g., reading values of 10 or greater
- Empty files (there are no "nil" returns)
- Incorrectly formatted filenames.

Files which contain these issues must be identified and logged using an appropriate technique; it is intended that these logs can be ingested by another application for monitoring and reporting purposes – this is currently outside development scope, however.
## Task 4: Coding standards and documentation
All code should be written and documented to appropriate standards using the selected programming language(s)
The precise method of coding is selected by the team and can contains components written in different languages, operating in concert. For example – PowerShell for FTP interaction, Python for data file processing etc.
It is critical that all code is held securely within a suitably secure remote repository that utilizes a popular VCS (version control system).
