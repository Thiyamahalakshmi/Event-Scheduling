from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, SubmitField, SelectField
from wtforms.validators import DataRequired, NumberRange

class ResourceForm(FlaskForm):
    resource_name = StringField('Name', validators=[DataRequired()])
    resource_type = SelectField('Type', choices=[('room','room'),('instructor','instructor'),('equipment','equipment')])
    capacity = IntegerField('Capacity', default=1, validators=[NumberRange(min=1)])
    submit = SubmitField('Save')
