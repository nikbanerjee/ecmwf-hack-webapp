from flask import *
from Forms import SettingsForm
import utils as utils

app = Flask(__name__)

@app.route("/")
def hello():
    return app.send_static_file('index.html')

@app.route("/settings", methods=["GET", "POST"])
def settings():
    form = SettingsForm(request.form)
    if request.method == 'POST' and form.validate():
        surfaceTempField = form.surfaceTempField
        seaWaterTempField = form.seaWaterTempField
        precipitationField = form.precipitationField
        cloudCoverageField = form.cloudCoverageField
        sunDurationField = form.sunDurationField
        snowThickness = form.snowThickness

        settingsString = "" +surfaceTempField + "\n"
        settingsString += "" + seaWaterTempField + "\n"
        settingsString += "" + precipitationField + "\n"
        settingsString += "" + cloudCoverageField + "\n"
        settingsString += "" + sunDurationField + "\n"
        settingsString += "" + snowThickness

        utils.write_file("settings.txt", settingsString)
        flash("Settings saved.")

    render_template('index.html')
    #return to home here

if __name__ == "__main__":
    app.run()
