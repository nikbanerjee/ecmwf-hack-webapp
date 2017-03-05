from wtforms import Form, BooleanField, StringField, TextAreaField, DateTimeField, IntegerField, widgets, validators
from wtforms.validators import DataRequired, Length

class SettingsForm(Form):
    #surfaceTemp = IntegerField(widget=NumberInput())
    surfaceTempField = StringField('Surface Temperature')
    seaWaterTempField = StringField('Sea Water Temperature')
    cloudCoverageField = StringField('Cloud coverage')
    snowThicknessField = StringField('Snow Thickness (cm)')
