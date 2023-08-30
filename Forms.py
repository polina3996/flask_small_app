from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, BooleanField, PasswordField
from wtforms.validators import DataRequired, Email, Length, EqualTo


# a class of some kind to represent and validate our
# client-side form data. For example, WTForms is a library that will
# handle this for us, and we use a custom LoginForm to validate.

class LoginForm(FlaskForm):
    username = StringField('Имя: ', validators=[Length(min=4, max=100,
                                                       message='Имя должно быть от 4 до 100 символов')])
    psw = PasswordField('Пароль: ', validators=[DataRequired(), Length(min=4, max=100, message='Пароль должен быть от '
                                                                                               '4 до 100 символов')])
    remember = BooleanField('Запомнить', default=False)
    submit = SubmitField('Войти')


class RegisterForm(FlaskForm):
    username = StringField('Имя: ', validators=[Length(min=4, max=100,
                                                       message='Имя должно быть от 4 до 100 символов')])
    email = StringField('Email: ', validators=[
        Email('Некорректный email')])
    psw = PasswordField('Пароль: ', validators=[DataRequired(), Length(min=4, max=100, message='Пароль должен быть от '
                                                                                               '4 до 100 символов')])
    psw2 = PasswordField('Повтор пароля: ', validators=[DataRequired(), EqualTo('psw', message='Пароли не совпадают')])
    submit = SubmitField('Зарегистрироваться')
