from flask import Flask, render_template, redirect, request, make_response
from flask_login import login_manager
from flask_restful import Api

from data import db_session
from data.users import User, LoginForm
from data.jobs import Jobs
from flask_login import *
from data.jobs_form import JobsForm
from api import blueprint as jobs_blueprint
from users_resource import UserResource, UsersListResource

app = Flask(__name__)
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'
login_manager = LoginManager()
login_manager.init_app(app)
api = Api(app)


@app.route('/')
@app.route('/works_log')
def works_log():
    session = db_session.create_session()
    jobs = session.query(Jobs).all()
    return render_template('index.html', jobs=jobs)


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        user = db_sess.query(User).filter(User.email == form.email.data).first()
        if user and user.check_password(form.password.data):
            login_user(user, remember=form.remember_me.data)
            return redirect("/")
        return render_template('login.html',
                               message="Неправильный логин или пароль",
                               form=form)
    return render_template('login.html', title='Авторизация', form=form)


@login_manager.user_loader
def load_user(user_id):
    db_sess = db_session.create_session()
    return db_sess.query(User).get(user_id)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect('/')


@app.route('/add_job',  methods=['GET', 'POST'])
@login_required
def add_jobs():
    form = JobsForm()
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        job = Jobs()
        job.job = form.job.data
        job.work_size = form.work_size.data
        job.collaborations = form.collaborations.data
        job.start_date = form.start_date.data
        job.end_date = form.end_date.data
        job.is_private = form.is_private.data
        current_user.jobs.append(job)
        db_sess.merge(current_user)
        db_sess.commit()
        return redirect('/')
    return render_template('add_job.html', title='Добавление новости',
                           form=form)


def main():
    db_session.global_init("db/mars_explorer.db")
    app.register_blueprint(jobs_blueprint)
    session = db_session.create_session()
    api.add_resource(UserResource, '/api/v2/users/<int:user_id>')
    api.add_resource(UsersListResource, '/api/v2/users')
    #user = User(name='testuser2222', email='111mail@mail.ru')
    #user.set_password('12345678')
    #session.add(user)
    #session.commit()
    app.run()


if __name__ == '__main__':
    main()
