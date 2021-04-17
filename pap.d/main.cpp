//////////////////////////////////////////////
// Author: Artur Z. (HUSKI3)                //
// Date:   18/3/21                          //
// Github: https://github.com/HUSKI3        //
// File:   main.cpp			    //
//////////////////////////////////////////////
/*
!!!
This software has no warranty and will only recieve
support for 10 days after the project is completed
!!!
*/
#include <stdio.h>
#include <stdlib.h>
#include <iostream>
#include <string>
#include <cstdio>
#include <fstream>
#include <streambuf>
#include <vector>
#include <usb.h>
#include <iomanip>
#include <fcntl.h>
#include <errno.h>
#include <termios.h>
#include <unistd.h>
#include "libs/rapidjson/document.h"
#include "libs/rapidjson/writer.h"
#include "libs/rapidjson/stringbuffer.h"
#include "libs/rapidjson/filereadstream.h"
#include "libs/daemonize.c"
#include "libs/display.cpp"
#include "libs/calls.cpp"
#include "libs/usbctl.c"
//#include "libs/serial.cpp"

using namespace rapidjson;

int main(int argc, char* argv[])
{
    // Init the daemon boolean
    bool daemon;
    // Set the usb loudness
    int usb_loud = 1;
    // Set the boolean for calls
    bool call;
    // Set the boolean for hub controls
    bool hubc;
    std::vector<std::string> hub_args;
    std::vector<std::string> call_args;
    std::cout << "[Plug-And-Play] Pre-loading config...\n";
    // Load configuration from '/etc/pap.d/config' ('etc/pap.d/config' for testing)
    // std::ifstream cfg_file("etc/pap.d/config");
    // Manually check content (Testing only)
    //std::cout << "========================== Config ==========================\n";
    //std::cout << cfg_file.rdbuf();
    //std::cout << "============================================================\n";
    /* Here I previously decided to use a multitude of JSON parsing libs which,
       broke after a while. So I instead made it convert file contents into a
       string and parse that.

       X This solution is a mess and will be fixed later on.
       V Fixed in version 0.0.02 by using a FileReadStream.
    */
    // Re-read the file
    // [OLD] Free memory from previous read
    FILE* fp = fopen("etc/pap.d/config", "r");
    // Create a buffer
    char readBuffer[65536];
    FileReadStream is(fp, readBuffer, sizeof(readBuffer));
    // Create a document DOM
    Document d;
    d.ParseStream(is);
    fclose(fp);
    // Check + Assign values
    //std::cout << "Version is: " << d["version"].GetString()  << std::endl;
    std::string version = d["version"].GetString();
    std::string main_display = d["main_display"].GetString();
    std::string lock = d["locked"].GetString();
    if (lock == "false")
    while(1)
    {
	lock = d["locked"].GetString();
	// Start the logging
        syslog (LOG_NOTICE, "Plug-And-Play live! Happy playing! ;)");
	// Arguments to be supplied
	for (int i = 1; i < argc; ++i) {
        	std::string arg = argv[i];
		if (call == false && hubc == false){
		if ((arg == "-h") || (arg == "--help")){
			std::cout << "[Plug-and-Play Daemon]\nVersion:" << version << std::endl;
			std::cout << "Be wary as this is an Alpha build,\nit may cause some issues on the system if used without care.\n";
			std::cout << "\t -h / --help   - Shows this!\n";
			std::cout << "\t -v / --verbal - Ouputs verbally!\n";
			std::cout << "\t --call - Sends a call!\n";
			std::cout << "\t --qusb - Does not show USB info during debugging!\n";
			return 0;
		}
		else if(arg == "-v"){
			std::cout << "Started in verbal mode!" << std::endl;
		}
		else if(arg == "-d"){
			daemon = true;
			skeleton_daemon();
		}
		else if(arg == "--qusb"){
			usb_loud = 0;
		}
		else if(arg == "--call"){
			call = true;
                }
		else if(arg == "-c"){
			hubc = true;
			// Debugging, it became a mess needed something easy to see
			//std::cout << "\n OOOOOOOOOOOO \n";
		}
		}
		else {
			if(hubc == true){
				hub_args.push_back(arg);
				// Debugging, it became a mess needed something easy to see
				//std::cout << "\n AAAAAAAAAAAA \n";
			}
			else{
				call_args.push_back(arg);
			}
		}
	}
	// Process per call
	if (call == true){
	for (int i = 0; i < call_args.size(); i++){
		caller::process(call_args[i]);
		}
	}
	else if (hubc == true){
        	process_usb(argc,argv);
	}
	else{
	if (daemon == true){
	syslog (LOG_NOTICE, "[Plug-And-Play] Loading I/O manager...");
	syslog (LOG_NOTICE, "[Plug-And-Play] Scanning available USB hubs...");
	}
	// USB bus
	struct usb_bus *bus;
	// USB device
    	struct usb_device *dev;
    	usb_init();
    	usb_find_busses();
    	usb_find_devices();
	for (bus = usb_busses; bus; bus = bus->next)
	if (usb_loud == 1 && daemon == false){
        	for (dev = bus->devices; dev; dev = dev->next){
            		std::cout << "Bus:" << bus << std::endl;
	            	printf("Located device %s/%s\n", bus->dirname, dev->filename);
        	    	printf("\tID_VENDOR = 0x%04x\n", dev->descriptor.idVendor);
            		printf("\tID_PRODUCT = 0x%04x\n", dev->descriptor.idProduct);
        	}
	}
	/* Here comes the point where we work with serial ports,
	   This is different from the previous USB detection part,
	   While that uses a library for just USB, this lets us access
	   Any device on a serial port can be detected through this method
	   [If you cant get this script to work.]
 	   To maintainers of this soon-to-be legacy codebase:
	   run `sudo adduser $USER dialout`
	   If you cant get this script to work (Permission Denied).
	*/
	/* [Note]
	   Moved to libs/serial.cpp
	*/
	// Run test on usb1 (located in /dev/bus/usb/001/001)
	// Fixes : added `| O_CREAT`
	std::cout << "Selecting /usb/001/001 as test candidate\n";
	int test_serial_port = open("/dev/bus/usb/001/001", O_RDWR | O_CREAT);
	serial::usb1(test_serial_port);
	serial::termi(test_serial_port);
	// Call Display info for debugging (Should not be mutable)
	std::cout << "=== Attached X Displays ===" << std::endl;
	printMonitorInfo();
	/* Here we are done with basic core functionality, it will be
	continued after the GUI for the project is in a good state
	as this can work without any issues at the moment.

	[Note | 02/04/21]
	Most parts of the daemon are complete, calls functionality is a bit
	broken but will works with some effort.

	[Note | 12/04/21]
	Daemon works on specific hubs and controls them with ease.
	*/
        break;
    }
    syslog(LOG_NOTICE, "Plug-And-Play deamon terminated. See you next time.");
    closelog();
    std::cout << "exiting\n";
    return EXIT_SUCCESS;
    }
}
