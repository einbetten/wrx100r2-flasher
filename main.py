'''
Created on 15 Aptil 2015.

@author: denis shashunkin, d.shashunkin@yandex.ru
@target: send firmware to wrx100-r2 modem

'''

import sys
import serial
import time
import re
import os
import binascii

comPort = "/dev/ttyUSB0"

#commCGMR = "AT+CGMR"
#answCGMR = re.compile(r'^OK|ERROR|(\+CM[ES] ERROR: \d+)|(COMMAND NOT SUPPORT)$')
#print  answCGMR


'''
Return a list of files from the modem
input: None
return: list
'''
def LsFilesOnTarget():
    print "Call GetRemoteListOfFiles()"
    
'''
Remove file on modem
@ input: string
@ return True or False
'''
def RmFilesOnTarget(file):
    print "Call GetRemoteListOfFiles()"

'''
Get size of host`s file
@ input: filename string
@ return True or False

'''     
def GetLocalFileSize(filename):
    statinfo = os.stat(filename)
    return statinfo.st_size

def SendFile(filename):
    fd = open(filename, "rb")
    fileSize = GetLocalFileSize(filename)
    bytesRead = fd.read()
    if ( fileSize != len(bytesRead) ):
        print "filesize != bytesRead!!!"
        print fileSize
        print len(bytesRead)
        return None
    else:
        #print ' '.join(hex(ord(i)) for i in bytesRead)
        return bytesRead
    
    #for b in bytesRead:


def TryOpenComPort(port):
    try:
        return serial.Serial(
                port,
                baudrate=9600,
                timeout=1,
                parity=serial.PARITY_NONE,
                stopbits=serial.STOPBITS_ONE,
                bytesize=serial.EIGHTBITS
                )
    except:
        return None

def ReadComPortByTimeout(ser, timeout):
    spendTime = 0
    rxBuffer = []
    while (spendTime < timeout):
        rxString = ser.readline()
        #print "Length rxString = %u" % len(rxString)
        if ( len(rxString) > 0 ):
            if ( rxString == b"OK\r\n" or
                    rxString == b"ERROR\r\n" or
                        rxString == b"NO CARRIER\r\n" ):
#                    print "Got 'OK'"
                break
            
            elif ( rxString == b"\r\r\n" or 
                    rxString == b"\r\n" ):
                continue
            rxBuffer.append(rxString)
            #answerList += byte
            #print answerList
            
            #print rxBuffer
              
        time.sleep(0.1)
        spendTime += 0.1
        
    #print 'end ReadComPortByTimeout()'
    return rxBuffer

def main():
    print "Start writing firmware to wrx100r2"
    
    #sys.stderr = sys.stdout
    
    ser = TryOpenComPort(comPort)
    if (ser == None):
        print "Error open %s" % comPort
        sys.exit(0)
    
    #message = "AT"
    #AT+CGMR
    #ser.write(message.encode() + b"\r")
#    ser.write(b"ATE0" + b"\r")
#    time.sleep(0.5)
#    print "%s" % (ser.readall())
    #ser.write(b"AT+CGMR" + b"\r")
    #ReadComPortByTimeout(ser, 2)
    
    #time.sleep(0.5)
    
 #   ser.write(b'AT#WSCRIPT="test1.pyo",340' + b"\r")
 #   ReadComPortByTimeout(ser, 1)
    
 #   print os.getcwd()
 #   ser.write(SendFile("test.pyo"))
    
 #   ReadComPortByTimeout(ser, 2)
    
    ser.write(b'AT#LSCRIPT' + b"\r")
    answer = ReadComPortByTimeout(ser, 1)
    
    # parse list of files
    existFiles = []
    freeBytes = 0
    for current in answer:
        #print current.strip()
        #print ' '.join(hex(ord(i)) for i in current)
        
        #splitAnsw = re.split(r'(?::|\"|,| )',current)[1:]
        #splitAnsw = [1:]
                
        splitAnsw = [x for x in re.split(r'(?::\s|\"|,|\r|\n)', current) if x != ''][1:]
        
        if not splitAnsw:
            continue
        
        print splitAnsw
        
        file,size = splitAnsw
        #print "File: %s\tSize: %u" %(file,int(size))
        
        if file == "free bytes":
            freeBytes = int(size)
        else:
            existFiles.append(file)
        
 #       start = current.find('"')
        #print "start is %s" % start
 #       end = current.find('"', start+1)
        #print "end is %s" % end
        #re.search(r"("*")", current).group(0)
 #       if ( ( start != -1 ) and ( end != -1 )):
 #           existFiles.append(current[start+1:end])
 #       else:
 #           start = current.find('free bytes: ')
 #           if (start != -1):
 #               end = current.find(b'\r\n')
 #               if ( end != -1 ):
 #                   freeBytes = int(current[start + len("free bytes: "):end])

    print freeBytes
#    print type(freeBytes)
    print existFiles
#    print type(existFiles) 
 
    time.sleep(0.5)
    #print "%s" % (ser.readall())
    ser.close()
    sys.exit(0)
    
    print "Exit programm!"

main()