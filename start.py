from flask import *
from Forms import SettingsForm
import utils as utils 
from shutil import copy
import json
import os

app = Flask(__name__)
app.secret_key = "asdxccxvfddfgdfg"

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
    
    precipitation = request.args.get('rainfall')
    temp = request.args.get('heat')
    snow_depth = request.args.get('snowfall')
    with open('static/destinations.json') as data_file:    
        data = json.load(data_file)
    
    return jsonify(data)
    
    
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
        precipitationField = form.precipitationField.data
        cloudCoverageField = form.cloudCoverageField.data
        sunDurationField = form.sunDurationField.data
        snowThicknessField = form.snowThicknessField.data
        
        settings_hash = {
            "surfaceTempField": str(surfaceTempField),
            "seaWaterTempField": str(seaWaterTempField),
            "precipitationField": str(precipitationField),
            "cloudCoverageField": str(cloudCoverageField),
            "sunDurationField": str(sunDurationField),
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

    

if __name__ == "__main__":
    with open("static/matches.json", mode='w', encoding='utf-8') as f:
        json.dump([], f)
    with open("static/settings.json", mode='w', encoding='utf-8') as f:
        json.dump({}, f)
#    copy("data/destination_base.json", "static/destinations.json")
    app.run(debug=True)
