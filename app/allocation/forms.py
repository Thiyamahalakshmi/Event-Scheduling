from flask_wtf import FlaskForm
from wtforms import SelectField, IntegerField, SubmitField
from wtforms.validators import DataRequired, NumberRange

class AllocationForm(FlaskForm):
    event_id = SelectField('Event', coerce=int, validators=[DataRequired()])
    resource_id = SelectField('Resource', coerce=int, validators=[DataRequired()])
    quantity = IntegerField('Quantity', default=1, validators=[NumberRange(min=1)])
    submit = SubmitField('Allocate')
