from wtforms import Form, BooleanField, StringField, TextAreaField, DateTimeField, IntegerField, widgets, validators
from wtforms.validators import DataRequired, Length

class SettingsForm(Form):
    #surfaceTemp = IntegerField(widget=NumberInput())
    surfaceTempField = IntegerField('Surface Temperature (C)', [validators.data_required])
    seaWaterTempField = IntegerField('Sea Water Temperature (C)', [validators.data_required])
    precipitationField = IntegerField('Precipitation (mm)', [validators.data_required])
    cloudCoverageField = IntegerField('Cloud coverage', [validators.data_required])
    sunDurationField = IntegerField('Sun duration (time)', [validators.data_required])
    snowThickness = IntegerField('Snow Thickness (cm)', [validators.data_required])
