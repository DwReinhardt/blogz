


@app.route('/newpost', methods=['POST', 'GET'])
def new_post():
    form = BlogForm()
    if request.method == 'POST':
        if not form.validate():
            return render_template('newpost.html', form=form)
        else:

            owner = User.query.filter_by(username=session['username']).first()
            blog_title = form.blog_title.data
            blog_post = form.blog_post.data

            new_blog = Blog(blog_title, blog_post, owner)
            db.session.add(new_blog)
            db.session.commit()

            return redirect(url_for('blog', id=new_blog.id))

    return render_template('newpost.html', form=form, title="Add a Blog Entry")


@app.route("/blog")
def blog():
    if not request.args:
        blogs = Blog.query.order_by(Blog.timestamp.desc()).all()
        return render_template("blog.html", blogs=blogs)
    elif request.args.get('id'):
        user_id = request.args.get('id')
        blog = Blog.query.filter_by(id=user_id).first()
        return render_template('blogpost.html', blog=blog)
    elif request.args.get('user'):
        user_id = request.args.get('user')
        user = User.query.filter_by(id=user_id).first()
        blogs = Blog.query.filter_by(owner_id=user_id).all()
        return render_template('user.html', blogs=blogs, user=user)


@app.route("/")
def index():
    users = User.query.all()
    return render_template('index.html', users=users)
