import numpy as np
import pandas as pd
import seaborn as sns
from PIL import Image

import tensorflow as tf
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense
import matplotlib.pyplot as plt
from sklearn.metrics import accuracy_score
from sklearn.metrics import f1_score
from sklearn.preprocessing import StandardScaler

import paho.mqtt.client as mqtt
import RPi.GPIO as GPIO
from time import sleep

# Load data from Excel sheet
data = pd.read_excel('/home/hollarsaint/Documents/School_Project_Intelligent_Fire_DS/Model_Training/OurDataSheetN.xlsx')

# data has features in columns 1-24 and the target variable in the last column (25th)
X = data.iloc[:, 1:25].values
y = data.iloc[:, 25].values

# Split data into training and testing sets (adjust as needed
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Normalize input features if necessary
sc = StandardScaler()
X_train = sc.fit_transform(X_train)

#for group 1
model1 = Sequential(
    	[
		tf.keras.Input(shape=(24,)),
		Dense(10, activation='sigmoid', name = 'layer1'), #using 10 hidden layers
		Dense(1, activation='sigmoid', name = 'layer2')
     	]
	)

#Assign the trained weight values (model1 ---> Artificial Neural Network)
W1 = np.array([[-9.13263559e-01  8.48385394e-01 -1.01333094e+00 -1.80591071e+00
  -8.55783522e-01  1.32804489e+00 -1.47663283e+00  1.49052119e+00
   9.44239855e-01 -1.38118541e+00]
 [ 4.51381296e-01  1.06618035e+00  7.72578895e-01  6.80561185e-01
  -1.19358194e+00 -4.10878152e-01  8.02703321e-01 -7.89371729e-01
   1.60419774e+00 -1.68712223e+00]
 [-1.19807303e-01 -1.57966882e-01 -9.15267169e-02 -2.02003509e-01
   2.66786784e-01 -3.08260322e-03 -1.11544162e-01 -3.17741483e-01
  -5.72736263e-02  2.60090500e-01]
 [-4.94857639e-01  9.12300408e-01 -8.19455326e-01 -1.12716091e+00
  -4.96654481e-01  6.72876298e-01 -1.11718988e+00  5.16825140e-01
   4.79250818e-01 -8.80428135e-01]
 [-2.76706338e-01  9.09828603e-01 -3.38134646e-01 -5.47142863e-01
  -7.46893764e-01  5.60024381e-01 -4.55855340e-01  4.66305345e-01
   1.25781882e+00 -7.52638638e-01]
 [ 1.88069358e-01 -3.49484205e-01  3.23020667e-01  5.23525000e-01
   8.56208980e-01 -9.85314965e-01  6.05139196e-01 -6.95249200e-01
  -2.41057687e-02  6.93145454e-01]
 [-7.54278064e-01  1.73619986e+00 -9.63616967e-01 -1.57964230e+00
  -1.50368702e+00  1.51869750e+00 -1.01777256e+00  9.57922518e-01
   1.35733771e+00 -1.36688459e+00]
 [ 5.56303620e-01  1.05407786e+00  5.13206899e-01  7.29082704e-01
  -7.46124625e-01 -3.88957292e-01  6.81089044e-01 -5.97747624e-01
   1.14380527e+00 -9.17668819e-01]
 [ 2.89829880e-01 -3.60852480e-02  3.01353306e-01 -3.93839806e-01
   4.02177840e-01 -2.44943202e-02 -3.66196275e-01 -9.70090330e-02
   1.01630121e-01 -8.44912529e-02]
 [-7.88677931e-01  6.51903331e-01 -4.74505872e-01 -8.29723358e-01
  -1.02011943e+00  6.41061306e-01 -5.59548020e-01  5.25727749e-01
   1.90416765e+00 -6.48858130e-01]
 [-5.28143406e-01  7.09192693e-01 -8.88846636e-01 -8.14122438e-01
  -9.15055990e-01  1.04905105e+00 -8.59881401e-01  6.43518806e-01
   1.16017461e+00 -7.58842170e-01]
 [ 6.16754949e-01 -1.55675009e-01  4.38679665e-01  4.94998753e-01
   2.61478961e-01 -4.62630153e-01  4.14190650e-01 -4.16983098e-01
  -3.25669684e-02  1.89413249e-01]
 [-1.03595841e+00  1.70752358e+00 -1.62817168e+00 -1.97922552e+00
  -1.38094020e+00  1.01718771e+00 -1.06826842e+00  1.43190181e+00
   2.44010687e+00 -1.53922749e+00]
 [ 7.95270085e-01  2.78032452e-01  7.63662279e-01  9.44403350e-01
  -1.81433707e-01 -1.30499518e+00  1.07481623e+00 -1.32132196e+00
   9.22554433e-01  4.07916866e-03]
 [ 3.70936483e-01  1.47513598e-01  8.30704272e-02 -2.25963786e-01
  -3.43431264e-01 -3.17411572e-01 -2.96355426e-01  2.42678195e-01
   3.54459494e-01 -1.87464282e-01]
 [ 9.72435847e-02 -1.09857865e-01 -1.57505304e-01 -1.20090991e-01
   3.16002220e-01  1.24740161e-01 -1.16775453e-01  1.99201465e-01
  -6.87308013e-01  4.36805934e-01]
 [-9.95725095e-01  1.13748014e+00 -1.32959580e+00 -1.75017095e+00
  -1.15032971e+00  1.21527696e+00 -1.62124956e+00  9.48508501e-01
   1.44251776e+00 -1.01435983e+00]
 [ 8.32606792e-01 -4.10776407e-01  8.08788776e-01  8.57675612e-01
   2.95095384e-01 -3.79029810e-01  7.87893414e-01 -7.42457926e-01
   1.17649771e-01  4.66287881e-01]
 [-1.08022058e+00  6.26641273e-01 -1.57753551e+00 -2.63055634e+00
  -1.23827255e+00  1.72893882e+00 -2.16255522e+00  1.42319429e+00
   2.46579833e-02 -1.22278118e+00]
 [ 4.99526531e-01  2.23736572e+00  2.76930928e-01  2.66400748e-03
  -2.03444529e+00 -3.22222888e-01  5.79628885e-01 -6.04500830e-01
   4.12594128e+00 -2.37355804e+00]
 [-3.80842775e-01 -3.36514801e-01  4.95411754e-02  1.24955326e-01
   3.67104203e-01 -1.64961368e-01 -1.27123386e-01 -3.20479572e-02
   1.42666310e-01  2.30824322e-01]
 [ 3.35866809e-01  8.37997869e-02  2.93052435e-01  8.94442916e-01
  -8.98861140e-02 -1.97391078e-01  4.52469766e-01 -6.20739758e-01
   1.71087384e-01 -1.72914982e-01]
 [-9.55495179e-01  8.91413331e-01 -6.69383764e-01 -5.37196696e-01
  -3.43269616e-01  7.22343564e-01 -7.31386662e-01  4.92591769e-01
   1.34188521e+00 -9.78359640e-01]
 [-2.02342033e-01  3.17993492e-01 -1.51367575e-01 -2.18135476e-01
  -3.24278235e-01  3.51684511e-01 -2.00724095e-01  4.81797010e-01
   6.33555949e-02 -3.29245329e-01]] )

