
from flask import Flask, request, redirect, render_template
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['DEBUG'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://build-a-blog:buildit@localhost:8889/build-a-blog'
app.config['SQLALCHEMY_ECHO'] = True
db = SQLAlchemy(app)


class Blog(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120))
    body = db.Column(db.String(1000))

    def __init__(self, title, body):
        self.title = title
        self.body = body

@app.route('/blog', methods=['POST','GET'])
def display_blogs():
    blogs = Blog.query.all()
    return render_template('blogs.html',title="Build A Blog!!", blogs=blogs)

@app.route('/newpost', methods=['POST', 'GET'])
def index():

    title_error = ''
    content_error = ''

    if request.method == 'POST':
        blog_name = request.form['title']
        blog_content = request.form['body']
        if blog_name == "":
            title_error = "Don't Forget to Enter a Title!!"
        if blog_content == "":
            content_error = "Don't Forget to Add Content!!"
        if title_error != '' or content_error != '':
            return render_template('newpost.html',title_error=title_error,content_error=content_error)

        new_post = Blog(blog_name,blog_content)
        db.session.add(new_post)
        db.session.commit()
        return redirect('/blog')
    else:
        return render_template('newpost.html')

        #TODO - Need to add the error message validation for the new post and add matching Jinja tags to the template "Newpost.html"


#@app.route('/delete-task', methods=['POST'])
#def delete_task():

#    task_id = int(request.form['task-id'])
#    task = Task.query.get(task_id)
#    task.completed = True
#    db.session.add(task)
#    db.session.commit()

#    return redirect('/')


if __name__ == '__main__':
    app.run()