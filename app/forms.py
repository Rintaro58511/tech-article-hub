from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Length, EqualTo, ValidationError
from model import User

class SignUpForm(FlaskForm):

    user_name = StringField('ユーザー名', validators=[DataRequired(), Length(min=3, max=50)])

    password = PasswordField('パスワード', validators=[DataRequired(), Length(min=6)])

    password_confirm = PasswordField('確認用パスワード', validators=[DataRequired(), EqualTo('password', message='パスワードが一致しません')])

    submit_button = SubmitField('新規登録')

    def validate_user_name(self, user_name):
        if User.query.filter_by(user_name=user_name.data).first():
            raise ValidationError('このユーザー名はすでに使われいてます')

class LoginForm(FlaskForm):

    user_name = StringField('ユーザー名', validators=[DataRequired(), Length(min=3, max=50)])

    password = PasswordField('パスワード', validators=[DataRequired(), Length(min=6)])

    submit_button = SubmitField('ログイン')
