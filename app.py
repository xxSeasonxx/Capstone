from flask import Flask, render_template, request,redirect
import pandas as pd
import numpy as np
import pandas as pd
import matplotlib.cm as cm
from itertools import cycle
from sklearn.utils import shuffle
from sklearn.linear_model import LogisticRegression
from collections import OrderedDict

#from bokeh.embed import components
#import requests
#from bokeh.plotting import figure, output_file, show

app = Flask(__name__)
app.vars = {}
complaint_types = ['APPLIANCE', 'Adopt-A-Basket', 'Air Quality', 'Animal Abuse', 'BEST/Site Safety', 'Bike Rack Condition', 'Bike/Roller/Skate Chronic', 'Blocked Driveway', 'Boilers', 'Bridge Condition', 'Broken Muni Meter', 'Broken Parking Meter', 'Building Condition', 'Building/Use', 'Bus Stop Shelter Placement', 'Collection Truck Noise', 'Cranes and Derricks', 'Curb Condition', 'DOOR/WINDOW', 'Damaged Tree', 'Dead Tree', 'Derelict Bicycle', 'Derelict Vehicle', 'Derelict Vehicles', 'Dirty Conditions', 'Disorderly Youth', 'Drinking', 'ELECTRIC', 'ELEVATOR', 'Electrical', 'Elevator', 'Emergency Response Team (ERT)', 'FLOORING/STAIRS', 'Foam Ban Enforcement', 'For Hire Vehicle Complaint', 'For Hire Vehicle Report', 'GENERAL', 'General Construction/Plumbing', 'Graffiti', 'HEAT/HOT WATER', 'Hazardous Materials', 'Highway Condition', 'Homeless Encampment', 'Illegal Fireworks', 'Illegal Parking', 'Illegal Tree Damage', 'Industrial Waste', 'Interior Demo', 'Investigations and Discipline (IAD)', 'Lead', 'Litter Basket / Request', 'Miscellaneous Categories', 'Missed Collection (All Materials)', 'Municipal Parking Facility', 'New Tree Request', 'Noise', 'Noise - Commercial', 'Noise - House of Worship', 'Noise - Park', 'Noise - Residential', 'Noise - Street/Sidewalk', 'Noise - Vehicle', 'Non-Emergency Police Matter', 'OUTSIDE BUILDING', 'Other Enforcement', 'Overflowing Litter Baskets', 'Overflowing Recycling Baskets', 'Overgrown Tree/Branches', 'PAINT/PLASTER', 'PLUMBING', 'Panhandling', 'Plumbing', 'Posting Advertisement', 'Recycling Enforcement', 'Rodent', 'Root/Sewer/Sidewalk Condition', 'SAFETY', 'Sanitation Condition', 'Scaffold Safety', 'Sewer', 'Sidewalk Condition', 'Snow', 'Special Enforcement', 'Special Projects Inspection Team (SPIT)', 'Squeegee', 'Stalled Sites', 'Street Condition', 'Street Light Condition', 'Street Sign - Damaged', 'Street Sign - Dangling', 'Street Sign - Missing', 'Sweeping/Inadequate', 'Sweeping/Missed', 'Taxi Complaint', 'Taxi Report', 'Traffic', 'Traffic Signal Condition', 'UNSANITARY CONDITION', 'Unsanitary Animal Pvt Property', 'Unsanitary Pigeon Condition', 'Urinating in Public', 'VACANT APARTMENT', 'Vacant Lot', 'Vending', 'WATER LEAK', 'Water Conservation', 'Water Quality', 'Water System']
Man_zipcodes = ['00083', '10000', '10001', '10002', '10003', '10004', '10005', '10006', '10007', '10009', '10010', '10011', '10012', '10013', '10014', '10016', '10017', '10018', '10019', '10020', '10021', '10022', '10023', '10024', '10025', '10026', '10027', '10028', '10029', '10030', '10031', '10032', '10033', '10034', '10035', '10036', '10037', '10038', '10039', '10040', '10041', '10044', '10048', '10065', '10069', '10075', '10103', '10107', '10111', '10112', '10119', '10122', '10123', '10128', '10129', '10153', '10162', '10278', '10280', '10281', '10282', '10463']

complain_times = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23]
complain_agencys = ['DEP', 'DOB', 'DOHMH', 'DOT', 'DPR', 'DSNY', 'HPD', 'NYPD', 'TLC']

# Initialize my input dic
com = OrderedDict()
zip  = OrderedDict()
ang = OrderedDict()

for each in complaint_types:
    com[each] = 0
for each in Man_zipcodes:
    zip[each] = 0
for each in complain_agencys:
    ang[each] = 0

## Read in Table
#df_model = pd.read_csv('model.csv')
#
## Get Dummies
#df_resol = pd.get_dummies(df_model['Resolution'])
#df_agency = pd.get_dummies(df_model['Agency'])
#df_complaint = pd.get_dummies(df_model['Complaint_Type'])
#df_zipcode = pd.get_dummies(df_model['Incident_Zip'])

## Concate
#df_x = pd.concat([df_model[['hours']],
#                  df_agency,df_complaint,df_zipcode],axis=1)
#
## Set X, y
#X = df_x
#y = df_resol

#for i, col in enumerate(y.columns.tolist(), 1):
#    y.loc[:, col] *= i
#y = y.sum(axis=1)

#random_state = np.random.RandomState(0)
## Construct training and testing set.
#X, y = shuffle(X, y, random_state=random_state)
#n_samples, n_features = X.shape
#half = int(n_samples/1.2)
#X_train, X_test = X[:half], X[half:]
#y_train, y_test = y[:half], y[half:]

#clf = LogisticRegression(multi_class = 'multinomial', solver='lbfgs')
#clf.fit(X_train, y_train)

# Index page
@app.route('/',methods=['GET','POST'])
def index():
    if request.method == 'GET':
        return render_template("index.html" ,complaint_types=complaint_types,Man_zipcodes= Man_zipcodes, complain_times = complain_times, complain_agencys = complain_agencys)
    else:
        app.vars['complaint_type'] = request.form["complaint_type"]
        app.vars['zipcode'] = request.form["zipcode"]
        app.vars['time'] = request.form["time"]
        app.vars['agency'] = request.form["agency"]

        com[app.vars['complaint_type'] ] = 1
        zip[app.vars['zipcode'] ] = 1
        ang[app.vars['agency']] = 1
        return redirect('/result')
#        return render_template("model.html")

@app.route('/result')
def result():
    input = [int(app.vars['time'])]
    input += ang.values()
    input += com.values()
    input += zip.values()
#    out = clf.predict_proba(input)*100
#    resolve_rate = out[0][-1]
#    fail_rate = out[0][1]
#    violation_rate = out[0][3]
#    noviolation_rate = out[0][2]
#    duplicate_rate = out[0][0]
#    tbd_rate = out[0][-2]
    return render_template("model.html", complaint = app.vars['complaint_type'],
                               zipcode = app.vars['zipcode'], time =app.vars['time'] , agency = app.vars['agency'],resolve_rate=resolve_rate,fail_rate = fail_rate, violation_rate=violation_rate, noviolation_rate=noviolation_rate,duplicate_rate=duplicate_rate,tbd_rate = tbd_rate )


# With debug=True, Flask server will auto-reload
# when there are code changes
if __name__ == '__main__':
    app.run(port=33507)
