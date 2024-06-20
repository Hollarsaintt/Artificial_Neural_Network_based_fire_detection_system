import joblib
import numpy as np
from PIL import Image

import paho.mqtt.client as mqtt
import RPi.GPIO as GPIO
from time import sleep


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

    
#initialize data_to_predict 
data_to_predict = [-1] * 24

#load trained models of the different subgroups
ANN_model = joblib.load('/home/firedetection/Documents/Central_system/Model_Training/pkl/ANN_cleaned.pkl')
LR_model = joblib.load('/home/firedetection/Documents/Central_system/Model_Training/logistic_r.pkl')
RF_model = joblib.load('/home/firedetection/Documents/Central_system/Model_Training/first_random_forest_model.pkl')

#LR_model = joblib.load('/home/firedetection/Documents/Central_system/Model_Training/pkl/logistic_regression_model.pkl')
#RF_model = joblib.load('/home/firedetection/Documents/Central_system/Model_Training/pkl/random_forest_model.pkl')



def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))
    client.subscribe("/data/1")
    client.subscribe("/data/2")
    client.subscribe("/data/3")
    client.subscribe("/data/4")
    # Add more topics as needed
pos_times = 0  #keep track of number of time predictionn is 1
def on_message(client, userdata, msg):
    global data_to_predict
    global pos_times
    print(f"Received message on topic {msg.topic}: {msg.payload.decode()}")

    if msg.topic == '/data/1':
        message1 = msg.payload.decode().split()
        for i in range(0,6):
            data_to_predict[i] = float(message1[i])

    elif msg.topic == '/data/2':
        message2 = msg.payload.decode().split()
        for i in range(6,12):
            data_to_predict[i] = float(message2[i-6])

    elif msg.topic == '/data/3':
        message3 = msg.payload.decode().split()
        for i in range(12,18):
            data_to_predict[i] = float(message3[i-12])

    elif msg.topic == '/data/4':
        message4 = msg.payload.decode().split()
        for i in range(18,24):
            data_to_predict[i] = float(message4[i-18])


    if -1 not in data_to_predict: #check if it has collect all data points messages
    	#blink led to indicate that data has been received
        GPIO.output(green_led, GPIO.HIGH)
        sleep(0.2) #sleep for 200 miliseconds
        GPIO.output(green_led, GPIO.LOW)
        
        
        data_np = np.array(data_to_predict)
        data = data_np.reshape(1, -1)
        
        ANN_pred = ANN_model.predict(data)
        LR_pred = LR_model.predict(data)
        RF_pred = RF_model.predict(data)
        
        print(LR_pred)
        print(RF_pred)
        
        ANN_pred = float(ANN_pred[0][0])
        LR_pred = float(LR_pred[0])
        RF_pred = float(RF_pred[0])
        
        ANN_pred = int(ANN_pred > 0.8)
        LR_pred = int(LR_pred > 0.8)
        RF_pred = int(RF_pred > 0.8)
        
        
        pred_arr = [ANN_pred, LR_pred, RF_pred]
        print(pred_arr)
        print(sum(pred_arr))
        print(pos_times)
        
        if sum(pred_arr) >= 2: #majority voting triggers notifiers
            pos_times = pos_times + 1
            if pos_times == 2:
                #sound notifiers #High red led and #activate buzzer
                im = Image.open('/home/firedetection/Documents/Central_system/Model_Training/fire.gif')
                im.show()
                GPIO.output(red_led, GPIO.HIGH)
                GPIO.output(buzzer, GPIO.HIGH)
                pos_times = 0 #reinitialize
        else:
            pos_times = 0 #reinitialize if prediction is zero
            #de sound notifiers #de High red led and deactivate the buzzer
            GPIO.output(red_led, GPIO.LOW)
            GPIO.output(buzzer, GPIO.LOW)
            im = Image.open('/home/firedetection/Documents/Central_system/Model_Training/fire.gif')
            im.close()
        
        data_to_predict = [-1] * 24 #re-initialize data_to_predict
        sleep(3) #sleep for 3seconds before trying to get another data for prediction """

client = mqtt.Client()
client.username_pw_set(mqtt_user, mqtt_password)
client.on_connect = on_connect
client.on_message = on_message

broker_address = "192.168.43.174"
client.connect(broker_address, 1883, 60)
client.loop_forever()
