from flask_wtf import FlaskForm
from wtforms import SubmitField, StringField, IntegerField, DateField, BooleanField
from wtforms.validators import DataRequired


class JobsForm(FlaskForm):
    job = StringField('Описание работы')
    work_size = IntegerField('Объем работы, ч')
    collaborations = StringField('Соучастники')
    start_date = DateField('начало работы, ч')
    end_date = DateField('конец работы, ч')
    is_finished = BooleanField('завершена')
    submit = SubmitField('применить')
