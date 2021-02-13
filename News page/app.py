from flask import Flask, redirect, url_for, render_template, request, session
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.secret_key = ''
app.config['SQLALCHEY_DATABSE_URI'] = 'sql://users.sqlite3'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class users(db.Model):
    _id = db.Column("id", db.Integer, primary_key=True)
    top = db.Column("topic", db.String(50))
    head = db.Column("head", db.String(100))

    def __init__ (self, top, head):
        self.top = top
        self.head = head


@app.route('/')
def home():
    return "<h1>Welcome to the home page</h1>"

@app.route('/admin_post', methods = ["GET","POST"])
def admin():
    if request.method == "POST":
        topic = request.form["topic"]
        body = request.form["body"]

        session["topic"] = topic
        session["body"] = body

        me = users(topic, body)
        db.session.add(me)
        db.session.commit()

        #inser into databse
        return redirect(url_for('newsPage'))
    else:
        return render_template('admin.html')

@app.route('/news')
def newsPage():
    if "topic" in session and "body" in session:
        heading = session["topic"]
        content = session["body"]

        #search in the databse and take last elements and return the array of elements. Then use a for loop to ge those values seperately in to p and h tags in newsapage.html
        # topics = users.query.filter(top).all()
        # bodies = users.query.filter(head).all()
        # x = len(topics)
        content = users.query.all()
        ren = content[-6:len(content)]
        ren.reverse()
        return render_template('newspage.html', heading = ren)
    else:
        return redirect(url_for('admin'))

if __name__ == "__main__":
    db.create_all()
    app.run(debug=True)
