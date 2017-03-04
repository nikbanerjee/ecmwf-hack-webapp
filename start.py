from flask import *
from Forms import SettingsForm
import utils as utils
import os

app = Flask(__name__)
app.secret_key = "asdxccxvfddfgdfg"
utils.write_file("hello.txt", "hello")

@app.route("/")
def hello():
    utils.write_file("hello.txt", "hello")
    return render_template('index.html')
    #return app.send_static_file('index.html')

@app.route("/settings", methods=["GET", "POST"])
def settings():
    form = SettingsForm(request.form)
    print("inside settings call")
    if request.method == "POST":#form.validate():#form.validate_on_submit(): # == 'POST': #and form.validate():
        print("inside post request")
        surfaceTempField = form.surfaceTempField.data
        seaWaterTempField = form.seaWaterTempField.data
        precipitationField = form.precipitationField.data
        cloudCoverageField = form.cloudCoverageField.data
        sunDurationField = form.sunDurationField.data
        snowThicknessField = form.snowThicknessField.data

        settingsString = "" +str(surfaceTempField) + "\n"
        settingsString += "" + str(seaWaterTempField) + "\n"
        settingsString += "" + str(precipitationField) + "\n"
        settingsString += "" + str(cloudCoverageField) + "\n"
        settingsString += "" + str(sunDurationField) + "\n"
        settingsString += "" + str(snowThicknessField)
        print(settingsString)

        scriptpath = os.path.dirname(__file__)
        filename = os.path.join(scriptpath, 'settings.txt')

        utils.write_file(filename, settingsString)
        flash("Settings saved.")
        return render_template('index.html')

    print("render settings")
    return render_template('settings.html', form=form)
    #return to home here

if __name__ == "__main__":
    app.run(debug=True)
