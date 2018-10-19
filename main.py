from flask import Flask, request, redirect, render_template, session, flash
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['DEBUG'] = True

app.secret_key = 'y337kGcys&zP3B'

# Note: the connection string after :// contains the following info:
# user:password@server:portNumber/databaseName
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://blogz:launchcode101@localhost:8889/blogz'
app.config['SQLALCHEMY_ECHO'] = True

db = SQLAlchemy(app)
app.secret_key = 'y337kGcys&zP3B'

class Blog(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120))
    body = db.Column(db.Text)
    timestamp = db.Column(db.DateTime)
    owner_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    def __init__(self, title, body, owner, timestamp=None):
        self.title = title
        self.body = body
        self.owner = owner
        if timestamp is None:
            timestamp = datetime.utcnow()
        self.timestamp = timestamp
  
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20))
    password = db.Column(db.String(20))
    blogs = db.relationship('Blog', backref='owner')

    def __init__(self, username, password):
        self.username = username
        self.password = password

def is_empty(value):
    if value:
        return True
    else:
        return False
''' UNMASK THIS BEFORE PRDUCTION!!!!
@app.before_request
def require_login():
    allowed_routes = ['login', 'signup', 'display_posts', 'index']
    if request.endpoint not in allowed_routes and 'username' not in session:
        return redirect('/login')
'''
@app.route('/signup', methods=['POST', 'GET'])
def signup():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        verify = request.form['verify']

#FAIL CHECKS
    # username: field will either be empty or invalid...it cannot be both
        if len(username) < 3 or len(username) > 20 or " " in username:
            flash('Invalid username, try again.', 'error')

    #password: field will either be empty or invalid...it cannot be both
        elif len(password) < 3 or len(password) > 20 or " " in password:
            flash('Invalid password, try again.', 'error')

    #ensure both submitted passwords are identical
        elif password != verify:
            flash('Passwords do not match, try again.', 'error')

    # Resolve conflicts and redirect or direct user to correct
        else:
            existing_user = User.query.filter_by(username=username).first()

            if existing_user:
                flash('User already exists', 'error')

            else:
                new_user = User(username, password)
                db.session.add(new_user)
                db.session.commit()
                session['username'] = username
                return redirect('/newpost')

    return render_template('signup.html')

@app.route('/login', methods=['POST', 'GET'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(username=username).first()
        if user and user.password == password:
            session['username'] = username
            return redirect('/newpost')
        else:
            flash('User password incorrect, or user does not exist', 'error')

    return render_template('login.html')

@app.route('/logout')
def logout():
    del session['username']
    return redirect('/blog')

@app.route('/blog')
def display_posts():
    user_id = request.args.get('user_id')
    blog_id = request.args.get('blog_id')
    blog = Blog.query.all()

    if blog_id:
        blog = Blog.query.get(blog_id)
        return render_template('blog_post.html', blog=blog)
    
    elif user_id:
        user = User.query.get(user_id)
        blogs = Blog.query.filter_by(owner=user).all()
        return render_template('single_user.html', blogs=blogs)
    
    else:
        blogs = Blog.query.all()
        return render_template('single_user.html', blogs=blogs)

@app.route('/blogpost', methods=['GET'])
def display_single_post():
    retrieved_id = session['username']
    posts = Blog.query.filter_by(id=retrieved_id).all()
    return render_template('blog_post.html', posts=posts)

@app.route('/newpost', methods=['POST', 'GET'])
def new_post():
    if request.method == 'GET':
        return render_template('newpost.html')

    post_title = ''
    post_body = ''
    title_error = ''
    body_error = ''
    empty_field_error = "Field cannot be blank"

    owner = User.query.filter_by(username=session['username']).first()

    if request.method == 'POST':
        post_title = request.form['title']
        post_body = request.form['body']
        #owner = User.query.filter_by(username=session['username']).first()

    if not is_empty(post_title):                
        title_error = empty_field_error
    if not is_empty(post_body):                
        body_error = empty_field_error

    if not title_error and not body_error:
        new_post = Blog(post_title, post_body, owner)
        db.session.add(new_post)
        db.session.commit() 
        return redirect('/blog=id' + str(new_post.id))
    else:
        return render_template('newpost.html',
            title_error = empty_field_error,
            body_error = empty_field_error,
            )

@app.route('/', methods=['POST', 'GET'])
def index():
    users = User.query.all()
    return render_template('index.html', users=users)

if __name__ == '__main__':
    app.run()