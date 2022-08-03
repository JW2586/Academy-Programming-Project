# Academy Programming Project
## Table of Contents
- [Introduction](#introduction)
- [Plan](#plan)
- [Program Development](#program-development)
  * [Plan languages and general Structure](#plan-languages-and-general-structure)
  * [Server Development](#server-development)
  * [GUI client development](#gui-client-development)
    + [FTP client UX](#ftp-client-ux)
    + [GUI client demo video](#gui-client-demo-video)

## Execution details
### FTP server
This is the FTP server for the project, it holds the medical CSV files.
Found in `/ftpserver/pythonftpserver.py`
IP: `127.0.0.1`
Port: `21`
Username: `user`
Password: `12345`
### Command-line FTP client
This is the command-line client for downloading and validating the CSV files from the FTP server
Found in `CLI-client.py`
[image]
### Graphical FTP client
This is the graphical user interface client for downloading and validating the CSV files from the FTP server
Found in `GUI-client.py`
[image]
### Automatic FTP client
This is the automatic client for downloading and validating the CSV files from the FTP server based on the current date. This can be scheduled to run daily via Windows Task Scheduler.
Found in `auto-client.py`
[image]
[image]

## Introduction

The project brief is that we create a client-side application that (using ftp) allows staff from a Medical School to download data in both a scheduled and interactive manner.

>'It is envisaged that a client-side application is needed that allows the staff in the Medical school to securely download data in both a scheduled (cron/scheduled task) and interactive manner, e.g.,requesting data for a specific date(the default being "today").Data must be validated (see Task 3) before it is accepted, copied for investigation,and thensecurely archivedin a logical directory hierarchy.  It is vitally important that there are no accidentally duplicated data sets as this could create bias problems during analysis, therefore a tracking mechanism must be used to keep each set unique.'

## Plan

To begin we decided to formulate a plan on how we would work on our project. Firstly the order of development and who would do what. We decided to develop in this order:

* Plan langauges and general structure first
* Develop the server
* Develop the client
* Develop the logic to filter the CSV files
* Tie the programs together and finish

## Program Development

### Plan languages and general Structure

We decided that to begin Sam would try to make an FTP server in C++, due to the fast nature and well documented librarys of the language. 
Jake would code the processing of the CSV's in python to save time and complexity. The GUI would be coded in Python as well.

### Server Development 
Sam started out with [fine-ftp server](https://github.com/eclipse-ecal/fineftp-server)- an open source C++ program. This allowed him to set up an ftp server with authentication as seen below

```cpp
#include <fineftp/server.h>
#include <thread>
 
int main() {
  // Create an FTP Server on port 2121. We use 2121 instead of the default port
  // 21, as your application would need root privileges to open port 21.
  fineftp::FtpServer ftp_server(2121);
 
  // Add the well known anonymous user. Clients can log in using username
  // "anonymous" or "ftp" with any password. The user will be able to access
  // your C:\ drive and upload, download, create or delete files. On Linux just
  // replace "C:\\" with any valid path. FineFTP is designed to be cross-platform.
  ftp_server.addUserAnonymous("C:\\", fineftp::Permission::All);
  
  // Start the FTP Server with a thread-pool size of 4.
  ftp_server.start(4);
 
  // Prevent the application from exiting immediately
  for (;;) std::this_thread::sleep_for(std::chrono::milliseconds(100));
  return 0;
}
```

This then would allow a working connection with both filezilla and powershell ftp as seen below:

![image](https://user-images.githubusercontent.com/110546631/183737642-94c055f7-afc0-4b43-9afe-af2a32f9fcec.png)

But Sam came across a big issue, the servers couldn't send anything beyond a simple handshake:

![image](https://user-images.githubusercontent.com/110546631/183737958-f3f5e362-4311-41df-ac7c-ab20b4bd58f5.png)

At the time Sam didn't know this so he moved onto a [new C++ library](https://github.com/DaHoC/ftpserver) that he could only use in linux due to the make file and the C++ structure.

```cpp

#include "ftpserver.h"

/**
 * This is the main program entry point
 * usage:
 * ftpserver <server root directory> <port to listen on for incoming connections> <telnet mode for use with telnet client, default = false>
 */
int main(int argc, char** argv) {
    unsigned short commandOffset = 1; // For telnet, we need 3 because of the enter control sequence at the end of command (+2 characters)
    unsigned int port = 4242; // Port to listen on (>1024 for no root permissions required)
    std::string dir = "./"; // Default dir
    if (argc < 2) {
        std::cout << "Usage: ftpserver <dir> <port> [telnetmode=no], using default dir '" << dir << "' , port " << port << std::endl;
    } else {
        switch (argc) {
            case 4:
                commandOffset = 3; // If any 3rd parameter is given, the server is started for use with telnet as client
            case 3:
                port = atoi(argv[2]); // Cast str to int, set port
            case 2:
                fileoperator* db = new fileoperator(dir);
                // Test if dir exists
                if (db->dirCanBeOpenend(argv[1])) {
                    dir = argv[1]; // set default server directory
                    db->changeDir(dir, false); // Assume the server side is allowed to change any directory as server root (thus the false for no strict mode)
                } else {
                    std::cout << "Invalid path specified ('" << argv[1] << "'), falling back to '" << dir << "'" << std::endl;
                }
                break;
        }
    }

    servercore* myServer = new servercore(port, dir, commandOffset);

    /// @TODO: some sort of server shutdown command??
    delete myServer; // Close connection, for the good tone

    return (EXIT_SUCCESS);
}

```
This would also run, but once again Sam came across the same issue in Kali as well :

![image](https://user-images.githubusercontent.com/110546631/183744538-79bfee90-6e7d-4d09-9993-404cf5771218.png)

After a lot of testing Sam discovered that it was the firewalls stopping the code from running and the complexity of the C++ code made it hard to debug. We decided to switch to an FTP server library in python - [pyftpdlib](https://pypi.org/project/pyftpdlib/)



### GUI client development
Up to this stage we had tested the servers using FileZilla client programs, we now needed to implement the client program ourselves.
Jake began by finding an [open source python script](https://github.com/jbblackett/Python-GUI-FTP-Client)that created a tkinter graphical interface for an FTP client, he based our solution off of this, modifying it for our needs.
#### FTP client UX
- The FTP client begins by asking the user to connect to the FTP server and login with the required credentials.
- The user then enters the date of the files they would like to download and clicks the `Download files` button
- The FTP client then downloads the requested files from the FTP server and stores them in a temporary location called `temp-downloads/`
- The user then clicks the `Validate files` button which checks the files against the following criteria
	- Duplicated batch_ids
	- Missing headers or misspelt/incorrect headers, e.g. "batch" rather than "batch_id"
	- Missing columns on a row
	- Invalid entries, e.g., reading values of 10 or greater
	- Empty files (there are no "nil" returns)s
	- Incorrectly formatted filenames
- If a file meets all of the requirements, it is saved by moving it into the `validated-files/` folder, structuring the directory based on `YYYY/MM/DD/`
- If a file fails to meet all of the requirements, it is deleted from the FTP client

#### GUI client demo video
[![Demo video](https://github.com/JW2586/Academy-Programming-Project/blob/main/Video%20thumbnail.jpg?raw=true)](https://imgur.com/a/MhVdohV)





