from flask import Flask, request, redirect, render_template, session
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['DEBUG'] = True


# Note: the connection string after :// contains the following info:
# user:password@server:portNumber/databaseName
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://blogz:launchcode101@localhost:8889/build-a-blog'
app.config['SQLALCHEMY_ECHO'] = True

db = SQLAlchemy(app)

class Blog(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120))
    body = db.Column(db.Text)
    timestamp = db.Column(db.DateTime)

    def __init__(self, title, body, timestamp=None):
        self.title = title
        self.body = body
        if timestamp is None:
            timestamp = datetime.utcnow()
        self.timestamp = timestamp
  
class User():

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True)
    password = db.Column(db.String(120))
    tasks = db.relationship('Blog', backref='owner')

    def __init__(self, email, password):
        self.email = email
        self.password = password

@app.before_request
def require_login():
    allowed_routes = ['login', 'register']
    if request.endpoint not in allowed_routes and 'email' not in session:
        return redirect('/login')

@app.route('/signup', methods=['POST', 'GET'])
def signup():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        verify = request.form['verify']

        # TODO - validate user's data

        existing_user = User.query.filter_by(email=email).first()
        if not existing_user:
            new_user = User(email, password)
            db.session.add(new_user)
            db.session.commit()
            session['email'] = email
            return redirect('/')
        else:
            # TODO - user better response messaging
            return "<h1>Duplicate user</h1>"

    return render_template('signup.html')

@app.route('/login', methods=['POST', 'GET'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        user = User.query.filter_by(email=email).first()
        if user and user.password == password:
            session['email'] = email
            flash("Logged in")
            return redirect('/newpost')
        else:
            flash('User password incorrect, or user does not exist', 'error')

    return render_template('login.html')

@app.route('/logout')
def logout():
    del session['email']
    return redirect('/')




#@app.route('/index')
#def index():

@app.route('/blog')
def display_posts():
    posts = Blog.query.all()
    return render_template('blog.html', posts=posts)

@app.route('/blogpost', methods=['GET'])
def display_single_post():
    retrieved_id = request.args.get('id')
    posts = Blog.query.filter_by(id=retrieved_id).all()
    return render_template('blog_post.html', posts=posts)

@app.route('/newpost', methods=['POST', 'GET'])
def new_post():

    post_title = ''
    post_body = ''
    title_error = ''
    body_error = ''
    empty_field_error = "Field cannot be blank"

    if request.method == 'POST':
        post_title = request.form['title']
        post_body = request.form['body']

    if not is_empty(post_title):                
        title_error = empty_field_error
    if not is_empty(post_body):                
        body_error = empty_field_error

    if not title_error and not body_error:
        new_post = Blog(post_title, post_body)
        db.session.add(new_post)
        db.session.commit()
        return redirect('/blogpost?id={0}'.format(new_post.id))
    else:
        return render_template('newpost.html',
            title_error = empty_field_error,
            body_error = empty_field_error,
            )


@app.route('/', methods=['POST', 'GET'])
def index():
    posts = Blog.query.all()
    return render_template('blog.html', posts=posts)

def is_empty(value):
    if value:
        return True
    else:
        return False

if __name__ == '__main__':
    app.run()