
from flask import Flask, request, redirect, render_template, session
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['DEBUG'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://blogz:blogz@localhost:8889/blogz'
app.config['SQLALCHEMY_ECHO'] = True
db = SQLAlchemy(app)
app.secret_key = 'y337j899s098uji'

class Blog(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120))
    body = db.Column(db.Text())
    owner_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    def __init__(self, title, body, owner):
        self.title = title
        self.body = body
        self.owner = owner

class User(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True)
    password = db.Column(db.String(120))
    blogs = db.relationship('Blog', backref='owner')

    def __init__(self, email, password, owner):
        self.email = email
        self.password = password

@app.before_request
def require_login():
    allowed_routes = ['login', 'register', 'display_blogs', 'index']
    if request.endpoint not in allowed_routes and 'email' not in session:
        return redirect('/login')

@app.route('/register', methods=['POST', 'GET'])
def register():

    username_error = ''
    password_error = ''
    verify_error = ''
    email_error = ''

    invalid_char = ' '

    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        verify = request.form['verify']

        existing_user = User.query.filter_by(email=email).first()
        if not existing_user and not email =="" and not password == "" and not verify == "" and password == verify and len(email) > 3 and len(password) > 3 and len(verify) > 3:
            new_user = User(email, password)
            db.session.add(new_user)
            db.session.commit()
            session['email'] = email
            return redirect('/newpost')
        else:
            if email == "" or len(email) <= 3:
                email = email
                email_error = "Please enter a valid email address"
            if existing_user:
                email = email
                email_error = "Email belongs to registered user. Please Login"
            else:
                if password == "" or len(password) <= 3:
                    password_error = "Please Enter a Valid Password"
                if verify == "" or len(verify) <= 3:
                    verify_error = "Please re-enter password"
                if password != verify:
                    verify_error = "Passwords do not match"

            return render_template("register.html",email = email, email_error = email_error, password_error = password_error, verify_error=verify_error)


    return render_template('register.html')

@app.route('/login', methods=['POST', 'GET'])
def login():

    login_error = ''
    password_not_found = ''

    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        user = User.query.filter_by(email=email).first()
        if user and user.password == password:
            session['email'] = email
            return redirect('/newpost')
        if not user:
            email = email
            login_error = 'Email address does not exist in our system. Please register'
        if user and user.password != password:
            email = email
            password_not_found = "Incorrect Username or Password"
        return render_template('login.html', login_error = login_error, password_not_found = password_not_found, email = email)

    return render_template('login.html')

@app.route('/logout')
def logout():
    del session['email']
    return redirect('/blog')

@app.route('/blog', methods=['POST','GET'])
def display_blogs():
    
    blog_id = request.args.get('id')
    if blog_id:
        content = Blog.query.get(blog_id)
        return render_template('blogpost.html', content = content)
    else:
        blogs = Blog.query.all()
        return render_template('blogs.html',title="Build A Blog!!", blogs=blogs)

@app.route('/newpost', methods=['POST', 'GET'])
def new_post():

    title_error = ''
    content_error = ''
    owner = User.query.filter_by(email = session['email']).first()

    if request.method == 'POST':
        blog_name = request.form['title']
        blog_content = request.form['body']
        if blog_name == "":
            title_error = "Don't Forget to Enter a Title!!"
        if blog_content == "":
            content_error = "Don't Forget to Add Content!!"
        if title_error != '' or content_error != '':
            return render_template('newpost.html',title_error=title_error,content_error=content_error)

        new_post = Blog(blog_name,blog_content,owner)
        db.session.add(new_post)
        db.session.commit()

        if new_post:
            post_id = new_post.id
            blog_post = Blog.query.get(post_id)
            return render_template('blogpost.html', content = blog_post)
    else:
        return render_template('newpost.html')

@app.route('/')
def index():
    authors = User.query.all()
    return render_template('index.html', authors=authors)


if __name__ == '__main__':
    app.run()