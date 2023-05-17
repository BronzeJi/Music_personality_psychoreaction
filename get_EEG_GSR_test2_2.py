import serial
import time
import threading

def start_file(name):
	with open(name+'.txt', 'w') as file:
		start_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
		file.write("READY\n")
		file.write(start_time + '\n')
	#file.close();
	print("file close after init"+name);
	print(". File initial successed!");
	#file.read();

def read_GSR(ser, name):
    # Open the file in write mode
    file=open('GSR.txt', 'a');
    file.write('file open \n');
    while True:
        if ser.in_waiting > 0:
            data = ser.readline().decode().strip()
            file.write(data + '\n')
            print(data)
    print("GSR close");
    file.close();
		
    '''try:
        while True:
            if ser.in_waiting > 0:
                data = ser.readline().decode().strip()
                file.write(data + '\n')
                print(data)
    except KeyboardInterrupt:
	# Handle Ctrl+C interruption
        pass
    finally:
	# Close the file
        end_time= time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        file.write("Close file!"+end_time);
        file.close()'''

def read_EEG(ser, name):
    # Open the file in write mode
    with open(name+'.txt', 'a') as file:
        file.write('file open \n')
        while True:
            if ser.in_waiting > 0:
                data = ser.readline().strip()  # Read the data as bytes
                # Perform operations with the byte data
                # For example, you can print the byte data as hexadecimal
                print("Received data:", data.hex())
                file.write(data.hex() + '\n')
    #print("close eeg!!!!!!!!!!!")
 
"""def read_stop(thread1,thread2):
	
	while True:
		stop=input("###################typr here/n");
		if stop=="s":
			thread1.stop();
			thread2.stop();
			print("#############/n")
		print("333333333/n")"""
    
def main():
    port1 = '/dev/ttyUSB0'  # Replace with the actual port for device 1
    port2 = '/dev/rfcomm0'  # Replace with the actual port for device 2

    baud_rate_1 = 9600  # Replace with the appropriate baud rate
    baud_rate_2 = 9600
    serial_port1 = serial.Serial(port1, baud_rate_1)
    serial_port2 = serial.Serial(port2, baud_rate_2)

    start_file("GSR");
    start_file("EEG");

    thread1 = threading.Thread(target=read_GSR, args=(serial_port1, "GSR"))
    thread2 = threading.Thread(target=read_EEG, args=(serial_port2, "EEG"))
   
    try:
        thread1.start()
        thread2.start()
    except KeyboardInterrupt:
	# Handle Ctrl+C interruption
        """with open('GSR.txt', 'w') as file:
            start_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
            file.write("made!!!!!!!\\n")
            file.write(start_time + '\n')"""
        pass;
    finally:
		# Close the file
        print("nihao");
        with open('GSR.txt', 'a') as file:
            start_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
            file.write("!!!!!!!\n")
            file.write(start_time + '\n')

if __name__ == '__main__':
    main()
