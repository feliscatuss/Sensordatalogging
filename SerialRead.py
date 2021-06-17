import serial      #To read values directly from Serial Port
import time        #Used to get waiting time in the system
import csv         #For storing values in CSV file
import datetime    #For current Time
from ftplib import FTP    #For FTP File transfer
import os         #Using it here to change Directory

list_values = []
list_in_float = []
readingnum = 1

def file_RW():
    try:
        esp =  serial.Serial('com3',9600) #specify your port name and baud rate

    except serial.SerialException:
        print(" SerialException has occured, please reconnect your controller to port")
        answer = input("Type ok After connecting controller to port: ")
        if(answer == 'ok'):
            esp = serial.Serial('com3',9600)
    finally:
        
        print('Established serial connection to port ')
        esp_data = esp.readline()
        decoded_values = str(esp_data[0:len(esp_data)-2].decode("utf-8"))  #decoding serial port readings
        list_values = decoded_values.split('x')  #Spliting string 

        for item in list_values:
            
            list_in_float.append(str(item))   #appending only temp and humidity
        

        global readingnum 
        print(f'Collected reading no: {readingnum} from Serial Port: {list_in_float}')   
        now = datetime.datetime.now()
        curtime = now.strftime("%d/%m/%Y %H:%M:%S")    #Instance at which reading was received

        counter= readingnum

        temptrash = str(list_in_float[0])  #indexing to temp value
        temp = filter(str.isdigit, temptrash)
        cleantemp = "".join(temp)

        try:
            temperature = float(cleantemp)/100
        except ValueError:
            temperature = float(cleantemp+"1")/100

        

        
        humidity = str(list_in_float[1])         #indexing to Humid value

        data_dict = {}
        for variable in ['curtime','humidity','temperature']:
            data_dict[variable] = eval(variable)             #Creating a dictionary to store Time, Humidity, Temperature
        values = [data_dict[key]for key in data_dict.keys()]     #Creating a list of values

        global File_name              #Making it global declaration 
        #writing readings in csv file     
        with open(f'{File_name}.csv','a', newline = "") as f:        #Opening File in Append mode
            write = csv.writer(f)
            write.writerow(values)    
  
        list_in_float.clear()       #Clearing all variables in lists
        list_values.clear()         
        global readingwait
        time.sleep(readingwait)    #Interval in Readings
        #time.sleep(12)
        readingnum+=1
        #print(readingnum)
        #function ends here

#User Inputs
thismany = int(input("How many reading would you like to take ? : "))   
readingwait = int(input("Timeinterval: "))   
File_name = input("Give a name to your data file: ")
headers = ['Time','Humidity','Temperature']

#file creation
with open(f'{File_name}.csv','w', newline="") as csvf:   
    write = csv.writer(csvf)                          
    write.writerow(headers)     #Writing Headers in every new file generated.
print(f"Succesfully created {File_name}.csv file")

#counter
counter = 1  
while counter< thismany+1:
    file_RW()            #Calling function to take readings
    counter+= 1
print(f"Collected {counter-1} readings ")

#for uploading data through FTP
print(f"Uploading {File_name}.csv to FTP Server")
print('https:replaceitwithyourftpserveraddress)

os.chdir(r"yourdirnamewhereyouwouldliketocreatecsvfile")  #changing directory
ftp = FTP('Replaceitwithyourftpserveraddress')
ftp.login('yourftpusername','yourftppassword') #logging in with credentials
print("Logged into FTP server")
ftp.cwd('/replaceitwithyourdir/')  #Directory in FTP Server
with open(f'{File_name}.csv', 'rb') as f:   #FTP Only works with byte like data hence the 'rb' (Read binary)
    ftp.storlines('STOR %s' % f'{File_name}.csv', f)  
ftp.quit()
print("Upload finished cheers!!!")
print("Logged out from FTP server")


#For closing program 
print("Closing program in 20 seconds, run again to record sessions ")
time.sleep(20)    #IDKWHY20SECONDS
print("Program closed") 

