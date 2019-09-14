from flask_wtf import FlaskForm
from wtforms import IntegerField, SubmitField
from wtforms.validators import DataRequired


class QuizForm(FlaskForm):
    no_of_questions = IntegerField(
        'Number of Questions', validators=[DataRequired()])
    submit = SubmitField('Submit')
