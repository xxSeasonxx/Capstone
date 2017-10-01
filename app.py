from flask import Flask, render_template, request
import pandas as pd
#from bokeh.embed import components
#import requests
#from bokeh.plotting import figure, output_file, show

app = Flask(__name__)

feature_names = ['Noise', 'Traffic', 'Consumer', 'Water']
# Index page
@app.route('/')
def index():
    return render_template("index.html" ,feature_names=feature_names)

# With debug=True, Flask server will auto-reload
# when there are code changes
if __name__ == '__main__':
    app.run(port=33507)
