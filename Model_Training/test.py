import joblib
import numpy as np

load_model = joblib.load('/home/firedetection/Documents/Central_system/Model_Training/logistic_r.pkl')

new_data =np.array([38.87,43.39,0.00,16.00,0.00,11.67,35.62,53.36,0.00,0.00,0.00,18.33,58.07,19.89,0.00,12.00,1694.00,15.00,34.22,100.00,0.00,26.00,0.00,25.83])
arr = new_data.reshape(1, -1)
prediction = load_model.predict(arr)
print(prediction)
