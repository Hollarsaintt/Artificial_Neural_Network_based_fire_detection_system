from PIL import Image
from time import sleep
im = Image.open('/home/hollarsaint/Documents/School_Project_Intelligent_Fire_DS/Model_Training/fire.gif')

im.show()
sleep(1)
im.close()
