# Importing essential libraries
from flask import Flask, render_template, request
import pickle
import numpy as np

filename = 'resolvr_lgbm_model.pkl'
regressor = pickle.load(open(filename, 'rb'))

app = Flask(__name__)

@app.route('/')
def home():
	return render_template('index.html')

def get_number(res):
    try:
        if res == 'vds':
            return 1
        elif res == 'ds':
            return 2
        elif res == 'neutral':
            return 3
        elif res == 's':
            return 4
        elif res == 'vs':
            return 5
        else:
            return 0
    except:
        return "Something Went Wrong in selection of variables"

@app.route('/predict', methods=['POST'])
def predict():

    if request.method == 'POST':

        g = request.form['gender']
        gender = 1 if g == 'Male' else 0

        age = int(request.form['Age'])
        c_type = request.form['cust_type']
        cust_type = 0 if c_type == 'Loyal Customer' else 0

        travel = request.form['type_of_travel']
        type_of_travel = 0 if travel == 'Business travel' else 1

        c = request.form['Class']
        if c == 'Business':
            Class = 0
        elif c == 'Eco':
            Class = 1
        else:
            Class = 2

        f_dist = abs(float(request.form['f_dist']))
        d_delay = abs(float(request.form['Dep_Delay']))
        a_delay = abs(float(request.form['Arr_Delay']))

        wifi = get_number(request.form['wifi'])
        time_convenient = get_number(request.form['time_convenient'])
        online_booking = get_number(request.form['online_booking'])
        gate_loc = get_number(request.form['gate_loc'])
        f_d = get_number(request.form['f_d'])
        onl_boarding = get_number(request.form['onl_boarding'])
        seat = get_number(request.form['seat'])
        ent = get_number(request.form['ent'])
        on_board = get_number(request.form['on_board'])
        leg_room = get_number(request.form['leg_room'])
        baggage = get_number(request.form['baggage'])
        checking = get_number(request.form['checking'])
        inflight = get_number(request.form['inflight'])
        cleanliness = get_number(request.form['cleanliness'])
        
        indep_var = [gender, cust_type, age, type_of_travel, Class, f_dist, wifi,
                        time_convenient, online_booking, gate_loc, f_d, onl_boarding, seat, ent, on_board,
                        leg_room, baggage, checking, inflight, cleanliness, d_delay, a_delay, ]
        
        data = np.array([indep_var])
        prediction = int(regressor.predict(data)[0])

        my_prediction = "Satisfied" if prediction == 1 else "Dissatisfied"
              
        return render_template('result.html', satisfaction_class = my_prediction)

if __name__ == '__main__':
	app.run(debug=True)
