from models import db, User
from forms import RegistrationForm, LoginForm, ProfileForm, AchievementForm, TakeOffForm
from config import Config
from flask import Flask, render_template, redirect, url_for, request, flash
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required, current_user

app = Flask(__name__)
app.config.from_object(Config)

db.init_app(app)

login_manager = LoginManager(app)
login_manager.login_view = 'login'

@login_manager.user_loader
def load_user(user_id):
    try:
        user = User.query.get(int(user_id))
        return user
    except Exception as e:
        print(f"Error loading user: {e}")
        return None

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        existing_user = User.query.filter_by(email=form.email.data).first()
        if existing_user:
            flash('Email уже зарегистрирован.', 'danger')
            return redirect(url_for('register'))

        user = User(
            email=form.email.data,
        )
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Регистрация прошла успешно!', 'success')
        return redirect(url_for('login'))
    return render_template('register.html', form=form)

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and user.check_password(form.password.data):
            login_user(user)
            flash('Вход выполнен.', 'success')
            return redirect(url_for('dashboard'))
        else:
            flash('Неверный email или пароль.', 'danger')
    return render_template('login.html', form=form)

@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Вы вышли из профиля.', 'info')
    return redirect(url_for('home'))

@app.route('/dashboard', methods=['GET', 'POST'])
@login_required
def dashboard():
    profile_form = ProfileForm(obj=current_user)
    achievement_form = AchievementForm()
    if profile_form.submit_profile.data and profile_form.validate():
        current_user.first_name = profile_form.first_name.data
        current_user.last_name = profile_form.last_name.data
        current_user.patronymic = profile_form.patronymic.data
        current_user.age = profile_form.age.data
        db.session.commit()
        flash('Профиль обновлён.', 'success')
    if achievement_form.submit_achievement.data and achievement_form.validate():
        current_user.achievements = achievement_form.achievements.data
        db.session.commit()
        flash('Достижения обновлены.', 'success')
    return render_template('dashboard.html', profile_form=profile_form, achievement_form=achievement_form)

@app.route('/support-measures')
def support_measures():
    federal_url = 'https://www.gosuslugi.ru/itindustry'
    regional_url = 'https://depit.admhmao.ru/mery-podderzhki-proektov/'
    return render_template('support_measures.html', federal_url=federal_url, regional_url=regional_url)

@app.route('/events')
def events():
    events = [
        {'name': 'Tech Conference 2024', 'date': '2024-05-20', 'location': 'Москва'},
        {'name': 'Startup Expo', 'date': '2024-06-15', 'location': 'Санкт-Петербург'},
    ]
    return render_template('events.html', events=events)

@app.route('/takeoff', methods=['GET', 'POST'])
@login_required
def takeoff():
    form = TakeOffForm()
    goals = None
    if form.validate_on_submit():
        preferences = form.preferences.data
        goals = [f'Пройти обучение в области {preferences}', 'Сотрудничать с профессионалами', 'Запустить проект']
    return render_template('takeoff.html', form=form, goals=goals)

with app.app_context():
    db.create_all()

if __name__ == '__main__':
    app.run(debug=True)
