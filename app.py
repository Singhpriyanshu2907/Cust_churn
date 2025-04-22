import joblib
import numpy as np
from config.paths import model_path
from flask import Flask, render_template,request

app = Flask(__name__)

loaded_model = joblib.load(model_path)

@app.route('/',methods=['GET','POST'])
def index():
    if request.method=='POST':

        arrivalmonth = int(request.form["arrival_month"])
        Totalspend = float(request.form["Total_spend"])
        noofspecialrequest = int(request.form["no_of_special_request"])
        arrivaldate = int(request.form["arrival_date"])
        age = int(request.form["age"])
        Usagefrequency = int(request.form["Usage_frequency"])
        Supportcalls = int(request.form["Support_calls"])
        marketsegmenttype = int(request.form["market_segment_type"])
        type_plan = int(request.form["type_plan"])
        arrivalyear = int(request.form["arrival_year"])


        features = np.array([[arrivalmonth,Totalspend,noofspecialrequest,arrivaldate,age,Usagefrequency,Supportcalls,marketsegmenttype,type_plan,arrivalyear]])

        prediction = loaded_model.predict(features)


        return render_template('index.html', prediction=prediction[0])
    
    return render_template("index.html" , prediction=None)

if __name__=="__main__":
    app.run(host='0.0.0.0' , port=8080)
