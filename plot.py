import csv
import copy
from itertools import chain
import matplotlib.pyplot as plt
from ftplib import FTP

 
ftp = FTP('Replaceitwithyourftpserveraddress')
ftp.login('yourftpusername','yourftppassword')
ftp.cwd('/yourftpdirname')
ftp.retrlines('LIST')
file_n = input("\n Type a file name without the extension: ")
file_name = (f'{file_n}.csv')
my_file = open(file_name, 'wb')
ftp.retrbinary('RETR ' + file_name, my_file.write, 1024)
my_file.close()
ftp.quit()

with open(file_name, newline='') as f:
    reader = csv.reader(f)
    data = list(reader)
    data1=copy.deepcopy(data)
    data2=copy.deepcopy(data)
    data3=copy.deepcopy(data)
    lines= len(data)
    print(lines) 

""" print (data1)  """


l=0
while 0<=l<lines:
    data1[l].pop(2)
    data1[l].pop(1)
    flatlist1=[]
    for elem in data1:
        flatlist1.extend(elem)

    l+=1
flatlist1.remove("Time")
print(flatlist1) 

m=0
while  0<=m<lines:
    data2[m].pop(2)
    data2[m].pop(0)
    flatlist2=[]
    for elem in data2:
        flatlist2.extend(elem)
    m+=1
flatlist2.remove("Humidity")
print(flatlist2) 

n=0
while 0<=n<lines:
    data3[n].pop(0)
    data3[n].pop(0)
    flatlist3=[]
    for elem in data3:
        flatlist3.extend(elem)
    n+=1
flatlist3.remove("Temperature")
print(flatlist3)  

plt.figure(figsize=(12,4))

plt.plot(flatlist1,flatlist3,label="Temperature")
plt.plot(flatlist1,flatlist2,label='Humidity')
plt.legend()
""" plt.title("Minutely") """
plt.xlabel("Time")
plt.ylabel("Temperature(deg C)/Humidity(%)")
""" plt.xlim(0, 25) """
plt.xticks(flatlist1,flatlist1, rotation='vertical')
""" plt.yscale("linear") """
plt.grid()
plt.subplots_adjust(left=0.125, bottom=0.3, right=0.9, top=0.9, wspace=None, hspace=None)
plt.savefig(file_n+".png",dpi=300)
plt.show()

img_name = (f'{file_n}'+".png")
file = open(img_name,'rb')
ftp = FTP('Replaceitwithyourftpserveraddress')
ftp.login('yourftpusername','yourftppassword')
ftp.cwd('/yourdir/')
ftp.storbinary('STOR ' + img_name, open(img_name,'rb'))
ftp.quit() 
my_file.close()


""" print("all files are stored in htdocs") """

func=input("Do you want to upload or download?\nIf upload enter 1 else 0\n")
if func=="1":
    ftp = FTP('Replaceitwithyourftpserveraddress')
    ftp.login('yourftpusername','yourftppassword')
    ftp.cwd('/yourdir/')
    
    file_name =input("Enter name of file which is to be uploaded\n")
    file = open(file_name,'rb')
    ftp.storbinary('STOR ' + file_name, open(file_name,'rb'))
    file.close()
    ftp.quit()
    print("Done")
   
    

elif func=="0":
    ftp = FTP('Replaceitwithyourftpserveraddress')
    ftp.login('yourftpusername','yourftppassword')

    ftp.cwd('/yourdir/')
    ftp.retrlines('LIST')
    
    file_name = str(input("Enter name of file with extension as shown in the list\n"))
    my_file = open(file_name, 'wb')
    ftp.retrbinary('RETR ' + file_name, my_file.write, 1024)
    my_file.close()
    ftp.quit()
    print("Done")
    
else :
    print("Invalid option run again")
