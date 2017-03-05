from flask import *
from Forms import SettingsForm
import utils as utils 
import json
import os

app = Flask(__name__)
#app.secret_key = "asdxccxvfddfgdfg"

@app.route("/")
def hello():
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
    return jsonify(data)


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
    print("inside settings call")
    if request.method == "POST":#form.validate():#form.validate_on_submit(): # == 'POST': #and form.validate():
        surfaceTempField = form.surfaceTempField.data
        seaWaterTempField = form.seaWaterTempField.data
        precipitationField = form.precipitationField.data
        cloudCoverageField = form.cloudCoverageField.data
        sunDurationField = form.sunDurationField.data
        snowThicknessField = form.snowThicknessField.data

        settingsString = "surfaceTempField: " + str(surfaceTempField) + "\n"
        settingsString += "seaWaterTempField: " + str(seaWaterTempField) + "\n"
        settingsString += "precipitationField: " + str(precipitationField) + "\n"
        settingsString += "cloudCoverageField: " + str(cloudCoverageField) + "\n"
        settingsString += "sunDurationField: " + str(sunDurationField) + "\n"
        settingsString += "snowThicknessField: " + str(snowThicknessField)
        print(settingsString)

        scriptpath = os.path.dirname(__file__)
        filename = os.path.join(scriptpath, 'settings.txt')

        utils.write_file(filename, settingsString)
        flash("Settings saved.")
        return redirect('/')

    print("render settings")
    return render_template('settings.html', form=form)

if __name__ == "__main__":
    with open("static/matches.json", mode='w', encoding='utf-8') as f:
        json.dump([], f)
    app.run(debug=True)
