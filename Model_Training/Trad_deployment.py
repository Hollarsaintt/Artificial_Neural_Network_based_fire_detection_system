import paho.mqtt.client as mqtt
import datetime
import RPi.GPIO as GPIO
from time import sleep
from PIL import Image


#Grant access to mqtt broker
mqtt_user = "firedetection"
mqtt_password = "firedetection"

#class_label switch and leds set up
switch_input = 4
green_led = 11 #for data logging or data receiving notification (blinks)
red_led = 10 #for fire notification (blinks)
buzzer = 17
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
GPIO.setup(switch_input, GPIO.IN)
GPIO.setup(green_led, GPIO.OUT, initial = GPIO.LOW)
GPIO.setup(red_led, GPIO.OUT, initial = GPIO.LOW)
GPIO.setup(buzzer, GPIO.OUT, initial = GPIO.LOW)

    
#initialize data_to_log to all -1
data_to_predict = [-1] * 24



def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))
    client.subscribe("/data/1")
    client.subscribe("/data/2")
    client.subscribe("/data/3")
    client.subscribe("/data/4")
    # Add more topics as needed

def on_message(client, userdata, msg):
    global data_to_predict
    #pos_times = 0 #keep track of number of time predictionn is 1
    print(f"Received message on topic {msg.topic}: {msg.payload.decode()}")


    if msg.topic == '/data/1':
        message1 = msg.payload.decode().split()
        for i in range(0,6):
            data_to_predict[i] = message1[i]

    elif msg.topic == '/data/2':
        message2 = msg.payload.decode().split()
        for i in range(6,12):
            data_to_predict[i] = message2[i-6]

    elif msg.topic == '/data/3':
        message3 = msg.payload.decode().split()
        for i in range(12,18):
            data_to_predict[i] = message3[i-12]

    elif msg.topic == '/data/4':
        message4 = msg.payload.decode().split()
        for i in range(18,24):
            data_to_predict[i] = message4[i-18]


    if -1 not in data_to_predict: #check if it has collect all data points messages
    	#blink led to indicate that data has been received
        GPIO.output(green_led, GPIO.HIGH)
        sleep(0.2) #sleep for 200 miliseconds
        GPIO.output(green_led, GPIO.LOW)
        
        if float(data_to_predict[0]) > 35.0 or float(data_to_predict[6])  > 35.0 or float(data_to_predict[12]) > 35.0 or float(data_to_predict[18]) > 35.0:
          #sound notifiers #High red led and #activate buzzer
            im = Image.open('/home/firedetection/Documents/Central_system/Model_Training/fire.gif')
            GPIO.output(red_led, GPIO.HIGH)
            GPIO.output(buzzer, GPIO.HIGH)
              

        elif float(data_to_predict[1]) < 60.0 or float(data_to_predict[7]) < 60.0 or float(data_to_predict[13]) < 60.0 or float(data_to_predict[19]) < 60.0:
        #notifies
            im = Image.open('/home/firedetection/Documents/Central_system/Model_Training/fire.gif')
            GPIO.output(red_led, GPIO.HIGH)
            GPIO.output(buzzer, GPIO.HIGH)
            
        elif float(data_to_predict[2]) > 60.0 or float(data_to_predict[8]) > 60.0 or float(data_to_predict[14]) > 60.0 or float(data_to_predict[20]) > 60.0:
        #notifies
            im = Image.open('/home/firedetection/Documents/Central_system/Model_Training/fire.gif')
            GPIO.output(red_led, GPIO.HIGH)
            GPIO.output(buzzer, GPIO.HIGH)
            
        elif float(data_to_predict[3]) > 60.0 or float(data_to_predict[9]) > 60.0 or float(data_to_predict[15]) > 60.0 or float(data_to_predict[21]) > 60.0:
        #notifies
            im = Image.open('/home/firedetection/Documents/Central_system/Model_Training/fire.gif')
            GPIO.output(red_led, GPIO.HIGH)
            GPIO.output(buzzer, GPIO.HIGH)
        
        elif float(data_to_predict[4]) > 60.0 or float(data_to_predict[10]) > 60.0 or float(data_to_predict[16]) > 60.0 or float(data_to_predict[22]) > 60.0:
        #notifies
            im = Image.open('/home/firedetection/Documents/Central_system/Model_Training/fire.gif')
            GPIO.output(red_led, GPIO.HIGH)
            GPIO.output(buzzer, GPIO.HIGH)
              
                
        else:
            #pos_times = 0 #reinitialize if prediction is zero
            #de sound notifiers #de High red led and deactivate the buzzer
            im = Image.open('/home/firedetection/Documents/Central_system/Model_Training/fire.gif')
            im.close()
            GPIO.output(red_led, GPIO.LOW)
            GPIO.output(buzzer, GPIO.LOW)
        
        
        data_to_predict = [-1] * 24 #re-initialize data_to_predict
        sleep(5) #sleep for 3seconds before trying to get another data for prediction

client = mqtt.Client()
client.username_pw_set(mqtt_user, mqtt_password)
client.on_connect = on_connect
client.on_message = on_message

broker_address = "192.168.43.174"
client.connect(broker_address, 1883, 60)
client.loop_forever()

