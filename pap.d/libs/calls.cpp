#include "serial.cpp"

class caller{
public:
static int process(std::string call)
{
	std::cout << "Opening "<< call << std::endl;
	const char * call_new = call.c_str();
	int test_serial_port = open(call_new, O_RDWR | O_CREAT);
        serial::usb1(test_serial_port);
        serial::termi(test_serial_port);
	return 0;
}
};
