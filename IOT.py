#!/usr/local/bin/python
import RPi.GPIO as GPIO
import time
import dropbox
import picamera
from datetime import datetime
from time import sleep
camera = picamera.PiCamera()

GPIO.setmode(GPIO.BOARD)
GPIO.setup(12,GPIO.OUT)
GPIO.setwarnings(False)
GPIO.setup(11, GPIO.IN)         #Read output from PIR motion sensor
GPIO.setup(3, GPIO.OUT)         #LED output pin

#define the pin that goes to the circuit
pin_to_circuit = 7
def cloud(name):
 	dbx=dropbox.Dropbox('9PPzW__QX7AAAAAAAAAADve08bN0R2e4ZsS-UjpfPEJ0eBaE5B_D_JLbVz9Hp3dN')
	
	with open("/home/pi/Darshan/photo/"+name, "rb") as f:
        	dbx.files_upload(f.read(),'/'+name, mute = True)
        #f=open("up.txt")
	print("open")
        #dbx.files_upload(f,'/upload.txt')
	f.close()

def rc_time (pin_to_circuit):
    count = 0
  
    #Output on the pin for 
    GPIO.setup(pin_to_circuit, GPIO.OUT)
    GPIO.output(pin_to_circuit, GPIO.LOW)
    time.sleep(0.1)

    #Change the pin back to input
    GPIO.setup(pin_to_circuit, GPIO.IN)
  
    #Count until the pin goes high
    while (GPIO.input(pin_to_circuit) == GPIO.LOW):
        count += 1

    return count

#Catch when script is interrupted, cleanup correctly
def light():
       	cn=rc_time(pin_to_circuit)
        print(cn)
	if(cn>1500):
		print "LED on"
		GPIO.output(12,GPIO.HIGH)
	else:
		print "LED off"
		GPIO.output(12,GPIO.LOW)
	
def capture():
#	print("1")
        name=datetime.now().strftime('%Y-%m-%d_%H:%M:%S')
	name=name+'.jpg'
#	print("2")
	light()
       	camera.capture('photo/'+name)
	print('done')
	cloud(name)
	print("upload")
	GPIO.output(12,GPIO.LOW) #switch of the light after the photo
        #capture()
        

while True:
	
    i=GPIO.input(11)
    if i==0:                 #When output from motion sensor is LOW
        print "No intruders",i
        time.sleep(0.1)
    elif i==1:               #When output from motion sensor is HIGH
        print "Intruder detected",i
        capture()
        time.sleep(10)
