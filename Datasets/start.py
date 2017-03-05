from flask import *
from Forms import SettingsForm
import utils as utils 
from shutil import copy
import json
import os

app = Flask(__name__)
app.secret_key = "asdxccxvfddfgdfg"

selection_criteria = {
    "surface_temp": {
        "Cold": [-60, 5],
        "Average": [5, 15],
        "Warm": [15, 25],
        "Hot": [25, 60]
    },
    "cloud_coverage": {
        "ClearSkies": [0, 0.20],
        "Cloudy": [0.20, 0.40],
        "VeryCloudy": [0.40, 0.60],
        "Overcast": [0.60, 1.00]
    },
    "sea_temp": {
        "Cold": [-60, 2],
        "Average": [2, 10],
        "Warm": [10, 25],
        "Hot": [25, 60]
    },
    "snow_thickness": {
        "NoSnow": [0, 0],
        "LightSnow": [0, 0.2],
        "HeavySnow": [0.2, 0.8],
        "Snowstorm": [0.8, 1],
    }
}


@app.route("/")
def start():
    with open('static/settings.json') as data_file:    
        data = json.load(data_file)
    if (data == {}):
        return redirect("/settings")
    return render_template('index.html')
    
    #return app.send_static_file('index.html')
    
@app.route("/matches", methods=["GET", "POST"])
def match():
    if request.method == "POST":
        with open("static/matches.json") as data_file:
            matches_array = json.load(data_file)
        matches_array.append(request.get_json())
        with open("static/matches.json", 'w') as outfile:
            json.dump(matches_array, outfile, indent=4, sort_keys=True)
        return redirect("/")
    
    with open('static/matches.json') as data_file:    
        data = json.load(data_file)
    data_format = request.args.get('format')
    if data_format == "json":
        return jsonify(data)
    else:
        return render_template('matches.html', json_data=data)
    

@app.route("/destinations", methods=["GET", "POST"])
def destination():
    if request.method == "POST":
        with open("static/destinations.json") as data_file:
            dest_json = json.load(data_file)
        dest_json.append(request.get_json())
        with open("static/destinations.json", 'w') as outfile:
            json.dump(dest_json, outfile, indent=4, sort_keys=True)
        return redirect("/")
    
    with open('static/destinations.json') as data_file:    
        data = json.load(data_file)
    
    res = list()
    params_active = False
    params = ['surface_temp', 'sea_temp', 'cloud_coverage', 'snow_thickness']
    for param in params:
        arg = request.args.get(param)
        if arg is not None:
            params_active = True
            res += get_destinations_matching_criteria(data, param, arg)
    
    # Remove duplicates    
    final_res = list()
    for dest in res:
        if dest["location"] not in final_res:
            final_res.append(dest)
            
    if not params_active:
        return jsonify(data)
    else:
        return jsonify(final_res)
    
    
@app.route("/destinations/<int:id>", methods=["POST"])
def patch_destination(id):
    with open("static/destinations.json") as data_file:
        dest_json = json.load(data_file)
    for json_key in dest_json[id].keys():
        if json_key in request.get_json().keys():
            dest_json[id][json_key] = request.get_json()[json_key]
    with open("static/destinations.json", 'w') as outfile:
        json.dump(dest_json, outfile, indent=4, sort_keys=True)
    return redirect("/")
    

@app.route("/settings", methods=["GET", "POST"])
def settings():
    form = SettingsForm(request.form)
    if request.method == "POST":#form.validate():#form.validate_on_submit(): # == 'POST': #and form.validate():
        surfaceTempField = form.surfaceTempField.data
        seaWaterTempField = form.seaWaterTempField.data
        cloudCoverageField = form.cloudCoverageField.data
        snowThicknessField = form.snowThicknessField.data
        
        settings_hash = {
            "surfaceTempField": str(surfaceTempField),
            "seaWaterTempField": str(seaWaterTempField),
            "cloudCoverageField": str(cloudCoverageField),
            "snowThicknessField": str(snowThicknessField)
        }
        
        with open("static/settings.json", 'w') as outfile:
            json.dump(settings_hash, outfile, indent=4, sort_keys=True)
            
        flash("Settings saved.")
        return redirect('/')
    
    data_format = request.args.get('format')
    if data_format == "json":
        with open('static/settings.json') as data_file:    
            data = json.load(data_file)
        return jsonify(data)
    else:
        return render_template('settings.html', form=form)

    
def get_destinations_matching_criteria(data, category, criteria):
    res = []
    for d in data:
        if (float(d["metrics"][category]) > float(selection_criteria[category][criteria][0]) and (float(d["metrics"][category]) < float(selection_criteria[category][criteria][1]))):
            res.append(d)
    return res
    

if __name__ == "__main__":
    with open("static/matches.json", mode='w', encoding='utf-8') as f:
        json.dump([], f)
    with open("static/settings.json", mode='w', encoding='utf-8') as f:
        json.dump({}, f)
#    copy("data/destination_base.json", "static/destinations.json")
    app.run(debug=True)
