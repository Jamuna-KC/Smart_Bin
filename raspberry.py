# code running in Raspberry-pi which senses the Ultrasonic sensor value and updates it to the Firebase
from firebase import firebase
import RPi.GPIO as GPIO
import time
import datetime as dt

# url of the Firebase
url='your_firebase_url'
firebase=firebase.FirebaseApplication(url)
# setting up GPIO pins
GPIO.setmode(GPIO.BCM)
GPIO_TRIG=5
GPIO_ECHO=6
GPIO.setwarnings(False)
GPIO.setup(GPIO_TRIG,GPIO.OUT)
GPIO.setup(GPIO_ECHO,GPIO.IN)
# reading ultrasonic values every 5 seconds
while(1):
    time.sleep(5)
    GPIO.output(GPIO_TRIG,True)
    time.sleep(0.0001)
    GPIO.output(GPIO_TRIG,False)

    while(GPIO.input(GPIO_ECHO)==False):
        start=time.time()

    while(GPIO.input(GPIO_ECHO)==True):
        end=time.time()

    sig_time=end-start
    distance=sig_time/0.00005
    timestamp= dt.datetime.now()
    print("Timestamp : " , timestamp)
    print("Distance:{}cm",format(round(distance,2)))
    dist=firebase.put("S-001","Distance",round(distance,2))
    tim=firebase.put("S-001","Time",timestamp)

GPIO.cleanup()

# the Uploaded data to the firebase will be further fetched in program analysis_pannel.py to display the fill level Graphically
