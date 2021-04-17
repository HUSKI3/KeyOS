build:
	clang++ main.cpp -lusb -lusb-1.0 -lX11 -lXrandr -I/usr/include/jsoncpp  -o papd 
test:
	@sudo truncate -s 0 /var/log/syslog
	@clang++ main.cpp -lusb -lusb-1.0 -lX11 -lXrandr -I/usr/include/jsoncpp  -o papd 
	@./papd -d
	@echo "================================ PID ================================="
	@ps -xj | grep papd
	@echo "================================ Logs ================================"
	@grep papd /var/log/syslog
	@echo "======================================================================"
