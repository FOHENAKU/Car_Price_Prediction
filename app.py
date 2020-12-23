from flask import Flask, render_template, request
import jsonify
import requests
import pickle
import numpy as np
import sklearn
from sklearn.preprocessing import StandardScaler
app = Flask(__name__)
model = pickle.load(open('rdm_frst_regr_model.pkl', 'rb'))
@app.route('/',methods=['GET'])
def Home():
    return render_template('index.html')


standard_to = StandardScaler()
@app.route("/predict", methods=['POST'])
def predict():
    Fuel_Type_Diesel=0
    if request.method == 'POST':
        Year = int(request.form['Year'])
        Mileage=int(request.form['Mileage'])
        Owner=int(request.form['Owner'])
        Fuel_Petrol=request.form['Fuel_Type_Petrol']
        if(Fuel_Petrol=='Petrol'):
                Fuel_Petrol=1
                Fuel_Diesel=0
                Fuel_LPG=0
                Fuel_Electric=0
        elif(Fuel_Petrol=='Diesel'):
                Fuel_Petrol=0
                Fuel_Diesel=1
                Fuel_LPG=0
                Fuel_Electricity=0
        elif(Fuel_Petrol=='LPG'):
                Fuel_Petrol=0
                Fuel_Diesel=0
                Fuel_LPG=1
                Fuel_Electric=0               
        else:
                Fuel_Petrol=0
                Fuel_Diesel=0
                Fuel_LPG=0
                Fuel_Electric=1               
                 
                
        Year=2020-Year
        Seller_Type_Individual=request.form['Seller_Type_Individual']
        if(Seller_Type_Individual=='Individual'):
            Seller_Type_Individual=1
        else:
            Seller_Type_Individual=0
            
        Transmission_Mannual=request.form['Transmission_Mannual']
        if(Transmission_Mannual=='Mannual'):
            Transmission_Mannual=1
        else:
            Transmission_Mannual=0
            
        prediction=model.predict([[Mileage,Owner,Year,Fuel_Petrol,Fuel_Diesel,Fuel_LPG,Fuel_Electric,Seller_Type_Individual,Transmission_Mannual]])
        output=round(prediction[0],2)
        if output<0:
            return render_template('index.html',prediction_texts="Sorry you cannot sell this car")
        else:
            return render_template('index.html',prediction_text="You Can Sell The Car at {}".format(output))
    else:
        return render_template('index.html')

if __name__=="__main__":
    app.run(debug=True)