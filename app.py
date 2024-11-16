from flask import Flask, render_template, redirect, url_for, request, flash
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, IntegerField, TextAreaField, SubmitField, SelectField
from wtforms.validators import DataRequired, Email, EqualTo, NumberRange
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required, current_user

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
db = SQLAlchemy(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'

# Модель пользователя
class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), unique=True, nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(100), nullable=False)
    age = db.Column(db.Integer, nullable=False)
    achievements = db.Column(db.Text, nullable=True)
    experience = db.Column(db.Text, nullable=True)

# Форма регистрации
class RegistrationForm(FlaskForm):
    username = StringField('Имя пользователя', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Пароль', validators=[DataRequired()])
    confirm_password = PasswordField('Повторите пароль', validators=[DataRequired(), EqualTo('password')])
    age = IntegerField('Возраст', validators=[DataRequired(), NumberRange(min=14, max=100)])
    submit = SubmitField('Зарегистрироваться')

# Форма логина
class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Пароль', validators=[DataRequired()])
    submit = SubmitField('Войти')

# Форма для профиля
class ProfileForm(FlaskForm):
    achievements = TextAreaField('Достижения', validators=[DataRequired()])
    experience = TextAreaField('Опыт', validators=[DataRequired()])
    submit = SubmitField('Сохранить изменения')

# Главная страница
@app.route('/')
def index():
    return render_template('index.html')

# Регистрация
@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        # Check if the email already exists
        existing_user = User.query.filter_by(email=form.email.data).first()
        if existing_user:
            flash('Email уже зарегистрирован. Пожалуйста, используйте другой email.', 'danger')
            return redirect(url_for('register'))

        # If no existing user with the same email, proceed to register the new user
        user = User(username=form.username.data, email=form.email.data, password=form.password.data, age=form.age.data)
        db.session.add(user)
        db.session.commit()
        flash('Регистрация прошла успешно! Теперь вы можете войти.', 'success')
        return redirect(url_for('login'))
    return render_template('register.html', form=form)


# Логин
@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and user.password == form.password.data:
            login_user(user)
            return redirect(url_for('profile'))
        else:
            flash('Неверный email или пароль', 'danger')
    return render_template('login.html', form=form)

# Личный кабинет
@app.route('/profile', methods=['GET', 'POST'])
@login_required
def profile():
    form = ProfileForm()
    if form.validate_on_submit():
        current_user.achievements = form.achievements.data
        current_user.experience = form.experience.data
        db.session.commit()
        flash('Профиль обновлен!', 'success')
    return render_template('profile.html', form=form, user=current_user)

# Раздел с федеральными и региональными мерами поддержки
@app.route('/support')
def support():
    federal_url = "https://www.gosuslugi.ru/itindustry"
    regional_url = "https://depit.admhmao.ru/mery-podderzhki-proektov/"
    return render_template('support.html', federal_url=federal_url, regional_url=regional_url)

# Раздел мероприятий
@app.route('/events')
def events():
    events_list = [
        {'title': 'IT-Форум', 'date': '2024-12-01', 'location': 'Москва'},
        {'title': 'Хакатон', 'date': '2024-12-15', 'location': 'Санкт-Петербург'},
    ]
    return render_template('events.html', events=events_list)

# Раздел "На взлёт!"
@app.route('/takeoff', methods=['GET', 'POST'])
@login_required
def takeoff():
    questions = [
        {'question': 'Какие направления вам интересны?', 'options': ['Разработка ПО', 'Аналитика', 'Менеджмент']},
        {'question': 'Сколько лет вы работаете в отрасли?', 'options': ['0-2 года', '3-5 лет', '5+ лет']},
    ]
    if request.method == 'POST':
        answers = request.form.to_dict()
        # Логика построения индивидуальной траектории (упрощена)
        checklist = ['Пройти курсы повышения квалификации', 'Участвовать в хакатонах', 'Изучить новые технологии']
        return render_template('takeoff_results.html', checklist=checklist)
    return render_template('takeoff.html', questions=questions)

# Выход из системы
@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Вы вышли из системы', 'info')
    return redirect(url_for('index'))

# Загрузка пользователя
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# Инициализация базы данных
with app.app_context():
    db.create_all()

if __name__ == '__main__':
    app.run(debug=True)
