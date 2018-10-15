from flask import Flask, request, redirect, render_template, session
from flask_sqlalchemy import SQLAlchemy

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
        self.title = name
        self.body = post
        if timestamp is None:
            timestamp = datetime.utcnow()
        self.timestamp = timestamp
  
@app.route('/blog', methods=['POST'])


@app.route('/newpost', methods=['POST', 'GET'])
def new_post():
    
    return render_template('blog.html')

@app.route('/', methods=['POST', 'GET'])
def index():

    if request.method == 'POST':
        post_title = request.form['title']
        post_body = request.form['body']
        new_post = Blog(post_title, post_body)
        db.session.add(new_post)
        db.session.commit()

    posts = Blog.query.all()
    return render_template('blog.html', posts=posts)




if __name__ == '__main__':
    app.run()