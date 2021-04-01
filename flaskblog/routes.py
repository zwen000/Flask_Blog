from flask import render_template, url_for, flash, redirect, request
from flaskblog import app, db, bcrypt
from flaskblog.forms import RegistrationForm, LoginForm, UpdateAccountForm
from flaskblog.models import User, Post
from flask_login import login_user, current_user, logout_user, login_required
import secrets
import os
from PIL import Image

posts = [
    {
        'author':  'Corey Schafer',
        'title': 'Blog Post 1',
        'content': 'First Post Content',
        'date_posted': 'April 20, 2018'
    },
    {
        'author':  'Jane doe',
        'title': 'Blog Post 2',
        'content': 'Second Post Content',
        'date_posted': 'April 21, 2018'
    },

]

@app.route('/')
@app.route('/home')
def home():
    return render_template("home.html", posts=posts)

@app.route('/about/')
def about():
    team = [
        {
            'name': 'Chrystal Mingo',
            'image': url_for('static', filename="profile_pics/CM.png"),
            'description': "is a senior majoring in Computer Science at The City College of New York. She has interned at various companies such as Verizon, Morgan Stanley, and Citi as a software developer. She also has a passion for teaching and has worked as a Teacher for the Girls Who Code Summer Immersion Program, and taught Algebra I and II, as well as Intro and AP Computer Science courses in Spanish and English at Gregorio Luperon High School. Chrystal Mingo is also a Grace Hopper 2019 Scholarship Recipient, and current President of Women in Computer. She will be graduating from CCNY in Spring 2021 and entering Citi’s EIOT full-time rotational program as a project manager. She is one of the frontend developers for AdviseMe and believes this project will be a game-changer for advisement at CCNY.",
            'git': 'https://github.com/chrystalmingo',
            'linkedin': '',
            'email':''
        },
        {
            'name': 'Zhicong Wen',
            'image': url_for('static', filename="profile_pics/ZW.jpg"),
            'description': "is a senior majoring in Computer Science at City College of New York. Previously he was interning as a Python programmer at the NYC Department of Environmental Protection(DEP). He also worked on Quality Assurance of the New York City sewer system database. He will be graduating from CCNY in Fall 2021. He is one of the frontend developers for AdviseMe.",
            'git': 'https://github.com/zwen000',
            'linkedin': 'https://www.linkedin.com/in/zhicongw-b243a7169/',
            'email': ''
        },
        {
            'name': 'Xunshan Lin',
            'image': url_for('static', filename="profile_pics/XL.jpg"),
            'description': "is a senior majoring in computer engineering at The City College of New York. Previously he was interning as a Python programmer at Mini circuits company. He is beginning to pick up an interest in full-stack development at his senior design project at CCNY. He works as one of the backend developers for AdviseMe and hopes this platform will help students make better academic plans at CCNY.",
            'git': 'https://github.com/linxunshan',
            'linkedin': '',
            'email': ''
        },
        {
            'name': 'Rehman Arshad',
            'image': url_for('static', filename="profile_pics/RA.png"),
            'description': "is a senior majoring in Computer Science at The City College of New York. He has interned at various academic research institutions at The Groove school of Engineering, such as NOAA Crest (National Oceanic Atmospheric Administration) and Professor Tarek Sadawi. At NOAA Crest, he worked on data collection and analysis using data from the National Weather Service. With Professor Tarek Sadawi he worked on an IoT medical application that would enable remote patient monitoring as a research assistant. He was a part of CUNY Tech Prep cohort 5, a Full Stack program part of NYC Tech Talent Pipeline. Also, he has a fascination with mathematics and a passion for computer graphics and video game development. He will be graduating from The City College of New York in Fall 2021. He is one of the backend developers for AdviseMe and hopes this online platform can help the next generation of students entering CCNY.",
            'git': 'https://github.com/rehman000',
            'linkedin': '',
            'email': ''
        },
    ]

    return render_template("about.html", title="About", team=team)

@app.route('/register/', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('home'))

    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username=form.username.data, email=form.email.data, password=hashed_password)
        db.session.add(user)
        db.session.commit()

        flash(f'Your account has been created for {form.username.data}! You are now able to log in', 'success')
        return redirect(url_for('login'))

    return render_template("register.html", title="Register", form=form)

@app.route('/login/', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))

    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            flash('Login Successful!', 'success')
            next_page = request.args.get('next')

            return redirect(next_page) if next_page else redirect(url_for('home'))
        else:
            flash('Login Unsuccessful. Please check email and password!', 'danger')
    return render_template("login.html", title="Login", form=form)

@app.route('/logout/', methods=['GET', 'POST'])
def logout():
    logout_user()
    flash('Your account is logged out', 'success')
    return redirect(url_for('home'))


def save_picture(form_picture):
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(form_picture.filename)
    picture_fn = random_hex + f_ext
    picture_path = os.path.join(app.root_path, 'static/profile_pics', picture_fn)

    # resize
    output_size = (125,125)
    i = Image.open(form_picture)
    i.thumbnail(output_size)

    i.save(picture_path) #save the picture in picture_path
    return picture_fn

@app.route('/account/', methods=['GET', 'POST'])
@login_required
def account():
    form = UpdateAccountForm()
    if form.validate_on_submit():
        if form.picture.data:
            picture_file = save_picture(form.picture.data)
            current_user.image_file = picture_file

        current_user.username = form.username.data
        current_user.email = form.email.data
        db.session.commit()
        flash('Your account has been updated!', 'success')
        return redirect(url_for('account'))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.email.data = current_user.email

    image_file = url_for('static', filename= "profile_pics/" + current_user.image_file)
    return render_template("account.html", title="Account",
                           image_file=image_file, form=form)