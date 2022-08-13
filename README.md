# Academy Programming Project

## Introduction

The project brief is that we creat a client-side application that (using ftp) allows staff from a Medical School to download data in both a scheduled and interactive manner.

>'It is envisaged that a client-side application is needed that allows the staff in the Medical school to securely download data in both a scheduled (cron/scheduled task) and interactive manner, e.g.,requesting data for a specific date(the default being "today").Data must be validated (see Task 3) before it is accepted, copied for investigation,and thensecurely archivedin a logical directory hierarchy.  It is vitally important that there are no accidentally duplicated data sets as this could create bias problems during analysis, therefore a tracking mechanism must be used to keep each set unique.'

## Plan

To begin me and jake decided to formulate a plan on how we would work on our project. Firstly the order of development and who would do what. We decided to develop in this order:

* Plan langauges and general structure first
* Develop the server
* Develop the client
* Develop the logic to filter the CSV files
* Tie the programs together and finish

## Program Development

### Plan languages and general Structure

We decided that to begin I would try and make a CPP server, due to the fast nature and well documented librarys of the language. 
Jake would code the processing of the CSV's in python to save time and complexity. The GUI would be coded in Python as well.

### Server Development 

I (sam) started out with one library in cpp known as 'fine-ftp server' that allowed me in give or take 10 lines of code to set up an ftp server with auth etc as seen below (From the git-hub cited below):

```
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

But I came across a big issue, the servers couldent send anything beyond a simple handshake:

![image](https://user-images.githubusercontent.com/110546631/183737958-f3f5e362-4311-41df-ac7c-ab20b4bd58f5.png)

At the time I didn't know this so I moved onto a new cpp library that I could only use in linux due to the make file and the cpp structure (Github Linked at end of the document):

```

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
This would also run, but once again I came across the same issue in Kali as well :

![image](https://user-images.githubusercontent.com/110546631/183744538-79bfee90-6e7d-4d09-9993-404cf5771218.png)

Worked out after a lot of testing that it was the firewalls in the end stopping the code from running!
So jake found a python library that could do it and implamented that in the end.

### Client Development

Up to this stage we had tested the servers using filezilla client programs, we now needed to implament the client program ourselves.
We decided to use Tkinter to build the GUI which also outputs to command line as well. 

[PHOTO OF TKINTER CLIENT HERE]

### CSV sorting Logic

To sort the CSV files we made a python scrypt that will firstly...

### Implamentation

Talk about how we wrapped it all up together 

## 



## Git-Hub Links

Fine-ftp : https://github.com/eclipse-ecal/fineftp-server/blob/master/README.md
Ftp server : https://github.com/DaHoC/ftpserver




