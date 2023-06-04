from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, IntegerField, TextAreaField
from wtforms.validators import DataRequired, Optional, NumberRange


class RegisterForm(FlaskForm):
    name = StringField('Имя пользователя', validators=[DataRequired()])
    max_members = IntegerField('Максимальное число участников:', validators=[DataRequired(), NumberRange(min=1)])
    description =  TextAreaField('')
    submit = SubmitField('Создатб')