from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, IntegerField, TextAreaField
from wtforms.validators import DataRequired, Optional, NumberRange


class CreateProjectForm(FlaskForm):
    name = StringField('Имя проекта', validators=[DataRequired()])
    max_members = IntegerField('Максимальное число участников:', validators=[DataRequired(), NumberRange(min=1)])
    description =  TextAreaField('Введите описание:', validators=[Optional()])
    submit = SubmitField('Создать')