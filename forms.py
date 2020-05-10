from flask_wtf import FlaskForm
from wtforms import SubmitField, SelectField
from wtforms.validators import DataRequired


class InputForm(FlaskForm):
    city = SelectField('Select the City', validators=[DataRequired()],
                       choices=['Chicago', 'Washington', 'New York City'])
    month = SelectField('Select one or more months',
                        choices=['All', 'January', 'February', 'March', 'April', 'May', 'June'],
                        default='All')
    day_of_week = SelectField('Select one or more days',
                              choices=['All', 'Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun'],
                              default='All')
    submit = SubmitField('Find BikeShare Data')
