from flask import render_template, flash, redirect, request, session, url_for, jsonify
from app import app, db, models
from .forms import *

@app.route('/', methods=['GET'])
@app.route('/index', methods=['GET'])
def index():
    user = None
    if 'username' in session:
        user = models.User.query.filter_by(username = session['username']).first()
    return render_template("index.html", user = user)

@app.route('/parli', methods=['GET'])
def parli():
    user = None
    if 'username' in session:
        user = models.User.query.filter_by(username = session['username']).first()
    return render_template("parli.html", user = user)

@app.route('/tournaments', methods=['GET'])
def tournaments():
    user = None
    if 'username' in session:
        user = models.User.query.filter_by(username = session['username']).first()
    return render_template("tournament.html", user = user)

@app.route('/contact_us', methods=['GET'])
def contact_us():
    user = None
    if 'username' in session:
        user = models.User.query.filter_by(username = session['username']).first()
    return render_template("contact_us.html", user = user)

@app.route('/about_us', methods=['GET'])
def about_us():
    user = None
    if 'username' in session:
        user = models.User.query.filter_by(username = session['username']).first()
    return render_template("about_us.html", user = user)

@app.route('/join_us', methods=['GET'])
def join_us():
    user = None
    if 'username' in session:
        user = models.User.query.filter_by(username = session['username']).first()
    return render_template("join_us.html", user = user)

@app.route('/faqs', methods=['GET'])
def faqs():
    user = None
    if 'username' in session:
        user = models.User.query.filter_by(username = session['username']).first()
    return render_template("faq.html", user = user)

@app.route('/rules_and_guides', methods=['GET'])
def rules_and_guides():
    return redirect('http://apdaweb.org/guide/rules')

@app.route('/create', methods=['GET', 'POST'])
def create():
    create_form = CreateForm()

    if create_form.validate_on_submit():
        new_user = models.User(fname = create_form.fname.data,
                               lname = create_form.lname.data,
                               username = create_form.username.data,
                               email = create_form.email.data,
                               school = create_form.school.data,
                               permissions = '')
        new_user.add_permission('user')
        new_user.add_permission('register')
        new_user.set_password(create_form.password.data)
        db.session.add(new_user)
        db.session.commit()
        flash('Account created')
        return redirect('login')


    return render_template('create.html', create_form = create_form)

@app.route('/login', methods=['GET', 'POST'])
def login():
    login_form = LoginForm()

    if login_form.validate_on_submit():
        session['username'] = login_form.username.data
        flash('Logged in')
        return redirect('index')

    return render_template('login.html', login_form = login_form)

@app.route('/view_registration', methods=['GET'])
def view_registration():
    user = models.User.query.filter_by(username = session['username']).first()

    if not user:
        flash('There was an authentication error')
        return redirect('login')

    return render_template('view_registration.html', user = user, teams = user.registrations.first().teams, judges = user.registrations.first().judges, num_teams = user.registrations.first().num_teams)

@app.route('/admin_view_registration/<string:username>', methods=['GET'])
def admin_view_registration(username = ''):
    user = models.User.query.filter_by(username = session['username']).first()

    if not user:
        flash('There was an authentication error')
        return redirect('login')

    if not user.check_permission('admin'):
        flash('You do not have permission to view this page')
        return redirect('login')
        
    user_to_get = models.User.query.filter_by(username = username).first()
    
    if not user_to_get.registrations.first():
        flash('This user has yet to register')
        return redirect('users')

    return render_template('admin_view_registration.html', user = user, teams = user_to_get.registrations.first().teams, judges = user_to_get.registrations.first().judges, num_teams = user_to_get.registrations.first().num_teams, user_to_get = user_to_get)


@app.route('/users', methods = ['GET'])
@app.route('/users/<int:page>', methods=['GET'])
def users(page = 1):
    user = models.User.query.filter_by(username = session['username']).first()

    if not user:
        flash('There was an authentication error')
        return redirect('login')

    if not user.check_permission('admin'):
        flash('You do not have permission to view this page')
        return redirect('login')

    users = models.User.query.paginate(page, app.config['ELEMENTS_PER_PAGE'], False)

    return render_template('users.html', user = user, users = users)

@app.route('/toggle_admin/<string:username>', methods=['GET'])
def toggle_admin(username = ''):
    user = models.User.query.filter_by(username = session['username']).first()

    if not user:
        flash('There was an authentication error')
        return redirect('login')

    if not user.check_permission('admin'):
        flash('You do not have permission to view this page')
        return redirect('login')

    user = models.User.query.filter_by(username = username).first()
    if user.check_permission('admin'):
        user.remove_permission('admin')
    else:
        user.add_permission('admin')
    db.session.commit()
    return redirect('users')


@app.route('/register', methods=['GET', 'POST'])
def register():
    user = models.User.query.filter_by(username = session['username']).first()

    if not user:
        flash('There was an authentication error')
        return redirect('login')

    if request.method == 'POST':
        num_teams = int(request.form['num_teams'])
        teams = ''
        judges = ''
        for i in range(1, num_teams + 1):
            teams += request.form[str(i) + '_1'] + ',' + request.form[str(i) + '_2'] + ';'

        for i in range(1, ((num_teams + 1) / 2) + 1):
            judges += request.form['j_' + str(i)] + ','

        registration = models.Registration(num_teams = num_teams,
                                           teams = teams,
                                           judges = judges,
                                           tournament = 'Horace Mann Invitational')
        user.registrations.append(registration)
        user.remove_permission('register')
        user.add_permission('view_registration')
        db.session.add(registration)
        db.session.commit()
        
        flash('You are registered')
        return redirect('index')

    return render_template('register.html', user = user)

@app.route('/logout', methods=['GET'])
def logout():
    session.pop('username', None)
    flash('You have been logged out')
    return redirect('index')
