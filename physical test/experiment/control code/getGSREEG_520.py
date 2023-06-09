import serial
import time
import threading
import matplotlib.pyplot as plt
import re
import os
os.environ['PYGAME_HIDE_SUPPORT_PROMPT']="hide"
import pygame
from colorama import Fore, Style


global stop
stop =False

def play_music(filename, name):
    try:
        global stop
        while not stop:
            pygame.mixer.init()
            pygame.mixer.music.load(filename)
            tag_file(name[0])#tag in file when music starts
            tag_file(name[1])
            pygame.mixer.music.play()
            while pygame.mixer.music.get_busy():
                time.sleep(0.1)
            print("Thank You :)")
            tag_file(name[0])#tag in file when music ends
            tag_file(name[1])
            time.sleep(1) # 1 second pause 
            stop=True
        #comment=input("Any comments?");
    except Exception as e:
        # Handle the exception here or print a custom error message
        print("An error occurred while playing the music:", str(e))

def tag_file(name):
    try:
        with open(name + '.txt', 'a') as file:
            start_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
            file.write("AAAAA\n Music mark\n")
            file.write(start_time + '\n')
    except Exception as e:
        # Handle the exception here or print a custom error message
        print("An error occurred while tagging the file:", str(e))

def start_file(name):
    try:
        with open(name + '.txt', 'w') as file:
            start_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
            file.write("READY\n")
            file.write(start_time + '\n')
        #print("File initialization succeeded!")
    except Exception as e:
        # Handle the exception here or print a custom error message
        print("An error occurred while initializing the file:", str(e))

def read_GSR(ser, name):
    try:
        global stop
        while not stop:
            #while True:
            if ser.in_waiting > 0:
                with open(name + '.txt', 'a') as file:
                    data = ser.readline().decode().strip()
                    file.write(data + '\n')
        print("GSR file is saved")
    except Exception as e:
        # Handle the exception here or print a custom error message
        print("An error occurred while reading GSR:", str(e))

def read_EEG(ser, name):
    try:
        global stop
        while not stop:
            #while True:
            if ser.in_waiting > 0:
                with open(name + '.txt', 'a') as file:
                    data = ser.readline().strip()
                    file.write(data.hex() + '\n')  
        print("EEG file is saved")  

    except Exception as e:
        # Handle the exception here or print a custom error message
        print("An error occurred while reading EEG:", str(e))
        

def plotGSR(fileID):
    with open (fileID+'_GSR.txt', 'r') as file:
        # Read the contents of the file
        contents = file.read()
        
        num_tem = re.findall(r'\d+', contents)
        
        # Convert the extracted numbers to integers
        num_list = [int(num) for num in num_tem]
        
        end_index= num_list[12:].index(2023)+12 #the last dataindex 
        
        X= [num for num in range(0, len(num_list[12:end_index]))]
        
        plt.plot(X,num_list[12:end_index], linewidth=2.0)
        
        
        ddot=len(X)/981
        ticks=[]
        label = list(range(1, 13))
        for i in range(10,900,80):#12 songs begin time
            ticks.append(i*ddot)
            
        plt.xticks(ticks,label)
        plt.grid(True)
        plt.show();
        plt.savefig(fileID+'plot.png');



def main():

    
    input(Fore.GREEN+"------W E L C O M E ! ! !------\n (Press enter to continue.)\n (If you feel uncomfortable, you can quit anytime by pressing Ctrl+C)")
    personCode = input(Style.RESET_ALL+"Type your code here (the one used in the survey): ")
    emotion = input("How do you feel today: ")
    command = input("Are you ready? Lets play music !\n\
(Press enter to continue.)")

    port1 = '/dev/ttyUSB0'  # Replace with the actual port for device 1
    port2 = '/dev/rfcomm0'  # Replace with the actual port for device 2

    baud_rate_1 = 9600  # Replace with the appropriate baud rate
    baud_rate_2 = 9600
    serial_port1 = serial.Serial(port1, baud_rate_1)
    serial_port2 = serial.Serial(port2, baud_rate_2)

    name = [personCode+"_GSR", personCode + "_EEG"]

    start_file(name[0])
    start_file(name[1])

    thread1 = threading.Thread(target=read_GSR, args=(serial_port1, name[0]))
    thread2 = threading.Thread(target=read_EEG, args=(serial_port2, name[1]))
    thread3 = threading.Thread(target=play_music, args=("music.mp3", name))

    thread3.start()
    thread1.start()
    thread2.start()
    
    thread1.join();
    thread2.join();
    comment=input("Comments? ")
    print("Have a lovely day!")  
    with open ("info.txt","a")as file:
        file.write(personCode+':'+emotion+comment+'\n');
    
    plotGSR(personCode);

if __name__ == '__main__':
    main()