b1 = np.array([-0.5815199   0.6641463  -0.8852635  -1.2784353  -0.7525275   0.8836851
 -1.0417453   0.65584695 -0.9016939  -0.773622  ])
 
W2 = np.array([[-0.8429078]
	 [ 3.3444827]
	 [-1.1286826]
	 [-1.1210185]
	 [-1.994257 ]
	 [ 2.5478222]
	 [-1.1030408]
	 [ 2.5242636]
	 [ 2.5828793]
	 [-1.7091254]])
	 
b2 = np.array([1.0066196])

model1.get_layer("layer1").set_weights([W1,b1])
model1.get_layer("layer2").set_weights([W2,b2])


#Grant access to mqtt broker
mqtt_user = "firedetection"
mqtt_password = "firedetection"

#class_label switch and leds set up
switch_input = 4
green_led = 11 #for data logging or data receiving notification (blinks)
red_led = 10 #for fire notification (blinks)
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
GPIO.setup(switch_input, GPIO.IN)
GPIO.setup(green_led, GPIO.OUT, initial = GPIO.LOW)
GPIO.setup(red_led, GPIO.OUT, initial = GPIO.LOW)

    
#initialize data_to_predict 
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
    pos_times = 0 #keep track of number of time predictionn is 1
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
        
        
        #preprocess data and combine with trained model, then predict.
        data_np = np.array(data_to_predict)
        data_norm = sc.transform(data_np)
        
        pred1 = model1.predict(data_norm)
	pred1_class = (pred > 0.5).astype(int)
	
	if pred1_class == 1:
		pos_times = pos_times + 1
		if pos_times == 2
			#sound notifiers #High red led and #activate buzzer
			im = Image.open('/home/hollarsaint/Documents/School_Project_Intelligent_Fire_DS/Model_Training/fire.gif')
			pos_times = 0 #reinitialize
	else:
		pos_times = 0 #reinitialize if prediction is zero
		#de sound notifiers #de High red led and deactivate the buzzer
		im.close()
        
 

        
        
        data_to_predict = [-1] * 24 #re-initialize data_to_predict
        sleep(3) #sleep for 3seconds before trying to get another data for prediction

client = mqtt.Client()
client.username_pw_set(mqtt_user, mqtt_password)
client.on_connect = on_connect
client.on_message = on_message

broker_address = "192.168.43.174"
client.connect(broker_address, 1883, 60)
client.loop_forever()
