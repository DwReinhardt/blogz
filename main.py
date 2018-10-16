from flask import Flask, request, redirect, render_template, session
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['DEBUG'] = True


# Note: the connection string after :// contains the following info:
# user:password@server:portNumber/databaseName
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://build-a-blog:launchcode101@localhost:8889/build-a-blog'
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
  
@app.route('/blog', methods=['POST'])
def display_posts():
    posts = Blog.query.all()
    return render_template('blog.html', posts=posts)


@app.route('/newpost', methods=['POST', 'GET'])
def new_post():
    if request.method == 'POST':
        post_title = request.form['title']
        post_body = request.form['body']
        new_post = Blog(post_title, post_body)
        db.session.add(new_post)
        db.session.commit()
        return display_posts()
    return render_template('newpost.html')

@app.route('/blog_post')
def get post(post_id):
    request.args.get('id'):
        blog_id = request.args.get('id')
        blog = Blog.query.filter_by(id=blog_id)
    return render_template('blog_post.html', blog=blog)

@app.route('/', methods=['POST', 'GET'])
def index():
    posts = Blog.query.all()
    return render_template('blog.html', posts=posts)




if __name__ == '__main__':
    app.run()