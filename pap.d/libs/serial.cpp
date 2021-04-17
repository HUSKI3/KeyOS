// C library headers
#include <stdio.h>
#include <string.h>

// Linux headers
#include <fcntl.h> // Contains file controls like O_RDWR
#include <errno.h> // Error integer and strerror() function
#include <termios.h> // Contains POSIX terminal control definitions
#include <unistd.h> // write(), read(), close()

class serial{
public:
	static int usb1(int serial_port){
        // Check for errors
	// Test USB 001 tty access
	/*
	  Another permission error may occur, the following is the fix:
	  sudo adduser $USER dialout
	*/
	std::cout << serial_port << std::endl;
	if (serial_port < 0) {
                printf("[Plug-and-Play] Error %i can not open due to: %s\n", errno, strerror(errno));
        }
	else{
		printf("[Plug-and-Play] Opened with %i\n", serial_port);
	}
	return 0;
	}
	static void termi(int serial_port){
        // Create termios for loading USB configurations
        struct termios tty;
        if(tcgetattr(serial_port, &tty) != 0) {
                // [No longer applies] This part will be left as is until the display part is complete
                printf("[Plug-and-Play] Error %i from tcgetattr: %s\n", errno, strerror(errno));
        }
	struct termios {
	tcflag_t c_iflag;		/* input mode flags */
	tcflag_t c_oflag;		/* output mode flags */
	tcflag_t c_cflag;		/* control mode flags */
	tcflag_t c_lflag;		/* local mode flags */
	cc_t c_line;			/* line discipline */
	cc_t c_cc[NCCS];		/* control characters */
	};
	tty.c_cflag &= ~PARENB; // Clear parity bit, disabling parity (most common)
	tty.c_cflag &= ~CSTOPB;
	tty.c_cflag &= ~CSIZE;
	tty.c_cflag |= CS8;
	tty.c_cflag &= ~CRTSCTS;
	tty.c_cflag |= CREAD | CLOCAL; // Turn on READ & ignore ctrl lines (CLOCAL = 1)
	tty.c_lflag &= ~ICANON;
	tty.c_lflag &= ~ECHO; // Disable echo
	tty.c_lflag &= ~ECHOE; // Disable erasure
	tty.c_lflag &= ~ECHONL; // Disable new-line echo
	tty.c_lflag &= ~ISIG; // Disable interpretation of INTR, QUIT and SUSP
	tty.c_iflag &= ~(IXON | IXOFF | IXANY); // Turn off s/w flow ctrl
	tty.c_iflag &= ~(IGNBRK|BRKINT|PARMRK|ISTRIP|INLCR|IGNCR|ICRNL); // Disable any special handling of received bytes
	tty.c_oflag &= ~OPOST; // Prevent special interpretation of output bytes (e.g. newline chars)
	tty.c_oflag &= ~ONLCR;
	tty.c_cc[VTIME] = 10;    // Wait for up to 1s (10 deciseconds), returning as soon as any data is received.
	tty.c_cc[VMIN] = 0;
	//cfsetispeed(&tty, B9600);
	//cfsetospeed(&tty, B9600);
	// Unify
	cfsetspeed(&tty, B9600);
	unsigned char msg[] = { 'T', 'e', 's', 't', '\r' };
	write(serial_port, msg, sizeof(msg));
	printf("Sent %lu bytes. Sent message: %s\n", sizeof(msg), msg);
	char read_buf [256];
	int num_bytes = read(serial_port, &read_buf, sizeof(read_buf));
	if (num_bytes < 0) {
        printf("Error reading: %s", strerror(errno));
  	}
	printf("Read %i bytes. Received message: %s\n", num_bytes, read_buf);
	close(serial_port);
	}
};
