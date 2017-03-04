from wtforms import Form, BooleanField, StringField, TextAreaField, DateTimeField, IntegerField, widgets, validators
from wtforms.validators import DataRequired, Length

class SettingsForm(Form):
    #surfaceTemp = IntegerField(widget=NumberInput())
    surfaceTempField = IntegerField('Surface Temperature (C)', [validators.DataRequired()])
    seaWaterTempField = IntegerField('Sea Water Temperature (C)', [validators.DataRequired()])
    precipitationField = IntegerField('Precipitation (mm)', [validators.DataRequired()])
    cloudCoverageField = IntegerField('Cloud coverage', [validators.DataRequired()])
    sunDurationField = IntegerField('Sun duration (time)', [validators.DataRequired()])
    snowThicknessField = IntegerField('Snow Thickness (cm)', [validators.DataRequired()])
